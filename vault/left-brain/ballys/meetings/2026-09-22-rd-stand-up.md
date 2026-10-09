---
type: meeting-note
title: "R&D - Stand up"
date: 2026-09-22
project: "General AI R&D"
attendees: "Al Jepps, Frank Enendu, Sudhanva Mysore Ganesh, Marcos Michel"
source: teams-transcript
---

# R&D - Stand up — 2026-09-22

## Attendees
- Al Jepps
- Frank Enendu
- Sudhanva Mysore Ganesh (Sonny)
- Marcos Michel

## Summary
Stand-up covered the personalised-sections proposal for Adaptive Layouts, extending the pipeline to Spain, and a long debate about R&D comms channels now that the ai@ballys.com shared mailbox exists. Al also passed on asks from the DevEx session at TLT, including a "starter pack" of skills for engineers.

## Key Decisions
- Start the personalised-sections work without promotions; promotions stay fixed until a normalisation approach for banner/promo click-through data is found
- Working principle: anything that can go in the recommendation engine goes in, unless explicitly told otherwise
- No new models for Spain — reuse the UK classification model, differentiate only via Contentful concept tags
- Use the existing R&D Teams channel (already wired to the R&D loop) rather than a new one; run both a support channel and a broadcast channel/email digest and instrument which gets traction
- Error analysis session with the Intralot people to be booked in by Friday, and advertised in AI Vibes

## Action Items
- [ ] Al Jepps: Follow up with marketing on what click-through data exists for promotions/banners
- [ ] Al Jepps: Package contextual bandits work for AWS, pairing Sonny with their ML team
- [ ] Sudhanva: Talk to the Ops team about Spain vs UK section overlap and concept tags
- [ ] Sudhanva: Run the pipeline over Spain users, partition and check cluster distribution
- [ ] Sudhanva: Regenerate and send Frank the list of minimum games required for game experience metadata
- [ ] Frank: Check whether a "starter pack" of 5–10 skills for engineers already exists; if so package and signpost it on the R&D site
- [ ] Frank: Send Sonny details of the ai@ballys.com shared mailbox and how to add it in Outlook
- [ ] Frank: Use the existing AI R&D channel rather than the one he created
- [ ] Frank: Run error analysis on the Game Experience Profile output; deploy Owen's project
- [ ] Marcos: Raise a ticket with Enterprise IT about the M365 connector disconnecting (cc Bartek)
- [ ] Al Jepps: Get the Intralot error analysis session in the diary by Friday
- [ ] All: Outstanding AI field notes owed — two each
- [ ] Frank: Re-source candidates after two interview no-shows (mobile native engineer, product)

## Notes
**Personalised sections** — Sonny reviewed Al's proposal and rated it a good first approach that avoids changing the core of Adaptive Layouts. He sees it as a step toward contextual bandits, though at t−1 rather than real time. Open question is how to treat promotions in the same context as games; marketing data may not support it, and promotions may have to stay fixed anyway.

**Spain rollout** — Pipeline expected to be near-identical to UK. Only real variable is how Ops handle concept tags and whether Spain sections overlap with UK ones. Al pushed hard on not over-engineering it.

**Game experience metadata** — Sonny confirmed the pipeline is modular; the games-metadata module can simply be swapped for game experience metadata. The experiment worth running is where to inject it into the user behaviour clusters, since it adds dimensionality beyond the current "top three games played" column.

**Comms** — ai@ballys.com now exists (needs adding as a second mailbox in Outlook, which isn't obvious). Al wants a broadcast surface for R&D output, arguing the team ships far more than it communicates. Frank and Marcos argued for a DevOps-style support channel so requests are visible rather than landing in DMs. Landed on doing both plus possibly forwarding channel messages to the AI Intralot inbox.

**DevEx findings** — Al's read is that most gaps are awareness, not capability: things already exist but nobody knows. Signposting and comms are the fix.
