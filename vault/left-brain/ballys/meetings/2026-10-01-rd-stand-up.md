---
type: meeting-note
title: "R&D - Stand up"
date: 2026-10-01
project: "General AI R&D"
attendees: "Frank Enendu, Sudhanva Mysore Ganesh"
source: teams-transcript
---

# R&D - Stand up — 2026-10-01

## Attendees
- Frank Enendu
- Sudhanva Mysore Ganesh

## Summary
Short stand-up (others did not join; office Wi-Fi was down). Frank walked Sudhanva through his AWS migration idea: one command run against a codebase that generates a merge request to the infra repo to move a project onto standard AWS resources. Sudhanva will review and give feedback.

## Key Decisions
- Scope the tool to simple deployments (e.g. AI transformation projects), not bigger pipelines such as Adaptive Layouts or Game Experience.
- Meeting cancelled early due to office Wi-Fi outage.

## Action Items
- [ ] Sudhanva: review Frank's AWS migration package and reply
- [ ] Sudhanva: test it on his demo app
- [ ] Frank: test on a couple more projects, then share with the team
- [ ] Frank: add a "grill me" style skill so new projects gather requirements before Terraform is generated
- [ ] Sudhanva: tag relevant people on the work

## Notes
- Sudhanva: API Gateway not needed for every app (single route); Lambda URLs can expose a Lambda directly.
- Tool should understand what the codebase needs rather than create resources blindly.
