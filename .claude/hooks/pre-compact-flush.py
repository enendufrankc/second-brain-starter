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
    """Extract decisions, action items, and important facts from transcript."""
    items = []

    for msg in messages:
        content = msg.get("content", "")

        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
            content = "\n".join(text_parts)

        if not isinstance(content, str):
            continue

        lower = content.lower()
        for indicator in [
            "decided to", "decision:", "we agreed", "the plan is",
            "going with", "chose to", "will use", "switching to",
            "action item", "todo:", "need to", "must do",
            "important:", "key finding", "learned that", "turns out",
        ]:
            if indicator in lower:
                for sentence in content.split(". "):
                    if indicator in sentence.lower():
                        clean = sentence.strip().rstrip(".")
                        if 10 < len(clean) < 300:
                            items.append(clean)
                break

    seen = set()
    unique = []
    for item in items:
        normalized = item.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(item)

    return unique[:10]


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
