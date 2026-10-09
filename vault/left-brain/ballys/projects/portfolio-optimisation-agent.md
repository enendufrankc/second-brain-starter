---
project: Portfolio Optimisation Agent
type: ballys-project
priority: P0
status: NCR presented — costing outstanding
criticality: High
owner: Sudhanva Mysore Ganesh
gitlab_issues: "#16"
due_date:
last_updated: 2026-09-21
---

# Portfolio Optimisation Agent

> ⚠️ **Refreshed 2026-09-21** by the weekly backlog review from the 27 Aug iGaming Tech NCR and the Aug standups. Frank was not present to confirm. The April due date (2026-04-25) was five months stale and has been cleared rather than guessed at — set a real one at the next live review.

## Overview
Data-backed hold / enhance / withdraw recommendations plus gap analysis across games, brands, markets and segments. Built generically as one reusable platform serving both Bally's iGaming and Intralot Fast Play — only the optimisation policy differs between them. Packaged with the Game Ideation Agent as a single connected pipeline: portfolio gaps feed ideation, which feeds Wonder Machine and the studios.

## Status
- **Stage:** NCR presented 27 Aug 2026 and judged strong in principle; generic agent built and smoke-tested; Intralot shaping session next
- **In Use:** No
- **Owner shift:** Sudhanva (Sunny) leads the build. Frank owns the demand-signal sourcing, the later pipeline stages, and joint costing.
- **Related:** Game Ideation Intelligence Platform, Game Experience Profile, Adaptive Layouts

## Key Decisions (27 Aug 2026 — iGaming Tech NCR)
- Portfolio Optimisation and Game Ideation are packaged as **one connected pipeline**, with an automated shared data interface passing agreed gaps from optimisation into ideation.
- Human-in-the-loop only — no autonomous decisions, no recommendation without policy, context and cited evidence.
- **Responsible gaming dropped from scope** — existing mechanisms cover it.
- Placement, promotion and exposure are **context inputs only** — the agent will not issue placement or promotion recommendations.
- Costing taken offline into a separate session (Sunny + Frank).
- Built as one reusable platform for Bally's and Intralot; pilots scoped separately (Intralot wants a narrower pilot area).
- A third pipeline element for prototype and artwork generation to be explored with the Free Play team and Gael, potentially its own NCR.

## Milestones
- [x] Define agent scope and data sources (#16) (2026-08)
- [x] Architecture design — generic agent, pluggable optimisation policy (2026-08)
- [x] Core agent build + production smoke test across all pipelines (2026-08-27)
- [x] NCR draft written and presented to iGaming Tech (2026-08-27)
- [ ] Complete costing for both NCRs in a follow-up session (Sunny + Frank — due on Marcos's return)
- [ ] Al to route the case to Chris for a soft dollar-value estimate
- [ ] Share the portfolio optimisation pack with Dez and gather Intralot insights, not just data (Sunny)
- [ ] Remove responsible gaming from the required-teams / scope slide (Sunny)
- [ ] Factor adaptive layouts into the context model — a game can now appear in multiple positions and placement correlates strongly with revenue (Sunny)
- [ ] Fold the already-ticketed persona / game-affinity work into the segments dimension (Sunny)
- [ ] Al + Sunny shaping session for Intralot / Massachusetts ahead of Al's meeting with them
- [ ] Integration with Game Experience Agent
- [ ] Testing and validation
- [ ] Production deploy

## Sources
- [2026-08-27 — iGaming Tech NCR](../meetings/2026-08-27-igaming-tech-ncr.md)
- [2026-08-25 — R&D Stand up](../meetings/2026-08-25-rd-stand-up.md)
- [2026-08-27 — R&D Stand up](../meetings/2026-08-27-rd-stand-up.md)
