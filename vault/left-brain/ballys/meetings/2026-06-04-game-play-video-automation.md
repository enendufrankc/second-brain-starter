---
type: meeting-note
title: "Game Play Video Automation"
date: 2026-06-04
project: "Game Experience Profile"
attendees: "Frank Enendu, Nathan Maddock"
source: teams-transcript
---

# Game Play Video Automation — 2026-06-04

## Attendees
- Frank Enendu
- Nathan Maddock

## Summary
Nathan walked Frank through the Harmon QA agent tool and demonstrated how to generate gameplay videos. The tool uses a "developer agent" that takes a game URL, credentials, and a test plan document to automate gameplay and record it as an MP4. Nathan shared the Confluence page with all live game links (by game slug) and offered to request access for Frank from the Harmon team.

## Key Decisions
- Use the **developer agent** (not the planner) for video generation — planner is unreliable for structured tasks
- Test plan document format: plain text instruction list (load game, set min coin size, spin 10 times, navigate help pages with 10s pauses, capture pay table)
- Game links follow a slug pattern; a Confluence page (maintained by Kaan) lists all live UK game URLs
- Audio capture is not yet available — a known limitation; escalate to Harmon team
- Bulk/concurrent testing is in development: currently 2 sessions max concurrently, but architecture is hardware-scalable
- Staging environment is preferred (no need to set minimum coin size, has unlimited test funds)

## Action Items
- [ ] Nathan: Request Frank's access to Harmon tool (reaching out to Harmon/Weepro team)
- [ ] Nathan: Send Frank the Confluence page with full live game URL list
- [ ] Nathan: Send Frank the completed test session videos once runs finish
- [ ] Frank: Replicate Nathan's demo steps independently to confirm workflow
- [ ] Frank: Ask Harmon team about audio capture fix timeline and bulk game processing
- [ ] Frank: Begin generating ~10 videos as initial batch while awaiting bulk processing feature

## Notes
- Harmon tool has two components: Planner (creates test plans — poor quality) and Developer Agent (executes tests — solid)
- Demo session ran on production using Khan's credentials (staging was down); in future use staging
- Test plan that worked well: load game fully → set lowest coin size → spin 10 times → click all help/how-to-play pages (10s between each) → capture pay table
- Multiple games can be fed via a document listing URLs; Harmon confirmed 2 concurrent sessions now, more when scaled
- Live games list: API endpoint exposed by Jon, turned into a PowerShell app by player experience team, updated by Kaan every couple of weeks → outputs full URL list by venture (UK + Spain)
- Same game across 6 UK brands shares the same software; only RTP/maths differ, gameplay is identical
- Frank initially scoping for Jackpot Joy only; Nathan's list will allow easy expansion to all brands
- Audio gap: Frank's plan is to start with silent videos and iterate once audio is fixed; won't block progress
