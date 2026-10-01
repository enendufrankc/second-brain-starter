#!/usr/bin/env python3
"""
Teams Integration — Monitor chat messages and calendar events.

Usage:
    python3 teams.py messages        # Recent messages from AI R&D group + unread DMs
    python3 teams.py calendar        # Today's meetings + upcoming 24h
    python3 teams.py summary         # Full Teams summary
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    from microsoft_graph import api_get
except ImportError:
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
    from microsoft_graph import api_get

# AI R&D group chat thread ID
AI_RD_CHAT_ID = "19:02a862626ca54619b6babc5593aa33a3@thread.v2"


def get_calendar_events(hours_ahead: int = 24) -> str:
    """Get upcoming calendar events."""
    now = datetime.utcnow()
    end = now + timedelta(hours=hours_ahead)

    events = api_get("/me/calendar/events", {
        "$orderby": "start/dateTime",
        "$filter": f"start/dateTime ge '{now.isoformat()}Z' and start/dateTime le '{end.isoformat()}Z'",
        "$select": "subject,start,end,location,organizer,isAllDay,showAs",
        "$top": 20,
    })

    lines = ["## Calendar — Next 24 Hours\n"]
    if not events:
        lines.append("No upcoming events.")
        return "\n".join(lines)

    for event in events:
        subject = event.get("subject", "Untitled")
        start = event.get("start", {}).get("dateTime", "?")[:16]
        end_time = event.get("end", {}).get("dateTime", "?")[:16]
        organizer = event.get("organizer", {}).get("emailAddress", {}).get("name", "?")
        location = event.get("location", {}).get("displayName", "")
        show_as = event.get("showAs", "")

        if event.get("isAllDay"):
            lines.append(f"- 📅 **{subject}** (All day)")
        else:
            lines.append(f"- 📅 **{subject}** ({start} → {end_time})")

        details = []
        if organizer:
            details.append(f"Organizer: {organizer}")
        if location:
            details.append(f"Location: {location}")
        if show_as:
            details.append(f"Show as: {show_as}")
        if details:
            lines.append(f"  {' | '.join(details)}")

    return "\n".join(lines)


def get_group_messages(count: int = 15) -> str:
    """Get recent messages from the AI R&D group chat."""
    messages = api_get(f"/chats/{AI_RD_CHAT_ID}/messages", {
        "$top": count,
        "$orderby": "createdDateTime desc",
    })

    lines = ["## AI R&D Group Chat — Recent Messages\n"]
    if not messages:
        lines.append("No recent messages.")
        return "\n".join(lines)

    for msg in messages:
        sender = msg.get("from", {})
        if sender:
            sender_name = sender.get("user", {}).get("displayName", "Unknown")
        else:
            sender_name = "System"

        body = msg.get("body", {}).get("content", "")
        # Strip HTML tags for plain text
        import re
        body = re.sub(r"<[^>]+>", "", body).strip()
        if len(body) > 200:
            body = body[:200] + "..."

        timestamp = msg.get("createdDateTime", "?")[:16]
        lines.append(f"- **{sender_name}** ({timestamp}): {body}")

    return "\n".join(lines)


def get_unread_dms() -> str:
    """Get chats with unread messages."""
    chats = api_get("/me/chats", {
        "$filter": "chatType eq 'oneOnOne'",
        "$expand": "lastMessagePreview",
        "$top": 20,
    })

    lines = ["## Unread DMs\n"]
    unread_count = 0

    for chat in chats:
        unread = chat.get("unreadCount", 0) if isinstance(chat.get("unreadCount"), int) else 0
        if unread > 0:
            unread_count += 1
            preview = chat.get("lastMessagePreview", {})
            sender = preview.get("from", {}).get("user", {}).get("displayName", "?")
            body = preview.get("body", {}).get("content", "")[:100]
            lines.append(f"- **{sender}** ({unread} unread): {body}")

    if unread_count == 0:
        lines.append("No unread DMs.")

    return "\n".join(lines)


def get_full_summary() -> str:
    """Full Teams summary."""
    sections = [
        "# Teams Summary — " + datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
        get_calendar_events(),
        "",
        get_group_messages(count=10),
        "",
        get_unread_dms(),
    ]
    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Teams integration for Second Brain")
    parser.add_argument("command", choices=["messages", "calendar", "dms", "summary"],
                        help="What to query")
    parser.add_argument("--count", type=int, default=15, help="Number of messages")
    args = parser.parse_args()

    commands = {
        "messages": lambda: get_group_messages(args.count),
        "calendar": get_calendar_events,
        "dms": get_unread_dms,
        "summary": get_full_summary,
    }

    result = commands[args.command]()
    print(result)


if __name__ == "__main__":
    main()
