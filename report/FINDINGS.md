# Findings

**Corpus scanned:** 62 publicly available agent skills.
**Sources:** [`anthropics/skills`](https://github.com/anthropics/skills) (18 skills, first-party) + [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills) (44 skills, community, 31k★).
**Date:** 2026-07-01 · **Tool version:** v2 (post CE-EVAL refinement — see RQ3).
**Reproduce:** `python audit.py <corpus>` over the two repos, each skill directory (the folder containing `SKILL.md`) treated as one unit.

> These numbers are from a real scan. The corpus is deliberately two *reputable* sources — one first-party, one high-adoption community repo — so "how clean is the curated end of the ecosystem?" is the question being answered. It is **not** a random sample of the long tail, where risk is expected to be higher.

## RQ1 — Prevalence of high-severity signals

| Risk level | Count | % of 62 |
|---|---|---|
| CRITICAL | 2 | 3% |
| HIGH | 8 | 13% |
| MEDIUM | 1 | 2% |
| LOW | 3 | 5% |
| INFO | 48 | 77% |

**Headline:** 10 / 62 skills (**16%**) scored HIGH+, and the same 16% carry bundled executables. The other 84% are prose-only skills with no risk signals. **But see RQ3 — the 2 CRITICALs are both false positives.**

### Per-category prevalence

| Category | Skills | % |
|---|---|---|
| credential-reach | 5 | 8% |
| code-execution | 5 | 8% |
| filesystem | 5 | 8% |
| supply-chain (`@latest`/unpinned) | 3 | 5% |
| prompt-injection | 3 | 5% |
| network-egress | 3 | 5% |

Risk concentrates entirely in the **executable-carrying minority**. Every code-execution / credential-reach hit came from the 10 skills that ship `.py` helpers; the 52 prose-only skills were clean on those axes.

## RQ2 — Dangerous pairs

The tool flags two combinations as the ones that actually matter:

| Pair | Meaning | Flagged | **True on manual review** |
|---|---|---|---|
| credential-reach + network-egress | exfiltration primitive | 3 (`docx`, `pptx`, `xlsx`) | **0** |
| prompt-injection + executable | remote control | 1 (`skill-creator`) | **0** |

**This is the reassuring result.** All three "cred+egress" flags are the *same* pattern — the Office skills open a `socket.AF_UNIX` (a **local** IPC socket to LibreOffice), which the `NE-SOCKET` signal counts as networking but is not egress. The one "injection+exec" flag was a benign doc line ("use the model ID from your system prompt"). **In 62 reputable skills there were zero genuine exfiltration or remote-control patterns.**

## RQ3 — Tool vs. manual review (precision)

I hand-reviewed all 10 HIGH+ skills, blind-labeling each signal as a true capability or a misfire.

+ **On "does this skill carry real executable capability worth reading before install?" → 8 / 10 correct (80% precision).** The 8 true positives (`docx`, `pptx`, `xlsx`, `skill-creator`, `webapp-testing`, `mcp-builder`, plus `ad-creative` & `video` for unpinned `@latest`) genuinely run subprocesses, read `os.environ`, or install unpinned packages. The capability is *legitimate* for what they do — but it is exactly the surface you'd audit in an **un**trusted skill.
+ **On prompt-injection specifically → 0 / 2 (both CRITICALs were false positives).** `skills__claude-api` tripped `PI-EXFIL`×5 and `PI-SYSTEM`×18 on **API documentation** discussing credentials, vaults, and system prompts. `marketingskills__social` tripped `PI-EXFIL` on an **evals fixture**. The prose signals over-flag documentation- and eval-heavy skills badly.

**Dominant false-positive pattern:** prose regexes (`PI-*`) fire on skills that *write about* security/credentials/system-prompts rather than *attack* them. **Under-flag risk:** static analysis can't see what `@latest` resolves to at run time.

### Iteration (before → after)

v1 flagged `skills__algorithmic-art` HIGH on `CE-EVAL` — but the match was JavaScript's `regex.exec(hex)`, not code execution. I tightened `CE-EVAL` with a negative lookbehind (skip `.exec(`/method calls; real shell-out is covered by `CE-SHELL`). After the fix, `algorithmic-art` correctly dropped **HIGH → LOW** with no new misses on the fixtures. This is the methodology's "feed disagreements back into the catalogue" step, done once and measured.

## Takeaway

Three honest conclusions from the data:

1. **The curated end of the skill ecosystem is clean.** Zero real exfiltration or remote-control patterns across 62 first-party + high-adoption skills. "Popular / official = low risk" held here.
2. **Risk lives entirely in the executable 16%.** A prose-only skill is nearly inert; the moment a skill ships `.py`/`.js` helpers, `subprocess` + `os.environ` + install-time `@latest` become the surface to read. The tool's real job is **triage** — it correctly narrowed 62 skills to the ~10 a human should actually open.
3. **Severity must be capability-plus-review, not regex-alone.** The two scariest-looking scores (CRITICAL) were the two least reliable (documentation prose). Static signals are a *pre-filter for human review*, not a verdict — precisely why the tool prints evidence lines and exits non-zero rather than auto-blocking.

The practical rule this supports: **prose-only skill → low concern; executable skill → read every bundled script and pin the version before install; never trust `@latest` on a machine with live keys.** That is the manual gate I already ran by hand — now measured, not asserted.

---
*Limitations carry over from [`METHODOLOGY.md`](METHODOLOGY.md) §Threats to validity. This corpus is two reputable sources; the long-tail / low-adoption ecosystem is the obvious next scan and is where the Snyk injection-prevalence figure would be properly tested.*
