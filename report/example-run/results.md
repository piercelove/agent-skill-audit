# Agent-Skill Audit Report

**Scanned:** `/tmp/claude-0/-home-user-obsidian-vault/0d1794d8-ab33-5131-8fb2-edb81ed11810/scratchpad/corpus`  
**Skills:** 62  
**Risk mix:** CRITICAL=2, HIGH=8, MEDIUM=1, LOW=3, INFO=48

| Skill | Risk | Files | Exec? | Categories |
|---|---|---|:--:|---|
| `marketingskills__social` | **CRITICAL** | 9 | no | prompt-injection |
| `skills__claude-api` | **CRITICAL** | 66 | no | prompt-injection, supply-chain |
| `marketingskills__ad-creative` | **HIGH** | 4 | no | supply-chain |
| `marketingskills__video` | **HIGH** | 3 | no | supply-chain |
| `skills__docx` | **HIGH** | 17 | yes | code-execution, credential-reach, filesystem, network-egress |
| `skills__mcp-builder` | **HIGH** | 9 | yes | credential-reach |
| `skills__pptx` | **HIGH** | 20 | yes | code-execution, credential-reach, filesystem, network-egress |
| `skills__skill-creator` | **HIGH** | 16 | yes | code-execution, credential-reach, filesystem, prompt-injection |
| `skills__webapp-testing` | **HIGH** | 6 | yes | code-execution |
| `skills__xlsx` | **HIGH** | 15 | yes | code-execution, credential-reach, filesystem, network-egress |
| `skills__web-artifacts-builder` | **MEDIUM** | 4 | yes | filesystem |
| `skills__algorithmic-art` | **LOW** | 3 | yes | — |
| `skills__pdf` | **LOW** | 12 | yes | — |
| `skills__slack-gif-creator` | **LOW** | 7 | yes | — |
| `marketingskills__ab-testing` | **INFO** | 4 | no | — |
| `marketingskills__ads` | **INFO** | 6 | no | — |
| `marketingskills__ai-seo` | **INFO** | 6 | no | — |
| `marketingskills__analytics` | **INFO** | 5 | no | — |
| `marketingskills__aso` | **INFO** | 7 | no | — |
| `marketingskills__churn-prevention` | **INFO** | 4 | no | — |
| `marketingskills__co-marketing` | **INFO** | 2 | no | — |
| `marketingskills__cold-email` | **INFO** | 7 | no | — |
| `marketingskills__community-marketing` | **INFO** | 2 | no | — |
| `marketingskills__competitor-profiling` | **INFO** | 4 | no | — |
| `marketingskills__competitors` | **INFO** | 4 | no | — |
| `marketingskills__content-strategy` | **INFO** | 3 | no | — |
| `marketingskills__copy-editing` | **INFO** | 5 | no | — |
| `marketingskills__copywriting` | **INFO** | 4 | no | — |
| `marketingskills__cro` | **INFO** | 4 | no | — |
| `marketingskills__customer-research` | **INFO** | 3 | no | — |
| `marketingskills__directory-submissions` | **INFO** | 4 | no | — |
| `marketingskills__emails` | **INFO** | 5 | no | — |
| `marketingskills__free-tools` | **INFO** | 3 | no | — |
| `marketingskills__image` | **INFO** | 3 | no | — |
| `marketingskills__launch` | **INFO** | 2 | no | — |
| `marketingskills__lead-magnets` | **INFO** | 4 | no | — |
| `marketingskills__marketing-ideas` | **INFO** | 3 | no | — |
| `marketingskills__marketing-plan` | **INFO** | 15 | no | — |
| `marketingskills__marketing-psychology` | **INFO** | 2 | no | — |
| `marketingskills__offers` | **INFO** | 8 | no | — |
| `marketingskills__onboarding` | **INFO** | 3 | no | — |
| `marketingskills__paywalls` | **INFO** | 3 | no | — |
| `marketingskills__popups` | **INFO** | 2 | no | — |
| `marketingskills__pricing` | **INFO** | 4 | no | — |
| `marketingskills__product-marketing` | **INFO** | 2 | no | — |
| `marketingskills__programmatic-seo` | **INFO** | 3 | no | — |
| `marketingskills__prospecting` | **INFO** | 7 | no | — |
| `marketingskills__public-relations` | **INFO** | 5 | no | — |
| `marketingskills__referrals` | **INFO** | 4 | no | — |
| `marketingskills__revops` | **INFO** | 6 | no | — |
| `marketingskills__sales-enablement` | **INFO** | 6 | no | — |
| `marketingskills__schema` | **INFO** | 3 | no | — |
| `marketingskills__seo-audit` | **INFO** | 4 | no | — |
| `marketingskills__signup` | **INFO** | 2 | no | — |
| `marketingskills__site-architecture` | **INFO** | 5 | no | — |
| `marketingskills__sms` | **INFO** | 5 | no | — |
| `skills__brand-guidelines` | **INFO** | 2 | no | — |
| `skills__canvas-design` | **INFO** | 29 | no | — |
| `skills__doc-coauthoring` | **INFO** | 1 | no | — |
| `skills__frontend-design` | **INFO** | 2 | no | — |
| `skills__internal-comms` | **INFO** | 6 | no | — |
| `skills__theme-factory` | **INFO** | 12 | no | — |

---

## Details

### `marketingskills__social` — CRITICAL

+ **[CRITICAL] PI-EXFIL** (prompt-injection) — Prose instructs the agent to send secrets somewhere.  
  `marketingskills__social/evals/evals.json:38` → `"expected_output": "Should trigger on casual phrasing. Should apply the content repurposing system. Should use the Blog `

### `skills__claude-api` — CRITICAL

+ **[CRITICAL] PI-EXFIL** (prompt-injection) — Prose instructs the agent to send secrets somewhere.  
  `skills__claude-api/SKILL.md:180` → `**Supporting endpoints** — Batches (`POST /v1/messages/batches`), Files (`POST /v1/files`), Token Counting (`POST /v1/me`
+ **[CRITICAL] PI-EXFIL** (prompt-injection) — Prose instructs the agent to send secrets somewhere.  
  `skills__claude-api/shared/managed-agents-client-patterns.md:209` → `**Security note:** this does not expose a public endpoint. `agent.custom_tool_use` arrives on the SSE stream your orches`
+ **[CRITICAL] PI-EXFIL** (prompt-injection) — Prose instructs the agent to send secrets somewhere.  
  `skills__claude-api/shared/prompt-caching.md:189` → `For fan-out patterns: send 1 request, await the first streamed token (not the full response), then fire the remaining N−`
+ **[CRITICAL] PI-EXFIL** (prompt-injection) — Prose instructs the agent to send secrets somewhere.  
  `skills__claude-api/shared/managed-agents-tools.md:204` → `Vaults store credentials; those credentials **never enter the sandbox**. This is a deliberate security boundary — code r`
+ **[CRITICAL] PI-EXFIL** (prompt-injection) — Prose instructs the agent to send secrets somewhere.  
  `skills__claude-api/shared/managed-agents-api-reference.md:157` → `| `POST`   | `/v1/vaults/{vault_id}/credentials`                               | CreateCredential   | Create a credentia`
+ **[HIGH] SC-LATEST** (supply-chain) — Auto-updating / unpinned execution — no version you can trust.  
  `skills__claude-api/shared/anthropic-cli.md:28` → `go install github.com/anthropics/anthropic-cli/cmd/ant@latest`
+ **[HIGH] PI-OVERRIDE** (prompt-injection) — Instruction-override language aimed at the agent.  
  `skills__claude-api/shared/model-migration.md:829` → `Phrase these as **context, not commands**. State the fact and let Claude act on it; avoid override-style language ("igno`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/SKILL.md:246` → `**Prefix match.** Any byte change anywhere in the prefix invalidates everything after it. Render order is `tools` → `sys`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-events.md:16` → `| `system.message`          | Update the agent's system prompt between turns — **Claude Opus 4.8 only**; see § Updating `
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-core.md:9` → `| **Agent** | `/v1/agents` | A persisted, versioned object defining the agent's capabilities and persona: model, system `
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-client-patterns.md:211` → `**Do not embed API keys in the system prompt or user messages as a workaround.** Prompts and messages are stored in the `
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/prompt-caching.md:27` → `3. **Check rendered order matches stability order.** Stable content must physically precede volatile content. If a times`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-tools.md:212` → `**Do not put API keys in the system prompt or user messages as a workaround** — they persist in the session's event hist`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-api-reference.md:349` → `> `system.message` events (update the system prompt between turns) use the same envelope with `type: "system.message"` —`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-onboarding.md:5` → `Claude Managed Agents is a hosted agent: Anthropic runs the agent loop and provisions a sandboxed container per session `
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-multiagent.md:3` → `A coordinator agent can delegate to other agents within one session. All agents **share the container and filesystem**; `
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-overview.md:3` → `Managed Agents provisions a container per session as the agent's workspace. The agent loop runs on Anthropic's orchestra`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/model-migration.md:26` → `**TL;DR:** Change the model ID string. If you were using `budget_tokens`, switch to `thinking: {type: "adaptive"}`. If y`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/agent-design.md:93` → `| Editing the system prompt mid-session invalidates the cache. | Append a `{"role": "system", ...}` message to `messages`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/shared/managed-agents-memory.md:75` → `Each attached store is mounted in the session container at `/mnt/memory/<store-name>/`. The agent interacts with it usin`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/python/managed-agents/README.md:66` → `### With system prompt and custom tools`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/python/claude-api/README.md:193` → `Cache large context to reduce costs (up to 90% savings). **Caching is a prefix match** — any byte change anywhere in the`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/typescript/managed-agents/README.md:72` → `### With system prompt and custom tools`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/typescript/claude-api/README.md:136` → `**Caching is a prefix match** — any byte change anywhere in the prefix invalidates everything after it. For placement pa`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__claude-api/curl/managed-agents.md:82` → `### With system prompt, custom tools, and GitHub repo`

### `marketingskills__ad-creative` — HIGH

+ **[HIGH] SC-LATEST** (supply-chain) — Auto-updating / unpinned execution — no version you can trust.  
  `marketingskills__ad-creative/references/generative-tools.md:563` → `npx create-video@latest`

### `marketingskills__video` — HIGH

+ **[HIGH] SC-LATEST** (supply-chain) — Auto-updating / unpinned execution — no version you can trust.  
  `marketingskills__video/SKILL.md:88` → `npx create-video@latest`

### `skills__docx` — HIGH

+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__docx/scripts/accept_changes.py:68` → `result = subprocess.run(`
+ **[HIGH] CR-ENV** (credential-reach) — Reads environment variables (may reach API keys).  
  `skills__docx/scripts/office/soffice.py:25` → `env = os.environ.copy()`
+ **[HIGH] NE-SOCKET** (network-egress) — Raw socket networking.  
  `skills__docx/scripts/office/soffice.py:46` → `s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__docx/scripts/office/soffice.py:14` → `subprocess.run(["soffice", ...], env=env)`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__docx/scripts/office/validators/redlining.py:138` → `result = subprocess.run(`
+ **[MEDIUM] FS-DELETE** (filesystem) — Deletes files.  
  `skills__docx/scripts/office/soffice.py:64` → `src.unlink()`

### `skills__mcp-builder` — HIGH

+ **[HIGH] CR-DOTENV** (credential-reach) — Reads a .env file.  
  `skills__mcp-builder/scripts/evaluation.py:344` → `env_vars = parse_env_vars(args.env) if args.env else None`
+ **[HIGH] CR-DOTENV** (credential-reach) — Reads a .env file.  
  `skills__mcp-builder/scripts/connections.py:80` → `self.env = env`

### `skills__pptx` — HIGH

+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__pptx/scripts/thumbnail.py:161` → `result = subprocess.run(`
+ **[HIGH] CR-ENV** (credential-reach) — Reads environment variables (may reach API keys).  
  `skills__pptx/scripts/office/soffice.py:25` → `env = os.environ.copy()`
+ **[HIGH] NE-SOCKET** (network-egress) — Raw socket networking.  
  `skills__pptx/scripts/office/soffice.py:46` → `s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__pptx/scripts/office/soffice.py:14` → `subprocess.run(["soffice", ...], env=env)`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__pptx/scripts/office/validators/redlining.py:138` → `result = subprocess.run(`
+ **[MEDIUM] FS-DELETE** (filesystem) — Deletes files.  
  `skills__pptx/scripts/clean.py:63` → `slide_file.unlink()`
+ **[MEDIUM] FS-DELETE** (filesystem) — Deletes files.  
  `skills__pptx/scripts/office/soffice.py:64` → `src.unlink()`

### `skills__skill-creator` — HIGH

+ **[HIGH] CR-ENV** (credential-reach) — Reads environment variables (may reach API keys).  
  `skills__skill-creator/scripts/improve_description.py:33` → `env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__skill-creator/scripts/improve_description.py:35` → `result = subprocess.run(`
+ **[HIGH] CR-ENV** (credential-reach) — Reads environment variables (may reach API keys).  
  `skills__skill-creator/scripts/run_eval.py:83` → `env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__skill-creator/scripts/run_eval.py:85` → `process = subprocess.Popen(`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__skill-creator/eval-viewer/generate_review.py:291` → `result = subprocess.run(`
+ **[MEDIUM] PI-SYSTEM** (prompt-injection) — References the system/developer layer — common injection framing.  
  `skills__skill-creator/SKILL.md:390` → `Use the model ID from your system prompt (the one powering the current session) so the triggering test matches what the `
+ **[MEDIUM] FS-DELETE** (filesystem) — Deletes files.  
  `skills__skill-creator/scripts/run_eval.py:181` → `command_file.unlink()`

### `skills__webapp-testing` — HIGH

+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__webapp-testing/scripts/with_server.py:69` → `process = subprocess.Popen(`

### `skills__xlsx` — HIGH

+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__xlsx/scripts/recalc.py:34` → `subprocess.run(`
+ **[HIGH] CR-ENV** (credential-reach) — Reads environment variables (may reach API keys).  
  `skills__xlsx/scripts/office/soffice.py:25` → `env = os.environ.copy()`
+ **[HIGH] NE-SOCKET** (network-egress) — Raw socket networking.  
  `skills__xlsx/scripts/office/soffice.py:46` → `s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__xlsx/scripts/office/soffice.py:14` → `subprocess.run(["soffice", ...], env=env)`
+ **[HIGH] CE-SHELL** (code-execution) — Spawns shell/child processes.  
  `skills__xlsx/scripts/office/validators/redlining.py:138` → `result = subprocess.run(`
+ **[MEDIUM] FS-DELETE** (filesystem) — Deletes files.  
  `skills__xlsx/scripts/office/soffice.py:64` → `src.unlink()`

### `skills__web-artifacts-builder` — MEDIUM

+ **[MEDIUM] FS-DELETE** (filesystem) — Deletes files.  
  `skills__web-artifacts-builder/scripts/bundle-artifact.sh:36` → `rm -rf dist bundle.html`


---
*Signals are heuristics, not verdicts. Confirm each before trusting or discarding a skill.*