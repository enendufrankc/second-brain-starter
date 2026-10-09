---
type: meeting-note
title: "AL - Milestone 1 - Catch up"
date: 2026-09-24
project: "Adaptive Layouts"
attendees: "Marcos Michel, Al Jepps, Juan Impey, Adam Bailey, Sudhanva Mysore Ganesh, Frank Enendu"
source: teams-transcript
---

# AL - Milestone 1 - Catch up — 2026-09-24

## Attendees
- Marcos Michel
- Al Jepps
- Juan Impey
- Adam Bailey
- Sudhanva Mysore Ganesh (Sonny)
- Frank Enendu

## Summary
Working session on the 5% rollout targeted at 1 October, what sits in 1.1, and the Spain timeline. Agreed Spain gets its own A/B experiment rather than being folded into the current one, which needs dev work to support multiple concurrent tests. Also covered stripping commercial weighting out of Vitruvian's recommender output, and confirmed contextual bandits moves out of 1.0 scope.

## Key Decisions
- 5% increase target remains 1 October; outstanding work is game ordering, Programme Analytics reporting and one MFE launch
- Spain gets a separate A/B experiment — no fallback of enabling Spain in the current test
- A/B testing must be extended to support multiple concurrent experiments (goes on the 1.1 backlog)
- Spain realistically end of October at best (Contentful tags plus games metadata, both multi-week)
- Commercial optimisation of recommender results moves in-house; Vitruvian returns vanilla scores. Not in scope for the 1 October 5% step
- For 1 October: Contentful-sourced fixed-game sections reordered by commercial score; personalised sections keep current ordering
- Contextual bandits moves out of 1.0 (frees ~£100k allocated in the first initiative); semantic search stays in 2.0
- This meeting is repurposed to cover all Adaptive Layouts versions — 1.0, 1.1, 2.0 — rather than adding new meetings

## Action Items
- [ ] Juan: Scope the dev work to support two separate A/B tests
- [ ] Adam: Add the multi-experiment A/B testing item to PBI this afternoon
- [ ] Adam: Confirm with Craig whether dynamically ordered personalised sections land in 1.1, 1.2 or 2.0
- [ ] Freddie (via Juan): Add content tags to Spanish sections, starting tomorrow after the content freeze
- [ ] KK: Produce games metadata for Spain
- [ ] Al: Work through the commercial-weighting change with Dez — needs buy-in, changes how they operate
- [ ] Marcos: Move remaining tickets with Adam and close out 1.0 epics
- [ ] Marcos: Revisit budget once advanced search sprint estimates are in
- [ ] Adam/Thunderbird: Deliver advanced search sprint-level estimates by end of sprint

## Notes
**Spain A/B** — Current A/B framework was built all-or-nothing in November last year, so Spain sits in the same experiment but disabled client-side, which explains the slight undershoot on the 1% target. Al pushed for proper isolation over a quick enable.

**Recommender weighting** — Goal is one consistent weighting approach everywhere, with commercial optimisation under Bally's control. Al framed supplier-paid pinned rows/positions as opportunity cost that should be evaluated against recommender performance.

**Scope boundaries** — Advanced search is the original filtering-based search, no semantic component. 2.0 currently holds row reordering, semantic search, contextual bandits (now going to AWS) and hyper-personalisation. Al noted the team is effectively booked until Christmas, so 2.0 sequencing is a January problem.

**Budget** — Marcos flagged the project is over budget and has already warned Al and Craig by email. Advanced search estimates have shifted since native was dropped from scope.
