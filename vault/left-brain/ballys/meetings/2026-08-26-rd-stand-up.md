---
type: meeting-note
title: "R&D - Stand up"
date: 2026-08-26
project: "General AI R&D"
attendees: "Al Jepps, Marcos Michel, Frank Enendu, Sudhanva Mysore Ganesh"
source: teams-transcript
---

# R&D - Stand up — 2026-08-26

## Attendees
- Al Jepps (speaker attribution inferred — transcript labelled this speaker as unnamed)
- Marcos Michel
- Frank Enendu
- Sudhanva Mysore Ganesh (invited)

## Summary
Al covered the iGaming revamp, the new Massachusetts retail-terminals/instant-games capability, and a new internal Teams channel intended both as a leadership broadcast and a showcase/community space. Frank is preparing for the NCR session tomorrow and wants to publish an official architecture diagram for the Game Experience Agent; Al directed him to the standard C4 approach via PlantUML. Hackathon platform work is largely done, with E2E testing agent coverage added around review and judging.

## Key Decisions
- Game Experience Agent architecture must follow the house C4 standard: system context diagram, container diagram, plus sequence diagrams for important flows — produced with PlantUML (Docker container / PlantUML server).
- Hackathon judging will be run as a separate session, not at the end of the event day (last time it was too draining).
- The new Teams channel is internal only; a separate mechanism already exists for C-level comms.
- Two separate workshop tracks are acceptable if one workshop would be too large for the group.

## Action Items
- [ ] Frank — prepare for NCR tomorrow (top priority)
- [ ] Frank — produce C4 system + container + sequence diagrams for the Game Experience Agent using PlantUML
- [ ] Frank — think about what automation could be built into the new iGaming/showcase Teams channel
- [ ] Frank — talk to Sudhanva about the workshop: whether he joins, contributes to Frank's material, or runs his own
- [ ] Al/Frank — find workable dates for the workshop around existing deadlines
- [ ] Al — finish building out the iGaming "home" site previously demoed

## Notes
- iGaming console/hub is being revamped and rolled out across both apps and the wider business; includes automation work. Sizeable R&D workload in this space.
- Massachusetts project: new capability for retail terminals with instant games — brand new for the team. Al built a delivery-oriented site for it with a coding-agent + form interface that lets non-developers update content without touching code.
- Skills / field notes work demoed yesterday is working and will be pushed out to the rest of game engineering.
- New channel serves two purposes: leadership broadcast ("we don't do that very well") and community/showcase — explicitly called out as a good canvas for Frank's weekly output.
- Hackathon platform: E2E testing agent set up two days ago to exercise every feature, especially review and judging, to avoid surprises on the day. Josephine contributed work on judging, reviewed by Frank.
- Craig has flagged that Al is moving too fast; Al's position is that Craig should keep pace.
