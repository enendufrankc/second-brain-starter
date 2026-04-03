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
            user_messages.append(content[:200])

    if not user_messages:
        return ""

    topics = []
    for msg in user_messages[:5]:
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
