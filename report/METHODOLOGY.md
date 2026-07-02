# Methodology — auditing the agent-skill supply chain

This is the study design behind `agent-skill-audit`. The framing follows the
empirical-research standard: a measurable question, a baseline, a reproducible
method, and honest limitations.

## Research question

**RQ1.** What fraction of publicly available agent skills / MCP servers carry at
least one high-severity risk signal (prompt injection, credential reach, network
egress, obfuscated execution, or unpinned auto-update)?

**RQ2.** How often do skills combine the *dangerous pairs* — credential-reach +
network-egress (exfiltration primitive), or injection-prose + executable-helper
(remote control) — that turn individual capabilities into an actual threat?

**RQ3.** Does a lightweight static analyzer agree with a careful manual review?
Where does it over- or under-flag?

## Baseline / comparison

+ **External baseline:** the reported prevalence of prompt injection in tested
  skills from prior public analysis (Snyk). RQ1 measures whether an independent
  scan reproduces a comparable order of magnitude.
+ **Internal baseline:** manual review of a labeled subset. The tool's output is
  scored against hand labels to estimate precision/recall (RQ3).

## Method

1. **Corpus.** Collect a sample of N skills from public sources (marketplaces,
   GitHub topics). Record source, star count / adoption, and last-update date.
2. **Automated pass.** Run `audit.py` over the corpus. Record each skill's risk
   level, categories, and matched signals (`report.json`).
3. **Manual labeling.** For a random subset of M skills, a human reviewer reads
   every prose and code file and independently labels risk category present /
   absent, blind to the tool output.
4. **Agreement.** Compare tool vs. human labels → precision, recall, and the
   confusion cases. Feed disagreements back into the signal catalogue.
5. **Pair analysis.** Compute how many skills exhibit each dangerous *pair*
   (RQ2), since combined capability — not any single signal — is the real risk.
6. **Iterate.** Tighten regexes that over-flag; add signals for missed vectors.
   Re-run. Report the before/after on the labeled set.

## Metrics

+ **Prevalence:** % of corpus at HIGH+ overall, and per category.
+ **Pair prevalence:** % exhibiting each dangerous pair.
+ **Tool precision / recall** vs. human labels on the subset.
+ **Adoption vs. risk:** does star count correlate with lower risk? (Tests the
  "popular = safe" assumption people rely on when installing.)

## Reproducibility

Every number in `FINDINGS.md` is produced by `python audit.py <corpus>`, whose
output (`report.json`) is committed alongside the corpus manifest. Anyone can
rerun the scan and get the same result; the manual-label sheet is published so
the agreement numbers can be checked.

## Threats to validity

+ **Static-only.** Cannot see what `@latest` resolves to at run time (which is
  why unpinned installs are themselves scored HIGH).
+ **Heuristic signals.** Regex matching over-flags benign network use and misses
  novel obfuscation — quantified by the precision/recall step, not hand-waved.
+ **Capability ≠ intent.** A HIGH means "this *can* reach your keys," not proof
  of malice. The study measures attack *surface*, which is the actionable thing
  at install time.
+ **Sampling.** Results generalize only to the sampled sources; the corpus
  manifest states exactly what was covered.
