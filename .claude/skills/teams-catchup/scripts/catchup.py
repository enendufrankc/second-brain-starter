#!/usr/bin/env python3
"""
Teams Catchup — Gathers Teams messages + calendar events and formats them
for the agent to triage into: needs attention, FYI, can wait.

This script uses the M365 MCP connector (when available in Cowork) or falls back
to the Microsoft Graph integration scripts. It outputs structured data that the
agent then reasons over.

Usage:
    python3 catchup.py                  # Default: last 24 hours
    python3 catchup.py --hours 48       # Custom lookback window
    python3 catchup.py --json           # Machine-readable output
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent  # skills/teams-catchup/scripts -> root
INTEGRATIONS_DIR = PROJECT_ROOT / ".claude" / "scripts" / "integrations"
VAULT_DIR = PROJECT_ROOT / "vault"

# Frank's key contacts — messages from these people are higher priority
PRIORITY_SENDERS = [
    "al jepps", "alastair jepps",
    "sudhanva", "sudhanva mysore ganesh",
    "lynn murphy",
    "juan impey",
    "miguel caron",
    "sherrine",
]

# Noise senders — auto-classify as "can wait"
NOISE_PATTERNS = [
    "bot", "notification", "automated", "noreply", "no-reply",
    "splunk", "azure devops", "system",
]


def run_integration(module: str, command: str) -> str:
    """Run an integration script and capture output."""
    script = INTEGRATIONS_DIR / f"{module}.py"
    if not script.exists():
        return f"Integration script not found: {module}.py"
    try:
        result = subprocess.run(
            [sys.executable, str(script), command],
            capture_output=True, text=True, timeout=30,
            cwd=str(PROJECT_ROOT),
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return f"Timeout running {module} {command}"
    except Exception as e:
        return f"Failed to run {module} {command}: {e}"


def read_memory_context() -> str:
    """Read MEMORY.md for context about active deadlines."""
    memory_file = VAULT_DIR / "MEMORY.md"
    if memory_file.exists():
        return memory_file.read_text()[:2000]
    return ""


def read_recent_daily_log() -> str:
    """Read today's daily log if it exists."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = VAULT_DIR / "daily" / f"{today}.md"
    if log_file.exists():
        return log_file.read_text()[:1000]
    return ""


def classify_sender(sender_name: str) -> str:
    """Classify a message sender as priority, normal, or noise."""
    name_lower = sender_name.lower()
    for noise in NOISE_PATTERNS:
        if noise in name_lower:
            return "noise"
    for priority in PRIORITY_SENDERS:
        if priority in name_lower:
            return "priority"
    return "normal"


def gather_catchup_data(hours: int = 24) -> dict:
    """Gather all data needed for catchup."""
    since = (datetime.now() - timedelta(hours=hours)).isoformat()

    data = {
        "timestamp": datetime.now().isoformat(),
        "lookback_hours": hours,
        "teams": {
            "messages": run_integration("teams", "messages"),
            "calendar": run_integration("teams", "calendar"),
        },
        "outlook": {
            "unread": run_integration("outlook", "unread"),
        },
        "context": {
            "memory": read_memory_context(),
            "daily_log": read_recent_daily_log(),
        },
    }
    return data


def format_catchup_report(data: dict) -> str:
    """Format catchup data as a markdown report for the agent."""
    lines = [
        f"# Teams Catchup — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Lookback: {data['lookback_hours']} hours\n",
        "---\n",
        "## Teams Messages\n",
        data["teams"]["messages"],
        "\n---\n",
        "## Calendar\n",
        data["teams"]["calendar"],
        "\n---\n",
        "## Unread Emails\n",
        data["outlook"]["unread"],
        "\n---\n",
        "## Active Context (from MEMORY.md)\n",
        data["context"]["memory"][:500] if data["context"]["memory"] else "No memory context loaded.",
    ]

    lines.extend([
        "\n---\n",
        "## Agent Instructions\n",
        "Triage the above into three buckets:\n",
        "### 🔴 Needs Your Attention",
        "- Direct questions from priority contacts (Al, Sudhanva, Lynn, Juan)",
        "- Meeting invites requiring response",
        "- DMs waiting for reply (note how long they've waited)",
        "- Anything mentioning deadlines in MEMORY.md\n",
        "### 🟡 FYI — Worth Knowing",
        "- Team updates, shipped features, shared links",
        "- Calendar changes",
        "- General discussion highlights\n",
        "### ⚪ Can Wait",
        "- Casual chat, social messages",
        "- Automated notifications",
        "- Already seen/replied messages",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Teams catchup — what did Frank miss?")
    parser.add_argument("--hours", type=int, default=24, help="Lookback window in hours")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    data = gather_catchup_data(args.hours)

    if args.json:
        print(json.dumps(data, indent=2, default=str))
    else:
        print(format_catchup_report(data))


if __name__ == "__main__":
    main()
