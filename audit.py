#!/usr/bin/env python3
"""
agent-skill-audit — a static analyzer for the agent-skill / MCP supply chain.

Scans a directory of Claude Code (or similar) "skills" / MCP servers and flags
signals associated with prompt injection, credential reach, network egress,
code execution, and unsafe supply-chain practices. Emits a scored report so a
human can make an install / no-install decision before running third-party
agent code on a machine that holds live credentials.

This is a DEFENSIVE tool: it reads files and reports risk signals. It never
executes the code it inspects.

Usage:
    python audit.py <path-to-skills-dir> [--out audit-report] [--json]

A "skill" is taken to be each immediate subdirectory of <path>. Files that live
directly under <path> are grouped under a skill named after the directory.

No third-party dependencies. Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --- File classification -----------------------------------------------------

PROSE_EXT = {".md", ".mdx", ".markdown", ".txt", ".rst"}
CODE_EXT = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".sh", ".bash",
            ".rb", ".ps1", ".php", ".pl"}
# Extensions we skip entirely (binary / noise).
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
            ".woff", ".woff2", ".ttf", ".otf", ".pdf", ".zip", ".gz",
            ".lock", ".map"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
             "build", ".mypy_cache"}

# Severity ordering used to roll a skill's signals up to one risk level.
SEVERITY_ORDER = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


@dataclass
class Signal:
    id: str
    category: str
    severity: str
    applies_to: str          # "prose" | "code" | "any"
    pattern: re.Pattern
    note: str


def _rx(p: str) -> re.Pattern:
    return re.compile(p, re.IGNORECASE)


# --- The signal catalogue ----------------------------------------------------
# Each signal is a heuristic, not proof. The tool is a triage aid: it tells a
# human where to look, and the human makes the call.

SIGNALS = [
    # 1. Prompt injection — override / hidden-instruction language in prose.
    Signal("PI-OVERRIDE", "prompt-injection", "HIGH", "prose",
           _rx(r"\b(ignore|disregard|forget)\b[^.\n]{0,40}\b(previous|prior|above|earlier|all)\b[^.\n]{0,20}\b(instruction|prompt|rule|direction)"),
           "Instruction-override language aimed at the agent."),
    Signal("PI-HIDE", "prompt-injection", "HIGH", "prose",
           _rx(r"\bdo not (tell|inform|mention|reveal)[^.\n]{0,30}\b(user|human|owner)\b"),
           "Tells the agent to hide actions from the user."),
    Signal("PI-EXFIL", "prompt-injection", "CRITICAL", "prose",
           _rx(r"\b(send|upload|post|exfiltrate|forward|leak)\b[^.\n]{0,40}\b(key|token|secret|credential|\.env|password|api[_-]?key)"),
           "Prose instructs the agent to send secrets somewhere."),
    Signal("PI-SYSTEM", "prompt-injection", "MEDIUM", "prose",
           _rx(r"\b(system prompt|developer message|your (real )?instructions are)\b"),
           "References the system/developer layer — common injection framing."),
    Signal("PI-ZEROWIDTH", "prompt-injection", "MEDIUM", "any",
           re.compile(r"[​‌‍⁠﻿]"),
           "Zero-width / invisible characters — used to hide instructions."),

    # 2. Credential reach — code touching secrets.
    Signal("CR-ENV", "credential-reach", "HIGH", "code",
           _rx(r"(os\.environ|os\.getenv|process\.env|getenv\()"),
           "Reads environment variables (may reach API keys)."),
    Signal("CR-DOTENV", "credential-reach", "HIGH", "code",
           _rx(r"(\.env\b|dotenv|read.{0,10}\.env)"),
           "Reads a .env file."),
    Signal("CR-SECRETPATH", "credential-reach", "CRITICAL", "code",
           _rx(r"(~/\.aws|~/\.ssh|\.aws/credentials|id_rsa|keychain|keyring|\.netrc|\.git-credentials)"),
           "Reaches into well-known credential stores."),
    Signal("CR-SECRETNAME", "credential-reach", "MEDIUM", "code",
           _rx(r"\b(api[_-]?key|secret[_-]?key|access[_-]?token|client[_-]?secret|private[_-]?key)\b"),
           "Handles secret-named material."),

    # 3. Network egress — where data could leave.
    Signal("NE-HTTP", "network-egress", "MEDIUM", "code",
           _rx(r"\b(requests\.(get|post|put)|urllib\.request|httpx\.|http\.client|fetch\(|axios\.|XMLHttpRequest|WebSocket\()"),
           "Makes outbound HTTP(S) requests."),
    Signal("NE-SOCKET", "network-egress", "HIGH", "code",
           _rx(r"\b(socket\.socket|socket\.connect|net\.connect|dgram)\b"),
           "Raw socket networking."),
    Signal("NE-SHELLNET", "network-egress", "HIGH", "code",
           _rx(r"\b(curl|wget|nc|netcat|scp|rsync)\b\s+[^\n]*https?://"),
           "Shell-based data transfer to a URL."),

    # 4. Code execution / obfuscation.
    Signal("CE-EVAL", "code-execution", "HIGH", "code",
           # Negative lookbehind for '.' / word-char so we skip JS regex `.exec()`
           # and `subprocess.exec`-style method calls (real shell-out is CE-SHELL).
           _rx(r"(?<![.\w])(eval|exec)\s*\(|new Function\(|[^.\w]Function\("),
           "Dynamic code execution (eval/exec)."),
    Signal("CE-SHELL", "code-execution", "HIGH", "code",
           _rx(r"\b(os\.system|subprocess\.|child_process|execSync|spawnSync|popen|shell_exec)"),
           "Spawns shell/child processes."),
    Signal("CE-OBFUS", "code-execution", "CRITICAL", "code",
           _rx(r"(base64|b64decode|atob|fromCharCode|codecs\.decode)[^\n]{0,60}(exec|eval|Function|system)"),
           "Decodes then executes — classic obfuscated payload."),
    Signal("CE-PICKLE", "code-execution", "HIGH", "code",
           _rx(r"\b(pickle\.loads|marshal\.loads|yaml\.load\()"),
           "Unsafe deserialization."),

    # 5. Supply-chain / auto-update hygiene.
    Signal("SC-LATEST", "supply-chain", "HIGH", "any",
           _rx(r"(npx\s+-y|@latest|pip install\s+[^=\n]+(?<![=<>~])$|curl[^\n]+\|\s*(sh|bash))"),
           "Auto-updating / unpinned execution — no version you can trust."),
    Signal("SC-CURLPIPE", "supply-chain", "CRITICAL", "any",
           _rx(r"curl[^\n]+\|\s*(sudo\s+)?(sh|bash)"),
           "curl | sh — remote code, unreviewed, at run time."),

    # 6. Filesystem mutation.
    Signal("FS-DELETE", "filesystem", "MEDIUM", "code",
           _rx(r"\b(rm\s+-rf|shutil\.rmtree|os\.remove|unlink\(|fs\.rm)"),
           "Deletes files."),
    Signal("FS-GITSTASH", "filesystem", "LOW", "any",
           _rx(r"\bgit\s+stash\b"),
           "Uses git stash — can silently hide local changes."),
]


@dataclass
class Match:
    signal: Signal
    file: str
    line: int
    excerpt: str


@dataclass
class SkillResult:
    name: str
    files_scanned: int = 0
    has_executable: bool = False
    matches: list = field(default_factory=list)

    @property
    def risk(self) -> str:
        if not self.matches:
            # An executable-carrying skill with no signals is still worth a look.
            return "LOW" if self.has_executable else "INFO"
        top = max(self.matches, key=lambda m: SEVERITY_ORDER[m.signal.severity])
        return top.signal.severity

    @property
    def categories(self) -> list:
        return sorted({m.signal.category for m in self.matches})


def classify(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in PROSE_EXT:
        return "prose"
    if ext in CODE_EXT:
        return "code"
    return "other"


def scan_file(path: Path, kind: str) -> list:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return []
    lines = text.splitlines()
    found = []
    for sig in SIGNALS:
        if sig.applies_to != "any" and sig.applies_to != kind:
            continue
        for m in sig.pattern.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            excerpt = lines[line_no - 1].strip()[:120] if line_no <= len(lines) else ""
            found.append(Match(sig, str(path), line_no, excerpt))
            break  # one hit per signal per file is enough for triage
    return found


def scan_skill(name: str, root: Path) -> SkillResult:
    result = SkillResult(name=name)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            fp = Path(dirpath) / fn
            ext = fp.suffix.lower()
            if ext in SKIP_EXT:
                continue
            kind = classify(fp)
            if kind == "other" and ext not in CODE_EXT:
                # still count it, but only scan text-ish files
                if ext not in {"", ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini"}:
                    continue
                kind = "prose"
            if ext in CODE_EXT:
                result.has_executable = True
            result.files_scanned += 1
            result.matches.extend(scan_file(fp, "code" if ext in CODE_EXT else kind))
    return result


def discover_skills(root: Path) -> list:
    subdirs = [p for p in sorted(root.iterdir()) if p.is_dir() and p.name not in SKIP_DIRS]
    if subdirs:
        return [(p.name, p) for p in subdirs]
    return [(root.name, root)]  # flat layout: treat the whole dir as one skill


def render_markdown(results: list, root: Path) -> str:
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    results = sorted(results, key=lambda r: (order[r.risk], r.name))
    counts = {}
    for r in results:
        counts[r.risk] = counts.get(r.risk, 0) + 1
    out = []
    out.append(f"# Agent-Skill Audit Report\n")
    out.append(f"**Scanned:** `{root}`  ")
    out.append(f"**Skills:** {len(results)}  ")
    out.append("**Risk mix:** " + ", ".join(f"{k}={counts.get(k,0)}"
               for k in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]) + "\n")
    out.append("| Skill | Risk | Files | Exec? | Categories |")
    out.append("|---|---|---|:--:|---|")
    for r in results:
        out.append(f"| `{r.name}` | **{r.risk}** | {r.files_scanned} | "
                   f"{'yes' if r.has_executable else 'no'} | {', '.join(r.categories) or '—'} |")
    out.append("\n---\n\n## Details\n")
    for r in results:
        if not r.matches:
            continue
        out.append(f"### `{r.name}` — {r.risk}\n")
        for m in sorted(r.matches, key=lambda x: order[x.signal.severity]):
            rel = os.path.relpath(m.file, root)
            out.append(f"+ **[{m.signal.severity}] {m.signal.id}** "
                       f"({m.signal.category}) — {m.signal.note}  ")
            out.append(f"  `{rel}:{m.line}` → `{m.excerpt}`")
        out.append("")
    out.append("\n---\n*Signals are heuristics, not verdicts. Confirm each "
               "before trusting or discarding a skill.*")
    return "\n".join(out)


def to_json(results: list, root: Path) -> dict:
    return {
        "scanned": str(root),
        "skills": [
            {
                "name": r.name,
                "risk": r.risk,
                "files_scanned": r.files_scanned,
                "has_executable": r.has_executable,
                "categories": r.categories,
                "matches": [
                    {
                        "signal": m.signal.id,
                        "category": m.signal.category,
                        "severity": m.signal.severity,
                        "file": os.path.relpath(m.file, root),
                        "line": m.line,
                        "excerpt": m.excerpt,
                        "note": m.signal.note,
                    }
                    for m in r.matches
                ],
            }
            for r in results
        ],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Audit agent skills / MCP servers for supply-chain risk.")
    ap.add_argument("path", help="Directory containing skills (each subdir = one skill).")
    ap.add_argument("--out", default="audit-report", help="Output directory (default: audit-report).")
    ap.add_argument("--json", action="store_true", help="Also print JSON to stdout.")
    args = ap.parse_args(argv)

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    results = [scan_skill(name, path) for name, path in discover_skills(root)]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    md = render_markdown(results, root)
    (out_dir / "report.md").write_text(md, encoding="utf-8")
    payload = to_json(results, root)
    (out_dir / "report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Console summary
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    for r in sorted(results, key=lambda x: (order[x.risk], x.name)):
        print(f"  [{r.risk:>8}] {r.name}  "
              f"({r.files_scanned} files, {'exec' if r.has_executable else 'no-exec'}, "
              f"{', '.join(r.categories) or 'no signals'})")
    print(f"\nWrote {out_dir/'report.md'} and {out_dir/'report.json'}")
    if args.json:
        print(json.dumps(payload, indent=2))

    # Non-zero exit if anything HIGH+ so it can gate CI / a pre-install hook.
    worst = min((order[r.risk] for r in results), default=4)
    return 1 if worst <= order["HIGH"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
