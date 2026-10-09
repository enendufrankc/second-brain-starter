---
project: Adaptive Layouts
type: ballys-project
priority: P0
status: 5% UK step approved 1 Oct (confirm landed); Spain end-Oct at 5%; flagged over budget
criticality: High
owner: Sudhanva Mysore Ganesh
gitlab_issues: none
due_date: 2026-10-01
last_updated: 2026-10-05
---

# Adaptive Layouts

> ⚠️ **Reconstructed 2026-09-21** by the weekly backlog review from meeting notes (27 Aug, 8 Sep). Frank was not present to confirm. Treat milestone ticks as evidence-backed but unverified — correct anything wrong at the next live review.

> ⚠️ **Refreshed 2026-09-28** by the weekly backlog review from four meetings this week (22–25 Sep: R&D stand-ups, the AL Milestone 1 catch-up, and the pipeline read on GGR/ARPU). Frank was not present to confirm — same caveat applies.

> ⚠️ **Refreshed 2026-10-05** by the weekly backlog review from the 30 Sep–1 Oct meetings (R&D stand-ups, AL Milestone 1 catch-up, Spain go-live plan). Frank was not present to confirm — unverified; whether the 1 Oct 5% switch actually landed is NOT confirmed in the vault.

## Overview
AI-generated lobby personalisation for iGaming. Static sections live in Contentful; a back office tool (built by Freddie/Sahil) marks each section fixed or dynamic per cluster; the Adaptive Layouts app (built by Sudhanva) generates AI recommendations that substitute into the dynamic slots. Running across 22 production clusters with control / treatment / unaffected groups for A/B testing.

## Status
- **Stage:** MVP launched 9 Sep 2026 to a minimal cohort; 5% rollout date now firm for **1 October** (game ordering, Programme Analytics reporting, and one MFE launch are the remaining gates)
- **In Use:** Yes — production, limited cohort, ramping
- **Frank's role:** R&D contributor and standup participant; delivery led by Sudhanva, accountable exec Al Jepps, programme managed by Marcos Michel / Adam Bailey
- **⚠️ Risk — over budget:** Marcos flagged the project over budget and emailed Al/Craig (2026-09-24). Advanced-search estimates have shifted since native was dropped from scope; budget to be revisited once those estimates land.
- **⚠️ Risk — A/B read is ambiguous:** GGR is up in the treatment group but ARPU is down; Al suspects this is a skew artefact of casino's right-tailed spend distribution and has asked Insights to model median/distribution alongside mean before drawing conclusions (2026-09-25).
- **Spain:** Gets its own separate A/B experiment (no folding into the current UK test — the current framework is all-or-nothing). UK/Spain clustering audit came back clean both directions, so no new clustering needed; Spain rollout defaults to matching whatever percentage UK is running, once ready. Realistic target **end of October** (Contentful tags + games metadata, both multi-week). Still open: game ops readiness, Thunderbird's Spain A/B experiment build, and Spain compliance sign-off (concerns raised, unresolved).
- **Scope moves (24 Sep milestone catch-up):** Contextual bandits confirmed out of 1.0 scope (frees ~£100k), moving to AWS PACE instead. Commercial optimisation of recommender output is moving in-house — Vitruvian will return vanilla scores. Multi-concurrent-experiment A/B testing goes on the 1.1 backlog (Juan scoping the dev work).

- **1 Oct update:** UK move to 5% approved, targeted within 2–3h of backend + Remote Config release (worst case 8pm). Juan cutting 12h client-side variant cache to max 1h permanently (worst case ~0.9% extra users briefly in treatment). Spain starts directly at 5% (compliance OK at 5%, not higher), target end Oct; KK says Spain content ready in ~10 days. Only open Spain technical gap: locale-specific RTP (may ship as-is). Scope: AL1 agreed; advanced search + contextual bandits next; everything else is AL2 needing time/budget/priority talk with Al. Weekly programme meeting becomes fortnightly and shorter. Lapsed-user (~0.2%/day) A/B pool-balance fix: top up with new users. Spain privacy confirmation (Marcos) still open.

## Architecture
- **Contentful** — all static sections configured for production
- **Back Office App** — fixed vs dynamic section tagging per cluster (handover to Ops/marketing pending)
- **Adaptive Layouts App** — AI recommendation generation into dynamic slots
- **OpenSearch (OPEC)** — full trace capture, LLM call visibility, run status and flagging dashboards
- **Chrome extension** — cluster/variant switching for UAT without member ID insertion
- Materialisation every 6 hours for drafts; instant on publish

## Milestones
- [x] Staging pipelines PO1–PO8 green (2026-08-27)
- [x] Staging and production infrastructure complete (2026-08-27)
- [x] S3 export so pipeline runs surface on the demo dashboard, removing BI dependency (2026-08-27)
- [x] Privacy review — confirmed low risk, no privacy actions required (2026-08-27)
- [x] Production parameters and thresholds finalised and signed off by Al (2026-08-27)
- [x] First production pipeline run (~4–5h runtime) (2026-08-28)
- [x] Monitoring and reporting live — OpenSearch traces, status dashboard (2026-09-08)
- [x] UAT testing setup — Chrome extension across 22 clusters, automated testing across all ventures/platforms (2026-09-08)
- [x] MVP launch to minimal cohort (2026-09-09)
- [x] Decide cohort ramp percentage — 5% locked, target rollout date 1 October (2026-09-24)
- [x] UK/Spain clustering audit — clean both directions, no negative effect, no new clusters needed (2026-09-25)
- [ ] Confirm 5% UK step actually went live (approved 1 Oct, release 2026-10-01 — landing unconfirmed)
- [ ] Juan: backend release removing 12h client cache, then Remote Config release (2026-10-01)
- [ ] Juan: assess RTP locale override; Sudhanva to handle Spain/UK RTP or go without
- [ ] Sudhanva: real numbers on lapsed users + Codex/Chris view on A/B impact
- [ ] Marcos: follow up Spain privacy confirmation; Spain go-live date meeting
- [ ] Finish game ordering for the 5% step (Contentful-sourced fixed sections reordered by commercial score; personalised sections keep current ordering)
- [ ] Ship Programme Analytics reporting for the 5% step
- [ ] Land the one remaining MFE launch for the 5% step
- [ ] Resolve ops-pinned first 6 rows — unpin or make dynamic so adaptive layouts can be evaluated properly (Al drafting message to Dez)
- [ ] Add "suggested for you" section to the AI recommendation pool via Contentful pipeline changes (Sudhanva estimating)
- [ ] Optimise prompts for best-matching sections in row 1
- [ ] Native event tracking — payload testing, dependent on Thunderbird/MFE (Salvatore DeCicco, chased by Adam)
- [ ] Decide whether web-only reporting is acceptable at launch or web+native must align day one
- [ ] Reporting dashboards for native (starts once event testing completes)
- [ ] Data-usage-for-personalisation sign-off — Privacy form outstanding (Adam)
- [ ] Contentful metadata clean-up — ~20,000 of ~35,000 entries validated (Kyriacos)
- [ ] Fix historic data bug — script inserted "1" into gaps, producing symbol counts / max prizes of 1
- [ ] Investigate two discrepancies found in automated testing (Juan)
- [ ] Fix Virgin Games Chrome extension not refreshing between clusters (Juan)
- [ ] Back office tool handover session to Ops and marketing
- [ ] Architecture: decouple fixed/dynamic sections — treat fixed rows as slots the algorithm flows around rather than exclusions (Al's ask, held for consideration)
- [ ] Move commercial optimisation of recommender output in-house — Vitruvian to return vanilla scores (not required for the 1 Oct step)
- [ ] Extend A/B testing to support multiple concurrent experiments (1.1 backlog — Juan scoping)
- [ ] Al to draft a single commercial control-plane proposal for row weighting (all rows, not just row one) and run it by product
- [ ] Spain: add Contentful concept tags to Spanish sections (Freddie/Juan, started after content freeze), games metadata (KK), Thunderbird Spain A/B build, compliance sign-off
- [ ] Insights to add median/distribution modelling to the A/B read alongside mean ARPU
- [ ] Resolve the budget flag raised to Al/Craig (2026-09-24)

## Sources
- [2026-08-27 — AL Milestone 1 Catch up](../meetings/2026-08-27-al-milestone-1-catch-up.md)
- [2026-08-27 — Adaptive Layouts GO live plan](../meetings/2026-08-27-adaptive-layouts-go-live-plan.md)
- [2026-09-08 — Adaptive Layouts UAT Testing Set Up](../meetings/2026-09-08-adaptive-layouts-uat-testing-setup.md)
- [2026-09-08 — R&D Stand up](../meetings/2026-09-08-rd-stand-up.md)
- [2026-09-22 — R&D Stand up](../meetings/2026-09-22-rd-stand-up.md)
- [2026-09-24 — AL Milestone 1 Catch up](../meetings/2026-09-24-al-milestone-1-catch-up.md)
- [2026-09-24 — R&D Stand up](../meetings/2026-09-24-rd-stand-up.md)
- [2026-09-25 — R&D Stand up](../meetings/2026-09-25-rd-stand-up.md)
- [2026-09-30 — R&D Stand up](../meetings/2026-09-30-rd-stand-up.md)
- [2026-10-01 — AL Milestone 1 Catch up](../meetings/2026-10-01-al-milestone-1-catch-up.md)
- [2026-10-01 — Spain go-live plan](../meetings/2026-10-01-adaptive-layouts-go-live-plan-spain.md)
