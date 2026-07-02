# agent-skill-audit
**Static analysis for the agentic supply chain.**

Autonomous agents are becoming the primary interface for local systems, handling credentials, filesystem access, and network connections. agent-skill-audit provides a triage pre-filter for evaluating third-party skills (e.g., MCP servers) before they are executed. It focuses on the reality that installing a skill is a supply-chain trust decision, yet community auditing remains largely manual.

## Core Capability
This tool identifies high-risk signals in codebases without executing them:

- **Prompt Injection:** Detects instruction-override prose and obfuscated payloads.

- **Credential Reach:** Flags access patterns for `~/.aws`, `.env`, and other sensitive stores.

- **Capability Mapping:** Identifies network egress, filesystem mutation, and opaque code execution (`eval`/`exec`).

- **Supply-Chain Hygiene:** Monitors for unpinned dependencies and dangerous install patterns like `npx -y`.

## The Empirical Value
This tool is the foundation of my internal AI infrastructure. By running it against public corpuses (62+ skills analyzed as of 2026-07-01), I have established that static analysis serves as a vital human-in-the-loop triage aid, not a false sense of security.

## Usage

```bash
# Audit a directory of skills (each subdirectory is treated as one skill)
python audit.py ~/.claude/skills

# Custom output location, and echo JSON
python audit.py ~/.claude/skills --out my-report --json
```

Outputs `report.md` (human-readable) and `report.json` (machine-readable) into the output directory. Exit code is 1 if any skill scores HIGH or CRITICAL, allowing for integration into CI pipelines or pre-install hooks.

## Methodology
Each signal carries a severity (INFO→CRITICAL). A skill's risk is the highest severity among its matched signals. Signals are heuristics, not verdicts — the tool tells you where to look; you decide.

**Limitations:** Regex-based static analysis is a triage aid, not a proof of safety. It reasons about capabilities present in the code, not intent.

## License
MIT — see [LICENSE](LICENSE).
