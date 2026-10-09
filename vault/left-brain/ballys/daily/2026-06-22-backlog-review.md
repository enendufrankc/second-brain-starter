---
type: backlog-review
date: 2026-06-22
run: automated (Frank not present)
---

# Weekly Backlog Review — Monday 22 June 2026

> **Automated run.** Frank was not present to confirm milestone status, so **no project files or frontmatter were changed** and no milestones were checked off. This is a read-only snapshot of where the backlog stands today, plus the questions to resolve when Frank is next available. Mirrors the prior absent-run pattern (2026-06-08, 2026-06-15).

## TL;DR

- **Nothing is due in the vault frontmatter for this week** — every dated project file is already overdue.
- **BUT one GitLab-tracked item is genuinely due this week:** **#32 Prototyping Platform — Stadium Integration, due Fri 27 Jun (5 days).** This is the one live deadline to protect.
- Two GitLab items quietly slipped overdue since the last review: **#13 Hackathon infra migration (was Jun 13, now 9d late)** and **#19 Data Agent harness (was Jun 20, now 2d late)**.
- The two P0s remain the same as last week and are still unconfirmed: **#41 IGNITE Showcase (S3+CF)** and **#13 infra migration**.
- A large amount of the "overdue" list is stale frontmatter dates from April/May that have never been reconciled. The vault dates and the GitLab dates have drifted apart and need a one-time clean-up.

## Due this week (the thing that matters)

| Item | Project | Due | Countdown | Notes |
|---|---|---|---|---|
| #32 | Bally's Prototyping Platform — Stadium Integration | **27 Jun** | **5 days** | On track per last health check. Depends on Stadium repo access from Bhav (still "promised", not delivered). Confirm access is in hand and integration is actually progressing. |

## Slipped overdue since last review (GitLab dates)

| Item | Project | Pri | Was due | Late |
|---|---|---|---|---|
| #13 | Hackathon infra migration | P0 | 13 Jun | **9 days** |
| #19 | Data Agent — agentic harness | P1 | 20 Jun | **2 days** |

## P0 — Critical path (unchanged, still unconfirmed)

- **#41 IGNITE Showcase on S3 + CloudFront** — assigned by Al 7 May, IGNITE-blocking. Status still unknown across three consecutive reviews. **Needs Frank's update.**
- **#13 Hackathon infra migration** — now 9 days overdue (GitLab Jun 13). Last pipeline activity on `hackathon-v2` branch failed 18 May; no commits since. **Needs Frank's update.**
- **Game Experience Profile** — all build milestones complete; only blocker is **Al's review**, outstanding since 22 Apr. This is a P0 sitting idle purely waiting on a review — chase Al to close it.
- **Portfolio Optimisation Agent (#16)** — P0, still "Scoping", no milestones started, frontmatter due 25 Apr. MEMORY notes a possible reassignment to Sudhanva — confirm whether this is still Frank's and still P0, or should be closed/reassigned.

## Overdue (frontmatter dates — mostly stale, need reconciliation)

| Project | Pri | Frontmatter due | Days late | Real status to confirm |
|---|---|---|---|---|
| Game Experience Profile | P0 | 16 Apr | 67 | Done bar Al's review |
| Portfolio Optimisation Agent | P0 | 25 Apr | 58 | Scoping not started — still live? |
| AI R&D Tracker | P1 | 11 Apr | 72 | Shipped; only CI/CD + adoption left — likely closeable |
| Ballys Skills Repo | P1 | 17 Apr | 66 | Broadcast email (#33) + showcase still open |
| Conference Write-Up | P1 | 17 Apr | — | Marked **Complete**; stray open milestones (RFC #29) can be split out |
| Data Analyst Agent | P1 | 30 Apr | 53 | Pivoted to Tableau summariser w/ Dez; #19 now the live tracker |
| Capex Machine | P1 | 16 May | 37 | Planning complete, implementation **not started** — still live or parked? |
| Error Analysis | P2 | 9 May | 44 | Deprioritised; pipeline broken since 18 May — formal archive? |
| Roadmap Intelligence | P2 | 9 May | 44 | Resumed activity 27–29 May — re-date and continue |
| Tableau MCP Agent | P2 | 23 May | 30 | LangGraph + Tableau API still open |
| Video Analysis | P3 | 30 May | 23 | Databricks validation outstanding |
| R&D Prototype SSO/DNS | P2 | 20 Apr | 63 | #15 reported closed — confirm and close project |

## No due date set (consider dating or parking)

- AI R&D User Access Strategy (P1, Not Started) — this is GitLab **#31**, reported **9 days overdue** on the 1 Jun health check. Has a real deadline in GitLab but none in the vault — reconcile.
- Bally's Prototyping Platform (P1, Active) — owns the live #32 deadline above.
- Game Ideation Intelligence Platform (P2, Concept) — scoping session #35 was overdue 30 May.
- Jira Documentation Agent (P2, Prototype).
- R&D Catalogue (P3, Early Dev).

## Pipeline / health flags (from 1 Jun health check)

- 🔴 **evaluations-error-analysis** — failed on main + branches since 18 May, no commits since. Recommended for **formal archive**.
- 🟡 **hackathon-management-platform** — main green (16 May) but `hackathon-v2` failed 18 May, no activity since.
- 🟡 **ballys-skills-repo** — dormant since 19 Mar; broadcast email (#33) overdue.
- 🟡 **data-analyst-agent / data-agent** — long dormant; #19 now the active thread.

## New projects / initiatives to check (carried from prior reviews)

These were flagged in earlier runs and still need Frank to confirm whether they should be tracked as projects:

- **GitLab × Claude** workstream — untracked.
- **HARMAN / WIPRO POC** — untracked.
- **Hive Metastore shutdown** (was 31 May) — confirm no R&D pipeline depended on it; if it did and broke, that's now ~3 weeks silent.

## Questions for Frank (resolve at next live sync)

1. **#41 IGNITE Showcase (S3+CF)** — done, in progress, or blocked? (3rd review unanswered.)
2. **#13 infra migration** — 9 days overdue; what's the real state and is the `hackathon-v2` pipeline failure relevant?
3. **#32 Prototyping Platform** — due Fri; do you have Stadium repo access from Bhav yet?
4. **Portfolio Optimisation Agent (#16)** — still yours and still P0, or reassigned to Sudhanva / close?
5. **Capex Machine** — implementation still planned, or parked pending Richard Duffy's Jira Cloud steer?
6. **Error Analysis** — OK to formally archive (pipeline dead since 18 May)?
7. **Stale April/May frontmatter dates** — approve a one-time re-date so the dashboard stops showing 70-day "overdue" noise.
8. **Untracked workstreams** — should GitLab×Claude and HARMAN/WIPRO POC become tracked projects?

---

*Generated 2026-06-22 by the weekly backlog-review scheduled task. No write actions taken against project files because Frank was not present to confirm changes.*
