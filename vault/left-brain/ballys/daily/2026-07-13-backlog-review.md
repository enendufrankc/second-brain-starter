---
type: backlog-review
date: 2026-07-13
present: false
projects_scanned: 18
projects_updated: 0
---

# Weekly Backlog Review — Mon 13 Jul 2026

**Frank not present. No milestones confirmed, no project files or MEMORY.md changed.** Report only. (MEMORY.md run-note line refreshed to record this run.)

## Headline

Sixth consecutive review with no user in the room. The vault still hasn't been touched by human hands since the May 6 hackathon-platform edit — now ~10 weeks of purely automated reviews. Every dated project is technically overdue, but this remains a bookkeeping artefact: 13/13 dated projects carry due_dates from Apr–May 2026 that have never been re-dated. The single highest-leverage action is unchanged from the last five Mondays — one manual pass to re-date frontmatter would clear the entire dashboard's red state.

## Nothing due this week (13–20 Jul) or this month

Zero projects have a due_date in the coming 7 days. Zero in the coming 30. All dated work sits in the overdue bucket.

## Overdue register (all 13 dated projects)

| Project | Pri | Was due | Days over | Notes |
|---|---|---|---|---|
| game-experience-prototype | P0 | 2026-04-16 | 88d | Awaiting Al review since Apr 22 (~12 wks) |
| hackathon-platform | P0 | 2026-04-17 | 87d | #13 infra migration still open; #41 IGNITE showcase (S3+CF) open |
| portfolio-optimisation-agent | P0 | 2026-04-25 | 79d | 0/6 milestones — scoping never started |
| ai-rd-tracker | P1 | 2026-04-11 | 93d | CI/CD + adoption open |
| conference-writeup | P1 | 2026-04-17 | 87d | Status = Complete in frontmatter but 4 unchecked bullets |
| ballys-skills-repo | P1 | 2026-04-17 | 87d | Broadcast email still not sent; Al approved strategy in Apr |
| data-analyst-agent | P1 | 2026-04-30 | 74d | Tableau pivot open; Dez collab dormant |
| capex-machine | P1 | 2026-05-16 | 58d | Implementation sprint not started; awaiting Richard Duffy steer since Apr 22 |
| rd-prototype-sso-dns | P2 | 2026-04-20 | 84d | Marked Deprioritised — safe to archive |
| roadmap-mcp | P2 | 2026-05-09 | 65d | DNS/SSL/SSO + user testing open |
| error-analysis | P2 | 2026-05-09 | 65d | Marked Deprioritised; pipeline red since Apr 2 — safe to archive |
| tableau-mcp-agent | P2 | 2026-05-23 | 51d | LangGraph + Tableau API not connected |
| video-analysis | P3 | 2026-05-30 | 44d | Databricks validation open |

## Undated projects (no due_date in frontmatter)

- ai-rd-user-access (P1) — Not Started, 0/5 milestones
- ballys-prototyping-platform (P1) — Active, 6/14 done, still blocked on Bhav's Stadium repo access (promised Apr 22, never delivered — now 82 days silent)
- jira-documentation-agent (P2) — Prototype, 4/7
- game-ideation-agent (P2) — Concept, 3/9
- rd-catalogue (P3) — Early dev, 1/5

## Cross-cutting blocker

PIT infrastructure (DNS / SSL / SSO) is still an unchecked milestone in 8 projects: game-experience-prototype, ballys-skills-repo, data-analyst-agent, capex-machine, roadmap-mcp, error-analysis, rd-prototype-sso-dns, ballys-prototyping-platform. Al's Apr 21 decision (no SSO for demos, self sign-up for PII apps) means most of these DNS/SSL/SSO bullets can be crossed off or restructured — the change has still not been propagated into the project files.

## Recommended actions (for Frank, when next in session)

1. **One-time re-date pass.** Bump due_date on every still-live project to a realistic July/August target. Clears the "13 overdue" alert on DASHBOARD in one move.
2. **Archive the two Deprioritised P2s** (rd-prototype-sso-dns, error-analysis) — remove from the active list, keep the files. error-analysis pipeline has been red since Apr 2; formal archive was already recommended in the Jun 1 health check.
3. **Close conference-writeup** if genuinely Complete, or correct the frontmatter status.
4. **Chase Al on game-experience-prototype review** — 12 weeks silent; likely needs re-scoping rather than re-reviewing.
5. **Chase Bhav on Stadium repo access** — 82-day silence blocks the prototyping platform entirely.
6. **Propagate Al's Apr 21 user-access decision** into the 8 project files still listing SSO/DNS as open.
7. **Personal:** Life insurance (~80+ days overdue) and finance statement uploads (Apr/May/Jun/Jul all missing — Aug review will block a 4th month) remain the two highest-priority personal items in MEMORY.md.

## What changed vs 6 Jul review

- +7 days on every "overdue" counter. Nothing closed, nothing new added, no signal of activity in any project file.
- No new slippage elsewhere — everything dated was already deep in the red.
- This is the only structural difference: sixth straight absent run. If the pattern holds, the review is now producing near-identical reports weekly; worth either committing to the one-time re-date pass or pausing/rescoping this scheduled task so it stops flagging the same static backlog.
