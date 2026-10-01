#!/usr/bin/env python3
"""
Sessions Digest — summarise recent Claude Code and Codex transcripts per repo
so the morning brief knows what Frank was working on. No LLM.

Only repos under ~/Documents/Work and ~/Documents/Projects are included.
Contract and Personal repos are excluded so client names never reach the
work brief.

Usage:
    python3 .claude/scripts/sessions_digest.py              # last 36 h, markdown
    python3 .claude/scripts/sessions_digest.py --hours 48 --json
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

INCLUDE_PREFIXES = ("Documents/Work", "Documents/Projects")
NOISE_PREFIXES = (
    "<system-reminder>", "<command-name>", "<command-message>", "<local-command",
    "<skills_instructions>", "<environment_context>", "# AGENTS.md instructions",
    "<task-notification>", "<pasted_content",
)
TEXT_BLOCK_TYPES = ("text", "input_text", "output_text")
ASK_CHARS = 300
ASSISTANT_CHARS = 500


def truncate(text: str, limit: int) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    return collapsed[:limit]


def text_of(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [b["text"] for b in content
                 if isinstance(b, dict) and b.get("type") in TEXT_BLOCK_TYPES and b.get("text")]
        return "\n".join(parts).strip()
    return ""


def is_noise(text: str) -> bool:
    return not text or text.startswith(NOISE_PREFIXES)


def parse_claude(path: Path) -> dict | None:
    cwd = None
    users, assistants = [], []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = row.get("type")
            if kind not in ("user", "assistant"):
                continue
            cwd = cwd or row.get("cwd")
            if row.get("isSidechain"):
                continue
            text = text_of((row.get("message") or {}).get("content"))
            if is_noise(text):
                continue
            (users if kind == "user" else assistants).append((row.get("timestamp", ""), text))
    if not cwd:
        return None
    return {"cwd": cwd, "users": users, "assistants": assistants}


def parse_codex(path: Path) -> dict | None:
    cwd = None
    users, assistants = [], []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = row.get("payload") or {}
            if row.get("type") == "session_meta":
                cwd = payload.get("cwd")
                continue
            if row.get("type") != "response_item" or payload.get("type") != "message":
                continue
            text = text_of(payload.get("content"))
            role = payload.get("role")
            if role == "user" and not is_noise(text):
                users.append((row.get("timestamp", ""), text))
            elif role == "assistant" and text:
                assistants.append((row.get("timestamp", ""), text))
    if not cwd:
        return None
    return {"cwd": cwd, "users": users, "assistants": assistants}


def in_scope(cwd: str, home: Path) -> bool:
    try:
        rel = Path(cwd).resolve().relative_to(home.resolve()).as_posix()
    except ValueError:
        return False
    return rel.startswith(INCLUDE_PREFIXES)


def collect(claude_dir: Path, codex_dir: Path, hours: int, home: Path, now: float | None = None) -> list[dict]:
    now = now or time.time()
    cutoff = now - hours * 3600
    grouped: dict[str, dict] = {}
    warnings: list[str] = []

    candidates = [(p, parse_claude) for p in claude_dir.glob("*/*.jsonl")] + \
                 [(p, parse_codex) for p in codex_dir.rglob("*.jsonl")]
    for path, parser in candidates:
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if mtime < cutoff:
            continue
        try:
            parsed = parser(path)
        except Exception as exc:
            warnings.append(f"{path.name}: {exc.__class__.__name__}")
            continue
        if not parsed or not in_scope(parsed["cwd"], home):
            continue
        bucket = grouped.setdefault(parsed["cwd"], {"users": [], "assistants": [], "sessions": 0, "last_active": 0.0})
        bucket["users"].extend(parsed["users"])
        bucket["assistants"].extend(parsed["assistants"])
        bucket["sessions"] += 1
        bucket["last_active"] = max(bucket["last_active"], mtime)

    repos = []
    for cwd, bucket in grouped.items():
        users = sorted(bucket["users"], key=lambda t: t[0])
        assistants = sorted(bucket["assistants"], key=lambda t: t[0])
        if not users and not assistants:
            continue
        repos.append({
            "repo": Path(cwd).name,
            "cwd": cwd,
            "sessions": bucket["sessions"],
            "last_active": bucket["last_active"],
            "first_ask": truncate(users[0][1], ASK_CHARS) if users else "",
            "last_asks": [truncate(t, ASK_CHARS) for _, t in users[-2:]],
            "last_assistant": truncate(assistants[-1][1], ASSISTANT_CHARS) if assistants else "",
        })
    repos.sort(key=lambda r: r["last_active"], reverse=True)
    collect.warnings = warnings  # exposed for main(); tests call collect() directly
    return repos


def format_markdown(repos: list[dict], warnings: list[str]) -> str:
    if not repos:
        lines = ["No work sessions in the window."]
    else:
        lines = []
        for r in repos:
            when = datetime.fromtimestamp(r["last_active"]).strftime("%H:%M")
            lines.append(f"## {r['repo']}  ({r['sessions']} sessions, last active {when})")
            lines.append(f"- First ask: {r['first_ask']}")
            lines.append(f"- Last asks: {' | '.join(r['last_asks'])}")
            lines.append(f"- Last assistant: {r['last_assistant']}")
            lines.append("")
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"- {w}" for w in warnings)
    return "\n".join(lines).rstrip()


def main():
    parser = argparse.ArgumentParser(description="Digest recent Claude Code and Codex sessions per repo")
    parser.add_argument("--hours", type=int, default=36)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--claude-dir", type=Path, default=None)
    parser.add_argument("--codex-dir", type=Path, default=None)
    args = parser.parse_args()

    claude_dir = args.claude_dir or args.home / ".claude" / "projects"
    codex_dir = args.codex_dir or args.home / ".codex" / "sessions"
    repos = collect(claude_dir, codex_dir, args.hours, args.home)
    warnings = getattr(collect, "warnings", [])
    if args.json:
        print(json.dumps({"repos": repos, "warnings": warnings}, indent=2))
    else:
        print(format_markdown(repos, warnings))


if __name__ == "__main__":
    main()
