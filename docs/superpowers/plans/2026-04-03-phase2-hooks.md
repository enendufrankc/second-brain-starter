# Phase 2: Hooks (Context Persistence) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build three lifecycle hooks that inject vault memory into every Claude Code session and persist important context before it's lost to compaction or session end. Also includes a daily action tracker surfaced at session start.

**Architecture:** Python scripts in `.claude/hooks/` triggered by Claude Code lifecycle events. SessionStart reads vault files and outputs JSON to stdout (injected as conversation context). PreCompact and Stop hooks read the transcript and append important items to the daily log. Configured via `.claude/settings.json`.

**Tech Stack:** Python 3, JSON (stdin/stdout), Claude Code hooks API

---

## File Structure

| File | Responsibility |
|------|---------------|
| `.claude/hooks/session-start-context.py` | Read SOUL.md + USER.md + MEMORY.md + HABITS.md + last 3 daily logs + today's action items. Output JSON with `additionalContext` to stdout. |
| `.claude/hooks/pre-compact-flush.py` | Read transcript from `transcript_path`, extract key decisions/facts/action items, append to today's daily log. |
| `.claude/hooks/session-end-flush.py` | On Stop event, read transcript, extract session summary, append to daily log. |
| `.claude/settings.json` | Register all three hooks in the Claude Code hooks config. |

---

### Task 1: Create session-start-context.py

**Files:**
- Create: `.claude/hooks/session-start-context.py`

- [ ] **Step 1: Create the hooks directory**

```bash
mkdir -p .claude/hooks
```

- [ ] **Step 2: Write session-start-context.py**

Create `.claude/hooks/session-start-context.py`:

```python
#!/usr/bin/env python3
"""SessionStart hook: Injects vault memory into every Claude Code conversation."""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_vault() -> Path:
    """Find the vault directory relative to the working directory."""
    cwd = os.environ.get("CLAUDE_CWD", os.getcwd())
    vault = Path(cwd) / "vault"
    if vault.is_dir():
        return vault
    # Fallback: check if we're in a subdirectory of the project
    for parent in Path(cwd).parents:
        candidate = parent / "vault"
        if candidate.is_dir():
            return candidate
    return Path(cwd) / "vault"


def read_file(path: Path) -> str:
    """Read a file, return empty string if it doesn't exist."""
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return ""


def get_recent_daily_logs(vault: Path, count: int = 3) -> str:
    """Read the most recent N daily log files."""
    daily_dir = vault / "daily"
    if not daily_dir.is_dir():
        return ""

    log_files = sorted(daily_dir.glob("*.md"), reverse=True)[:count]
    if not log_files:
        return ""

    sections = []
    for log_file in log_files:
        content = read_file(log_file)
        if content.strip():
            sections.append(content)

    return "\n\n---\n\n".join(sections)


def get_todays_action_items(vault: Path) -> str:
    """Extract unchecked items from HABITS.md and any TODO items from recent logs."""
    lines = []

    # Unchecked habits
    habits = read_file(vault / "HABITS.md")
    if habits:
        unchecked = [
            line.strip()
            for line in habits.splitlines()
            if line.strip().startswith("- [ ]")
        ]
        if unchecked:
            lines.append("### Habits (unchecked today)")
            lines.extend(unchecked)

    # Heartbeat priorities
    heartbeat = read_file(vault / "HEARTBEAT.md")
    if heartbeat:
        lines.append("\n### Monitoring Priorities")
        for line in heartbeat.splitlines():
            if "Priority:" in line:
                lines.append(line.strip())

    return "\n".join(lines)


def main():
    # Read hook input from stdin (may be empty for SessionStart)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        hook_input = {}

    vault = find_vault()

    # Build context from vault files
    soul = read_file(vault / "SOUL.md")
    user = read_file(vault / "USER.md")
    memory = read_file(vault / "MEMORY.md")
    habits = read_file(vault / "HABITS.md")
    daily_logs = get_recent_daily_logs(vault)
    action_items = get_todays_action_items(vault)

    today = datetime.now().strftime("%Y-%m-%d %A")

    context_parts = [
        f"# Second Brain Context — {today}",
        "",
    ]

    if soul:
        context_parts.append(soul)
        context_parts.append("")

    if user:
        context_parts.append(user)
        context_parts.append("")

    if memory:
        context_parts.append(memory)
        context_parts.append("")

    if action_items:
        context_parts.append("# TODAY'S ACTION ITEMS")
        context_parts.append("")
        context_parts.append(action_items)
        context_parts.append("")

    if habits:
        context_parts.append(habits)
        context_parts.append("")

    if daily_logs:
        context_parts.append("# RECENT DAILY LOGS")
        context_parts.append("")
        context_parts.append(daily_logs)

    additional_context = "\n".join(context_parts)

    # Output JSON to stdout — Claude Code injects this into the conversation
    output = json.dumps(additional_context)
    print(output)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Make executable**

```bash
chmod +x .claude/hooks/session-start-context.py
```

- [ ] **Step 4: Test the hook locally**

```bash
echo '{}' | python3 .claude/hooks/session-start-context.py | head -5
```

Expected: JSON string containing the vault context (SOUL.md content as first part).

- [ ] **Step 5: Commit**

```bash
git add .claude/hooks/session-start-context.py
git commit -m "feat: add SessionStart hook that injects vault memory into conversations"
```

---

### Task 2: Create pre-compact-flush.py

**Files:**
- Create: `.claude/hooks/pre-compact-flush.py`

- [ ] **Step 1: Write pre-compact-flush.py**

Create `.claude/hooks/pre-compact-flush.py`:

```python
#!/usr/bin/env python3
"""PreCompact hook: Extracts key context from transcript before compaction."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def find_vault() -> Path:
    """Find the vault directory relative to the working directory."""
    cwd = os.environ.get("CLAUDE_CWD", os.getcwd())
    vault = Path(cwd) / "vault"
    if vault.is_dir():
        return vault
    for parent in Path(cwd).parents:
        candidate = parent / "vault"
        if candidate.is_dir():
            return candidate
    return Path(cwd) / "vault"


def read_transcript(transcript_path: str) -> list[dict]:
    """Read JSONL transcript file, return list of message dicts."""
    messages = []
    path = Path(transcript_path)
    if not path.exists():
        return messages
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except (FileNotFoundError, PermissionError):
        pass
    return messages


def extract_key_items(messages: list[dict]) -> list[str]:
    """Extract decisions, action items, and important facts from transcript messages."""
    items = []

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")

        # Handle content that might be a list of content blocks
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
            content = "\n".join(text_parts)

        if not isinstance(content, str):
            continue

        # Look for decision indicators
        lower = content.lower()
        for indicator in [
            "decided to", "decision:", "we agreed", "the plan is",
            "going with", "chose to", "will use", "switching to",
            "action item", "todo:", "need to", "must do",
            "important:", "key finding", "learned that", "turns out",
        ]:
            if indicator in lower:
                # Extract the sentence containing the indicator
                for sentence in content.split(". "):
                    if indicator in sentence.lower():
                        clean = sentence.strip().rstrip(".")
                        if 10 < len(clean) < 300:
                            items.append(clean)
                break

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for item in items:
        normalized = item.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(item)

    return unique[:10]  # Cap at 10 items per compaction


def append_to_daily_log(vault: Path, items: list[str]):
    """Append extracted items to today's daily log."""
    if not items:
        return

    today = datetime.now().strftime("%Y-%m-%d")
    daily_dir = vault / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    log_file = daily_dir / f"{today}.md"

    timestamp = datetime.now().strftime("%H:%M")

    lines = [f"\n- {timestamp} | [pre-compact] Key context extracted before compaction:"]
    for item in items:
        lines.append(f"  - {item}")

    if log_file.exists():
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    else:
        header = f"# {today} — Daily Log\n\n> Append-only. Never edit past entries. Timestamps in ET.\n\n## Log\n"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(lines) + "\n")


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        hook_input = {}

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    vault = find_vault()
    messages = read_transcript(transcript_path)

    if not messages:
        sys.exit(0)

    items = extract_key_items(messages)
    append_to_daily_log(vault, items)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Make executable**

```bash
chmod +x .claude/hooks/pre-compact-flush.py
```

- [ ] **Step 3: Commit**

```bash
git add .claude/hooks/pre-compact-flush.py
git commit -m "feat: add PreCompact hook that saves key context to daily log before compaction"
```

---

### Task 3: Create session-end-flush.py

**Files:**
- Create: `.claude/hooks/session-end-flush.py`

- [ ] **Step 1: Write session-end-flush.py**

Create `.claude/hooks/session-end-flush.py`:

```python
#!/usr/bin/env python3
"""Stop hook: Appends a session summary to today's daily log."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def find_vault() -> Path:
    """Find the vault directory relative to the working directory."""
    cwd = os.environ.get("CLAUDE_CWD", os.getcwd())
    vault = Path(cwd) / "vault"
    if vault.is_dir():
        return vault
    for parent in Path(cwd).parents:
        candidate = parent / "vault"
        if candidate.is_dir():
            return candidate
    return Path(cwd) / "vault"


def read_transcript(transcript_path: str) -> list[dict]:
    """Read JSONL transcript file, return list of message dicts."""
    messages = []
    path = Path(transcript_path)
    if not path.exists():
        return messages
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except (FileNotFoundError, PermissionError):
        pass
    return messages


def summarize_session(messages: list[dict]) -> str:
    """Create a brief summary of what happened in the session."""
    user_messages = []
    assistant_messages = []

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")

        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
            content = "\n".join(text_parts)

        if not isinstance(content, str):
            continue

        if role == "user":
            # Take first 200 chars of each user message
            user_messages.append(content[:200])
        elif role == "assistant":
            assistant_messages.append(content[:200])

    if not user_messages:
        return ""

    # Build a brief summary from user requests
    topics = []
    for msg in user_messages[:5]:  # First 5 user messages
        first_line = msg.split("\n")[0].strip()
        if first_line and len(first_line) > 5:
            topics.append(first_line)

    if topics:
        return "Topics: " + " | ".join(topics[:3])

    return "Session with no clear topic extracted"


def append_to_daily_log(vault: Path, summary: str):
    """Append session summary to today's daily log."""
    if not summary:
        return

    today = datetime.now().strftime("%Y-%m-%d")
    daily_dir = vault / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    log_file = daily_dir / f"{today}.md"

    timestamp = datetime.now().strftime("%H:%M")
    entry = f"\n- {timestamp} | [session-end] {summary}\n"

    if log_file.exists():
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)
    else:
        header = f"# {today} — Daily Log\n\n> Append-only. Never edit past entries. Timestamps in ET.\n\n## Log\n"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(header + entry)


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        hook_input = {}

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    vault = find_vault()
    messages = read_transcript(transcript_path)

    if not messages:
        sys.exit(0)

    summary = summarize_session(messages)
    append_to_daily_log(vault, summary)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Make executable**

```bash
chmod +x .claude/hooks/session-end-flush.py
```

- [ ] **Step 3: Commit**

```bash
git add .claude/hooks/session-end-flush.py
git commit -m "feat: add Stop hook that saves session summary to daily log"
```

---

### Task 4: Configure hooks in settings.json

**Files:**
- Create: `.claude/settings.json`

- [ ] **Step 1: Write settings.json**

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/session-start-context.py"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-compact-flush.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/session-end-flush.py"
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -c "import json; json.load(open('.claude/settings.json')); print('Valid JSON')"
```

Expected: `Valid JSON`

- [ ] **Step 3: Commit**

```bash
git add .claude/settings.json
git commit -m "feat: register SessionStart, PreCompact, and Stop hooks in settings.json"
```

---

### Task 5: End-to-end test

- [ ] **Step 1: Test SessionStart hook**

```bash
echo '{}' | python3 .claude/hooks/session-start-context.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('Context length:', len(d), 'chars'); print('Has SOUL:', 'SOUL' in d); print('Has ACTION ITEMS:', 'ACTION ITEMS' in d)"
```

Expected:
```
Context length: [number] chars
Has SOUL: True
Has ACTION ITEMS: True
```

- [ ] **Step 2: Test PreCompact hook with empty input**

```bash
echo '{}' | python3 .claude/hooks/pre-compact-flush.py; echo "Exit code: $?"
```

Expected: `Exit code: 0` (graceful exit when no transcript)

- [ ] **Step 3: Test Stop hook with empty input**

```bash
echo '{}' | python3 .claude/hooks/session-end-flush.py; echo "Exit code: $?"
```

Expected: `Exit code: 0` (graceful exit when no transcript)

- [ ] **Step 4: Verify all hooks are executable**

```bash
ls -la .claude/hooks/*.py
```

Expected: All three files with execute permission (-rwxr-xr-x or similar)

---
