#!/usr/bin/env python3
"""SessionStart hook: Injects vault memory into every Claude Code conversation."""

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
    """Extract unchecked items from HABITS.md and monitoring priorities."""
    lines = []

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

    heartbeat = read_file(vault / "HEARTBEAT.md")
    if heartbeat:
        lines.append("\n### Monitoring Priorities")
        for line in heartbeat.splitlines():
            if "Priority:" in line:
                lines.append(line.strip())

    return "\n".join(lines)


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        hook_input = {}

    vault = find_vault()

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

    output = json.dumps(additional_context)
    print(output)


if __name__ == "__main__":
    main()
