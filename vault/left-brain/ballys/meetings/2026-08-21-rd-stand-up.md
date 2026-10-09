---
type: meeting-note
title: "R&D - Stand up"
date: 2026-08-21
project: "General AI R&D"
attendees: "Marcos Michel, Al Jepps, Sudhanva Mysore Ganesh, Frank Enendu"
source: teams-transcript
---

# R&D - Stand up — 2026-08-21

## Attendees
- Marcos Michel
- Al Jepps
- Sudhanva Mysore Ganesh (Sunny)
- Frank Enendu

## Summary
Adaptive Layouts pipeline was unblocked — Sunny fixed two bugs and a schema/data mismatch, getting the full end-to-end pipeline working with offline and online evals. Discussion turned into frustration with Nightwatch's contribution to the delivery chain, and Al raised the AI tooling budget for this year and next. Frank reported progress on the interview platform (auth and deployment).

## Key Decisions
- Nightwatch's role in the Adaptive Layouts chain to be reviewed with John after launch, treated as a "phase two" improvement rather than acted on now.
- Group calibration session format (everyone reviewing together) worked well and will be reused for future calibration rounds.
- AI tooling budget direction: retire Cursor, put budget against OpenRouter, run a large Codex trial, move low-token users to AI Gateway (~£8K net increase for rest of year).

## Action Items
- [ ] Sunny — make full staging pipeline green end-to-end (call with Seth today)
- [ ] Sunny — drive Adaptive Layouts deployment to production; don't wait on Nightwatch
- [ ] Sunny — process ~82 reviews, calibrate the LLM, create production golden dataset and thresholds, sign off with Al then Product
- [ ] Sunny — review Al's AI tooling budget
- [ ] Frank — switch endpoint from Web to SPA, finish auth, deploy interview platform and share the link
- [ ] Frank — send/commit the second Jack interview transcript to the repo (the shared one is only 6 minutes)
- [ ] Al — raise Nightwatch value question with John when he's back from holiday

## Notes
- Adaptive Layouts: two small bugs and basic schema mismatches fixed; full pipeline working end to end with offline and online evals. Context, a report and change documentation handed to Seth — staging only needs environment variables added.
- Friction with Nightwatch: Sunny's merge request sat for a week with no flagged issues, then Seth reported nothing was green. Al questioned what value Nightwatch adds when Sunny has done ~90% of the work. Marcos noted mitigating context — Stefan and Billy left and the team was merged into Thunderbird, so there's readjustment.
- Marcos said the sprint finishes Wednesday with dev done by then so end-to-end testing can start; Al pushed back that no dev is outstanding — it's just a prod deployment.
- Calibration: ~82 reviews collected across observations and calibration dataset.
- Sunny has started looking at portfolio optimization and the CR.
- Al considers Codex the strongest model right now and thinks the function is sleeping on it.
- Marcos posted another interview transcript to the chat; more interviews scheduled.
