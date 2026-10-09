---
project: Game Experience Profile
type: ballys-project
priority: P0
status: In rework post-review — presenting to Product/Tech leadership
criticality: High
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/Game Experience
production_url: https://main.d2igua90qmin6r.amplifyapp.com/
intended_domain: https://gameexperienceprofile.ballys.tech
gitlab_issues: "#11, #12"
due_date:
pit_sso: suspended
pit_dns: suspended
pit_cert: suspended
last_updated: 2026-10-05
---

# Game Experience Profile

> ⚠️ **Refreshed 2026-09-28** by the weekly backlog review from the 23 Sep "Game Exp Pipeline Update" meeting. The Al review that had been listed as pending/silent since April finally happened this week — Frank presented, Al gave a verdict. Frank was not present to confirm this reconciliation; ticks are evidence-backed but unverified. Priority/criticality raised (Low → High) because this now feeds Adaptive Layouts and is going in front of Product/Tech leadership. Correct anything wrong at the next live review. Due date cleared — the April 16 date was five months stale; no new date confirmed yet beyond "next week" for the leadership presentation (as of 23 Sep).

> ⚠️ **Refreshed 2026-10-05** from the 30 Sep (Adam Bailey) and 1 Oct (Shannon Gavin) rubric-validation calls. Frank not present to confirm; unverified.

## Overview
AI agent that watches gameplay video and extracts rich semantic experience profiles — internally called the "Game DNA" pipeline. A Fargate capture agent (Chromium + FFmpeg) records real game sessions to S3 with metadata in DynamoDB; an AI agent combines video analysis with Databricks maths data to synthesise a DNA profile, gated by QA checks at both capture and profile stages, emitted as a vector DNA profile plus a text JSON blob. Feeds Adaptive Layouts (automatic/dynamic lobby rows) and adds user-behaviour information to the clustering.

## Status
- **23 Sep review verdict (Al):** ~80% there — strong on architecture, diagrams and UI. Pushback on two rubric dimensions ("mechanics", "tempo"/"spin rhythm") and on numeric scores inside embeddings ("really problematic" — descriptive words group better for row generation).
- **Capture progress:** ~330 of ~3,000 games in the catalogue captured (~11%); selection currently random and needs to switch to popularity-ordered.
- **Cost:** ~$0.21/game for the full pipeline; regenerating the ~300 existing profiles is cheap since video is already captured.
- **Error analysis:** consolidating onto the one shared error-analysis tool rather than maintaining a separate eval UI (see `error-analysis.md`) — Frank's eval output feeds it via API.
- **Next:** Frank presents the pipeline to Product and Technology leadership (targeted the week of 23 Sep, per that meeting — exact date unconfirmed).
- **PIT Status:** DNS, cert, SSO all still suspended — using basic admin auth.
- **In Use:** Yes (internal prototype).

## Rubric Validation (30 Sep / 1 Oct 2026)
- Adam: spin cycle UKGC-regulated (min 2.5s) — tempo should capture spin rhythm/feedback timing; avoid "fast-paced" player labels (compliance risk), use neutral naming and check with compliance. Metadata shows tags only, never numeric breakdown.
- Shannon: add anticipation, perceived persistence, readability, reasons-to-continue; add intensity flag for safer-gambling review; don't score bonus payout from video; raise min recording from 40 to 80 spins, record 5–10 spins after a feature; win-celebration vs stake rule.

## Tech Stack
- Python 3.13+, Google ADK, LiteLLM, Gemini 3 Flash, Pydantic, uv
- Web scraping: slotcatalog.com, olbg.com
- Video: YouTube Data API; capture: AWS Fargate, Chromium, FFmpeg, S3, DynamoDB
- Embeddings: Vector DB for similarity search
- Maths/clustering: Databricks (existing 14-cluster model)

## Key Decisions (23 Sep 2026 — Pipeline Review)
- Drop numeric scores from the DNA profile and its embedding; descriptive words only
- "Mechanics" rejected as currently defined; "tempo"/"spin rhythm" needs reframing from audio/visual signals, not spin timing (spin cycles are ~2.5s by design, so timing alone doesn't discriminate). Rewards/volatility feel, reward pattern, metagame and session narrative accepted as-is
- Game selection to be popularity-ordered, not random sampling
- Spin count (currently a fixed 40, chosen from 6–8 manual runs) must be derived from Databricks average/median session-length data instead
- One error-analysis system only — Frank's eval output feeds the shared tool via API rather than maintaining a second UI
- Parallelisation to be done in-house by Frank (20–30 concurrent capture containers), not by Juan's engineers
- Frank presents the pipeline to Product and Technology leadership next

## Milestones
- [x] Core agent built with Google ADK
- [x] Web scraping pipeline (slotcatalog, olbg)
- [x] YouTube video analysis working
- [x] Vector embeddings and similarity search
- [x] Decompress dimensions from 9 to 5/6 (#11) ✅ 2026-04-22
- [x] Run full game catalogue — Sunny's list (#12) ✅ 2026-04-22
- [x] Al review — verdict ~80% there, architecture/UI strong, two rubric dimensions and numeric-score embeddings need rework (2026-09-23)
- [x] Rubric validation call with Adam Bailey (2026-09-30)
- [x] Rubric validation call with Shannon Gavin (2026-10-01)
- [ ] Refine tempo definitions (spin rhythm, feedback timing, session flow) + anticipation; compliance check on naming
- [ ] Add perceived persistence, readability, reasons-to-continue + intensity flag to rubrics
- [ ] Bump spin target to 80 + record 5–10 spins after a feature; capture win size vs stake via maths metadata
- [ ] Add SOP for big vs small wins/bonuses
- [ ] Sort Adam's access to the Game DNA page
- [ ] Trigger from Game Ops (e.g. SharePoint) on game updates to re-record/regenerate DNA
- [ ] Build golden dataset with reviewer scores in error-analysis tool
- [ ] Find more slot-expertise reviewers (Al, Craig, others)
- [ ] Drop numeric scores from the DNA profile, its embedding, the QA gate, and the eval UI
- [ ] Rework "mechanics" and "tempo"/"spin rhythm" dimensions and resubmit (consider reinstating the earlier "screen pressure" concept)
- [ ] Switch game selection to popularity-ordered rather than random sampling
- [ ] Derive spin count from Databricks average/median session-length data (pull the data first)
- [ ] Migrate the eval/tagging UI into the shared error-analysis tool, or submit output via its API
- [ ] Confirm the shared error-analysis tool exposes the API methods needed, incl. managing Frank's own data source
- [ ] Modify the error-analysis project page so captured video renders in the input-data pane
- [ ] Parallelise capture — scale from ~330 toward ~3,000 games via 20–30 concurrent containers
- [ ] Get Tableau access working (broken back token — Frank emailing Georgia) to self-serve game performance data
- [ ] Run a ~1hr group review session (6–7 people) walking input/output traces, as done for Adaptive Layouts
- [ ] Build a golden dataset from clustered errors to improve prompts
- [ ] Revisit whether to rerun the clustering model (still the original 14-cluster model)
- [ ] Productionise the REST API layer for Adaptive Layouts to consume
- [ ] Present the pipeline to Product and Technology leadership
- [ ] Al to review the profile dimensions with Dez and/or an external slots expert, then report back to Frank
- [ ] Al to go through Frank's code and return a list of atomic changes (mechanics, tempo)
- [ ] DNS: gameexperienceprofile.ballys.tech (suspended — using basic admin auth for now)
- [ ] SSL certificate (suspended)
- [ ] SSO configuration (suspended)
- [ ] Production deployment and handoff

## Sources
- [2026-04-16 — Game Experience Tech Talk](../meetings/2026-04-16-game-experience-tech-talk.md)
- [2026-09-23 — Game Exp Pipeline Update](../meetings/2026-09-23-game-exp-pipeline-update.md)
- [2026-09-23 — R&D Stand up](../meetings/2026-09-23-rd-stand-up.md)
- [2026-09-25 — R&D Stand up](../meetings/2026-09-25-rd-stand-up.md)
- [2026-09-30 — Rubric validation (Adam Bailey)](../meetings/2026-09-30-game-dna-rubric-validation-adam-bailey.md)
- [2026-10-01 — Rubric validation (Shannon Gavin)](../meetings/2026-10-01-game-dna-rubric-validation-shannon-gavin.md)
