#!/usr/bin/env python3
"""
Outlook Integration — Monitor inbox, draft replies.

Usage:
    python3 outlook.py inbox          # Recent important emails
    python3 outlook.py unread         # Unread count + priority senders
    python3 outlook.py summary        # Full email summary
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta

try:
    from microsoft_graph import api_get
except ImportError:
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
    from microsoft_graph import api_get


# Senders to always surface (case-insensitive partial match)
PRIORITY_SENDERS = [
    "alastair.jepps",
    "al.jepps",
    "s.mysoreganesh",
    "sudhanva",
    "juan.impey",
    "lynn.murphy",
]

# Senders to filter out (noise)
NOISE_SENDERS = [
    "splunk",
    "noreply",
    "no-reply",
    "notifications@",
    "mailer-daemon",
    "postmaster",
]


def is_priority_sender(email: str) -> bool:
    """Check if sender is a priority contact."""
    email_lower = email.lower()
    return any(p in email_lower for p in PRIORITY_SENDERS)


def is_noise_sender(email: str) -> bool:
    """Check if sender is noise."""
    email_lower = email.lower()
    return any(n in email_lower for n in NOISE_SENDERS)


def get_inbox(count: int = 20) -> str:
    """Get recent inbox emails, filtered for relevance."""
    messages = api_get("/me/mailFolders/inbox/messages", {
        "$select": "from,subject,receivedDateTime,bodyPreview,isRead,importance",
        "$orderby": "receivedDateTime desc",
        "$top": count,
    })

    lines = ["## Inbox — Recent Emails\n"]
    if not messages:
        lines.append("No recent emails.")
        return "\n".join(lines)

    priority_emails = []
    normal_emails = []
    noise_count = 0

    for msg in messages:
        sender = msg.get("from", {}).get("emailAddress", {})
        sender_email = sender.get("address", "")
        sender_name = sender.get("name", sender_email)

        if is_noise_sender(sender_email):
            noise_count += 1
            continue

        subject = msg.get("subject", "No subject")
        preview = msg.get("bodyPreview", "")[:150]
        is_read = msg.get("isRead", True)
        importance = msg.get("importance", "normal")
        timestamp = msg.get("receivedDateTime", "?")[:16]

        read_marker = "" if is_read else "🔵 "
        importance_marker = "❗ " if importance == "high" else ""

        entry = f"- {read_marker}{importance_marker}**{sender_name}**: {subject}\n  {timestamp} | {preview}"

        if is_priority_sender(sender_email) or importance == "high" or not is_read:
            priority_emails.append(entry)
        else:
            normal_emails.append(entry)

    if priority_emails:
        lines.append("### Priority")
        lines.extend(priority_emails)
        lines.append("")

    if normal_emails:
        lines.append("### Other")
        lines.extend(normal_emails[:10])

    if noise_count > 0:
        lines.append(f"\n({noise_count} automated/noise emails filtered)")

    return "\n".join(lines)


def get_unread_summary() -> str:
    """Get unread email count and priority senders."""
    messages = api_get("/me/mailFolders/inbox/messages", {
        "$filter": "isRead eq false",
        "$select": "from,subject,importance",
        "$top": 50,
    })

    lines = ["## Unread Emails\n"]
    if not messages:
        lines.append("Inbox zero! No unread emails.")
        return "\n".join(lines)

    total = len(messages)
    priority = [m for m in messages if is_priority_sender(
        m.get("from", {}).get("emailAddress", {}).get("address", "")
    )]
    high_importance = [m for m in messages if m.get("importance") == "high"]
    noise = [m for m in messages if is_noise_sender(
        m.get("from", {}).get("emailAddress", {}).get("address", "")
    )]

    lines.append(f"**Total unread:** {total}")
    lines.append(f"**Priority senders:** {len(priority)}")
    lines.append(f"**High importance:** {len(high_importance)}")
    lines.append(f"**Noise (filtered):** {len(noise)}")

    actionable = [m for m in messages if m not in noise]
    if actionable:
        lines.append("\n### Needs attention:")
        for msg in actionable[:10]:
            sender = msg.get("from", {}).get("emailAddress", {}).get("name", "?")
            subject = msg.get("subject", "No subject")
            lines.append(f"- **{sender}**: {subject}")

    return "\n".join(lines)


def get_full_summary() -> str:
    """Full Outlook summary."""
    sections = [
        "# Outlook Summary — " + datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
        get_unread_summary(),
        "",
        get_inbox(count=15),
    ]
    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Outlook integration for Second Brain")
    parser.add_argument("command", choices=["inbox", "unread", "summary"],
                        help="What to query")
    parser.add_argument("--count", type=int, default=20, help="Number of emails")
    args = parser.parse_args()

    commands = {
        "inbox": lambda: get_inbox(args.count),
        "unread": get_unread_summary,
        "summary": get_full_summary,
    }

    result = commands[args.command]()
    print(result)


if __name__ == "__main__":
    main()
