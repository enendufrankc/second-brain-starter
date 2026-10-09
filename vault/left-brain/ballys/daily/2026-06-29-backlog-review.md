---
type: backlog-review
date: 2026-06-29
present: false
---

# Weekly Backlog Review — 2026-06-29 (Mon)

> ⚠️ **Automated run. Frank was not present.** No interview answers were collected, so
> **no milestones were checked off and no project frontmatter was changed.** This is a
> read-only status report. Confirm the items below and I'll apply updates on the next
> live sync.

## TL;DR

- **Nothing strictly due this week** (Jun 29–Jul 6) by project `due_date`. Every project
  due_date is now stale (April/May), which is generating large false "overdue" counts on
  the dashboard. **The one-time re-date recommended in the last 4 reviews is still outstanding.**
- **Newly slipped:** GitLab **#32 Prototyping Platform — Stadium Integration** (was due Jun 27)
  is now **2 days overdue** — last live deadline, still blocked on Bhav's Stadium repo access.
- **Still unconfirmed across 5+ reviews:** P0 **#41 IGNITE Showcase (S3+CloudFront)** and
  P0 **#13 Hackathon infra migration** (now ~16d past its Jun 13 GitLab date).
- **Game Experience (P0)** complete bar **Al's review — open since Apr 22 (≈10 weeks).** Chase.
- **error-analysis** pipeline dead since 18 May. Formal archive still recommended.

---

## Open projects — status snapshot

Sorted by priority. "Overdue" is measured against the frontmatter `due_date` (many are stale).

### 🔴 P0

| Project | Status | Due (frontmatter) | Open items needing a decision |
|---|---|---|---|
| **Hackathon Platform** | Production | Apr 17 (73d) | #13 infra migration (GitLab date Jun 13, ~16d late); **#41 IGNITE Showcase S3+CloudFront** (assigned May 7, never confirmed); My App portal; AccessHub listing |
| **Game Experience Profile** | Awaiting Review | Apr 16 (74d) | **Al's review — open since Apr 22.** DNS/cert/SSO suspended (basic admin auth). Then deploy/handoff. |
| **Portfolio Optimisation Agent** | Scoping | Apr 25 (65d) | All 6 milestones open. #16 scope never defined. Is this still live or dormant? |

### 🟠 P1

| Project | Status | Due (frontmatter) | Open items needing a decision |
|---|---|---|---|
| **Bally's Prototyping Platform** | Active | none (GitLab #32 Jun 27, **2d late**) | Blocked on Bhav's Stadium repo access (promised Apr 22, never delivered). Then SDK eval, auth, scaffold, theming, data, pilot. |
| **Capex Machine** | Planning Complete | May 16 (44d) | Implementation **never started.** DNS/cert pending. Jira Cloud integration awaiting Richard Duffy steer. |
| **Ballys Skills Repo** | Active Dev | Apr 17 (73d) | Broadcast email (Al approved, GitLab #33 overdue); Eng Leads showcase; DNS/SSL; AI Code Review RFC #29. |
| **Data Analyst Agent** | Active | Apr 30 (60d) | Tableau pivot (Dez); agentic harness #19 (GitLab date Jun 20, ~9d late); DNS/cert/SSO. Repo dormant since Mar 16. |
| **AI R&D User Access Strategy** | Not Started | none | All 5 milestones open. GitLab #31 overdue. Write-up Al asked for Apr 21. |
| **AI R&D Tracker** | Active | Apr 11 (79d) | CI/CD pipeline; team adoption/training. |
| **Conference Write-Up** | Complete | Apr 17 | Marked Complete but 4 open items linger (RFC #29, 13 write-ups, theme groupings, Graham Whitelaw). Close fully or reopen? |

### ⚪ P2 / P3

| Project | Status | Due (frontmatter) | Note |
|---|---|---|---|
| **Roadmap Intelligence** | Active | May 9 (51d) | Resumed activity May 27–29. DNS/cert/SSO/testing open. |
| **Tableau MCP Agent** | Active | May 23 (37d) | LangGraph + Tableau API still open. Dez collab. |
| **Game Ideation Platform** | Concept | none | GitLab #35 scoping w/ Sudhanva overdue. |
| **Jira Documentation Agent** | Prototype | none | Live Jira API + validation open. |
| **R&D Catalogue** | Early Dev | none | Scaffold only. |
| **Video Analysis** | Validation | May 30 (30d) | Databricks validation + scale testing open. |
| **error-analysis** | Deprioritised | May 9 (51d) | 🔴 Pipeline failed since 18 May, no commits. **Recommend formal archive.** |
| **R&D Prototype SSO/DNS** | Deprioritised | Apr 20 (70d) | MEMORY says close #15. Superseded by User Access Strategy. |

---

## What's overdue or at risk

1. **#32 Prototyping Platform** — newly overdue (Jun 27 + 2d). Gated on Bhav's Stadium repo
   access, which has been "coming" since Apr 22. This dependency needs escalation or the
   project should be paused with that noted.
2. **Two P0s never confirmed** — #41 IGNITE Showcase (S3+CF) and #13 infra migration. These
   have been "status unknown" since early May. Either they shipped (close them) or they're
   stalled (re-plan).
3. **Game Experience (P0)** — done except Al's review, open ~10 weeks. This is a one-message chase.
4. **Capex Machine (P1)** — planning complete since April, zero implementation. Decide: schedule a
   build sprint, or drop priority.

## Coming up this week (Jun 29–Jul 6)

- **No project deadlines** fall in this window (all due_dates are stale).
- **Personal:** Finance review **1 Jul** (Q2 quarterly + June monthly). Apr/May/Jun statements
  must be uploaded first — flagged blocked in MEMORY for two consecutive months.

## Recommended actions (for when you're back)

1. **Re-date stale frontmatter** — single highest-value cleanup; kills the dashboard "overdue" noise.
   Asked for in the last 4–5 reviews and never done.
2. **Close-out sweep** — likely closeable: Conference Write-Up, #15 (SSO/DNS), error-analysis (archive).
3. **Confirm or re-plan the two P0s** (#41, #13).
4. **Chase Al** for the Game Experience review.
5. **Chase Bhav** for Stadium repo access (or pause #32).

*Report generated automatically. Prior runs: 2026-06-22, 2026-06-15, 2026-06-08 — same "no
confirmations collected" caveat applies.*
