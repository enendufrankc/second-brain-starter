---
type: meeting-note
title: "R&D - Stand up"
date: 2026-08-24
project: "General AI R&D"
attendees: "Marcos Michel, Al Jepps, Sudhanva Mysore Ganesh, Frank Enendu"
source: teams-transcript
---

# R&D - Stand up — 2026-08-24

## Attendees
- Marcos Michel
- Al Jepps
- Sudhanva Mysore Ganesh (Sunny)
- Frank Enendu

## Summary
The team agreed to launch Adaptive Layouts to a smaller cohort than the planned 5% and feather users in as confidence grows. Sunny reported staging nearly green with prod deployment targeted for tomorrow. Al revealed he built a session-analysis tool over the weekend that infers AI maturity from a user's Codex/Claude sessions, which could scale the AI-usage assessment beyond manual interviews, and Frank demoed the interview platform.

## Key Decisions
- Adaptive Layouts will launch to a cohort smaller than 5% (~1–2%) and be feathered in quickly if no issues. Framed externally as "tuning" rather than a reduction.
- Transformation meetings are cancelled for now until the format is reworked — Al is doing 90–95% of the work and that has to change.
- Grace workshop / hackathon dates likely to slip by about a week as current dates are too tight.
- Big rocks meeting has moved back a few weeks, freeing up time.

## Action Items
- [ ] Al — find out whether a release ticket is needed each time the Adaptive Layouts cohort is increased (ask Stefan, John is away)
- [ ] Sunny — finish staging run by end of today; deploy to prod and do a first dry run tomorrow
- [ ] Sunny — configure remaining S3 setup; finish LLM calibration and feed into staging
- [ ] Sunny — progress portfolio optimization for the NCR double bill (session Thursday)
- [ ] Al — share the session-analysis skill/tool with the team
- [ ] Frank — finish the interview engine and send out for testing this morning
- [ ] Frank — review Al's training site and feed back on structure, gaps and measurement
- [ ] Frank — make sure the hackathon platform and workshop resources are ready before annual leave next week
- [ ] Frank — prep for the NCR
- [ ] Open question — confirm whether the session-analysis approach works for Claude Desktop / Cowork users, not just Claude Code and Codex

## Notes
- Rollout maths: ~700k UK players across ventures, but Adaptive Layouts targets only those active in the last three months, so 5% is roughly 3.5–4k players. Marcos and Al both preferred starting smaller.
- Marcos is back for launch week; everything needs to be ready while he's away. Both Frank and Marcos are on leave next week, and Monday is a UK bank holiday, so stand-ups continue with just Sunny.
- Al wants a set of experiments to run off the back of launch — he isn't convinced the current clustering-then-LLM approach is the final design.
- Al's weekend build: reads a user's Codex/Claude sessions from the last two weeks, synthesises them, and sends to an API endpoint that reasons about setup sophistication. Includes cryptographic measures (hashing input data, output and prompts against a key from the API) so payloads can't be faked from the user's own machine. He tested it on himself and rated it accurate.
- Scale argument: ~250 engineers on Code plus ~80 product people; interview ~10% manually and cover the rest via the automated assessment. Frank noted most interviewees don't configure anything themselves — they just use Claude Desktop.
- Frank demoed the interview platform: audio conversation ran end to end via Siri, admins can create interviews from a dumped document which generates 20–30 topics to drive the conversation, then run analysis against the rubric (sufficient / insufficient evidence) and hand off to the field-note database (not yet connected).
- Rubric dimensions discussed: flow depth, quality, trust in generated output, exploration, edge shift (organisational role boundaries, inner sourcing), and friction — producing an overall maturity metric.
- Al's training site is well fleshed out now, with a topic/skill directory, measurement (subjective feedback plus objective counts of courses and articles launched) and an FAQ. He deep-linked Frank's content rather than duplicating it, and is open to a different approach.
