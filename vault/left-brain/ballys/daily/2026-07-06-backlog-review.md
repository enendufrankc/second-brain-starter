---
type: backlog-review
date: 2026-07-06
present: false
projects_scanned: 18
projects_updated: 0
---

# Weekly Backlog Review — Mon 6 Jul 2026

**Frank not present. No milestones confirmed, no project files or MEMORY.md changed.** Report only.

## Headline

Fifth consecutive review with no user in the room. Vault has not been touched by human hands since the May 6 hackathon-platform edit. Every dated project is now technically overdue, but "overdue" here is a bookkeeping artefact — 11/11 dated projects hold due_dates from Apr–May 2026 and haven't been re-dated in ~2 months of automated reviews. Same recommendation as the last four Mondays: one manual pass to re-date frontmatter would clear the entire dashboard's red state.

## Nothing due this week (6–13 Jul)

Zero projects have a due_date in the coming 7 days. Zero in the coming 30. All dated work is in the overdue bucket.

## Overdue register (all 11 dated projects)

| Project | Pri | Was due | Days over | Notes |
|---|---|---|---|---|
| hackathon-platform | P0 | 2026-04-17 | 80d | #13 infra migration still open; #41 IGNITE showcase (S3+CF) open |
| game-experience-prototype | P0 | 2026-04-16 | 81d | Awaiting Al review since Apr 22 (~11 wks) |
| portfolio-optimisation-agent | P0 | 2026-04-25 | 72d | 0/6 milestones done — scoping never started |
| ai-rd-tracker | P1 | 2026-04-11 | 86d | CI/CD + adoption open |
| conference-writeup | P1 | 2026-04-17 | 80d | Status = Complete in frontmatter but 4 unchecked bullets |
| ballys-skills-repo | P1 | 2026-04-17 | 80d | Broadcast email still not sent; Al approved strategy in Apr |
| data-analyst-agent | P1 | 2026-04-30 | 67d | Tableau pivot open; Dez collab dormant |
| capex-machine | P1 | 2026-05-16 | 51d | Implementation sprint not started; awaiting Richard Duffy steer since Apr 22 |
| rd-prototype-sso-dns | P2 | 2026-04-20 | 77d | Marked Deprioritised — safe to archive |
| roadmap-mcp | P2 | 2026-05-09 | 58d | DNS/SSL/SSO + user testing open |
| tableau-mcp-agent | P2 | 2026-05-23 | 44d | LangGraph + Tableau API not connected |
| error-analysis | P2 | 2026-05-09 | 58d | Marked Deprioritised — safe to archive |
| video-analysis | P3 | 2026-05-30 | 37d | Databricks validation open |

## Undated projects (no due_date in frontmatter)

- ai-rd-user-access (P1) — Not Started, 0/5 milestones
- ballys-prototyping-platform (P1) — Active, 6/14 done, still blocked on Bhav's Stadium repo access (promised Apr 22, never delivered — now 75 days silent)
- jira-documentation-agent (P2) — Prototype, 4/7
- game-ideation-agent (P2) — Concept, 3/9
- rd-catalogue (P3) — Early dev, 1/5

## Cross-cutting blocker

PIT infrastructure (DNS / SSL / SSO) is an unchecked milestone in 8 different projects: game-experience-prototype, ballys-skills-repo, data-analyst-agent, capex-machine, roadmap-mcp, error-analysis, rd-prototype-sso-dns, ballys-prototyping-platform. Al's Apr 21 decision (no SSO for demos, self sign-up for PII apps) means most of these DNS/SSL/SSO bullets can probably be crossed off or restructured — but the change hasn't been propagated into the project files.

## Recommended actions (for Frank, when next in session)

1. **One-time re-date pass.** For every project still live, bump due_date to a realistic July/August target. This clears the "13 overdue" alert on DASHBOARD.
2. **Archive the two Deprioritised P2s** (rd-prototype-sso-dns, error-analysis) — remove from active list, keep the files.
3. **Close conference-writeup** if it's genuinely Complete, or uncheck the frontmatter status.
4. **Chase Al on game-experience-prototype review** — 11 weeks is long enough that it may need re-scoping rather than re-reviewing.
5. **Chase Bhav on Stadium repo access** — 75-day silence blocks prototyping platform entirely.
6. **Propagate Al's Apr 21 user-access decision** into the 8 project files still listing SSO/DNS as open milestones.
7. **Personal:** Life insurance (~75+ days overdue) and finance statement uploads (Apr/May/Jun/Jul all missing) — still the two highest-priority personal items carried from MEMORY.md.

## What changed vs 29 Jun review

- +7 days on every "overdue" counter.
- Ballys Prototyping Platform's stale due_date (Jun 27) was already flagged last week — no new slippage this week because everything else is already deep in the red.
- Nothing closed, nothing new added. No signal of activity in any project file.
