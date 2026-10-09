---
type: meeting-note
title: "Game Exp Pipeline Update"
date: 2026-09-23
project: "Game Experience Profile"
attendees: "Frank Enendu, Al Jepps, Sudhanva Mysore Ganesh"
source: teams-transcript
---

# Game Exp Pipeline Update — 2026-09-23

## Attendees
- Frank Enendu (presenting)
- Al Jepps
- Sudhanva Mysore Ganesh (Sonny)

## Summary
Frank walked through the current Game Experience / "Game DNA" pipeline: a Fargate capture agent running Chromium plus FFmpeg to record real game sessions to S3, then an AI agent combining video analysis with Databricks maths data to produce a DNA profile, gated by QA checks at capture and profile stages. Al's verdict was roughly 80% there — strong on architecture, diagrams and UI — but he pushed back on two rubric dimensions, on numeric scores in embeddings, and on parameters not grounded in data. The group also agreed there will be one error analysis system, not two.

## Key Decisions
- Drop numeric scores from the DNA profile and embedding; use descriptive words only
- "Mechanics" rejected as currently defined; "tempo"/"spin rhythm" needs reframing — tempo should come from audio/visual, not spin timing. Rewards/volatility feel, reward pattern, metagame and session narrative accepted
- Game selection to be popularity-ordered, not random sampling from the catalogue
- Spin count (currently 40) must be derived from Databricks average/median session data
- One error analysis system only. Frank's eval output feeds the shared error analysis tool via API; the shared tool stays project-agnostic and API-first, and Frank can keep his own UI on top
- Parallelisation done in-house by Frank rather than waiting on Juan's engineers
- Frank presents the pipeline to Product and Technology leadership next week

## Action Items
- [ ] Sudhanva: Send Frank the ~150-game list used for adaptive layouts testing
- [ ] Frank: Use that list as the starting capture set
- [ ] Frank: Get access to the Tableau game performance dashboards and self-serve via Tableau MCP rather than asking game ops
- [ ] Frank: Pull average/median session length per game from Databricks to justify spin count
- [ ] Frank: Rework the mechanics and tempo dimensions and resubmit; consider reinstating the earlier "screen pressure" concept
- [ ] Al Jepps: Review the profile dimensions with Dez and/or an external slots expert, then come back to Frank
- [ ] Al Jepps: Go through Frank's code tonight and return a list of atomic changes (mechanics and tempo)
- [ ] Frank: Strip numeric scores from the profile, QA gate and eval UI
- [ ] Frank: Migrate the eval/tagging UI into the shared error analysis tool, or submit output via its API
- [ ] Frank/Sonny: Confirm the error analysis tool exposes the API methods Frank needs, including managing his own data source
- [ ] Sonny/Frank: Modify the error analysis project page so captured video renders in the input-data pane
- [ ] Frank: Run a ~1 hour group review session with 6–7 people walking input/output traces, as done for adaptive layouts
- [ ] Frank: Parallelise capture — 20–30 concurrent containers to scale from ~300 toward ~3,000 games
- [ ] Frank: Productionise the REST API layer for adaptive layouts to consume
- [ ] Frank: Build the golden dataset from clustered errors to improve prompts
- [ ] Frank: Revisit whether to rerun the clustering model (still the original 14-cluster model)

## Notes
**Capture status** — ~330 games captured against a catalogue of roughly 3,000; selection currently random, which is the main thing to change.

**Architecture** — Databricks maths and game titles feed a script that builds the game URL; Fargate spins up Chromium plus FFmpeg, records, stores video in S3 with metadata in DynamoDB. Capture runs in two stages (preliminaries: login and funding; then reaching a spinnable game page) with a Gemini-based watcher agent per step, since most failures happen at the spinnable-page stage.

**Capture routine** — Open and scroll the pay table, then at least 40 spins. The 40 came from 6–8 manual runs looking for wins, bonuses and feature coverage; Al accepted the rubric as adequate if the method is defensible, but wants the number data-derived.

**QA gates** — A capture gate (right game, right frame, pay table present) and a main gate before profile embedding. Failures flagged in DynamoDB for later error analysis.

**Profile generation** — One agent with multiple tools (video analysis on the S3 clip, maths tool on the Databricks catalogue), output synthesised, QA-gated, then emitted as both a vector DNA profile and a text JSON blob. Maths clustering uses the existing 14-cluster model; cluster membership doubles as a QA check and a maths-based similarity signal.

**Rubric contention** — Al questioned what a player would actually perceive from "spin rhythm", "win character" and "mechanics", noting spin cycles are all around 2.5s by design. Numbers inside embeddings were called "really problematic"; descriptive words group better for adaptive-layout row generation.

**Downstream** — The DNA feeds adaptive layouts, enabling automatic and dynamic lobby rows, and adds user-behaviour information to the clusters.

**Cost** — Approximately 21 cents per game for the full pipeline; regenerating the ~300 existing profiles is cheap as the videos are already captured.
