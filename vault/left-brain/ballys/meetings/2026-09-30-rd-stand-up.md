---
type: meeting-note
title: "R&D - Stand up"
date: 2026-09-30
project: "General AI R&D"
attendees: "Frank Enendu, Sudhanva Mysore Ganesh, Marcos Michel, Al Jepps, Serhii Tupikin"
source: teams-transcript
---

# R&D - Stand up — 2026-09-30

## Attendees
- Frank Enendu
- Sudhanva Mysore Ganesh
- Marcos Michel
- Al Jepps
- Serhii Tupikin (likely; some speakers unlabelled in transcript)

## Summary
Round-the-table update. Sudhanva flagged that ~0.2% of users lapse daily and are now removed from OpenSearch, raising an A/B pool-balance question for Adaptive Layouts. Frank covered rubric validation for the Game Experience agents and the interview agent; Al pushed for a pilot group and success criteria for R&D tools. Marcos set up a Spain compliance/commercial meeting.

## Key Decisions
- Lapsed-user effect on A/B pools: mitigate by topping up with new users to keep pool size/composition equal; get Codex and Chris's opinions first.
- Frank to find a pilot audience (and comms, success criteria) for the interview agent rather than only polishing it.
- Agent swarm / software factory: test on an internal problem space, not just open-source repos.

## Action Items
- [ ] Sudhanva: pull real numbers on lapsed users; get Codex + Chris's view on statistical impact for A/B testing
- [ ] Sudhanva: review benchmarking data from Ops team (~30 tasks from KK)
- [ ] Frank: Game DNA rubric validation calls with Adam (30 Sep) and Shannon (1 Oct); start own evals/annotation of rubrics
- [ ] Frank: add Kevin as platform admin on the interview agent
- [ ] Frank: pick pilot group + comms + success criteria for interview agent (Charlotte suggested as lead)
- [ ] Serhii: research how others (e.g. IBM) build agent swarms, define trade-offs and an MVP; test on an internal use case
- [ ] Al: AWS vending work for new products (domain/S3/API gateway/MCP); CloudFront fixed-IP fix for split-tunnel VPN (US/Greece, ~$180/month)
- [ ] Sudhanva/Frank: firm up contextual bandits solution pack with real lobby architecture (submitted to AWS PACE programme)
- [ ] Marcos: Adaptive Layouts Spain meeting with compliance and commercial to set go-live date

## Notes
- Sudhanva looked at ~600K users; lapsed users no longer get adaptive layouts, hence removal from OpenSearch.
- Al's view: easy mitigation by adding new users so test pools stay matched.
- Spain: compliance concerns raised via Marie (commercial); a compliance call with Nightwatch/Adam the day before found no blocking issue. Privacy contact has not yet confirmed whether the notice covers rest of Spain.
- Historical data is saved so commercials can be backfilled later.
