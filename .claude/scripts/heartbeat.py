#!/usr/bin/env python3
"""
Heartbeat — Proactive monitoring system for Frank's second brain.

Gathers data from all integrations, diffs against previous state, and outputs
a structured report for the agent (or scheduled task) to act on.

This is the "gather" phase — it runs Python-only (no LLM calls) to collect
data cheaply, then outputs a JSON/markdown report that can be passed to Claude
for reasoning and action.

Usage:
    python3 heartbeat.py                    # Full heartbeat cycle
    python3 heartbeat.py --check teams      # Only check Teams
    python3 heartbeat.py --check gitlab     # Only check GitLab
    python3 heartbeat.py --check outlook    # Only check Outlook
    python3 heartbeat.py --check habits     # Only check habits
    python3 heartbeat.py --check drafts     # Only check draft expiry
    python3 heartbeat.py --json             # JSON output
    python3 heartbeat.py --quiet            # Only output if something needs attention
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
VAULT_DIR = PROJECT_ROOT / "vault"
INTEGRATIONS_DIR = SCRIPT_DIR / "integrations"
STATE_FILE = PROJECT_ROOT / ".claude" / "data" / "state" / "heartbeat-state.json"
DAILY_DIR = VAULT_DIR / "daily"
DRAFTS_ACTIVE = VAULT_DIR / "drafts" / "active"
DRAFTS_EXPIRED = VAULT_DIR / "drafts" / "expired"


def load_state() -> dict:
    """Load previous heartbeat state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_state(state: dict):
    """Save heartbeat state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str))


def run_integration(module: str, command: str) -> str:
    """Run an integration script and capture output."""
    script = INTEGRATIONS_DIR / f"{module}.py"
    if not script.exists():
        return ""
    try:
        result = subprocess.run(
            [sys.executable, str(script), command],
            capture_output=True, text=True, timeout=30,
            cwd=str(PROJECT_ROOT),
            env={**os.environ, "PYTHONPATH": str(SCRIPT_DIR)},
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, Exception):
        return ""


def check_gitlab() -> dict:
    """Check GitLab for issues, MRs, and pipeline status."""
    return {
        "issues": run_integration("gitlab_integration", "issues"),
        "mrs": run_integration("gitlab_integration", "mrs"),
        "pipelines": run_integration("gitlab_integration", "pipelines"),
    }


def check_teams() -> dict:
    """Check Teams messages and calendar."""
    return {
        "messages": run_integration("teams", "messages"),
        "calendar": run_integration("teams", "calendar"),
    }


def check_outlook() -> dict:
    """Check Outlook inbox."""
    return {
        "unread": run_integration("outlook", "unread"),
        "summary": run_integration("outlook", "summary"),
    }


def check_drafts() -> dict:
    """Check for stale drafts and expire them."""
    results = {"expired": [], "active_count": 0}
    today = datetime.now().date()

    if not DRAFTS_ACTIVE.exists():
        return results

    for draft in DRAFTS_ACTIVE.glob("*.md"):
        results["active_count"] += 1
        try:
            date_str = draft.name[:10]
            draft_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            age_hours = (datetime.now() - datetime.combine(draft_date, datetime.min.time())).total_seconds() / 3600
            if age_hours > 24:
                # Move to expired
                DRAFTS_EXPIRED.mkdir(parents=True, exist_ok=True)
                shutil.move(str(draft), str(DRAFTS_EXPIRED / draft.name))
                results["expired"].append(draft.name)
                results["active_count"] -= 1
        except ValueError:
            pass

    return results


def check_habits() -> dict:
    """Check habits status for today."""
    habits_file = VAULT_DIR / "HABITS.md"
    if not habits_file.exists():
        return {"status": "no_habits_file"}

    content = habits_file.read_text()
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Count checked vs unchecked pillars
    checked = content.count("[x]") + content.count("[X]")
    unchecked = content.count("[ ]")
    total = checked + unchecked

    return {
        "date_current": today_str in content,
        "checked": checked,
        "unchecked": unchecked,
        "total": total,
        "needs_reset": today_str not in content,
        "late_day_nudge": unchecked >= 2 and datetime.now().hour >= 17,
    }


def diff_state(current: dict, previous: dict) -> dict:
    """Compare current data against previous state to find changes."""
    changes = {
        "new_items": [],
        "resolved_items": [],
        "unchanged": True,
    }

    # Simple hash-based diff: if the output text changed, something happened
    for key in current:
        if isinstance(current[key], dict):
            for subkey in current[key]:
                curr_val = current[key].get(subkey, "")
                prev_val = previous.get(key, {}).get(subkey, "")
                if curr_val != prev_val and curr_val:
                    changes["new_items"].append(f"{key}.{subkey} changed")
                    changes["unchanged"] = False
        elif isinstance(current[key], str):
            if current[key] != previous.get(key, ""):
                changes["new_items"].append(f"{key} changed")
                changes["unchanged"] = False

    return changes


def format_report(data: dict, changes: dict, quiet: bool = False) -> str:
    """Format heartbeat data as a markdown report."""
    if quiet and changes.get("unchanged", True):
        return ""

    now = datetime.now()
    lines = [f"# Heartbeat — {now.strftime('%Y-%m-%d %H:%M')}\n"]

    if changes.get("unchanged"):
        lines.append("No changes since last check.\n")
        return "\n".join(lines)

    # GitLab
    gitlab = data.get("gitlab", {})
    if gitlab.get("issues"):
        lines.append("## GitLab Issues\n")
        lines.append(gitlab["issues"])
        lines.append("")
    if gitlab.get("mrs"):
        lines.append("## Merge Requests\n")
        lines.append(gitlab["mrs"])
        lines.append("")
    if gitlab.get("pipelines"):
        lines.append("## Pipelines\n")
        lines.append(gitlab["pipelines"])
        lines.append("")

    # Teams
    teams = data.get("teams", {})
    if teams.get("messages"):
        lines.append("## Teams Messages\n")
        lines.append(teams["messages"])
        lines.append("")
    if teams.get("calendar"):
        lines.append("## Calendar\n")
        lines.append(teams["calendar"])
        lines.append("")

    # Outlook
    outlook = data.get("outlook", {})
    if outlook.get("unread"):
        lines.append("## Unread Emails\n")
        lines.append(outlook["unread"])
        lines.append("")

    # Drafts
    drafts = data.get("drafts", {})
    if drafts.get("expired"):
        lines.append("## Draft Management\n")
        for d in drafts["expired"]:
            lines.append(f"- Expired: {d}")
        lines.append("")
    if drafts.get("active_count", 0) > 0:
        lines.append(f"Active drafts pending review: {drafts['active_count']}\n")

    # Habits
    habits = data.get("habits", {})
    if habits.get("late_day_nudge"):
        lines.append("## Habits Nudge\n")
        lines.append(f"You have {habits['unchecked']} unchecked pillars today. Consider:")
        lines.append("- Did you make progress on your main project?")
        lines.append("- Any R&D exploration or team collaboration today?")
        lines.append("- Don't forget health and side projects!\n")
    elif habits.get("needs_reset"):
        lines.append("## Habits\n")
        lines.append("HABITS.md needs a daily reset.\n")

    # Changes summary
    if changes.get("new_items"):
        lines.append("## Changes Since Last Check\n")
        for item in changes["new_items"]:
            lines.append(f"- {item}")

    return "\n".join(lines)


def append_to_daily_log(content: str):
    """Append heartbeat summary to today's daily log."""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = DAILY_DIR / f"{today}.md"

    timestamp = datetime.now().strftime("%H:%M")
    entry = f"\n## {timestamp} — Heartbeat\n\n{content}\n"

    if log_file.exists():
        with open(log_file, "a") as f:
            f.write(entry)
    else:
        with open(log_file, "w") as f:
            f.write(f"# Daily Log — {datetime.now().strftime('%A, %B %d, %Y')}\n{entry}")


def main():
    parser = argparse.ArgumentParser(description="Second Brain Heartbeat")
    parser.add_argument("--check", choices=["teams", "gitlab", "outlook", "habits", "drafts"],
                        help="Only check specific integration")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--quiet", action="store_true", help="Only output if changes detected")
    parser.add_argument("--no-log", action="store_true", help="Don't append to daily log")
    args = parser.parse_args()

    previous_state = load_state()
    current_data = {}

    if args.check:
        checks = {args.check}
    else:
        checks = {"gitlab", "teams", "outlook", "drafts", "habits"}

    if "gitlab" in checks:
        current_data["gitlab"] = check_gitlab()
    if "teams" in checks:
        current_data["teams"] = check_teams()
    if "outlook" in checks:
        current_data["outlook"] = check_outlook()
    if "drafts" in checks:
        current_data["drafts"] = check_drafts()
    if "habits" in checks:
        current_data["habits"] = check_habits()

    # Diff against previous
    changes = diff_state(current_data, previous_state.get("data", {}))

    # Save new state
    save_state({
        "last_run": datetime.now().isoformat(),
        "data": current_data,
    })

    if args.json:
        output = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "data": current_data,
            "changes": changes,
        }, indent=2, default=str)
        print(output)
    else:
        report = format_report(current_data, changes, args.quiet)
        if report:
            print(report)
            if not args.no_log and not args.quiet:
                # Append a brief summary to daily log
                brief = f"Heartbeat ran. Changes: {len(changes.get('new_items', []))} detected."
                append_to_daily_log(brief)
        elif args.quiet:
            pass  # Silent when no changes
        else:
            print("Heartbeat: no changes detected.")


if __name__ == "__main__":
    main()
