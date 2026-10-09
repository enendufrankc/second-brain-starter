---
type: meeting-note
title: "AL - Milestone 1 - Catch up"
date: 2026-10-01
project: "Adaptive Layouts"
attendees: "Marcos Michel, Juan Impey, Sudhanva Mysore Ganesh, Adam Bailey, Frank Enendu"
source: teams-transcript
---

# AL - Milestone 1 - Catch up — 2026-10-01

## Attendees
- Marcos Michel
- Juan Impey
- Sudhanva Mysore Ganesh
- Adam Bailey
- Frank Enendu

## Summary
Reviewed readiness for the move to the 5% split and Spain go-live. Juan is fixing client-side caching of variant data (12h) that could blend old and new experiments; fallback is switching on at 8pm when caches expire. Remaining Spain gap is locale-specific RTP in game metadata.

## Key Decisions
- Move to 5% today: target within 2-3 hours after backend + Remote Config release, worst case 8pm tonight (approval already given).
- Client-side variant cache to be cut to max 1 hour permanently.
- RTP gap for Spain may be shipped as-is if the fix takes too long (Sudhanva: small blast radius; RTP not used for personas).
- Scope: AL1 is the agreed scope; advanced search and contextual bandits are next; everything else is AL2 and needs time/budget/priority discussion with Al.

## Action Items
- [ ] Juan: backend release removing 12h client cache, then Remote Config release to force clients out of cache state
- [ ] Juan: assess RTP locale-override work and tell Sudhanva the API response shape (Spain vs UK RTP)
- [ ] Sudhanva: handle Spain/UK RTP on his side or decide to go without
- [ ] Adam: Thunderbird ticket for RTP; flag next-sprint capacity clash (Win Boost target 12 Oct); discuss refinement sessions with Stuart
- [ ] Adam: advanced search discovery estimates by next week (catch-up with Tomasz Monday)
- [ ] Sudhanva: R&D on personalised sections, then tickets/handover (Serhii may pick up)
- [ ] Marcos: follow up on Spain privacy confirmation

## Notes
- Worst case 0.9% extra users briefly in treatment for 12h at the 5% switch.
- Max exposure also differs for Spain but is not needed for AL (impacts Vitruvian).
- Compliance (call 30 Sep) had no blockers beyond the privacy question.
- Semantic search and other 2.0 items unlikely before year end.
