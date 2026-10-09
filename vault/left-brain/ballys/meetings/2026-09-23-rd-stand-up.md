---
type: meeting-note
title: "R&D - Stand up"
date: 2026-09-23
project: "General AI R&D"
attendees: "Al Jepps, Frank Enendu, Sudhanva Mysore Ganesh, Marcos Michel"
source: teams-transcript
---

# R&D - Stand up — 2026-09-23

## Attendees
- Al Jepps
- Frank Enendu
- Sudhanva Mysore Ganesh (Sonny)
- Marcos Michel

## Summary
Round-the-table updates: Frank on error analysis and the new eval tab, Sonny on the Spain audit and benchmarking, Al on Serhii's start and a proposed software factory. Al also flagged a gap between R&D and the wider engineering teams that the software factory is meant to close.

## Key Decisions
- Serhii starts Monday and will pick up building a software factory as his embedding task
- Spain does not need separate clusters — existing clusters already contain Spain users; the fix is passing UK vs Spain provider information to the LLM re-ranker
- Personalised sections data work takes priority over model benchmarking
- Al will own the invite list for the Intralot error analysis session; Sonny runs it, early next week, as a demo rather than a polished product
- Adaptive Layouts mop-up session to be scheduled for next week

## Action Items
- [ ] Frank: Finish tweaks so traces fit the error analysis format
- [ ] Frank: Continue the eval tab and collect a golden dataset for prompt tuning
- [ ] Al Jepps: Email Serhii to introduce himself ahead of Monday
- [ ] Al Jepps: Put in the Adaptive Layouts mop-up session for next week
- [ ] Al Jepps: Send the invite for the Intralot error analysis session
- [ ] Al Jepps: Write up suggestions on the planner tool for Marcos, then book a session to compare with his plans
- [ ] Al Jepps: Find out from Mark who runs the payments team using AI heavily, and explore a showcase session
- [ ] Sudhanva: Finalise the Spain audit today and send the report to Al
- [ ] Sudhanva: Speak to Bessan about why the shared mailbox isn't showing in his account
- [ ] Sudhanva: Send the next draft of benchmarking info, and DM likely respondents on Teams directly
- [ ] Sudhanva: Pick up personalised-section data from Christopher and start experiments
- [ ] Marcos: Find out which payments team/PM is running AI-heavy delivery
- [ ] Frank & Sonny: Catch up later today on Serhii onboarding

## Notes
**Error analysis / eval** — Frank found only minor changes needed for his traces to fit the error analysis format. New eval tab added to the app, primarily to collect a golden dataset for later prompt adjustment.

**Software factory** — Came out of yesterday's planning. Al's framing: R&D is far ahead and the engineering teams are far behind, and a software factory is a good way to reset expectations about what's now possible and how quickly. Good embedding task for Serhii and useful for the teams.

**Spain audit** — Sonny confirmed Spain users are already inside the current clusters and no new clustering is required. The complication is that Ops content is provider-heavy, with some providers Spain-specific and some UK-specific, so AI-suggested rows can be dropped. Fix is to pass provider information per market into the final LLM re-ranker call rather than just filtering rows.

**Benchmarking** — No uptake so far on the benchmark request. Sonny will DM people who engaged with AI field notes since they've already shown interest. Opus 5.5 benchmarking was deprioritised in favour of personalised sections.

**Planner tool** — Al noted scheduling, prioritisation and slot filling are extremely well-trodden ML problems and wants Marcos to read a written-up proposal before deciding. Ambition is A/B/C planning scenarios with rationale attached.

**Payments team** — Marcos heard a payments engineering team is moving fast with AI; both agreed it's worth reaching out and possibly getting them to showcase to the gaming teams.
