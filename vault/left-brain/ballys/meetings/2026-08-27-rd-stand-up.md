---
type: meeting-note
title: "R&D - Stand up"
date: 2026-08-27
project: "General AI R&D"
attendees: "Al Jepps, Marcos Michel, Sudhanva Mysore Ganesh, Frank Enendu"
source: teams-transcript
---

# R&D - Stand up — 2026-08-27

## Attendees
- Al Jepps
- Marcos Michel
- Sudhanva Mysore Ganesh (Sunny)
- Frank Enendu

## Summary
Al confirmed he is instructing recruitment to make an offer to the senior AI engineer candidate from the recent screener, and reported three further screeners in the pipeline. Sunny reported staging fully green for the portfolio work and outlined a production smoke test today ahead of the NCR presentation this afternoon. Marcos pressed on NCR admin, confirming initiatives need creating in Jira, and noted he is on leave from tomorrow until Monday 7th.

## Key Decisions
- Proceed to offer for the senior AI engineer candidate from the screener stage.
- The team will not hold out for a lead hire — two seniors is acceptable, as the team is functioning without a lead.
- NCR presentation to be kept short and high-level, avoiding the over-detailed format used for the QA NCR.
- Portfolio optimization to be built generically so both iGaming and Intralot Fast Play can plug in different optimization policies.

## Action Items
- [ ] Al Jepps — instruct recruitment to proceed to offer for the senior AI engineer candidate
- [ ] Al Jepps — run the three remaining screener interviews
- [ ] Al Jepps — create the initiatives in Jira for the two NCR items (doing straight after the call)
- [ ] Al Jepps — continue propagating the skill/tooling work to get wider adoption
- [ ] Al Jepps + Sunny — catch up next week to shape portfolio optimization for Intralot before Al's meeting with them
- [ ] Al Jepps — catch up with Bath next week (on holiday this week) on the status of the stalled QA NCR
- [ ] Sunny — get the data-export merge request merged into the dashboard today
- [ ] Sunny — run a production smoke test today across all pipelines
- [ ] Sunny — merge cluster parameter changes and run production tomorrow morning
- [ ] Sunny — final review of the NCR draft ahead of this afternoon's presentation

## Notes
- Screener quality mixed: one candidate rejected outright on communication; three more scheduled.
- Al is working with Intralot on the Massachusetts project; portfolio optimization applies there with different data points. Scratch cards may lack enough variety for the ideation piece, but portfolio optimization is a clear fit — same problem space.
- Sunny has made the portfolio agent generic; only the optimization policy differs between Fast Play and iGaming.
- Staging green end-to-end; next steps are dashboard export, production smoke test, then production run tomorrow.
- Al pushed back on scope creep: R&D should not own setup, infrastructure, maintenance and logging for every project — projects need breaking down so R&D only owns its portion.
- Both NCR items (portfolio and ideation) are R&D-only work, which changes the admin route Marcos needs to follow.
- Marcos on annual leave from 28 Aug until Monday 7 September.
