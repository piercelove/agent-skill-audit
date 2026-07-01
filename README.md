# agent-skill-audit

**A static analyzer for the agent-skill / MCP supply chain.**

Third-party "skills" and MCP servers are code you hand an autonomous agent that
already has your credentials, your filesystem, and a network connection. Most
are a `SKILL.md` plus a few helper scripts, installed with a one-liner — and a
[widely-cited Snyk analysis found a large fraction of tested skills carried
prompt-injection or credential-reach vectors](https://snyk.io/). The install
step is a supply-chain trust decision, but almost nobody audits it.

`agent-skill-audit` reads a directory of skills and flags the signals that
matter before you run any of them:

+ **Prompt injection** — instruction-override and "hide this from the user" language, exfiltration prose, zero-width characters
+ **Credential reach** — env-var reads, `.env`, `~/.aws`, `~/.ssh`, keyrings
+ **Network egress** — HTTP clients, raw sockets, `curl | sh`
+ **Code execution / obfuscation** — `eval`/`exec`, shelling out, decode-then-run
+ **Supply-chain hygiene** — `@latest`, `npx -y`, unpinned installs, `curl | bash`
+ **Filesystem mutation** — deletes, `git stash`

It **never executes** the code it inspects. It produces a scored report so a
human makes the call.

## Why this exists

I run autonomous LLM agents (n8n + Claude Code) against live systems, on a
machine that holds real API keys. Before installing any community skill I was
already reading every `SKILL.md` and bundled script by hand for injection and
credential access, refusing auto-updating low-adoption packages, and pinning
versions. This tool is that manual process, made repeatable and shareable — and
the writeup in [`report/`](report/) turns it into an empirical study of how
risky the ecosystem actually is.

## Install

None. Python 3.8+, standard library only.

```bash
git clone https://github.com/piercelove/agent-skill-audit
cd agent-skill-audit
```

## Usage

```bash
# Audit a directory of skills (each subdirectory is treated as one skill)
python audit.py ~/.claude/skills

# Custom output location, and echo JSON
python audit.py ~/.claude/skills --out my-report --json
```

Outputs `report.md` (human-readable) and `report.json` (machine-readable) into
the output directory, and prints a one-line-per-skill summary. **Exit code is
`1` if any skill scores HIGH or CRITICAL**, so you can gate a pre-install hook
or CI job on it:

```bash
python audit.py ./incoming-skill || echo "Do not install without review."
```

## Try it

The repo ships two fixtures — a clean skill and a deliberately malicious one:

```bash
python audit.py examples
```

Expected: `risky-sync` → **CRITICAL** (injection + credential reach + egress +
obfuscated exec + `@latest`), `clean-formatter` → **INFO**.

## Results from a real scan

Ran against **62 public skills** (`anthropics/skills` + `coreyhaines31/marketingskills`) on 2026-07-01:

+ **16%** scored HIGH+, and risk lived **entirely** in the executable-carrying 16% — the 52 prose-only skills were clean.
+ **Zero** genuine exfiltration or remote-control patterns in this reputable corpus (the "cred + network" flags were local IPC sockets, not egress).
+ The two CRITICAL scores were **both false positives** — injection regexes firing on API *documentation* and an evals fixture. Manual-review precision on real executable capability was **80%**; on prompt-injection prose it was **0%**.

Full write-up in [`report/FINDINGS.md`](report/FINDINGS.md); the raw scan output and corpus manifest are in [`report/example-run/`](report/example-run/). The honest conclusion: **static signals are a triage pre-filter for human review, not a verdict** — which is exactly why the tool prints evidence and exits non-zero rather than auto-blocking.

## How risk is scored

Each signal carries a severity (`INFO`→`CRITICAL`). A skill's risk is the
highest severity among its matched signals; a skill that bundles executables but
trips no signal is still surfaced as `LOW` (executable surface = something to
read). Signals are **heuristics, not verdicts** — the tool tells you where to
look; you decide. Full signal catalogue and rationale in
[`taxonomy.md`](taxonomy.md).

## Limitations

+ Regex-based static analysis: it will miss cleverly obfuscated payloads and will occasionally over-flag benign code (e.g. a skill that legitimately needs the network). It is a triage aid, not a proof of safety.
+ It reasons about *capabilities present in the code*, not *intent* — a HIGH is "this can reach your keys," not "this will steal them."
+ Scope is the files on disk. It does not resolve what `npx -y foo@latest` actually pulls at run time — which is exactly why `@latest` is itself flagged.

See [`report/METHODOLOGY.md`](report/METHODOLOGY.md) for the study design and
[`report/FINDINGS.md`](report/FINDINGS.md) for results.

## License

MIT — see [`LICENSE`](LICENSE).
