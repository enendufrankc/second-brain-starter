---
type: meeting-note
title: "AL - Milestone 1 - Catch up"
date: 2026-08-27
project: "Adaptive Layouts"
attendees: "Marcos Michel, Al Jepps, Sudhanva Mysore Ganesh, Adam Bailey"
source: teams-transcript
---

# AL - Milestone 1 - Catch up — 2026-08-27

## Attendees
- Marcos Michel
- Al Jepps
- Sudhanva Mysore Ganesh (Sunny)
- Adam Bailey

## Summary
All staging pipelines (PO1–PO8) are green and both staging and production infrastructure is complete, with Sunny adding an S3 export so pipeline runs are visible on the Adaptive Layouts demo dashboard rather than requiring SageMaker access. Production pipeline runs can start tomorrow, but Nightwatch still has outstanding production deployment work (back office tool, dev tools, Golden Gate / PO9 testing), so real lobbies likely won't be viewable until early next week. Marcos flagged the 9 September launch as at risk; Al disagreed and pushed to qualify the remaining Nightwatch work, set Wednesday as the hard deadline to begin end-to-end testing, and keep the plan unchanged.

## Key Decisions
- End-to-end front-end testing to begin Tuesday if possible, with Wednesday treated as the hard deadline — missing Wednesday means the 9 September date is not achievable.
- The 9 September launch will proceed regardless of progress, but only to a minimal cohort of customers.
- Launch percentage (1% vs 5%) deferred — not decided today, to be revisited Wednesday.
- Marcos will not escalate the schedule risk to Craig or include it in his report; Al takes ownership of the consequences.
- Wider-group messaging this afternoon to stay vague: "working through the launch cohort."
- User testing will not place people into real clusters — a single user will switch lobbies via the dev tool to assess each persona.
- Marketing is not promoting the launch but stays involved for back office tool game promotion decisions.

## Action Items
- [ ] Sunny: merge the MR adding S3 export to the dev account so pipeline runs surface on the Adaptive Layouts demo dashboard
- [ ] Sunny: finalise all production parameters and thresholds by end of today
- [ ] Al: sign off the production parameters before production runs begin
- [ ] Sunny: trigger the production pipelines tomorrow (expect 4–5 hours runtime; lobbies viewable ~Monday)
- [ ] Adam: confirm with Nightwatch (Seth and Sahil) exactly what production deployment work remains and how long it will take
- [ ] Adam: press Nightwatch on timelines and put them on the clock
- [ ] Adam: add Sunny to the back office tool handover session on Wednesday next week
- [ ] Sunny: catch up on the back office tool (contact Sahil, since John is on holiday)
- [ ] Nightwatch: complete Golden Gate (PO9) testing and start the production deployment, including AWS alerts and production setup
- [ ] Sunny: support Nightwatch on any production pipeline or deployment fixes needed
- [ ] Adam and Marcos: brief the wider group this afternoon using vague launch-cohort wording
- [ ] Team: reconvene Wednesday to review testing readiness and decide the launch percentage

## Notes
- Staging pipelines PO1 to PO7/PO8 all running green; staging and production infra both complete.
- S3 export into the dev account removes the dependency on BI for dashboard availability across staging and production.
- Production pipeline run takes roughly 4–5 hours (docker build plus embedding pipeline), so actual lobby output realistically Monday.
- Nightwatch outstanding items: deploy back office tool to production, dev tools setup, Golden Gate (PO9) test completion.
- Back office tool essentially finished by Sahil; handover session with Ops and marketing scheduled Wednesday next week.
- Marcos considers the 9 September milestone at risk because end-to-end testing was meant to start this week and no start date is confirmed.
- Al's position: quantify the remaining Nightwatch work first, then judge risk; believes it is minor and not rocket science.
- Bank holiday Monday reduces available days before the Tuesday/Wednesday testing target.
- Front-end testing scope expected to be minimal; Sunny handles back-end and pipeline side.
- Test plan exists and Craig is aware; Craig will do some user/product testing.
- Marcos is on leave after today, returning on the 10th.
- Tension noted between risk reporting (Marcos's role) and Al's preference to handle issues quietly if they materialise.
