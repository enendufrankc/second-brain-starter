#!/bin/bash
# Morning brief runner. Design: docs/superpowers/specs/2026-10-01-morning-brief-design.md
# launchd calls this every 10 minutes. It exits fast unless the gate passes,
# then gathers inputs and runs one headless Claude session that posts to Teams.
# State (markers, cursor, run dirs) lives in .morning-brief/, not .claude/: headless claude cannot write under .claude/.
# Environment: MB_STATE_DIR, MB_DATE, MB_FAKE_NOW, MB_FAKE_NOW_ISO, MB_FAKE_DOW, MB_SKIP_VPN,
# MB_SKIP_CLAUDE (dry-run), MB_SKIP_GATHER (test mode: skip collectors), MB_CLAUDE_BIN, MB_CLAUDE_TIMEOUT
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

STATE_DIR="${MB_STATE_DIR:-$PROJECT_DIR/.morning-brief}"
TODAY="${MB_DATE:-$(date +%Y-%m-%d)}"
NOW_HHMM="${MB_FAKE_NOW:-$(date +%H%M)}"
NOW_HM="${NOW_HHMM:0:2}:${NOW_HHMM:2:2}"
NOW_ISO="${MB_FAKE_NOW_ISO:-$(date +%Y-%m-%dT%H:%M:%S%z)}"
DOW="${MB_FAKE_DOW:-$(date +%u)}"
PROBE_URL="${MB_PROBE_URL:-https://gitlab.ballys.tech/api/v4/version}"
CLAUDE_BIN="${MB_CLAUDE_BIN:-$HOME/.local/bin/claude}"
MARKER="$STATE_DIR/morning-brief-sent-$TODAY"
RUN_DIR="$STATE_DIR/run-$TODAY"
PROMPT_FILE="$SCRIPT_DIR/morning_brief_prompt.md"

FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1

log() { printf '%s | %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

mkdir -p "$STATE_DIR"

if (( FORCE == 0 )); then
  if (( DOW >= 6 )); then log "skip: weekend"; exit 0; fi
  if (( 10#$NOW_HHMM < 630 || 10#$NOW_HHMM > 1100 )); then log "skip: outside window ($NOW_HHMM)"; exit 0; fi
  if [[ -e "$MARKER" ]]; then log "skip: already sent today"; exit 0; fi
fi

if [[ "${MB_SKIP_VPN:-0}" != "1" ]]; then
  code="$(curl -s -o /dev/null -m 5 -w '%{http_code}' "$PROBE_URL" || true)"
  case "$code" in
    200|401) ;;
    *) log "skip: VPN down (probe ${code:-000})"; exit 0 ;;
  esac
fi

mkdir -p "$RUN_DIR"
find "$STATE_DIR" -path "$STATE_DIR/run-*" -type f -mtime +7 -delete 2>/dev/null || true
find "$STATE_DIR" -mindepth 1 -maxdepth 1 -type d -name 'run-*' ! -name "run-$TODAY" -empty -delete 2>/dev/null || true

if [[ "${MB_SKIP_GATHER:-0}" == "1" ]]; then
  log "gather: skipped (test mode)"
  echo "Sessions digest (test mode)." > "$RUN_DIR/digest.md"
  echo "GitLab issues (test mode)." > "$RUN_DIR/gitlab.md"
  echo "- AI news (test mode)." > "$RUN_DIR/news.md"
else
  log "gather: sessions digest"
  python3 .claude/scripts/sessions_digest.py --hours 36 > "$RUN_DIR/digest.md" 2>>"$RUN_DIR/gather.err" \
    || echo "Session digest unavailable." > "$RUN_DIR/digest.md"

  log "gather: gitlab"
  python3 .claude/scripts/integrations/gitlab_integration.py issues > "$RUN_DIR/gitlab.md" 2>>"$RUN_DIR/gather.err" \
    || echo "GitLab unavailable: check GITLAB_PAT." > "$RUN_DIR/gitlab.md"

  log "gather: news"
  if ! python3 .claude/scripts/news_digest.py --hours 24 > "$RUN_DIR/news.md" 2>>"$RUN_DIR/gather.err" \
     || ! grep -q '^- ' "$RUN_DIR/news.md"; then
    echo "AI news unavailable." > "$RUN_DIR/news.md"
  fi
fi

if [[ "${MB_SKIP_CLAUDE:-0}" == "1" ]]; then
  log "DRY_RUN: gather complete in $RUN_DIR"
  exit 0
fi

if [[ ! -x "$CLAUDE_BIN" ]]; then log "fail: claude binary not found at $CLAUDE_BIN"; exit 1; fi

if [[ ! -f "$PROMPT_FILE" ]]; then log "fail: prompt file not found at $PROMPT_FILE"; exit 1; fi

prompt="$(sed -e "s|{{RUN_DIR}}|$RUN_DIR|g" -e "s|{{STATE_DIR}}|$STATE_DIR|g" -e "s|{{DATE}}|$TODAY|g" -e "s|{{NOW}}|$NOW_HM|g" -e "s|{{NOW_ISO}}|$NOW_ISO|g" "$PROMPT_FILE")"

CLAUDE_TIMEOUT="${MB_CLAUDE_TIMEOUT:-900}"
log "run: claude -p (timeout ${CLAUDE_TIMEOUT}s)"
set +e
{
  "$CLAUDE_BIN" -p "$prompt" --output-format text \
    --allowedTools "Read" "Write" "Edit" "Bash(python3 .claude/scripts/sanitize.py:*)" \
      "WebFetch(domain:www.anthropic.com)" \
      "mcp__claude_ai_Microsoft_365__chat_message_search" \
      "mcp__claude_ai_Microsoft_365__read_resource" \
      "mcp__claude_ai_Microsoft_365__outlook_calendar_search" \
      "mcp__claude_ai_Microsoft_365__teams_send_chat_message" \
    </dev/null >"$RUN_DIR/claude.out" 2>>"$RUN_DIR/claude.err" &
  claude_pid=$!
  ( sleep "$CLAUDE_TIMEOUT"; kill -9 "$claude_pid" 2>/dev/null && echo "watchdog: killed claude after ${CLAUDE_TIMEOUT}s" >>"$RUN_DIR/claude.err" ) >/dev/null 2>&1 &
  watchdog_pid=$!
  wait "$claude_pid"
  rc=$?
  pkill -P "$watchdog_pid" 2>/dev/null || true
  kill "$watchdog_pid" 2>/dev/null || true
  wait "$watchdog_pid" 2>/dev/null || true
  set -e
  out="$(cat "$RUN_DIR/claude.out")"
}

if (( rc == 0 )) && grep -q 'BRIEF_SENT' <<<"$out"; then
  touch "$MARKER"
  log "done: brief sent ($(tail -n 1 <<<"$out"))"
  exit 0
fi
log "fail: rc=$rc, see $RUN_DIR/claude.out and claude.err"
exit 1
