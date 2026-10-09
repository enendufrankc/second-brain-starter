# Project Status Dashboard — 2026-06-01

*Auto-refreshed by `project-health-check` scheduled task. Source: live GitLab data for tracked projects.*

## Portfolio Health Summary

| Project | GitLab ID | Pipeline | Last Activity | Health |
|---|---|---|---|---|
| hackathon-management-platform | 8175 | ✅ success (main, May 16) · ❌ failed (hackathon-v2, May 18) | May 18 | 🟡 |
| game-experience-agent | 8248 | ✅ success (main, May 11) | May 11 | 🟢 |
| task-tracker | 8489 | ✅ success (main, May 19) | May 19 | 🟢 |
| roadmap-mcp | 8275 | ✅ success (main, May 29) | May 29 | 🟢 |
| ballys-skills-repo | 8284 | ✅ success (main, Mar 19) | Mar 19 | 🟡 |
| data-analyst-agent | 8184 | ✅ success (main, Mar 16) | Mar 16 | 🟡 |
| data-agent | 8276 | — no pipelines | Jan 29 | 🟡 |
| evaluations-error-analysis | 8069 | ❌ **failed** (main + branches, May 18) | May 18 | 🔴 |

Health legend: 🟢 healthy · 🟡 stale or low recent activity · 🔴 pipeline failed, overdue, or critical attention needed.

## 🔴 Red Flags — Act Now

### evaluations-error-analysis — pipeline broken (main + branches)
- Latest pipeline: [#2457901](https://gitlab.ballys.tech/igaming/ai-rd/evaluations-error-analysis/-/pipelines/2457901) — **failed** on `main` at 2026-05-18.
- Additional failures on `backend-test-coverage` branch and MR head (#2457903, #2457898) — same day.
- No open MRs. No commits since. Last activity: 2026-05-18.
- **Persistent red for multiple health checks.** Recommend formal archive decision.

### 3 overdue issues

| # | Priority | Title | Due | Days Late |
|---|---|---|---|---|
| #31 | P1 | Draft AI R&D User Access Strategy — Tiered Auth Approach | May 23 | **9** |
| #33 | P1 | Skills Repo Promotion — Broadcast Email & Showcase | May 30 | **2** |
| #35 | P2 | Game Ideation Scoping — Session with Sudhanva | May 30 | **2** |

## 🟡 Yellow — Needs Attention

- **hackathon-management-platform** — main branch pipeline green (May 16), but `hackathon-v2` branch failed May 18. No activity since. Issue #13 (Infra Migration) due Jun 13 — 12 days.
- **ballys-skills-repo** — last commit Mar 19 (74 days dormant). Pipeline green. Issue #33 (Broadcast Email) now **2 days overdue**.
- **data-analyst-agent** — last activity Mar 16 (77 days dormant). Pipeline green. Blocked on Tableau PAT from Giorgia. Pivoted to automated Tableau reporting agent with Dez Pazmany.
- **data-agent** — no pipelines ever; last activity Jan 29 (123 days). Issue #19 rescheduled to Jun 20.

## 🟢 Green — Healthy

- **roadmap-mcp** — ✅ Resumed activity after months dormant. 3 pipeline runs on May 27–29. Last activity May 29.
- **game-experience-agent** — pipeline green, active May 11. EventBridge fix and daily pipeline schedule committed.
- **task-tracker** — pipeline green, last updated May 19.

## Open Issues Snapshot

### 🔴 Overdue (3)

| # | Priority | Title | Due | Days Late |
|---|---|---|---|---|
| #31 | P1 | AI R&D User Access Strategy — Tiered Auth | May 23 | **9** |
| #33 | P1 | Skills Repo Promotion — Broadcast Email & Showcase | May 30 | **2** |
| #35 | P2 | Game Ideation Scoping w/ Sudhanva | May 30 | **2** |

### ✅ On Track (3)

| # | Priority | Title | Due | Days Left |
|---|---|---|---|---|
| #13 | P0 | Hackathon Platform Infra Migration | Jun 13 | 12 |
| #19 | P1 | Data Agent — Agentic Harness & Research Capability | Jun 20 | 19 |
| #32 | P1 | Prototyping Platform — Stadium Integration | Jun 27 | 26 |

## Changes Since Last Check (May 11)

- **#15, #16, #34 closed/resolved** — no longer in open issues. Overdue count dropped from 8 → 3. 
- **roadmap-mcp resumed** — was dormant since Mar 11, now has 3 new pipeline runs (May 27–29). 🟢 upgrade.
- **hackathon-management-platform main branch** now green (was failing May 11); new `hackathon-v2` branch failure introduced May 18.
- **evaluations-error-analysis** escalated: new failures added May 18 across main + branches.
- **Issue #19 rescheduled** — was overdue Apr 30, now due Jun 20. Pressure reduced.
- **Issue #32 (Prototyping Platform)** still on track — due Jun 27.

## Pipeline Details

| Project | Latest Pipeline | Status | Branch | Updated |
|---|---|---|---|---|
| hackathon-management-platform | [#2457217](https://gitlab.ballys.tech/igaming/ai-rd/hackathon-management-platform/-/pipelines/2457217) | ✅ success | main | May 16 |
| hackathon-management-platform | [#2458661](https://gitlab.ballys.tech/igaming/ai-rd/hackathon-management-platform/-/pipelines/2458661) | ❌ failed | hackathon-v2 | May 18 |
| game-experience-agent | [#2449511](https://gitlab.ballys.tech/igaming/ai-rd/game-experience-pipeline/-/pipelines/2449511) | ✅ success | main | May 11 |
| ballys-skills-repo | [#2385954](https://gitlab.ballys.tech/igaming/ai-rd/ballys-skills-repo/-/pipelines/2385954) | ✅ success | main | Mar 19 |
| roadmap-mcp | [#2473815](https://gitlab.ballys.tech/igaming/ai-rd/roadmap-agent/-/pipelines/2473815) | ✅ success | main | May 29 |
| task-tracker | [#2460181](https://gitlab.ballys.tech/igaming/ai-rd/task-tracker/-/pipelines/2460181) | ✅ success | main | May 19 |
| data-analyst-agent | [#2382121](https://gitlab.ballys.tech/igaming/ai-rd/data-analyst-agent/-/pipelines/2382121) | ✅ success | main | Mar 16 |
| data-agent | — | — no pipelines | — | — |
| evaluations-error-analysis | [#2457901](https://gitlab.ballys.tech/igaming/ai-rd/evaluations-error-analysis/-/pipelines/2457901) | ❌ failed | main | May 18 |

## Vault Lint Summary

**22 errors · 21 warnings · 13 info** (run: 2026-06-01)

- All 22 errors are broken wiki-links in DASHBOARD.md files (left-brain and right-brain) — not blocking, cosmetic only.
- 18 of 21 warnings are project files with no daily log mention in 7+ days — expected for dormant projects.
- Memory files over size limits: MEMORY.md (113/100 lines), SOUL.md (82/70), USER.md (136/120) — consolidation recommended.
- HABITS.md not recently reset.
- No structural errors auto-fixed (all errors are wiki-link issues, not auto-fixable).

*Last refreshed: 2026-06-01 08:21 (auto)*
