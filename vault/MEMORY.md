# MEMORY — Active Knowledge

> This file is loaded into every conversation. Keep it concise (<100 lines).
> Promoted from daily logs by the daily reflection script.

## Critical Deadlines

- **GitLab queue (all overdue, unchanged 12+ days, GitLab unreachable from this device again this run):** #42 June 2026 Plan (P0, 90d), #13 Hackathon infra migration (P0, 107d), #33 Skills Repo broadcast + leads showcase (P1, 121d), #35 Game Ideation scoping with Sudhanva (P2, 121d). Decision needed on each: re-date to Q4 or close. Unmoved for five straight Monday reviews.
- **Adaptive Layouts 5% rollout** — 1 Oct 2026 step approved (landing unconfirmed in vault; Spain starts at 5%, ~end Oct). Remaining gates: game ordering, Programme Analytics reporting, one MFE launch. **⚠️ Flagged over budget** by Marcos to Al/Craig (email, 24 Sep).
- **NCR costing (Portfolio Optimisation + Game Ideation)** — Frank + Sunny, still owed on Marcos's return from leave. Unchanged for the second week running.
- **Game Experience Profile ("Game DNA")** — Al's review finally happened (23 Sep, after ~5 months silent): verdict ~80% there, rework needed on two rubric dimensions + numeric-score embeddings before Frank presents to Product/Tech leadership.
- **Atlas discovery** — 1 week of R&D work Frank owns, still not started since sizing on 27 Aug (now 5+ weeks).
- **Life insurance** — ⛔ ~157+ days overdue. comparethemarket.com, £250k/25yr, ~20 min. Single-income family unprotected.
- **Monthly finance review** — ⛔ blocked 5+ consecutive months (May–Sep); no statements uploaded since April. Switch to auto bank-feed or a no-statements Q&A format.

_Weekly backlog review ran 2026-10-05 (unattended, no interview). Reconciled from 30 Sep–1 Oct meetings: **Adaptive Layouts** (5% UK step approved 1 Oct — landing unconfirmed; Spain start at 5%, end Oct; cache cut to 1h), **Game Experience** (Adam/Shannon rubric validation done; add anticipation/readability/intensity flag, 80 spins), **Interview Engine** (pilot group + success criteria needed). New candidate initiative, untracked: Frank's AWS-migration MR-generator tool (1 Oct stand-up; Sudhanva reviewing; add "grill me" requirements skill) — needs a project file if Frank confirms. GitLab queue (#42/#13/#33/#35), NCR costing, Atlas, life insurance, finance review all unchanged. Report: `daily/2026-10-05-backlog-review.md`._
_Earlier: weekly backlog review ran 2026-09-28 (unattended — Frank not present, no interview; AskUserQuestion is not available in this scheduled session). Followed the 2026-09-21 review's own recommendation: reconciled project files against this week's meeting-note evidence (22–25 Sep: three R&D stand-ups, the AL Milestone 1 catch-up, the Game Exp pipeline review, Serhii's onboarding) rather than filing another report with no vault changes. **Updated `adaptive-layouts.md`** (5% ramp decided, Oct 1 target, budget risk, Spain scope, GGR/ARPU read); **updated `game-experience-prototype.md`** (Al's long-pending review finally happened — verdict + rework list, priority raised Low→High); **updated `error-analysis.md`** (came back from "Deprioritised" — now the shared analysis backbone Game Experience feeds into). All three carry dated warning banners — evidence-backed, unconfirmed by Frank. Portfolio Optimisation, Game Ideation, Atlas, Interview Engine and Hackathon Platform had **no new evidence this week** and were left untouched (confirmed via the 25 Sep auto weekly-review, which also found "no project file was edited this week" before this run). Report: `vault/left-brain/ballys/daily/2026-09-28-backlog-review.md`. Standing asks unchanged from last week: (a) re-date or clear stale due dates on the ~11 untouched projects, (b) archive Deprioritised P2s (rd-prototype-sso-dns), (c) chase Al on the Game Experience follow-through now that his review has actually happened, (d) close out Bhav / Stadium repo access (~159 days silent — blocks Prototyping Platform), (e) propagate Al's Apr 21 user-access decision into files still listing SSO/DNS as open, (f) fix conference-writeup frontmatter mismatch, (g) new this week: resolve the Adaptive Layouts budget flag, and get GitLab access working from this device (VPN-gated) so future runs don't have to rely on meeting notes alone._
_(Prior unattended runs 2026-09-21, 2026-09-07 (paused), 2026-08-24, 2026-08-10, 2026-08-03, 2026-07-27, 2026-07-20, 2026-07-13, 2026-07-06, 2026-06-29, 2026-06-22, 2026-06-15, 2026-06-08 — reports in `daily/`.)_

## Active Projects

### Adaptive Layouts  ⬅️ dominant workstream
- **Status:** Live to a minimal cohort since 9 Sep; 5% rollout locked for 1 Oct 2026. Sudhanva leads build, Al accountable, Marcos/Adam programme-manage. Frank contributes via R&D standup. **Flagged over budget (24 Sep)**; A/B read shows GGR up / ARPU down, under investigation for skew.
- **Open:** game ordering, Programme Analytics reporting, one MFE launch (all gating the Oct 1 step); ops-pinned first 6 rows; native event tracking; Contentful metadata clean-up (~20k/35k validated); Spain A/B (separate experiment, ~end Oct, pending compliance).

### Game Experience Profile ("Game DNA")
- **Status:** Al's review (pending since April) happened 23 Sep — verdict ~80% there. Rework: drop numeric scores from embeddings, rebuild "mechanics"/"tempo" dimensions, popularity-order game selection, data-derive spin count. ~330/3,000 games captured. Presents to Product/Tech leadership soon. Priority raised Low→High.
- **Feeds into:** Adaptive Layouts (user-behaviour clustering); consolidating its eval tooling onto the shared Error Analysis platform.

### Error Analysis
- **Status:** Back to active after months as "Deprioritised" — now the team's one shared error-analysis system. Game Experience Profile's eval output merged in via API (25 Sep) instead of running a separate UI.

### Portfolio Optimisation Agent
- **Status:** NCR presented 27 Aug, judged strong. Generic agent built + smoke-tested; policy pluggable for iGaming vs Intralot Fast Play. Sunny leads; Frank owns demand-signal sourcing + later pipeline stages + joint costing. **Costing still outstanding, unchanged this week.**

### Game Ideation Intelligence Platform
- **Status:** NCR presented 27 Aug, packaged with Portfolio Optimisation as one pipeline. P1. Costing outstanding. Scoping session with Sudhanva (#35) now ~121d overdue.

### Atlas (Game Ops)
- **Status:** Discovery. T-shirt sized 27 Aug. Frank owns discovery (1wk), runner merge (~3wks), production rewrite (1wk). Not started — unchanged this week (5+ weeks since sizing).

### Interview Engine
- **Status:** Built and deployed Aug 2026, out for testing. Marcos trialling. Unchanged this week.

### Hackathon Management Platform
- **Status:** Production since May. #13 infra migration 107d overdue — close as deferred or re-date to Q4.
- **Repo:** gitlab.ballys.tech/igaming/ai-rd (hackathon-management-platform, ID: 8175)

### R&D Prototype SSO/DNS
- **Status:** Deprioritised (P2). Close #15. Decision (Apr 21): no SSO for demos, apps with PII use self sign-up.

### Data Agent
- **Status:** Active — P1. Tableau reporting pivot with Dez. No recorded movement since April.
- **Tracker:** #19

### Ballys Skills Repo
- **Status:** Active development
- **Repo:** gitlab.ballys.tech/igaming/ai-rd (ID: 8284)
- **Local:** /Users/frank.enendu/Documents/Projects/R&D Skills Repo

### Bally's Prototyping Platform
- **Status:** Active (#32, due May 16 — stale). Bhav check-in still overdue (~159 days silent).
- **Key decision (Apr 22):** Stadium (MUI-based, Storybook, brand tokens) is source of truth.

### Roadmap MCP
- **Status:** Active development
- **Repo:** gitlab.ballys.tech/igaming/ai-rd (ID: 8275)
- **Local:** /Users/frank.enendu/Documents/Projects/Roadmap MCP + Agent

## Automated System (built Apr 7)

- **Daily briefing:** 8:45am weekdays → vault/daily/YYYY-MM-DD.md
- **Deadline warnings:** 9:30am weekdays → flags 🔴 overdue and 🟠 due-tomorrow items
- **Pipeline/MR monitor:** 10am, 12pm, 2pm, 4pm weekdays → checks failures and review requests
- **Project health check:** Mon & Thu 9:15am → scans all 12 projects, writes vault/projects/STATUS-DASHBOARD.md
- **End-of-day wrap-up:** 6:30pm weekdays → captures completed, carried over, unanswered
- **Weekly retro:** Friday 5pm → summarizes week, creates GitLab weekly summary issue

## Key Decisions

- 2026-04-03: Started AI second brain. Phase 1 complete (Apr 19). Phase 2 (Contracts 360) next.
- 2026-08-27 (iGaming Tech NCR): Portfolio Optimisation + Game Ideation packaged as ONE connected Q4 pipeline with a shared data interface. Responsible gaming dropped from portfolio scope. Placement/promotion are context inputs only.
- 2026-09-09: Adaptive Layouts MVP live. Monitoring via OpenSearch with full trace capture.
- 2026-09-21: Vault reconciliation — project files had been frozen at April/May state while meeting notes captured Aug/Sep reality. Three untracked workstreams (Adaptive Layouts, Atlas, Interview Engine) were running with no project file at all. Fixed by the weekly review from meeting-note evidence.
- 2026-09-22/23 (Serhii onboarding): New senior AI engineer started 22 Sep. R&D covers Support Hub/Access Hub/AI Gateway/Claude/Cursor/GitLab/AWS access; HR/IT handle laptop and email. Weekly informal engineer catch-up (Fridays) started as a result.
- 2026-09-23 (Game Exp Pipeline Review): Al's long-pending review of Game Experience Profile happened — ~80% there; drop numeric scores from embeddings, rework mechanics/tempo, popularity-order game selection, data-derive spin count. One shared error-analysis system going forward, not two.
- 2026-09-24 (AL Milestone 1 catch-up): Adaptive Layouts 5% rollout firmed for 1 Oct. Spain gets its own A/B experiment (~end Oct). Contextual bandits confirmed out of 1.0 (frees ~£100k). Commercial optimisation of recommender output moves in-house (Vitruvian → vanilla scores). Marcos flagged the project over budget to Al/Craig.
- 2026-10-01 (AL catch-up / Spain plan): UK to 5% approved; Spain starts directly at 5% (compliance OK at 5%, not higher); client variant cache cut to 1h; AL1 scope fixed, rest is AL2; programme meeting goes fortnightly.
- 2026-09-30/10-01 (Game DNA rubric validation, Adam + Shannon): add anticipation, readability, perceived persistence, intensity flag; 80-spin recordings; neutral tempo naming pending compliance.
- 2026-09-25 (R&D stand-up): UK/Spain clustering audit clean both directions — Spain reuses existing clusters, rollout matches UK percentage pending compliance. Al pursuing a single commercial control-plane proposal for row weighting. A/B ARPU read to move to median/distribution given skew.
- **RECOMMENDATION (carried from 2026-09-21, still standing):** this task's interview step (AskUserQuestion) has never once run across 14 attempts — it is not available in unattended/scheduled sessions. The reconciliation-from-evidence approach is what actually works here; keep the live interview as something Frank triggers himself when free.

## Important Facts

- Frank's team: Al Jepps (manager), Sudhanva Mysore Ganesh, Serhii (senior AI engineer, started 2026-09-22). Communicates via AI R&D Teams group chat; new weekly informal Friday engineer catch-up.
- GitLab: self-hosted at gitlab.ballys.tech, PAT in .env. Task tracker project ID: 8489. **Unreachable from this device two runs running — needs corporate VPN.**
- GitHub: enendufrankc (82 repos). PAT in .env. Side projects: govwatch.uk, bizOS, gstack.
- AccessHub approvals: ✅ Approved Apr 7 (Claudia Pantiruc, Jack Edwards, Oktay Osmanov).

## Personal Finance (REVISED 2026-04-25 — after bank statement deep dive)

- **Family:** Wife Nnenna (28), baby son, all dependent on Frank's salary
- **3 bank accounts:** Lloyds (salary/bills), HSBC (holding, £3,950), Revolut (daily spending)
- **Gross salary:** £77,000/year (Gamesys Ltd / Bally's).
- **Net pay:** £4,402.84/month (March 2026 payslip).
- **STABILISATION SPRINT:** May–Oct 2026. No investing until debts cleared and spending under control.
- **Urgent debts:** Aqua £1,909 (44.9% APR), Klarna £292, Capital One £30
- **No life insurance** — ⛔ ~157+ days overdue, highest-priority item, flagged every review since May. comparethemarket.com, £250k/25yr, ~£15–25/mo, ~20 min.
- **Monthly review:** ⛔ blocked 6 consecutive months (1 Oct 2026 run blocked; 1 Sep never ran). 6-month sprint (May–Oct) ended unmeasured. Recommendation: switch to auto bank-feed or a no-statements Q&A format.
- **Last known balances (25 Apr 2026 — 159 days old at 1 Oct):** Aqua ~£1,209 | Klarna £292 (should be £0) | Cap One £30 (should be £0) | HSBC £3,950 | Car finance ~£8,150. ALL UNVERIFIED since.
- **Next review:** overdue — upload Apr–Sep statements or switch review format; this has been the top recommendation for 5 consecutive monthly reviews.
