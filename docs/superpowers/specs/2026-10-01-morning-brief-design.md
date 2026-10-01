# Morning Brief — Design

Date: 2026-10-01
Status: approved in conversation, awaiting written-spec review
Diagram: https://claude.ai/artifact/GZRNaQbTT8zj9d2AjPPtx7

## Goal

Each weekday, the first time Frank's laptop is open and the VPN is up between 06:30 and 11:00, post one short to-do list (at most five actions) to his Teams notes-to-self chat. The same chat is his dump inbox: anything he types there is captured verbatim into the vault and never turned into a to-do unless he prefixes it with `todo:`.

The brief is built from what Frank was actually doing and what the team asked of him, not from GitLab labels.

## Decisions already made

- Approach A: launchd on the laptop, one headless `claude -p` run per day. Cowork tasks and a pure-Python Graph client were rejected.
- Weekdays only.
- Work only. Personal items (life insurance, finance review) stay out of the Teams brief.
- Guardrail exception: the agent may send Teams messages to Frank's self-chat and to nothing else. This is enforced in the hook, not just stated in SOUL.md.
- Path split resolved in favour of reality: `vault/daily/` is the canonical work log. Nothing moves.

## Fixed identifiers

| Thing | Value |
|---|---|
| Self-chat (notes to self, 1 member) | `19:c142cf69-5033-4b79-9f1b-df23832c13d9_7cb48f87-e8c5-4ac2-8858-9b5433fc0d79@unq.gbl.spaces` |
| R&D Stand up (meeting chat) | `19:meeting_OGNlZjZhMWItMDQ2OS00M2ZlLTljOTUtNzA5MWZiNjQ1NDdk@thread.v2` |
| AI Interlock Team | `19:762ccb646d3447e7aec650273198e595@thread.v2` |
| AI R&D Crew | `19:02a862626ca54619b6babc5593aa33a3@thread.v2` |
| VPN probe | `https://gitlab.ballys.tech/api/v4/version` answering 200 or 401 within 5 s |
| `claude` binary | `/Users/frank.enendu/.local/bin/claude` |

## Components

### 1. `deploy/com.secondbrain.morning-brief.plist` (new)

- Runs `/bin/bash <project>/.claude/scripts/morning_brief.sh` every 600 s, `RunAtLoad` true.
- `WorkingDirectory` is the project root. Stdout and stderr go to `.claude/data/logs/morning-brief.log` and `morning-brief-error.log`.
- `EnvironmentVariables.PATH` includes `/Users/frank.enendu/.local/bin` so `claude` resolves, plus `/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin`. `HOME` is set explicitly.
- Added to the `PLISTS` arrays in `deploy/install.sh` and `deploy/status.sh`.

### 2. `.claude/scripts/morning_brief.sh` (new)

Bash, `set -euo pipefail`. Project root derived from the script's own path.

Gate, in order, each exiting 0 with a one-line log reason when it fails:

1. Weekday: `date +%u` in 1..5.
2. Window: local `HHMM` between `0630` and `1100` inclusive.
3. Not sent: marker file `.claude/data/state/morning-brief-sent-YYYY-MM-DD` absent.
4. VPN: curl probe above returns 200 or 401.

`--force` skips gates 1 to 3 only. The VPN gate always applies because nothing downstream works without it.

Gather, into a per-run temp dir under `.claude/data/state/run-YYYY-MM-DD/`:

- `digest.md` from `python3 .claude/scripts/sessions_digest.py --hours 36`. If the script fails, write one line: `Session digest unavailable.`
- `gitlab.md` from `python3 .claude/scripts/integrations/gitlab_integration.py issues`. If it fails (missing or expired token), write one line: `GitLab unavailable: check GITLAB_PAT.`

Run:

```
claude -p "$(cat .claude/scripts/morning_brief_prompt.md)" \
  --output-format text --max-turns 40 \
  --allowedTools "Read,Write,Edit,Bash(python3 .claude/scripts/sanitize.py:*),\
mcp__claude_ai_Microsoft_365__read_resource,\
mcp__claude_ai_Microsoft_365__chat_message_search,\
mcp__claude_ai_Microsoft_365__outlook_calendar_search,\
mcp__claude_ai_Microsoft_365__teams_send_chat_message"
```

The prompt receives the run dir path and today's date via environment variables `MB_RUN_DIR` and `MB_DATE`, which the prompt text references.

Mark: if `claude` exits 0 and its stdout contains the literal `BRIEF_SENT`, write the marker. Otherwise log the failure and leave no marker, so the next tick retries until 11:00. The prompt also tells Claude to write the marker itself immediately after a successful send, so a crash after sending cannot cause a duplicate post.

### 3. `.claude/scripts/sessions_digest.py` (new, LLM-free)

Scans two transcript stores for files modified in the last `--hours` (default 36):

- Claude Code: `~/.claude/projects/<slug>/*.jsonl`. The repo path is decoded from the directory slug (`-Users-frank-enendu-Documents-Work-...`).
- Codex: `~/.codex/sessions/**/*.jsonl`. The repo path is the `cwd` field of the first `session_meta` line.

Include a file only if its repo path starts with `~/Documents/Work` or `~/Documents/Projects`. Contract and Personal repos are excluded so the work brief never carries client names.

Per file: collect user turns (string content or `text` blocks; skip `tool_result` blocks and content that is only a `system-reminder`) and assistant `text` blocks. Group by repo. Emit markdown, most recently active repo first:

```
## <repo name>  (<n> sessions, last active HH:MM)
- First ask: <≤300 chars>
- Last asks: <≤300 chars> | <≤300 chars>
- Last assistant: <≤500 chars>
```

A file that fails to parse is skipped with a warning line at the end of the output. `--json` emits the same structure as JSON.

### 4. `.claude/scripts/morning_brief_prompt.md` (new)

The instructions for the headless run. Steps, in order:

1. Read `MB_RUN_DIR/digest.md`, `MB_RUN_DIR/gitlab.md`, the `## Critical Deadlines` section of `vault/MEMORY.md`, and `vault/daily/MB_DATE.md` if it exists.
2. Read `.claude/data/state/morning-brief-state.json` (`{"last_dump_ts": ISO-8601}`; treat a missing file as 24 h ago).
3. Read the three team chats since yesterday 06:00 via `read_resource` on `teams:///chats/<id>/messages`; if that resource is unavailable, fall back to `chat_message_search` with `afterDateTime` and keep only results from those three chats.
4. Read today's calendar via `outlook_calendar_search`.
5. Read the self-chat since `last_dump_ts`. Ignore messages the agent posted. For each message from Frank: if it starts with `todo:` (case-insensitive), it is a to-do candidate; otherwise append `- HH:MM | <text>` to `vault/left-brain/ballys/inbox/MB_DATE.md`, passing the text through `python3 .claude/scripts/sanitize.py --source teams` first. Create the file with a one-line header if absent.
6. Compose the brief. Pick at most five actions in this priority order: asks aimed at Frank in the three chats in the last 48 h; the next step left open in yesterday's sessions; prep for today's meetings; MEMORY.md deadlines. Drop anything silent for 14 days unless mentioned in the last 48 h. GitLab data is evidence only and never promotes an item on its own. Every line names a concrete action, the project, and a two-word source.
7. Send it with `teams_send_chat_message` to the self-chat id, `bodyType` text. Shape:

```
<Weekday> <d> <Mon>
1. <action> — <project> (<source>)
… up to 5
Meetings: <HH:MM title> · <HH:MM title>
Watch: GitLab <n> open, <m> overdue · <one line of FYI>
Captured <k> notes
```

   Twelve lines at most. Omit `Captured` when k is 0.
8. Immediately write the marker file `.claude/data/state/morning-brief-sent-MB_DATE`.
9. Append to `vault/daily/MB_DATE.md` a section `## Morning Brief (HH:MM)` containing the brief plus one evidence line per item (chat, session, calendar or MEMORY). Append-only: never edit earlier content. Create the file with the standard daily-log header if absent.
10. Update `morning-brief-state.json` with the newest self-chat message timestamp seen.
11. Print `BRIEF_SENT` as the last line of output.

If step 7 fails, do not write the marker, print `BRIEF_FAILED <reason>`, and stop.

### 5. `.claude/hooks/pre-tool-guardrail.py` (edit)

Add a connector branch before the final allow:

- Tool name ending in `teams_send_chat_message`: allow only if `tool_input.chatId` equals the self-chat id; otherwise block with reason `Teams send only allowed to Frank's notes-to-self chat`.
- Tool name ending in any of `teams_create_chat`, `teams_send_channel_message`, `teams_reply_channel_message`, `outlook_send_mail`, `outlook_send_draft`, `outlook_forward_mail`: always block.

Everything else unchanged. The self-chat id is a module constant so it is grep-able. This hook runs in interactive sessions too; messaging a colleague later requires deliberately loosening it.

### 6. `.claude/scripts/heartbeat.py` (edit)

Set `DAILY_DIR`, `DRAFTS_ACTIVE`, `DRAFTS_EXPIRED` to `vault/daily`, `vault/drafts/active`, `vault/drafts/expired` directly. Remove the left-brain preference and fallback block.

### 7. `.claude/skills/vault-structure/SKILL.md` (edit)

- Directory map: `daily/` and `drafts/` at the vault root are the canonical work log and draft store. `left-brain/ballys/daily/` is marked legacy, holding five April files, and `left-brain/ballys/drafts/` is removed from the map.
- Add `left-brain/ballys/inbox/YYYY-MM-DD.md` for raw dumps from the self-chat.
- Naming table rows for work daily log, AI news, and draft reply updated to the root paths; new row for inbox.
- `CLAUDE.md` landmine entry about the half-done migration rewritten to state the resolved rule.

### 8. `vault/SOUL.md` (Frank edits)

Rule 1 changes from "never send emails or Teams messages" to "never send emails; never send Teams messages except to Frank's own notes-to-self chat". The agent was denied reading this file in the current session, so Frank makes this one-line edit or re-grants the read.

## Data and state

| File | Owner | Content |
|---|---|---|
| `.claude/data/state/morning-brief-sent-YYYY-MM-DD` | shell + prompt | empty marker, one per day |
| `.claude/data/state/morning-brief-state.json` | prompt | `{"last_dump_ts": "..."}` |
| `.claude/data/state/run-YYYY-MM-DD/` | shell | `digest.md`, `gitlab.md`, kept for debugging; older than 7 days deleted by the shell at the start of each run |
| `vault/daily/YYYY-MM-DD.md` | prompt | `## Morning Brief (HH:MM)` section, append-only |
| `vault/left-brain/ballys/inbox/YYYY-MM-DD.md` | prompt | `- HH:MM \| text` lines |

## Error handling

- Any gate failure: exit 0, one log line, next tick retries. After 11:00 nothing runs until the next weekday.
- Digest or GitLab gather failure: continue with the one-line placeholder; the brief says so in `Watch`.
- Claude non-zero exit or missing `BRIEF_SENT`: no marker, log the tail of output, retry next tick. The in-prompt marker write prevents a second post if the send itself succeeded.
- Connector auth expired: the send fails, `BRIEF_FAILED` is printed, and the error log names the tool. Frank re-authenticates the Microsoft 365 connector in Claude.

## Verification

1. `python3 .claude/scripts/sessions_digest.py` lists game-experience-pipeline, ai-radar and interviewer for 30 Sep and nothing from `Contract/` or `Personal/`.
2. `bash .claude/scripts/morning_brief.sh --force` posts to the self-chat, appends the daily-log section, writes the marker, and prints `BRIEF_SENT`.
3. Hook: a fake `teams_send_chat_message` payload to the AI R&D Crew id returns block; to the self-chat id returns allow; a fake `outlook_send_mail` returns block.
4. `launchctl load` the plist, then the next tick's log line reads `already sent today`.
5. `./deploy/status.sh` shows the new plist loaded.

## Out of scope

- Afternoon or evening runs.
- Reading meeting transcripts (scope is granted, but historically produced nothing; separate task).
- Per-repo SessionStart status hooks in Ballys codebases (separate task).
- Any change to Cowork scheduled tasks.
