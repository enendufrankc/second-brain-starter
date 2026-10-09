---
type: backlog-review
date: 2026-09-28
status: COMPLETED — vault updated from meeting-note evidence, awaiting Frank's confirmation
---

# Weekly Backlog Review — Monday 28 September 2026

Frank was not present — this scheduled task has no way to interview him live (no AskUserQuestion tool in this session, and no one to answer it if there were). This is the fourteenth consecutive unattended run since June. Per last week's recommendation, this run again reconciled the project files against the vault's own evidence rather than filing an identical "nothing changed" report — this time against the four meeting notes and two daily briefs from 22–25 September.

GitLab itself was **not reachable from this device this run** (same as the 25 Sep auto weekly-review found) — likely VPN-gated. Everything below comes from meeting-note evidence only; the four aging GitLab issues could not be independently re-checked.

## What changed in the vault today

### Updated

| File | Change |
|------|--------|
| `projects/adaptive-layouts.md` | 5% cohort ramp decided, firm rollout date 1 Oct. Added budget-risk flag (Marcos → Al/Craig, 24 Sep), the GGR-up/ARPU-down A/B read under investigation, Spain's separate A/B experiment (~end Oct), contextual bandits confirmed out of 1.0 scope, commercial optimisation moving in-house, and the new 1.1/control-plane items. `due_date` moved from the passed 9 Sep MVP date to the 1 Oct rollout target. |
| `projects/game-experience-prototype.md` | The Al review that had been "pending" since April **actually happened** (23 Sep) — recorded the verdict (~80% there) and the full rework list (drop numeric-score embeddings, rebuild mechanics/tempo, popularity-order game selection, data-derive spin count). Priority/criticality raised Low → High since this now feeds Adaptive Layouts and is going to Product/Tech leadership. Stale April due date cleared. |
| `projects/error-analysis.md` | Brought back from "Deprioritised" — this week's stand-ups show it's now the team's one shared error-analysis system, with Game Experience Profile's eval output merging into it via API (25 Sep). Left the "pipeline failed since Apr 2" note in place as an open question since nothing this week explicitly confirmed that specific fix. |
| `MEMORY.md` | Refreshed deadline day-counts, added five new key decisions from this week, added Serhii to the team list, noted GitLab is unreachable from this device two runs running. |
| `DASHBOARD.md` | "This Week's Focus" moved w/c Sep 21 → w/c Sep 28. Rebuilt "Waiting On" — added four new asks from the Game Exp review and Tableau access, aged the rest, and closed out the "Game Experience review — Al Jepps" line since that review has now happened. |

All three project-file edits carry dated warning banners: evidence-backed, not confirmed by Frank.

### Left untouched (no new evidence this week)

`portfolio-optimisation-agent.md`, `game-ideation-agent.md`, `atlas-game-ops.md`, `interview-engine.md`, `hackathon-platform.md` — the 25 Sep auto weekly-review already confirmed no project file was edited this week and named these specifically as unchanged (NCR costing still "owed on Marcos's return", Atlas discovery "not yet started", etc.). Editing them today with no new evidence would just be guessing.

## Closed / resolved this week

From the evidence, not from Frank:

- ✅ **Adaptive Layouts 5% rollout date locked** — 1 October, ending the 1%-vs-5% deferral from 27 Aug
- ✅ **UK/Spain clustering audit clean both directions** — Spain reuses existing clusters, no new model needed
- ✅ **Al's Game Experience Profile review happened** — 152+ days silent, resolved 23 Sep with a concrete verdict and rework list
- ✅ **Serhii (new senior AI engineer) started and onboarded** — 22–23 Sep
- ✅ **Error-analysis consolidation merged** — one shared tool instead of two (25 Sep)
- ✅ **Contextual bandits confirmed out of Adaptive Layouts 1.0 scope** — frees ~£100k, moves toward AWS PACE

## Overdue or at risk

**The GitLab queue has still not moved — now roughly six weeks untouched.**

| Issue | Pri | Due | Days over (as of last known state) |
|-------|-----|-----|-----|
| #42 June 2026 Plan | P0 | Jun 30 | ~90 |
| #13 Hackathon infra migration | P0 | Jun 13 | ~107 |
| #33 Skills Repo broadcast + showcase | P1 | May 30 | ~121 |
| #35 Game Ideation scoping w/ Sudhanva | P2 | May 30 | ~121 |

**New this week — Adaptive Layouts flagged over budget** by Marcos to Al/Craig (24 Sep), with advanced-search estimates still shifting. This is the highest-profile project in the vault; worth resolving before it becomes a bigger conversation.

**Still silent for 4–5+ months:** Bhav on Stadium repo access (159d, blocking the Prototyping Platform), Richard Duffy on the Capex steer (159d), Mark Webster on Roadmap MCP testing (142d), Dez on the Tableau collab (164d).

## Coming up this week

1. Land the Adaptive Layouts 1 Oct 5% rollout (game ordering, Programme Analytics, one MFE)
2. Resolve the Adaptive Layouts budget flag with Al/Craig
3. Frank reworks the Game Experience Profile per Al's 23 Sep verdict, then presents to Product/Tech leadership
4. NCR costing for Portfolio Optimisation + Game Ideation, still owed
5. Clear the GitLab queue — six weeks untouched now
6. Get GitLab reachable from this device (or another route) so future runs aren't meeting-notes-only

## Still untracked

Real work with no project file, left alone because the evidence doesn't yet support reconstructing scope/ownership/dates honestly:

- **"Software factory"** — Al's proposal (harness that picks up a GitLab issue, plans, codes, tests, opens an MR), assigned to Serhii as his embedding task. Discussed twice this week (22, 23 Sep) but neither meeting settled a definition, scope or owner beyond "Serhii's task."
- **Al's delivery/scheduler/planner proposal** — three-part document (JIRA blocker analysis, org/process review, ML-based planning) that Marcos is reviewing. Al's initiative, not Frank's, but referenced across three of this week's meetings.
- **Adaptive Layouts commercial control-plane proposal** — Al drafting, not yet scoped as a deliverable.

## Personal

- ⛔ **Life insurance: ~157 days overdue.** Unchanged. comparethemarket.com, £250k/25yr, ~20 minutes.
- ⛔ **Finance review blocked 5+ consecutive months.** No statements since April. Standing recommendation unchanged: switch to auto bank-feed or a no-statements Q&A.

## Recommendation on this task (unchanged from last week)

Fourteen unattended runs, zero interviews. The interview step (`AskUserQuestion`) is not available in this scheduled/headless session, and even if it were, there's no one here to answer it. The reconciliation-from-evidence approach is the only version of this task that has ever changed anything in the vault two weeks running. Suggest formally re-scoping this scheduled task's prompt to drop the interview step, and treating a live interview as something Frank triggers himself, separately, when he has fifteen minutes.

---

**Generated:** 2026-09-28, unattended. All vault edits are evidence-backed and marked as unconfirmed.
