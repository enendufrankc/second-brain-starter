---
name: teams-catchup
description: >
  Catches Frank up on what he missed in Teams and his calendar. Runs teams + calendar queries,
  then summarizes: what needs immediate attention, what's FYI, what can wait.
  Triggers: "what did I miss", "teams catchup", "catch me up", "what's happening in teams",
  "morning briefing", "whats up today", "whats up for me", "/teams-catchup"
---

# Teams Catchup — What Did I Miss?

Summarizes recent Teams activity and calendar events into three buckets: act now, FYI, and can wait.

## Usage

Run the catchup script to gather data, then format for Frank:

```bash
# Default: last 24 hours
python3 .claude/skills/teams-catchup/scripts/catchup.py

# Custom window
python3 .claude/skills/teams-catchup/scripts/catchup.py --hours 48

# JSON output
python3 .claude/skills/teams-catchup/scripts/catchup.py --json
```

## What It Gathers

### Teams Messages (via M365 connector or integration scripts)
- AI R&D group chat messages since last check
- Direct messages / DMs to Frank
- @mentions of Frank in any chat

### Calendar (via M365 connector)
- Today's remaining events
- Tomorrow's events (if after 4 PM)
- Any new/changed meetings since last check

### Cross-Reference With
- `vault/MEMORY.md` — active deadlines and context
- `vault/projects/*.md` — project context for mentioned topics
- GitLab issues — if Teams messages mention MRs or issues

## Output Format

Present to Frank in three buckets:

### Needs Your Attention
- Direct questions from Al or Sudhanva
- Meeting invites requiring response
- DMs waiting for reply
- Messages mentioning Frank by name with a question

### FYI — Worth Knowing
- Team updates, shipped features, shared links
- Calendar changes (rescheduled, cancelled meetings)
- General team discussion highlights

### Can Wait
- Social/casual chat
- Automated notifications
- Messages Frank has already seen/replied to

## Presentation Rules

1. Lead with the count: "3 items need attention, 5 FYI, rest is noise"
2. For each item: one-line summary, sender, timestamp, link if available
3. If a message relates to a project, mention the project name
4. If someone is waiting for Frank's reply, say how long they've been waiting
5. Don't reproduce full message text — summarize the ask
6. If Frank is at a conference, bias toward "can wait" — only escalate truly urgent items

## After Catchup

- Append a catchup summary to today's daily log
- If any action items were surfaced, offer to create drafts
- Update `vault/MEMORY.md` if any new critical context was discovered
