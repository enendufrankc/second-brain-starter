---
date: 2026-05-18
type: weekly-review
auto_generated: true
---

# Weekly Backlog Review — Monday, May 18, 2026

> Automated review. Frank was not present for the interactive interview — this report summarises the current state and flags items needing decisions.

---

## Executive Summary

This is the **fifth consecutive week with zero milestone progress** across all 18 projects. Every project file still shows `last_updated: 2026-04-22` (26 days ago). Either significant work is happening and not being captured, or the backlog is genuinely stalled. Both scenarios need addressing.

Additionally, two infrastructure problems are degrading the automated system:
- **GitLab API unreachable** from the sandbox — PAT may have expired or VPN/network issue. Multiple weeks affected.
- **Outlook connector disconnected** — no calendar or email data available for briefs.

---

## Overdue Projects (11 of 18)

### P0 — Critical

| Project | Due | Overdue | Open Milestones | Decision Needed |
|---------|-----|---------|-----------------|-----------------|
| **Portfolio Optimisation Agent** | Apr 25 | **23 days** | 6/6 open (0%) | **Cancel, deprioritise, or timebox spike.** Six weeks at 0% on a P0 is unsustainable. |
| **Hackathon Platform** (#13 infra) | Apr 17 | **31 days** | 4/14 open | Ignite is done. Is #13 migration still relevant? Close or re-date. |
| **Game Experience Prototype** | Apr 16 | **32 days** | 5/11 open | Awaiting Al's review since Apr 22. Chase or deprioritise. |

### P1 — Important

| Project | Due | Overdue | Open Milestones | Decision Needed |
|---------|-----|---------|-----------------|-----------------|
| **Capex Machine** | May 16 | **2 days** | 6/11 open | Missed deadline. Awaiting Richard Duffy on Jira Cloud integration. Re-date or escalate. |
| **AI R&D Tracker** | Apr 11 | **37 days** | 2/6 open | CI/CD and team adoption still open. Close as "good enough" or set new date? |
| **Conference Write-Up** | Apr 17 | **31 days** | 4/11 open | Status says "Complete" but 4 milestones open. Formally close or finish remaining write-ups? |
| **Ballys Skills Repo** | Apr 17 | **31 days** | 5/11 open | Broadcast email flagged for 5 weeks. DNS ticket raised. Send email or drop it? |
| **Data Analyst Agent** | Apr 30 | **18 days** | 6/9 open | Tableau pivot with Dez agreed but no progress logged. Still active? |
| **AI R&D User Access** | No date | N/A | 5/5 open (0%) | 4 weeks at 0%. Blocks Prototyping Platform auth tier. 90-min timebox suggested repeatedly. |

### P2 — Lower Priority

| Project | Due | Overdue | Notes |
|---------|-----|---------|-------|
| **Error Analysis** | May 9 | 9 days | Deprioritised. Pipeline broken since Apr 2. Leave as-is? |
| **Roadmap MCP** | May 9 | 9 days | Waiting on Mark Webster testing. No movement. |
| **R&D Prototype SSO/DNS** | Apr 20 | 28 days | Deprioritised. Superseded by User Access Strategy. Close? |

---

## Due This Week

| Project | Due | Priority | Status |
|---------|-----|----------|--------|
| **Tableau MCP Agent** | May 23 | P2 | 3/7 milestones done. LangGraph integration, Tableau API connection still open. |

---

## Upcoming

| Project | Due | Priority | Status |
|---------|-----|----------|--------|
| **Video Analysis** | May 30 | P3 | Databricks validation pending |
| **Hive Metastore shutdown** | May 31 | — | Check if R&D pipelines depend on it (flagged in MEMORY.md) |

---

## Non-Project Items Needing Attention

| Item | Source | Status |
|------|--------|--------|
| **Life insurance** | MEMORY.md | OVERDUE since April. Must action immediately. |
| **2026 Goals in UKG** | People Team email May 5 | Unclear if submitted. Check deadline. |
| **John Streets skills distribution feedback** | MEMORY.md May 7 | Was 2 days overdue as of May 7 — now 11 days. Follow up? |
| **Qodo pilot** | Email thread Apr 30 | NDA signed. Scoping meeting status unclear. Follow up with Goffredo. |
| **Bhav / Stadium repo access** | Prototyping Platform | Promised Apr 22, revisit was w/c May 4 — now 14 days past. No update logged. |
| **Hive Metastore shutdown** | MEMORY.md | May 31. Verify R&D pipeline dependencies. |
| **Monthly finance review** | MEMORY.md | 1 Jun deadline — upload all May bank statements by then. |

---

## Infrastructure Issues

1. **GitLab PAT / API access** — Has been failing intermittently since ~May 8. Two full weeks of degraded automated briefs. Regenerate PAT and verify from sandbox.
2. **Outlook connector** — Disconnected. Calendar and email data unavailable for daily briefs. Reconnect in Cowork settings.
3. **Project file staleness** — All 18 project files last updated Apr 22. Even if work has happened, it's invisible to the tracking system.

---

## Recurring Patterns (Flagged for 3+ Weeks)

These items have appeared in weekly reviews repeatedly without resolution:

1. **"Push without closing"** — Noted as a pattern since late April. Zero GitLab issues closed since w/c May 4.
2. **Skills Repo broadcast email** — Flagged every week since Apr 22. Still not sent.
3. **AI R&D User Access draft** — Flagged every week since Apr 22. Still at 0%.
4. **Portfolio Optimisation Agent** — P0 at 0% for six consecutive weeks.
5. **Bhav/Stadium check-in** — Was due w/c May 4, now 14 days past.

---

## Decisions Needed From Frank

When you're back, please review these — each needs a quick call:

1. **Portfolio Optimisation Agent** — Keep at P0, deprioritise to P2, or close? It's been at 0% for 6 weeks.
2. **Hackathon Platform #13** — Post-Ignite, is the infra migration still needed? Close or re-date?
3. **#34 Ignite Hackathon Admin** — Ignite is done (May 5 post-mortem). Can this be closed?
4. **Conference Write-Up** — Status says "Complete" but has 4 open milestones. Close as-is or finish?
5. **R&D Prototype SSO/DNS** — Superseded by User Access Strategy. Formally close?
6. **Capex Machine** — Missed May 16 deadline. New target date?
7. **Skills Repo broadcast** — Are we sending this or not? It's been 5 weeks.
8. **AI R&D User Access** — Can you timebox 90 minutes this week to get a v1 draft?
9. **GitLab PAT** — Please verify/regenerate so automated tracking resumes.
10. **Outlook connector** — Please reconnect so daily briefs can pull calendar/email.

---

## DASHBOARD and DEADLINES Staleness Note

The DASHBOARD.md "This Week's Focus" section still shows content from w/c Apr 22 (almost a month ago). The DEADLINES.md "Hard Deadlines & Events" table references April dates that have all passed. Both need updating once Frank provides direction on the decisions above.

---

*Next scheduled review: Monday, May 25, 2026*
