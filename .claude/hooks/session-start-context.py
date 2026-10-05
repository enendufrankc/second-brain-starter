#!/usr/bin/env python3
"""
SessionStart hook: Injects vault memory into every Claude Code conversation.

Reads SOUL.md + USER.md + MEMORY.md + HABITS.md + recent daily logs.
Returns JSON on stdout with the proper hook output format.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Maximum context size to inject (chars) — leave room for the conversation
MAX_CONTEXT_CHARS = 30000


def find_vault() -> Path:
    """Find the vault directory relative to the working directory."""
    # Check env var first
    env_path = os.environ.get("SECOND_BRAIN_PATH", "")
    if env_path:
        vault = Path(env_path) / "vault"
        if vault.is_dir():
            return vault

    # Check cwd and parents
    cwd = Path(os.getcwd())
    for base in [cwd] + list(cwd.parents)[:5]:
        vault = base / "vault"
        if vault.is_dir() and (vault / "SOUL.md").exists():
            return vault

    # Hardcoded fallback for Frank's machine
    fallback = Path.home() / "Documents" / "Personal" / "Second Brain Starter" / "vault"
    if fallback.is_dir():
        return fallback

    return cwd / "vault"


def read_file(path: Path) -> str:
    """Read a file, return empty string if it doesn't exist."""
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return ""


def get_recent_daily_logs(vault: Path, count: int = 3) -> str:
    """Read the most recent N daily log files (excluding ai-news files)."""
    daily_dir = vault / "daily"
    if not daily_dir.is_dir():
        return ""

    # Only match YYYY-MM-DD.md pattern, exclude ai-news files
    log_files = sorted(
        [f for f in daily_dir.glob("????-??-??.md") if not f.name.startswith("ai-news")],
        reverse=True,
    )[:count]

    if not log_files:
        return ""

    sections = []
    for log_file in log_files:
        content = read_file(log_file)
        if content.strip():
            sections.append(f"### {log_file.stem}\n{content}")

    return "\n\n".join(sections)


def get_todays_action_items(vault: Path) -> str:
    """Extract unchecked items from HABITS.md."""
    habits = read_file(vault / "HABITS.md")
    if not habits:
        return ""

    unchecked = [
        line.strip()
        for line in habits.splitlines()
        if line.strip().startswith("- [ ]")
    ]
    if unchecked:
        return "### Unchecked Habits Today\n" + "\n".join(unchecked)
    return ""


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        hook_input = {}

    vault = find_vault()

    soul = read_file(vault / "SOUL.md")
    user = read_file(vault / "USER.md")
    memory = read_file(vault / "MEMORY.md")
    daily_logs = get_recent_daily_logs(vault)
    action_items = get_todays_action_items(vault)

    today = datetime.now().strftime("%Y-%m-%d %A")

    context_parts = [f"# Second Brain Context — {today}\n"]

    if soul:
        context_parts.append(soul)
    if user:
        context_parts.append(user)
    if memory:
        context_parts.append(memory)
    if action_items:
        context_parts.append(f"# TODAY'S ACTION ITEMS\n\n{action_items}")
    if daily_logs:
        context_parts.append(f"# RECENT DAILY LOGS\n\n{daily_logs}")

    additional_context = "\n\n---\n\n".join(context_parts)

    # Truncate if too long
    if len(additional_context) > MAX_CONTEXT_CHARS:
        additional_context = additional_context[:MAX_CONTEXT_CHARS] + "\n\n... (truncated)"

    # Output in the correct hook format
    result = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context
        }
    }
    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
