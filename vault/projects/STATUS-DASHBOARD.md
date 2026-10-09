---
type: project-dashboard
title: AI R&D Portfolio — Status Dashboard
description: Live health across the 8 tracked GitLab projects — pipelines, MRs, issues, CI config
resource: vault/projects/STATUS-DASHBOARD.md
tags: [projects, gitlab, health, dashboard]
timestamp: 2026-10-08T09:00:00+01:00
---

# AI R&D Portfolio — Status Dashboard

> Last updated: Thursday 8 October 2026
> *Scheduled `project-health-check` (8 Oct run; earlier sections retained below). All 8 tracked IDs queried live via GitLab API (read-only); `gather_status.py --pipelines` covers 4 repos, the rest queried directly.*

---

## 8 October Check — What Changed (since 5 Oct)

**Overall health: AMBER 🟡 — unchanged.** Same two red `main` branches, same 8 overdue issues (all task-tracker; 14th consecutive check with no movement).

| Project | ID | Default-branch pipeline | Open MRs | Open Issues | Last Activity | Status |
|---|---|---|---|---|---|---|
| game-experience-agent | 8248 | 🟢 MR !101 #2697301 green, can be merged; `main` #2697256 `manual` (by design) | 7 (!101 today, !76 15d, !27 43d, 4 drafts 77d) | 7 | today | 🟢 Healthy, shipping |
| ballys-skills-repo | 8284 | 🟢 PASS (#2669304, 24 Sep) | 1 (!1 **blocked 22d**, head pipeline #2653664 still failed) | 5 | 14d | 🟠 Green, unblock !1 |
| hackathon-management-platform | 8175 | 🟢 PASS (#2677028, 28 Sep) | 0 | 13 | 8d | 🟡 Green CI, #18 prod bug open; #13 migration overdue 117d |
| roadmap-mcp | 8275 | 🟢 PASS (#2624914, 29 Aug) | 0 | 0 | 40d | 🟢 Quiet, healthy |
| task-tracker | 8489 | 🔴 **FAIL** (#2697327, 7 Oct) — `pages` `stuck_or_timeout_failure` | 1 (!6, 122d) | 20 (**8 overdue**) | 88d | 🔴 CI dead since 15 Jun |
| evaluations-error-analysis | 8069 | 🔴 **FAIL** (#2686622, 2 Oct) — `smoke:fresh-stack`; no new run since | 0 | 6 | 5d | 🔴 `main` still red |
| data-analyst-agent | 8184 | ⚠️ Fossil green (#2382121, 16 Mar) | 0 | 0 | 206d | ⚫ Dormant |
| data-agent | 8276 | ⚫ No CI | 0 | 0 | 252d | ⚫ Dormant, archive candidate |

### 🚨 Red items
- 🔴 **task-tracker CI** — still failing nightly; `.gitlab-ci.yml` still uses dead tag `igaming-small-pgt` (swap to `tlg-teamspaces-small-pgt`). MR !6 stuck 122d.
- 🔴 **evaluations-error-analysis `smoke:fresh-stack`** — `main` red since 2 Oct, unfixed.
- 🔴 **ballys-skills-repo MR !1** — blocked 22 days, never retried.
- 🔴 **8 overdue issues (5 P0)** in task-tracker: #2, #5 (190d), #39, #35, #33, #16, #13, #42 — no due-date changes.
- 🟡 hackathon-management-platform #18 (`priority::high`) still open, no MR.

| Metric | 5 Oct | **8 Oct** |
|---|---|---|
| Overdue issues / P0 | 8 / 5 | **8 / 5** |
| Default-branch pipelines failing | 2 | **2** |
| Open MRs | 8 | **9** (+!101) |
| Blocked external MRs | 1 (19d) | **1 (22d)** |

---

## 5 October Check — What Changed (since 1 Oct)

**Overall health: AMBER 🟡 — unchanged.** Same two red `main` branches, same 8 overdue issues (13th consecutive check with no movement). `gather_status.py --pipelines` covers 4 repos only; the other 4 were queried directly via the GitLab API (read-only).

| Project | ID | Default-branch pipeline | Open MRs | Open Issues | Last Activity | Status |
|---|---|---|---|---|---|---|
| game-experience-agent | 8248 | 🟢 MRs green (#2690613); `main` #2690767 **running**, #2690616 manual | 6 (!76 12d, !27 40d, 4 drafts 74d) | 7 | today | 🟢 **Healthy, shipping** (MRs !86–!88 merged today) |
| ballys-skills-repo | 8284 | 🟢 PASS (#2669304, 24 Sep) | 1 (!1 **blocked 19d** 🔴) | 5 | 11d | 🟠 Green, unblock !1 |
| hackathon-management-platform | 8175 | 🟢 PASS (#2677028, 28 Sep) | 0 ✅ | 13 (#18 `priority::high`) | 5d | 🟡 Green CI, prod bug open |
| roadmap-mcp | 8275 | 🟢 PASS (#2624914, 29 Aug) | 0 ✅ | 0 ✅ | 37d | 🟢 Quiet, healthy |
| task-tracker | 8489 | 🔴 **FAIL** (#2689963, 4 Oct) — `pages` `stuck_or_timeout_failure`; failing nightly (2, 3, 4 Oct all red) | 1 (!6, 119d) | 20 (**8 overdue**) | 85d | 🔴 **CI dead since 15 Jun** |
| evaluations-error-analysis | 8069 | 🔴 **FAIL** (#2686622, 2 Oct) — `smoke:fresh-stack` `script_failure`; all other jobs pass | 0 ✅ (!19, !20 merged 2 Oct) | 6 (2 `ready-for-human`) | 2d | 🔴 **`main` still red on same job** |
| data-analyst-agent | 8184 | ⚠️ Fossil green (#2382121, 16 Mar) | 0 | 0 | 203d | ⚫ Dormant |
| data-agent | 8276 | ⚫ No CI | 0 | 0 | 249d | ⚫ Dormant — archive candidate |

### 🚨 Red items
- 🔴 **task-tracker CI** — red every night since 15 Jun (dead runner tag `igaming-small-pgt`; swap to `tlg-teamspaces-small-pgt`). MR !6 stuck 119d.
- 🔴 **evaluations-error-analysis `smoke:fresh-stack`** — failed again after MRs !19/!20 merged; fourth red `main` run on the same job (still unfixed since the 24 Sep 403 diagnosis).
- 🔴 **ballys-skills-repo MR !1** — blocked 19 days; pipeline #2653664 never retried.
- 🔴 **8 overdue issues (5 P0)** in task-tracker: #5, #2 (183d+), #39, #35, #33, #16, #13, #42 (oldest 187d) — no due-date changes.
- 🟡 hackathon-management-platform #18 (`priority::high` upload 500s) still open, no MR.

### Trend (additions)
| Metric | 1 Oct | **5 Oct** |
|---|---|---|
| Overdue issues / P0 | 8 / 5 | **8 / 5** |
| Default-branch pipelines failing | 2 | **2** |
| Repos on dead runner tag | 2 | **2** |
| Open MRs | 8 | **8** |
| Blocked external MRs | 1 (15d) | **1 (19d)** |

---

## 1 October Check — What Changed (since 28 Sep)

**Overall health: AMBER 🟡 — unchanged.** Same two chronic red repos, same stuck backlog; the two fixes identified on 24 Sep (runner-tag swap, smoke-test 403) are still unapplied.

🔴 **`task-tracker` `main` has failed 3 more nights (28, 29, 30 Sep)** — latest **#2683763, 30 Sep 22:00**, `pages` job, `stuck_or_timeout_failure`. `.gitlab-ci.yml` still has `igaming-small-pgt`. Streak now ~107 consecutive failures.

🔴 **`evaluations-error-analysis` `main` still red** — a *new* pipeline ran (**#2676678, 29 Sep**, after MR !18 merged 28 Sep) and **failed again on `smoke:fresh-stack`** (script_failure; same job as the 24 Sep 403). All other jobs pass. Third consecutive red `main` run on the same job.

🔴 **`ballys-skills-repo` MR !1 now blocked 15 days** — head pipeline still #2653664 (failed 16 Sep), never retried; runner-tag fix has been on `main` since 24 Sep.

🟡 **`hackathon-management-platform` #18 (`priority::high` upload 500s for all users) still open**, no MR in flight. Positive: MR !14 merged 28 Sep, `main` #2677028 green.

🟢 **`game-experience-agent` shipping** — MRs !84 and !85 merged 29–30 Sep; MR pipelines green. `main` pipelines (#2679870, #2682774) sit in `manual` (dev DNA/acceptance gates awaiting manual trigger — by design, not a failure; last auto-green `main` #2671693).

---

## 🚨 RED FLAGS

| Flag | Detail |
|---|---|
| **`task-tracker` CI dead since 15 Jun 🔴** | #2683763 (30 Sep) FAILED — `pages` job, no runner accepts tag `igaming-small-pgt`. Fix: swap to `tlg-teamspaces-small-pgt` (proven on ballys-skills-repo). MR !6 stuck behind it, 114d stale. |
| **`evaluations-error-analysis` smoke test failing 🔴** | #2676678 (29 Sep) FAILED on `smoke:fresh-stack`; deploy + build/lint/test pass. Previously diagnosed as a 403 from the preview frontend (CloudFront/WAF/origin auth). 2 `ready-for-human` issues (#4, #6) stalled. |
| **`ballys-skills-repo` MR !1 blocked 15d 🔴** | External contributor's first MR; one pipeline retry + a reply would unblock. |
| **8 overdue issues, 5 P0 — 12th consecutive check with no movement 🔴** | All in `task-tracker`; see table below. |
| **`hackathon-management-platform` #18 🟡** | Production bug, high priority, no PR in flight. |
| **`data-analyst-agent` fossil green ⚫** | Last pipeline 16 Mar; still on dead tag `igaming-small-pgt` — will fail on next push. |
| **`data-agent` ⚫** | No CI, 244d idle — archive candidate. |

---

## Project Health Table

| Project | ID | Default-branch pipeline | Open MRs | Open Issues | Last Activity | Status |
|---|---|---|---|---|---|---|
| game-experience-agent | 8248 | 🟢 MRs green; `main` #2682774 **manual** (gates awaiting trigger) | 6 (!76 7d, !27 35d, 4 drafts 69d) | 7 | 1d | 🟢 **Healthy, shipping** |
| ballys-skills-repo | 8284 | 🟢 **PASS** (#2669304, 24 Sep) | 1 (!1 **blocked 15d** 🔴) | 5 | 7d | 🟠 **Green, unblock !1** |
| hackathon-management-platform | 8175 | 🟢 **PASS** (#2677028, 28 Sep) | 0 ✅ | 13 (#18 `priority::high`) | 1d | 🟡 **Green CI, prod bug open** |
| roadmap-mcp | 8275 | 🟢 **PASS** (#2624914, 29 Aug) | 0 ✅ | 0 ✅ | 33d | 🟢 **Quiet, healthy** |
| task-tracker | 8489 | 🔴 **FAIL** (#2683763, 30 Sep) — dead runner tag, ~107 in a row | 1 (!6, 114d) | 20 (**8 overdue**) | 81d | 🔴 **CI dead since 15 Jun** |
| evaluations-error-analysis | 8069 | 🔴 **FAIL** (#2676678, 29 Sep) — `smoke:fresh-stack` | 0 ✅ | 6 (2 `ready-for-human`) | 3d | 🔴 **Active, `main` never green** |
| data-analyst-agent | 8184 | ⚠️ Fossil green (#2382121, 16 Mar), bad tag | 0 | 0 | 198d | ⚫ **Dormant + latently broken** |
| data-agent | 8276 | ⚫ No CI configured | 0 | 0 | 244d | ⚫ **Dormant — archive candidate** |

**Runner tag audit (today):** `igaming-small-pgt` (dead) still on `task-tracker` and `data-analyst-agent`; `ballys-skills-repo` fixed since 24 Sep.

---

## Issue Tracker

### 🔴 Overdue (all in `task-tracker`)

| # | Pri | Project label | Title | Due | Days Over |
|---|---|---|---|---|---|
| #5 | **P0** | harman | Evaluate Harman Automated Game Testing Tool | 1 Apr | **183** |
| #2 | **P0** | clustering | Test: Set up clustering pipeline | 1 Apr | **183** |
| #39 | P1 | adaptive-layouts | Backoffice tool build — Claude Code vs Pi agent experiment | 29 Apr | **155** |
| #35 | P2 | game-ideation | Game Ideation Intelligence Platform — Scoping w/ Sudhanva | 30 May | **124** |
| #33 | P1 | ballys-skills-repo | Skills Repo Promotion — Broadcast Email & Eng Leads Showcase | 30 May | **124** |
| #16 | **P0** | portfolio-optimisation-agent | Start brainstorming on Portfolio Optimisation | 6 Jun | **117** |
| #13 | **P0** | hackathon-management-platform | Migrating Hackathon Platform to scalable infrastructure | 13 Jun | **110** |
| #42 | **P0** | general | 📌 June 2026 Plan — Game Experience + Game Ideation (Frank) | 30 Jun | **93** |

No issue with a future due date exists across the 8 repos.

---

## Open Merge Requests

| Project | MR | Title | State |
|---|---|---|---|
| ballys-skills-repo | !1 | Add share-work-example benchmark contribution skill | **🔴 BLOCKED 15d** — head pipeline failed 16 Sep, unretried |
| task-tracker | !6 | feat: drive Gantt from shared #42 checklist + personal daily overlay | Blocked behind failing CI, 114d |
| game-experience-agent | !76 | feat(evaluation): hand DNA attempts to Error Analysis tool | Open, 7d |
| game-experience-agent | !27 | docs(capture): what causes a failed capture | Ready — 35d stale |
| game-experience-agent | !5 / !4 / !3 / !2 | Draft capture/E1/E3/E4 MRs | Drafts — 69d stale |

**Merged since 28 Sep: 4** (hackathon !14, game-experience-agent !84 & !85, evaluations-error-analysis !18).

---

## Recommended Actions

1. Change runner tag to `tlg-teamspaces-small-pgt` in `task-tracker` and `data-analyst-agent` `.gitlab-ci.yml`.
2. Retry pipeline #2653664 on `ballys-skills-repo` !1 and reply to the contributor.
3. Fix the `smoke:fresh-stack` failure on `evaluations-error-analysis` (check CloudFront/WAF/origin auth on the preview frontend).
4. Triage `hackathon-management-platform` #18.
5. One 15-minute pass over the 8 overdue `task-tracker` issues: close #2 and #42, re-date #5/#16/#35/#39, action #13 and #33.
6. Close or land `game-experience-agent` drafts !2–!5 and !27.
7. Archive `data-agent` (8276).

---

## Trend

| Metric | 21 Sep | 24 Sep | 28 Sep | **1 Oct** |
|---|---|---|---|---|
| Overdue issues | 8 | 8 | 8 | **8** |
| P0 overdue | 5 | 5 | 5 | **5** |
| Default-branch pipelines failing | 2 | 3 | 2 | **2** |
| Repos on dead runner tag | 3 | 2 | 2 | **2** |
| Open MRs | 8 | 8 | 8 | **8** |
| Blocked external MRs | 1 | 1 (8d) | 1 (12d) | **1 (15d)** |
| task-tracker failure streak | 97 | 100 | 103–104 | **~107** |
| Overall health | 🟠 | 🟠 | 🟡 | **🟡** |

---

*Generated by the `project-health-check` scheduled task, 1 October 2026. `gather_status.py --pipelines` run as specified (covers 4 repos only); remaining repos queried directly via the GitLab API.*
