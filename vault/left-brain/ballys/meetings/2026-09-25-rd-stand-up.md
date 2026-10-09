---
type: meeting-note
title: "R&D - Stand up"
date: 2026-09-25
project: "General AI R&D"
attendees: "Al Jepps, Sudhanva Mysore Ganesh, Frank Enendu, Marcos Michel"
source: teams-transcript
---

# R&D - Stand up — 2026-09-25

## Attendees
- Al Jepps
- Sudhanva Mysore Ganesh (Sonny)
- Frank Enendu
- Marcos Michel (joined partway through)

## Summary
Adaptive Layouts dominated: Al wants a single control plane for commercial row-weighting rather than the current top-row-only rules, and flagged that GGR is up but ARPU down in the treatment group — likely a skew issue, so he's asked insights for median/distribution modelling instead of mean. Sonny's UK/Spain clustering audit came back clean, and Spain product ops work is running ahead of schedule, though Spain compliance sign-off is still open. Al also walked through a three-part delivery/scheduler proposal (blocker data analysis, org/process review, and an ML approach to planning and slot-filling) that Marcos agreed to review.

## Key Decisions
- Spain rollout percentage will match whatever UK is on (parity), pending compliance sign-off — no separate cautious 1% for Spain
- Pursue a single commercial control-plane for row weighting (not just the top row) as a proposal to product, rather than one-off fixes
- Insights to move A/B test reporting to median/distribution rather than mean ARPU, given the skew

## Action Items
- [ ] All: Complete at least 2 AI field notes sessions each by next week (postponed from this week)
- [ ] Al: Draft the commercial control-plane proposal and run it by product
- [ ] Al: Send the delivery scheduler/planner proposal doc to Marcos
- [ ] Al: Pull JIRA timing data and analyse where delivery gets held up (enterprise IT, platform, data team steps)
- [ ] Marcos: Review Al's scheduler/planner proposal
- [ ] Frank: Email Georgia to fix Tableau access (back token not working)
- [ ] Frank: Follow up with Owen to run a field notes session today
- [ ] Frank: Track down the 9 games missing from the current catalogue (103 shared by Sonny vs. 94 found)

## Notes
**Adaptive Layouts — commercial control plane**: Al flagged the top row's commercial weighting rules as bespoke and hard to manage; he wants any such weighting (e.g. boosting a provider or setting a row's commercial split) available as a capability across all rows, not just row one. Plan is to scope it as a proposal for product rather than build it ad hoc.

**Spain/UK clustering audit**: Sonny completed the reverse audit (UK impact of including Spain in global clusters, having already checked the Spain-side impact). Result: no negative effect either direction, supporting a move to 5% and reusing the same clusters for Spain. Provider-specific clusters were the one wrinkle — confirmed the "provider" field reflects the actual game developer/studio, not the aggregator, which is the right signal.

**A/B test read**: GGR is up in the treatment group but ARPU is down, which Al thinks is misleading given casino's right-tailed spend distribution. He's asked insights to add median/distribution modelling alongside mean ARPU before drawing conclusions.

**Spain rollout**: Product Ops is close to finished, ahead of the original few-week estimate. Still pending: game ops readiness, Thunderbird's new A/B testing experiment for Spain, and compliance sign-off (Spain compliance raised unspecified concerns, not yet resolved). Default plan is to launch Spain at whatever percentage UK is running, once ready.

**Delivery/scheduler proposal (Al)**: Document is close to done, covering three areas — (1) data-driven blocker analysis using JIRA timings across enterprise IT, platform and data team steps, (2) org/process changes for iGaming, and (3) an ML-based approach to planning, slot-filling and scheduling as a research effort to compare against manual planning. Marcos will read and can action anything process-related directly.

**Frank's updates**: Merged the error-analysis changes so error analysis feeds the priority list already built in the eval tab. Of the 103 games Sonny shared, only 94 are in the current catalogue — still need to locate the other 9. Tableau access is blocked on a broken back token; emailing Georgia to resolve. Trying to line up a field notes session with Owen today, no reply yet.
