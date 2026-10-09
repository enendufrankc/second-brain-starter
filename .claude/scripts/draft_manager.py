#!/usr/bin/env python3
"""
Draft Manager — Manages the lifecycle of auto-generated reply drafts.

Draft lifecycle:
  1. Agent creates draft in vault/drafts/active/YYYY-MM-DD_<type>_<slug>.md
  2. This script checks for stale drafts (>24h) and moves them to expired/
  3. When Frank actually sends a reply, the agent moves the draft to sent/
  4. Sent drafts are used for voice-matching via memory_search.py

Usage:
    python3 draft_manager.py status          # Show active/expired/sent counts
    python3 draft_manager.py expire          # Move stale drafts to expired/
    python3 draft_manager.py create          # Create a new draft (interactive)
    python3 draft_manager.py list            # List all active drafts
    python3 draft_manager.py mark-sent <file> # Move a draft to sent/
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
VAULT_DIR = PROJECT_ROOT / "vault"
DRAFTS_DIR = VAULT_DIR / "drafts"
ACTIVE_DIR = DRAFTS_DIR / "active"
SENT_DIR = DRAFTS_DIR / "sent"
EXPIRED_DIR = DRAFTS_DIR / "expired"

EXPIRY_HOURS = 24

DRAFT_TEMPLATE = """---
type: {draft_type}
source_id: {source_id}
recipient: {recipient}
subject: {subject}
context: {context}
created: {created}
status: active
---

## Original Message

{original_message}

## Draft Reply

{draft_reply}
"""


def ensure_dirs():
    """Create draft directories if they don't exist."""
    for d in [ACTIVE_DIR, SENT_DIR, EXPIRED_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def list_drafts(directory: Path) -> list:
    """List all draft files in a directory."""
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"), key=lambda f: f.name, reverse=True)


def get_draft_age_hours(draft_path: Path) -> float:
    """Get the age of a draft in hours based on filename date."""
    try:
        date_str = draft_path.name[:10]
        draft_date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - draft_date).total_seconds() / 3600
    except ValueError:
        # Fallback to file modification time
        mtime = datetime.fromtimestamp(draft_path.stat().st_mtime)
        return (datetime.now() - mtime).total_seconds() / 3600


def cmd_status():
    """Show draft counts across all directories."""
    ensure_dirs()
    active = list_drafts(ACTIVE_DIR)
    sent = list_drafts(SENT_DIR)
    expired = list_drafts(EXPIRED_DIR)

    print("# Draft Status\n")
    print(f"- Active:  {len(active)} drafts pending review")
    print(f"- Sent:    {len(sent)} drafts (used for voice-matching)")
    print(f"- Expired: {len(expired)} drafts (stale, no action taken)")

    if active:
        print("\n## Active Drafts\n")
        for d in active:
            age = get_draft_age_hours(d)
            stale_marker = " ⚠️ STALE" if age > EXPIRY_HOURS else ""
            print(f"- {d.name} ({age:.0f}h old){stale_marker}")


def cmd_expire():
    """Move stale active drafts to expired/."""
    ensure_dirs()
    active = list_drafts(ACTIVE_DIR)
    expired_count = 0

    for draft in active:
        age = get_draft_age_hours(draft)
        if age > EXPIRY_HOURS:
            shutil.move(str(draft), str(EXPIRED_DIR / draft.name))
            print(f"Expired: {draft.name} ({age:.0f}h old)")
            expired_count += 1

    if expired_count == 0:
        print("No stale drafts to expire.")
    else:
        print(f"\nMoved {expired_count} draft(s) to expired/.")


def cmd_list():
    """List all active drafts with details."""
    ensure_dirs()
    active = list_drafts(ACTIVE_DIR)

    if not active:
        print("No active drafts.")
        return

    print("# Active Drafts\n")
    for d in active:
        age = get_draft_age_hours(d)
        # Read frontmatter
        content = d.read_text()
        lines = content.splitlines()
        recipient = ""
        subject = ""
        for line in lines:
            if line.startswith("recipient:"):
                recipient = line.split(":", 1)[1].strip()
            elif line.startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif line == "---" and recipient:
                break

        print(f"## {d.name}")
        print(f"  To: {recipient or 'unknown'}")
        print(f"  Subject: {subject or 'unknown'}")
        print(f"  Age: {age:.0f} hours")
        print()


def cmd_mark_sent(filename: str):
    """Move a specific draft to sent/."""
    ensure_dirs()
    # Find the draft
    draft_path = ACTIVE_DIR / filename
    if not draft_path.exists():
        # Try partial match
        matches = [f for f in ACTIVE_DIR.glob("*.md") if filename in f.name]
        if len(matches) == 1:
            draft_path = matches[0]
        elif len(matches) > 1:
            print(f"Multiple matches for '{filename}':")
            for m in matches:
                print(f"  - {m.name}")
            return
        else:
            print(f"Draft not found: {filename}")
            return

    # Update status in frontmatter
    content = draft_path.read_text()
    content = content.replace("status: active", "status: sent")

    # Write to sent directory
    sent_path = SENT_DIR / draft_path.name
    sent_path.write_text(content)

    # Remove from active
    draft_path.unlink()
    print(f"Moved to sent: {draft_path.name}")


def cmd_create(draft_type: str = "teams_message", recipient: str = "",
               subject: str = "", context: str = "",
               original: str = "", reply: str = ""):
    """Create a new draft file."""
    ensure_dirs()
    now = datetime.now()
    slug = subject.lower().replace(" ", "-")[:30] if subject else "untitled"
    # Clean slug
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    filename = f"{now.strftime('%Y-%m-%d')}_{draft_type}_{slug}.md"

    content = DRAFT_TEMPLATE.format(
        draft_type=draft_type,
        source_id="",
        recipient=recipient,
        subject=subject,
        context=context,
        created=now.strftime("%Y-%m-%dT%H:%M:%S"),
        original_message=original or "_Original message here_",
        draft_reply=reply or "_Draft reply here_",
    )

    filepath = ACTIVE_DIR / filename
    filepath.write_text(content)
    print(f"Created draft: {filepath.relative_to(PROJECT_ROOT)}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Draft management for Second Brain")
    parser.add_argument("command", choices=["status", "expire", "list", "mark-sent", "create"],
                        help="Command to run")
    parser.add_argument("filename", nargs="?", help="Filename for mark-sent command")
    args = parser.parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "expire":
        cmd_expire()
    elif args.command == "list":
        cmd_list()
    elif args.command == "mark-sent":
        if not args.filename:
            print("Usage: draft_manager.py mark-sent <filename>")
            sys.exit(1)
        cmd_mark_sent(args.filename)
    elif args.command == "create":
        cmd_create()


if __name__ == "__main__":
    main()
