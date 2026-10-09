#!/usr/bin/env python3
"""
Memory Reflect — Daily reflection that promotes important items from daily logs
to MEMORY.md and archives stale entries.

Designed to run daily at 8 AM or be called manually. Does NOT use an LLM —
uses heuristic pattern matching to identify promotable items. The agent can
run this and then review/approve the suggestions.

Usage:
    python3 memory_reflect.py                    # Reflect on yesterday
    python3 memory_reflect.py --date 2026-04-10  # Reflect on specific date
    python3 memory_reflect.py --archive          # Also archive stale MEMORY.md entries
    python3 memory_reflect.py --dry-run          # Show what would change without writing
"""

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
VAULT_DIR = PROJECT_ROOT / "vault"
MEMORY_FILE = VAULT_DIR / "MEMORY.md"
DAILY_DIR = VAULT_DIR / "daily"

# Patterns that indicate something worth promoting to MEMORY.md
DECISION_PATTERNS = [
    r"(?i)\bdecided\b",
    r"(?i)\bagreed\b",
    r"(?i)\bapproved\b",
    r"(?i)\bblocked\b",
    r"(?i)\bdeadline\b.*(?:moved|changed|extended|set)",
    r"(?i)\bmilestone\b",
    r"(?i)\bshipped\b",
    r"(?i)\blaunched\b",
    r"(?i)\bmerged\b",
    r"(?i)\bcompleted\b.*(?:phase|sprint|task|issue)",
    r"(?i)\bnew\s+(?:project|repo|requirement)",
    r"(?i)\b(?:key|important)\s+(?:decision|finding|insight)",
]

LESSON_PATTERNS = [
    r"(?i)\blearned\b",
    r"(?i)\bfixed\b.*\bbug\b",
    r"(?i)\bworkaround\b",
    r"(?i)\bgotcha\b",
    r"(?i)\btip\b",
    r"(?i)\bnote\s*(?:to\s+self|for\s+future)",
    r"(?i)\bimportant\b.*\bnote\b",
]

ACTION_PATTERNS = [
    r"(?i)\btodo\b",
    r"(?i)\baction\s+item\b",
    r"(?i)\bfollow\s+up\b",
    r"(?i)\bwaiting\s+(?:on|for)\b",
    r"(?i)\bneed\s+to\b",
    r"(?i)\breminder\b",
]

STALE_DAYS = 14  # Entries older than this in MEMORY.md are candidates for archiving


def read_daily_log(date_str: str) -> str:
    """Read a daily log file."""
    log_file = DAILY_DIR / f"{date_str}.md"
    if log_file.exists():
        return log_file.read_text()
    return ""


def extract_promotable_items(content: str, date_str: str) -> dict:
    """Extract items worth promoting from a daily log."""
    items = {
        "decisions": [],
        "lessons": [],
        "action_items": [],
    }

    lines = content.splitlines()
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue

        # Check each pattern category
        for pattern in DECISION_PATTERNS:
            if re.search(pattern, line_stripped):
                items["decisions"].append({
                    "text": line_stripped.lstrip("- ").lstrip("* "),
                    "date": date_str,
                    "line": i + 1,
                })
                break

        for pattern in LESSON_PATTERNS:
            if re.search(pattern, line_stripped):
                items["lessons"].append({
                    "text": line_stripped.lstrip("- ").lstrip("* "),
                    "date": date_str,
                    "line": i + 1,
                })
                break

        for pattern in ACTION_PATTERNS:
            if re.search(pattern, line_stripped):
                items["action_items"].append({
                    "text": line_stripped.lstrip("- ").lstrip("* "),
                    "date": date_str,
                    "line": i + 1,
                })
                break

    return items


def find_stale_memory_entries(memory_content: str) -> list:
    """Find MEMORY.md entries that reference dates older than STALE_DAYS."""
    stale = []
    today = datetime.now().date()
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')

    lines = memory_content.splitlines()
    for i, line in enumerate(lines):
        matches = date_pattern.findall(line)
        for match in matches:
            try:
                entry_date = datetime.strptime(match, "%Y-%m-%d").date()
                if (today - entry_date).days > STALE_DAYS:
                    stale.append({
                        "line": i + 1,
                        "text": line.strip(),
                        "date": match,
                        "age_days": (today - entry_date).days,
                    })
            except ValueError:
                pass

    return stale


def check_memory_size(memory_content: str) -> dict:
    """Check if MEMORY.md is approaching or exceeding size limits."""
    lines = memory_content.splitlines()
    return {
        "line_count": len(lines),
        "limit": 100,
        "over_limit": len(lines) > 100,
        "approaching_limit": len(lines) > 80,
    }


def format_reflection_report(items: dict, stale: list, size: dict, date_str: str) -> str:
    """Format the reflection findings as a report."""
    lines = [f"# Memory Reflection — {date_str}\n"]

    # Promotable items
    total_items = sum(len(v) for v in items.values())
    if total_items == 0:
        lines.append("No items found worth promoting from the daily log.\n")
    else:
        if items["decisions"]:
            lines.append("## Decisions to Promote\n")
            lines.append("These should be added to MEMORY.md under 'Key Decisions':\n")
            for item in items["decisions"]:
                lines.append(f"- [{item['date']}] {item['text']}")
            lines.append("")

        if items["lessons"]:
            lines.append("## Lessons Learned\n")
            lines.append("These should be added to MEMORY.md under 'Lessons Learned':\n")
            for item in items["lessons"]:
                lines.append(f"- [{item['date']}] {item['text']}")
            lines.append("")

        if items["action_items"]:
            lines.append("## Action Items Found\n")
            lines.append("Verify these are tracked in GitLab or MEMORY.md:\n")
            for item in items["action_items"]:
                lines.append(f"- [{item['date']}] {item['text']}")
            lines.append("")

    # Stale entries
    if stale:
        lines.append(f"## Stale MEMORY.md Entries ({len(stale)} found)\n")
        lines.append("These entries reference dates older than 14 days and may need archiving:\n")
        for entry in stale[:10]:  # Cap at 10
            lines.append(f"- Line {entry['line']} ({entry['age_days']} days old): {entry['text'][:80]}...")
        lines.append("")

    # Size check
    if size["over_limit"]:
        lines.append(f"## ⚠️ MEMORY.md Over Limit\n")
        lines.append(f"Currently {size['line_count']} lines (limit: {size['limit']}). Needs summarization.\n")
    elif size["approaching_limit"]:
        lines.append(f"## MEMORY.md Size Warning\n")
        lines.append(f"Currently {size['line_count']} lines (limit: {size['limit']}). Consider trimming soon.\n")

    return "\n".join(lines)


def archive_stale_entries(memory_content: str, stale_entries: list) -> str:
    """Remove stale entries from MEMORY.md (returns updated content)."""
    lines = memory_content.splitlines()
    stale_line_numbers = {e["line"] - 1 for e in stale_entries}  # 0-indexed

    # Only remove lines that are list items (start with - or *)
    new_lines = []
    for i, line in enumerate(lines):
        if i in stale_line_numbers and line.strip().startswith(("-", "*")):
            continue  # Skip stale list items
        new_lines.append(line)

    return "\n".join(new_lines)


def main():
    parser = argparse.ArgumentParser(description="Daily memory reflection")
    parser.add_argument("--date", type=str, help="Date to reflect on (YYYY-MM-DD)")
    parser.add_argument("--archive", action="store_true", help="Archive stale MEMORY.md entries")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    # Determine which date to reflect on
    if args.date:
        reflect_date = args.date
    else:
        reflect_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Read daily log
    log_content = read_daily_log(reflect_date)
    if not log_content:
        print(f"No daily log found for {reflect_date}.")
        # Still check memory health
        if MEMORY_FILE.exists():
            memory_content = MEMORY_FILE.read_text()
            stale = find_stale_memory_entries(memory_content)
            size = check_memory_size(memory_content)
            if stale or size["over_limit"]:
                print(format_reflection_report({"decisions": [], "lessons": [], "action_items": []}, stale, size, reflect_date))
        return

    # Extract promotable items
    items = extract_promotable_items(log_content, reflect_date)

    # Check MEMORY.md health
    memory_content = MEMORY_FILE.read_text() if MEMORY_FILE.exists() else ""
    stale = find_stale_memory_entries(memory_content)
    size = check_memory_size(memory_content)

    # Output report
    report = format_reflection_report(items, stale, size, reflect_date)
    print(report)

    # Archive if requested
    if args.archive and stale and not args.dry_run:
        updated = archive_stale_entries(memory_content, stale)
        MEMORY_FILE.write_text(updated)
        print(f"\nArchived {len(stale)} stale entries from MEMORY.md.")
    elif args.archive and stale and args.dry_run:
        print(f"\n[DRY RUN] Would archive {len(stale)} stale entries from MEMORY.md.")


if __name__ == "__main__":
    main()
