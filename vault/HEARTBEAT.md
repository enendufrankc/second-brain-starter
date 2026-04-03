# HEARTBEAT — Monitoring Checklist

> The heartbeat script reads this file to know what to check each cycle.
> Runs every 30 minutes during active hours (9 AM - 7 PM ET).

## Teams Calendar (Priority: Critical)

- [ ] Check for meetings in the next 2 hours
- [ ] Flag any schedule conflicts today
- [ ] Surface approaching deadlines this week

## Teams Chat (Priority: Critical)

- [ ] New messages in AI R&D group chat (19:02a862626ca54619b6babc5593aa33a3@thread.v2)
- [ ] Unread DMs from any individual
- [ ] Messages mentioning Frank by name in group chats

## GitLab (Priority: High)

- [ ] Open MRs assigned to Frank
- [ ] MRs where Frank's review is requested
- [ ] Failed pipelines in tracked projects
- [ ] New issues assigned to Frank

## Outlook (Priority: Medium)

- [ ] Unread emails from teammates or manager
- [ ] Emails requiring a response (direct questions)
- [ ] Calendar invites pending response

## Notification Rules

- **Urgent (notify immediately):** Meeting in <30 min, direct DM from manager, pipeline failure on Frank's MR
- **Important (batch every 30 min):** New MRs needing review, unread DMs, emails needing response
- **FYI (daily summary):** Group chat activity, resolved pipelines, FYI emails
