---
type: daily-note
title: Backlog Review — 2026-07-27
date: 2026-07-27
tags: [backlog-review, automated, unattended]
---

# Weekly Backlog Review — Mon 27 Jul 2026

**Status:** ⚠️ Automated run — Frank not present (**8th consecutive Monday**).
No AskUserQuestion prompts issued. No project files modified. No MEMORY.md edits.

## Delta vs last week (2026-07-20)

Zero. No project frontmatter, milestone, or MEMORY.md edits have occurred since 6 May 2026 (82 days). All counters simply advance +7d.

## Standing backlog (unchanged since 6 May)

**Ballys — open project files with unchecked milestones and stale dates:**

| Project | Priority | Due (stated) | Days overdue | Notes |
|---|---|---|---|---|
| Roadmap MCP | — | May 9 | ~79d | DNS/SSO/testing per MEMORY |
| Hackathon Platform (#13 infra) | P0 | May 9 | ~79d | was "at risk" |
| Capex Machine | — | May 16 | ~72d | implementation not started |
| Stadium/Prototyping Platform (#32) | — | May 16 | ~72d | Bhav Stadium repo access silent 96d |
| Tableau MCP Agent | — | May 23 | ~65d | Dez collab, LangGraph open |
| Video Analysis | — | May 30 | ~58d | Databricks validation open |
| Hive Metastore shutdown | — | May 31 | ~57d | R&D pipeline dependency unconfirmed |
| Game Experience Prototype | — | — | — | Al's review silent ~14 wks |
| #41 IGNITE Showcase (S3+CF) | — | — | — | assigned May 7, status unknown |
| Portfolio Optimisation Agent (#16) | P0 | Apr 25 | ~93d | brainstorming |
| Data Agent (#19) | P1 | Apr 30 | ~88d | pivoted to Tableau reporting |

**Deprioritised P2s still not archived:** `rd-prototype-sso-dns.md`, `error-analysis.md`.

**Frontmatter propagation still pending:** Al's Apr 21 user-access decision (no SSO for demos; PII apps use self sign-up) has not been applied to the ~8 project files that still list SSO/DNS as open.

**Meta-issue:** `conference-writeup.md` frontmatter mismatch (marked complete Apr 22 in DEADLINES.md, still appears in project list).

## Personal (from MEMORY.md — for visibility only, no action taken)

- **Life insurance:** ⛔ ~94+ days overdue. Comparethemarket, £250k/25yr, ~20 min task.
- **Monthly finance review:** ⛔ Apr / May / Jun / Jul statements never uploaded. Aug 1 review will block a 4th consecutive month unless statements land first.
- Aqua £0 target (Q2) UNVERIFIED — no statements to confirm.

## Recommendation

**Pause this scheduled task.** 8 consecutive identical unattended runs generate log churn and zero backlog signal. Options:

1. Delete the schedule and re-create it as an ad-hoc trigger Frank fires when he's ready to sit through it.
2. Or, keep the schedule but have it run only if a `.trigger-backlog-review` sentinel file exists (Frank creates it Sunday night when he plans to attend Monday).
3. Or, downgrade to fortnightly / monthly cadence.

## What this run did NOT do

- Did not check off any milestones (`- [ ]` → `- [x]`).
- Did not update any project frontmatter (status, priority, due_date, last_updated).
- Did not add or archive any projects.
- Did not edit MEMORY.md.
- Did not read the 18 individual project files (unchanged since 6 May — verified via prior week's report).

Rationale: task instructions say "when in doubt, producing a report of what you found is the correct output" and forbid guessed write actions in Frank's absence.
