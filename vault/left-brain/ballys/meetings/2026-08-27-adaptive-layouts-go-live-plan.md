---
type: meeting-note
title: "Adaptive Layouts - GO live plan"
date: 2026-08-27
project: "Adaptive Layouts"
attendees: "Marcos Michel, Salvatore DeCicco, Adam Bailey, Kyriacos Kyriacou, Christopher Syder, Dominik Babin, Freddie Watford, Ryan Marshall, Sudhanva Mysore Ganesh"
source: teams-transcript
---

# Adaptive Layouts - GO live plan — 2026-08-27

## Attendees
- Marcos Michel (chair)
- Salvatore DeCicco (Sol)
- Adam Bailey
- Kyriacos Kyriacou (KK)
- Christopher Syder
- Dominik Babin
- Freddie Watford
- Ryan Marshall
- Sudhanva Mysore Ganesh (Sunny)

## Summary
Workstream check-in two weeks out from the estimated 9 September iGaming MVP launch. Web tracking is in a comfortable place but native tracking remains the main risk, with Sol flagging the timeline as tight and no dashboarding work started yet. Pipeline issues introduced last week have been fixed in staging but production work remains, so end-to-end testing has slipped from today to next week — during which Marcos is on leave and Adam is covering.

## Key Decisions
- Data-usage-for-personalisation sign-off stays unticked until next week pending Privacy's response to Adam's form.
- End-to-end testing in UAT moves to next week (Monday is a bank holiday); Adam will confirm whether the launch date holds.
- Adam, not Marcos, will chase native/Thunderbird progress next week since Marcos is on leave.
- Privacy confirmed the initiative is low risk with no privacy actions required.

## Action Items
- [ ] Salvatore DeCicco — finalise native event payload testing, targeting next week
- [ ] Salvatore DeCicco — confirm with the group whether web-only reporting at launch is acceptable or web+native must be aligned from day one
- [ ] Salvatore DeCicco — start dashboarding once event testing completes
- [ ] Adam Bailey — chase Privacy on the outstanding data-usage form
- [ ] Adam Bailey — chase Harriet on native tracking once Thunderbird's piece is complete (native is dependent on Thunderbird)
- [ ] Adam Bailey — run the back office tool handover session on Wednesday next week; invite Sonny and anyone else who requests it
- [ ] Adam Bailey — schedule the dev tools session for anyone joining UAT testing
- [ ] Adam Bailey — confirm next week whether the 9 September date is safe
- [ ] Kyriacos Kyriacou — continue metadata clean-up, currently ~20,000 of ~35,000 entries validated
- [ ] Freddie Watford — add tags to the newly built carousels once the new app lands
- [ ] Freddie Watford + Ryan Marshall — align on final guard rails after the back office handover

## Notes
- Web tracking approach agreed and comfortable; native still being ironed out. Most native data actually comes from MFE, so the native layer itself has little to do.
- Sol's native contacts: Harriet Cole, plus Shane/Jake/Alex across MFE and Thunderbird.
- Sol mildly worried about the two-week timeline — it is not his team's only workstream.
- Christopher Syder: ready to go, no blockers, no concerns.
- Product ops and marketing both blocked on back office tool access; handover session now booked for Wednesday.
- Compliance: no outstanding concerns from Dominik. Privacy confirmed low risk.
- Metadata quality materially improved: Contentful entries being cross-checked against AI-extracted supplier portals, docs and game sheets. Green matches give confidence; mismatches are being fixed.
- Historic data bug found — a script inserted "1" into gaps, producing games with symbol counts or max prizes of 1. Being cleaned up. Completeness heading towards 60%.
- KK confident on the two-week runway (had thought only one week remained).
- Last week's quality-improvement changes broke the pipeline; all fixed in staging, production work outstanding, so end-to-end testing has not started.
- Marcos on leave next week; Adam covering.
