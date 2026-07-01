# Attack-surface taxonomy for agent skills

A skill / MCP server is untrusted code that runs inside an agent holding your
credentials, filesystem, and network. This taxonomy is the set of capability
classes `agent-skill-audit` looks for. Each maps to signal IDs in `audit.py`.

## 1. Prompt injection (`PI-*`)
The `SKILL.md` / prose *is* part of the agent's context — so prose is an attack
surface, not just documentation. Watch for:
+ **PI-OVERRIDE** — "ignore previous instructions / rules / confirmation."
+ **PI-HIDE** — "do not tell the user," silent actions.
+ **PI-EXFIL** — prose that instructs sending keys/tokens/`.env` somewhere. *(Critical.)*
+ **PI-SYSTEM** — references to the system/developer prompt (reframing attempts).
+ **PI-ZEROWIDTH** — zero-width / invisible characters hiding instructions from a human reviewer.

## 2. Credential reach (`CR-*`)
Can this code get to your secrets?
+ **CR-ENV** — reads environment variables (where API keys usually live).
+ **CR-DOTENV** — reads `.env`.
+ **CR-SECRETPATH** — `~/.aws`, `~/.ssh`, `id_rsa`, keychains, `.netrc`, `.git-credentials`. *(Critical.)*
+ **CR-SECRETNAME** — handles secret-named material (`api_key`, `access_token`…).

## 3. Network egress (`NE-*`)
If it can reach your secrets AND the network, exfiltration is one line away.
+ **NE-HTTP** — HTTP clients (`requests`, `fetch`, `axios`, WebSocket).
+ **NE-SOCKET** — raw sockets. *(High — unusual for a formatting skill.)*
+ **NE-SHELLNET** — `curl`/`wget`/`scp`/`nc` to a URL.

## 4. Code execution / obfuscation (`CE-*`)
+ **CE-EVAL** — `eval` / `exec` / `new Function`.
+ **CE-SHELL** — `os.system`, `subprocess`, `child_process`.
+ **CE-OBFUS** — decode (base64/`atob`/`fromCharCode`) *then* execute. *(Critical — the signature of a hidden payload.)*
+ **CE-PICKLE** — unsafe deserialization (`pickle.loads`, `yaml.load`).

## 5. Supply-chain hygiene (`SC-*`)
The code you read today is not the code that runs tomorrow if it auto-updates.
+ **SC-LATEST** — `@latest`, `npx -y`, unpinned `pip install`. You cannot audit a moving target.
+ **SC-CURLPIPE** — `curl … | sh`. Remote, unreviewed code executed at run time. *(Critical.)*

## 6. Filesystem mutation (`FS-*`)
+ **FS-DELETE** — `rm -rf`, `rmtree`, `os.remove`.
+ **FS-GITSTASH** — `git stash` can silently hide your local changes.

---

## Scoring model

+ Per-signal severity: `INFO < LOW < MEDIUM < HIGH < CRITICAL`.
+ A skill's overall risk = the **highest** severity it trips (one bad capability is enough to warrant review).
+ A skill with **bundled executables but no signals** is reported `LOW`, not `INFO` — the executable surface itself is something a human should read.
+ The tool exits non-zero at HIGH+ so it can gate an install hook or CI.

## The core asymmetry

The danger isn't any single capability — it's the **combination**. Credential
reach + network egress in the same skill is the exfiltration primitive.
Injection prose + an executable helper is remote control. `agent-skill-audit`
surfaces the categories per skill precisely so a reviewer can spot these
dangerous *pairs* at a glance.
