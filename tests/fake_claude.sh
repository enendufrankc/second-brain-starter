#!/bin/bash
# Test stand-in for the claude binary. Behaves per FAKE_CLAUDE_MODE.
# Save argv to file if requested (for test inspection).
if [[ -n "${FAKE_CLAUDE_ARGV:-}" && -w "$(dirname "$FAKE_CLAUDE_ARGV")" ]]; then
  {
    for arg in "$@"; do
      printf '%s\n' "$arg"
    done
  } >> "$FAKE_CLAUDE_ARGV" 2>/dev/null || true
fi
case "${FAKE_CLAUDE_MODE:-ok}" in
  ok)      echo "did things"; echo "BRIEF_SENT"; exit 0 ;;
  notoken) echo "did things but no sentinel"; exit 0 ;;
  fail)    echo "BRIEF_FAILED boom"; exit 1 ;;
  hang)    exec sleep 30 ;;
esac
