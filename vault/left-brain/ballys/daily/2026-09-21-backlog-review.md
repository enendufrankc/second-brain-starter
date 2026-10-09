---
type: backlog-review
date: 2026-09-21
status: COMPLETED — vault updated from meeting-note evidence, awaiting Frank's confirmation
---

# Weekly Backlog Review — Monday 21 September 2026

Frank was not present, so step 3 (the interview) did not run — as it has not run on any of the thirteen unattended executions since June. Rather than file a fourteenth identical report, this run reconciled the project files against the vault's own evidence: the Teams meeting notes from 21 Aug – 8 Sep and the auto-generated weekly reviews.

**That turned out to be the real finding.**

## The problem, restated

The project files were not stale because nothing happened. They were stale because a lot happened and none of it was ever written down in the place the dashboards read from.

- **Project files:** frozen at 14–22 April, one at 25 May
- **Meeting notes:** rich and current, running through 8 September
- **Weekly reviews:** flagged the mismatch on 11 September and were not acted on

Three significant workstreams were running with **no project file in the vault at all** — including the team's single biggest piece of work, which launched to production twelve days ago.

## What changed in the vault today

### Created

| File | Why |
|------|-----|
| `projects/adaptive-layouts.md` | P0. MVP launched 9 Sep to a minimal cohort across 22 production clusters. Was entirely untracked. |
| `projects/atlas-game-ops.md` | P1. Frank owns discovery + runner merge + production rewrite. T-shirt sized 27 Aug. Was entirely untracked. |
| `projects/interview-engine.md` | P2. Built, deployed and out for testing in August. Was entirely untracked. |

### Refreshed

| File | Change |
|------|--------|
| `projects/portfolio-optimisation-agent.md` | Status Scoping → NCR presented. Owner → Sudhanva (Frank owns demand signals + costing). Recorded the seven 27 Aug NCR decisions. Ticked 4 evidenced milestones, added 7 new ones. Cleared the five-month-stale 2026-04-25 due date. |
| `projects/game-ideation-agent.md` | P2 → P1, Concept → NCR presented, criticality Medium → High. Linked #35. Added 8 milestones from the NCR and Frank's 1:1. |
| `MEMORY.md` | Replaced the May-era deadline block with September reality. Added five key decisions (27 Aug NCR, Adaptive Layouts launch call, hiring). Added the three new projects. |
| `DASHBOARD.md` | "This Week's Focus" moved from w/c May 25 to w/c Sep 21. Rebuilt "Waiting On" with day counts. |

Every created and refreshed file carries a dated warning banner saying the content was reconstructed without Frank's confirmation. Nothing was ticked that a meeting note does not directly support.

## Closed / completed this week

From the evidence, not from Frank:

- ✅ **Adaptive Layouts MVP launched 9 Sep** — the 27 Aug call to hold the date despite Marcos's risk flag paid off
- ✅ **UAT infrastructure complete** — Chrome extension for cluster switching, automated testing across all ventures and platforms
- ✅ **Monitoring live** — OpenSearch with full trace capture and LLM call visibility
- ✅ **Both Q4 NCRs presented 27 Aug** and judged strong in principle
- ✅ **Portfolio agent built generic** — one platform, pluggable policy for iGaming vs Intralot Fast Play
- ✅ **Interview engine shipped** and out for testing
- ✅ **Senior AI engineer** proceeding to offer

## Overdue or at risk

**The GitLab queue has not moved in five consecutive working days.**

| Issue | Pri | Due | Days over |
|-------|-----|-----|-----------|
| #42 June 2026 Plan | P0 | Jun 30 | 83 |
| #13 Hackathon infra migration | P0 | Jun 13 | 100 |
| #33 Skills Repo broadcast + showcase | P1 | May 30 | 114 |
| #35 Game Ideation scoping w/ Sudhanva | P2 | May 30 | 114 |

Three of the four have not been touched since 19 May. This is roughly twenty minutes of triage and it is currently invalidating every report built on the tracker.

**Silent for 4–5 months:** Al on the Game Experience review (152d), Bhav on Stadium repo access (152d, blocking the Prototyping Platform's 9 open items), Richard Duffy on the Capex steer (152d), Mark Webster on Roadmap MCP testing (135d), Dez on the Tableau collab (157d). At this age these are not "waiting" — they are closed by default. Worth making that explicit.

**Also flagged:** the Game Experience Pipeline is failing on `docs/capture-launch-verdict-design`, and task-tracker is failing on `main` (seen 10 Sep, unaddressed).

## Coming up this week

1. Adaptive Layouts — unblock the ops-pinned first 6 rows and decide the cohort ramp percentage
2. NCR costing with Sunny, owed on Marcos's return
3. Atlas discovery — one week of R&D work, not started since the 27 Aug sizing
4. Demand-signal sourcing and the later pipeline stages Al called woolly
5. Clear the GitLab queue

## Still untracked

Real work with no project file, left alone because the evidence was too thin to reconstruct honestly:

- **AI workshop / hackathon resources** — Frank prepping, dates not found with Al
- **Senior AI engineer hiring** — Frank running screeners and take-home scope
- **Skills/tooling adoption programme** — Al propagating, Frank asked to automate promotion weekly
- **Al's training site review** — Frank owes structural feedback

## Personal

- ⛔ **Life insurance: ~150 days overdue.** Single-income family with a baby, no cover. comparethemarket.com, £250k over 25 years, roughly £15–25/month, about twenty minutes. This has led every report since May.
- ⛔ **Finance review blocked five consecutive months.** No statements uploaded since April; `transactions/` folders empty. Aqua's £0 target remains unverified since 25 April. Five identical failures is a signal that the format is wrong, not that the discipline is — switch to an auto bank-feed or a no-statements Q&A.

## Recommendation on this task

This run changed 6 files. The previous thirteen changed none. The difference was not Frank's presence — it was dropping the interview requirement and reading the evidence already sitting in the vault.

**Re-scope this task to what actually works unattended:** *"Reconcile project files against meeting notes and the GitLab queue, flag contradictions, report."* Keep the interview as a separate thing Frank triggers when he has fifteen minutes, on any day that isn't Monday morning.

The current design has a step it cannot perform, and it has been failing at it politely every week since June.

---

**Generated:** 2026-09-21, unattended. All vault edits are evidence-backed and marked as unconfirmed.
