# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Frank's personal AI "second brain": an Obsidian markdown vault (`vault/`) plus Python scripts, Claude Code hooks, and skills that give the agent persistent memory, proactive monitoring, and read-only integrations with Ballys GitLab, Teams, and Outlook. It started as a fork of `coleam00/second-brain-starter`; the README describes the generic starter and the `create-second-brain-prd` skill, not this customised build. `vault/BUILD-PLAN.md` is the live roadmap and `docs/superpowers/plans/` holds the phase 1–3 implementation plans.

There is no app to build and no test suite. Everything is a `python3` CLI run from the repo root. "Done" means the relevant script ran and produced the expected output.

## Commands

Install dependencies (fastembed, sqlite-vec, msal):

```bash
pip install -r requirements.txt --break-system-packages
```

Memory search (hybrid vector + FTS5 over the vault, DB in `.claude/data/memory.db`):

```bash
python3 .claude/scripts/memory_index.py            # incremental re-index (MD5 checksum per file)
python3 .claude/scripts/memory_index.py --force    # full re-index
python3 .claude/scripts/memory_index.py --stats
python3 .claude/scripts/memory_search.py "query" --top-k 5 --mode hybrid|vector|keyword --path-prefix drafts/sent --json
```

Proactive systems:

```bash
python3 .claude/scripts/heartbeat.py [--check teams|gitlab|outlook|habits|drafts] [--json] [--quiet]
python3 .claude/scripts/memory_reflect.py [--date YYYY-MM-DD] [--archive] [--dry-run]
python3 .claude/scripts/draft_manager.py status|expire|list|create|mark-sent <file>
```

Integrations (CLI wrapper pattern: the LLM calls these, never touches tokens):

```bash
python3 .claude/scripts/integrations/query.py gitlab mrs|issues|pipelines|activity|summary
python3 .claude/scripts/integrations/query.py teams messages|calendar|dms|summary
python3 .claude/scripts/integrations/query.py outlook inbox|unread|summary
python3 .claude/scripts/integrations/query.py all
python3 .claude/scripts/integrations/microsoft_graph.py auth|test|status   # device-code flow, one-time
```

Skill helper scripts:

```bash
python3 .claude/skills/vault-lint/scripts/lint_vault.py [--fix] [--json]
python3 .claude/skills/project-status/scripts/gather_status.py [--json] [--project <slug>] [--pipelines]
python3 .claude/skills/teams-catchup/scripts/catchup.py [--hours 48] [--json]
```

Security utilities (both usable as library or CLI):

```bash
python3 .claude/scripts/guardrails.py [--json] "<bash command>"
echo "text" | python3 .claude/scripts/sanitize.py --source teams|outlook|gitlab
```

Deployment (macOS launchd: heartbeat every 30 min, reflect 8am, index every 2h):

```bash
./deploy/install.sh
./deploy/status.sh        # health check of files, hooks, tokens, DB, plists
```

Test a hook by hand by piping its JSON payload:

```bash
echo '{}' | python3 .claude/hooks/session-start-context.py
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 .claude/hooks/pre-tool-guardrail.py
```

## Architecture

Four layers, wired together by `.claude/settings.json`:

1. **Vault (`vault/`)** is the data. Root core files `SOUL.md`, `USER.md`, `MEMORY.md`, `HABITS.md`, `HEARTBEAT.md` are injected into every session, so they have hard size caps (SOUL ~70 lines, USER ~120, MEMORY <100). Everything else lives under `left-brain/` (work: `ballys/`, `contracts/`) or `right-brain/` (personal: vision, goals, health, finance, norms, growth, relationships, projects, journal). The full schema, naming conventions, and firewall rules are in the `vault-structure` skill; read it before creating any vault file. `vault/index.md` is the progressive-disclosure entry point and `vault/log.md` the chronological log.

2. **Hooks (`.claude/hooks/`)** persist context. `SessionStart` reads the core files, unchecked HABITS items, and the last 3 daily logs (capped at 30k chars). `PreCompact` and `Stop` append extracted decisions / a topic summary to today's daily log. `PreToolUse` runs `pre-tool-guardrail.py`, which delegates Bash checks to `scripts/guardrails.py` and blocks `Write`/`Edit` to paths containing invoice/payment/salary/bank/payroll or outside the allowed roots (this repo, `~/Documents/Projects`, `/tmp`, `/sessions/`). If a tool call is unexpectedly blocked, that hook is why.

3. **Scripts (`.claude/scripts/`)** are deliberately LLM-free. Heartbeat, reflect, and integrations gather data, diff against JSON state in `.claude/data/state/`, and emit markdown/JSON for the agent to reason over. `memory_reflect.py` promotes daily-log items to `MEMORY.md` by regex heuristics; the agent reviews, it does not auto-apply. Memory search chunks markdown on `##` headers (~1600 chars), prefixes each chunk with its vault-relative path, embeds with `all-MiniLM-L6-v2` (384-dim), and scores 0.7 vector + 0.3 keyword.

4. **Skills (`.claude/skills/`)** are the agent playbooks: `ingest`, `meeting-notes`, `project-status`, `teams-catchup`, `vault-lint`, `vault-structure`, plus the original `create-second-brain-prd`. Scheduled Cowork tasks (documented in `vault/HEARTBEAT.md`) drive most unattended runs; launchd plists in `deploy/` are the local fallback.

External text from Teams/Outlook/GitLab must pass through `sanitize.sanitize_external_text()` before being stored or reasoned over.

## Conventions and landmines

- **Daily logs are append-only.** Add timestamped entries at the bottom; never edit past entries. Entries look like `- HH:MM | [tag] text`.
- **The guardrail hook regex-scans the entire Bash command string**, including heredoc bodies and quoted examples. A Bash call whose text merely mentions a recursive-force delete, an elevated-privilege prefix, a force push, or curl piped to a shell is blocked, even when writing documentation. Use the Write/Edit tools for such content; they are checked by path only.
- **Work logs live in `vault/daily/`, not `left-brain/ballys/daily/`.** The latter is legacy and holds five April files. The vault-structure skill, hooks, reflect, heartbeat and the morning brief all agree on this since 2026-10-01. Self-chat dumps go to `vault/left-brain/ballys/inbox/`.
- **Absolute paths are hardcoded** to `/Users/frank.enendu/Documents/Personal/Second Brain Starter` in `pre-tool-guardrail.py`, `deploy/*.sh`, and the plists; `find_vault()` in hooks/scripts also has that fallback. Env overrides: `SECOND_BRAIN_PATH` (project root), `SECOND_BRAIN_DB` (sqlite path), `GITLAB_URL`.
- **Secrets live in `.env`** (`GITLAB_PAT`, `MSFT_CLIENT_ID`, `MSFT_TENANT_ID`, optional `ANTHROPIC_API_KEY`) and the MSAL token cache in `.claude/data/state/`. Both are gitignored along with `*.db` and `.agent/`. Never read `.env` into the conversation; the scripts load it themselves.
- **GitLab is reached via `urllib`**, not `python-gitlab`, against `gitlab.ballys.tech`, and is VPN-gated. Tracked project IDs and the AI R&D Teams chat ID are constants in `integrations/gitlab_integration.py` and `integrations/teams.py`.
- **Finance files are off limits to the agent** by guardrail; finance analysis happens only when Frank drops statements into `right-brain/finance/transactions/YYYY-MM/`.
- **Root clutter is personal.** The `.docx`/`.xlsx`/`.pptx` files, `email-*.md`, and `tracker/` (a standalone "Frank Life Tracker" PWA, plain HTML/JS) are untracked personal artefacts, not part of the Python stack. Leave them alone unless asked.
- `.claude/settings.local.json` holds the permission allowlist; `.claude/.claude/` is a stray duplicate state dir.
