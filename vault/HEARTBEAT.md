# HEARTBEAT — Monitoring & Automation

> This file documents what the second brain monitors and how.
> The system uses 11 scheduled Cowork tasks + Claude in Chrome for browser actions.
> Last reviewed: 2026-04-16

## Automated Scheduled Tasks

| Task | Schedule | What It Does | Output | Last Ran | Status |
|------|----------|-------------|--------|----------|--------|
| AI News Briefing | 8:00am weekdays | Web searches for AI news from Anthropic, OpenAI, Google, Microsoft, top voices | `vault/daily/ai-news-YYYY-MM-DD.md` | Apr 16 | OK |
| Ballys 360 Morning Brief | 8:00am weekdays | Scan GitLab issues, Outlook calendar, project deadlines | Daily brief | Apr 15 | Missed Thu-Fri |
| Daily Briefing | 8:45am weekdays | Pulls calendar + GitLab tasks + Teams mentions + actionable emails | `vault/daily/YYYY-MM-DD.md` | Apr 17 | OK (but Outlook connectors intermittent) |
| Deadline Warnings | 9:30am weekdays | Flags overdue, due-tomorrow, due-in-3-days items from GitLab tracker | Appends to daily log | Apr 15 | Missed Thu-Fri |
| Project Health Check | Mon & Thu 9:15am | Scans all AI R&D GitLab projects (pipelines, MRs, issues, commits) | `vault/projects/STATUS-DASHBOARD.md` | Apr 14 | Missed Thu |
| Pipeline/MR Monitor | 10am, 12pm, 2pm, 4pm weekdays | Checks active project pipelines and open MRs needing review | Appends to daily log | Apr 15 | Missed Thu-Fri |
| Ballys Deadline Watchdog | 1:00pm weekdays | Flag GitLab issues due within 48 hours or overdue | Urgent alerts | Apr 15 | Missed Thu-Fri |
| Ballys Meeting Sync | 6:00pm weekdays | Pull Teams meeting transcripts, summarize into structured notes | `vault/meetings/` | Apr 15 | Ran but produced 0 notes |
| End-of-Day Wrapup | 6:30pm weekdays | Compares morning plan vs actual, captures completed/carried-over | Appends to daily log | Apr 15 | Missed Thu-Fri |
| Weekly Retro | Friday 5pm | Summarizes week, tracks velocity, creates GitLab weekly-summary issue | `vault/daily/YYYY-MM-DD.md` + GitLab issue | Apr 14 | Never ran on a Friday |
| Ballys Weekly Review | Friday 5pm | Compare progress, flag stalled work, celebrate wins, plan next week | Weekly summary | Never | Never ran |

## Known Issues (as of Apr 16)

1. **Tasks depend on Cowork app being open** — if Frank closes the app, scheduled tasks silently miss their window. Multiple tasks missed Thu Apr 16 and Fri Apr 17 runs.
2. **Outlook connectors intermittent** — daily brief for Apr 16 shows "Outlook Calendar unavailable" and "Outlook Email unavailable". Calendar and email data is unreliable.
3. **Meeting sync produces no output** — the ballys-meeting-sync task runs but generates zero meeting notes. Likely failing to access OneDrive Recordings or transcript parsing is broken.
4. **Duplicate morning briefs** — `daily-briefing` and `ballys-360-morning-brief` overlap in scope. Consider merging.
5. **Duplicate weekly reviews** — `weekly-retro` and `ballys-weekly-review` overlap. Neither has successfully run on a Friday.
6. **GitLab PAT expiring ~Apr 18** — all GitLab-dependent tasks will break if not renewed.

## What Gets Monitored

### Teams Calendar (Priority: Critical)
- Meetings in the next 2 hours
- Schedule conflicts today
- Approaching deadlines this week
- Conference and travel blocks

### Teams Chat (Priority: Critical)
- New messages in AI R&D group chat (`19:02a862626ca54619b6babc5593aa33a3@thread.v2`)
- AI R&D Crew small group chat
- Gaming Product Fr-AI-day group chat (added Apr 16)
- Unread DMs from any individual
- Messages mentioning Frank by name
- Key contacts: Al Jepps, Sudhanva, Lynn Murphy, Sherrine, Kyriacos Kyriacou

### GitLab (Priority: Critical)
- Open issues assigned to Frank (task tracker project ID: 8489)
- Failed pipelines across all AI R&D projects
- Open MRs assigned to Frank or needing his review
- Milestone and due date tracking
- Board status changes on "Development" board (ID: 223)

### Outlook (Priority: Medium)
- Unread emails from teammates or manager
- Emails requiring a response (direct questions, not Splunk/automated alerts)
- Calendar invites pending response
- GitLab folder (70 emails) — issue notifications

### AI/Tech News (Priority: Low — daily FYI)
- Anthropic (Claude releases, API changes, research papers)
- OpenAI (GPT updates, product launches)
- Google (Gemini, DeepMind research)
- Microsoft (Copilot, Azure AI)
- Top voices: Andrej Karpathy, Sam Altman, Dario Amodei, Yann LeCun, Jim Fan, Simon Willison
- AI engineering: coding agents, MCP protocol, agent frameworks

## Notification Rules

- **Urgent (surface immediately):** Meeting in <30 min, direct DM from manager, pipeline failure on Frank's MR, deadline tomorrow
- **Important (batch in scheduled runs):** New MRs needing review, unread DMs, emails needing response, issues assigned
- **FYI (daily summary):** Group chat activity, resolved pipelines, FYI emails, AI news

## Browser Actions (via Claude in Chrome)

When Chrome extension is connected, the agent can:
- Block/create calendar events in Outlook
- Navigate Support Hub for ticket requests
- Interact with GitLab UI when API isn't sufficient
- Fill forms and submit requests on Frank's behalf (with permission)
