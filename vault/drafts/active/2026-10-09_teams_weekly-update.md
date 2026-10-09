---
type: draft
channel: teams
target: AI Interlock Team
created: 2026-10-09
status: for Frank to review and paste
format_source: Al Jepps weekly update ("Shipped this week" / "In flight")
---

**Weekly Update — Frank**
Week commencing 6 October 2026

**Shipped this week**

- **Game DNA (Game Experience Profile).** Capture rubric v2 handoff merged (!101, !107). Gemini schema fix merged (!96). Re-profiling pipeline running — games being re-scored against the v2 rubric. Words-first branch (`feat/dna-words-first`) ready for review at d6c2508.
- **rd-init toolkit.** Access gate removed: `rd-init` is now `access: open` in the Skills Repo and the catalogue reads "Open to everyone" (uncommitted — will push today). Confirmed rd-init can go Internal in GitLab without moving repos (parent group is already public).
- **Casino Simulator research page.** Published to internal-share via MR !137 (merged 7 Oct). Live at https://internal-share.ai.ballys.tech/casino-simulator/ — includes prototype, Story Mode tab, and a 72-second explainer film.
- **R&D Comms strategy + video.** Built the "Comms Desk" concept and produced a 72s overview film (10 scenes, 1080p) pushed to share-ai-ballys. Awaiting merge to main to go live on internal-share.
- **AI Radar access guide.** MR !90 merged (28 Sep) — answers to open questions on how to get Codex, Claude, Jira & Confluence access, plus Opik and Error Analysis links.
- **iGaming Q4 Hackathon 2026.** Created the event on hackathon.ballys.com with all 9 suggested themes, Open Theme track, 6 challenges/bounties, and the 25/25/20/20/10 scoring rubric. Dates manually set by Frank.
- **Interview Engine / AI Field Notes.** Created 6 UX handoff issues in the survey repo (#15–#20) — consolidated study, participant navigation, data governance. MR !54 merged and deployed.
- **Bally's Prototyping Platform.** Completed full codebase review; agreed with Frank to pivot to open-source, self-hostable model with optional GitLab collaboration. Plan in progress.
- **Tech Constellation.** Dev environment live and verified at https://constellation-dev.ai.ballys.tech — all health checks passing.
- **Wunder Machine.** AGENTS.md contributed; built a minimal game UI to reverse-engineer the framework architecture; identified 3 Jokers Plus game as a reference.
- **Sports Product Studio.** CloudFront migration completed — sportstudio.ai.ballys.tech now served by own distribution with valid TLS, 0 placeholders, S3+OAC origin.
- **Second Brain (personal).** Committed and pushed the full proactive system (hooks, scripts, skills, launchd plists, memory search, morning brief, AI news crawler, MCP connector). Morning brief delivering daily to self-chat.

**In flight**

- **Game DNA rework** from Al's 23 Sep review: numeric scores out of embeddings, mechanics/tempo dimensions rebuilt, popularity-ordered game selection. Ahead of Product + Tech leadership presentation.
- **AI Planner #4/#5/#6 (Marcos).** Cage integration into the planner: #4 (can vpc00 reach Databricks EU prod?), #5 (service principal + SSM), #6 (S3 snapshot infra). Due 9 Oct; #4 and #5 need infra-team input.
- **Adaptive Layouts.** 5% UK step went live 1 Oct; Spain starting at 5% (~end Oct). Budget flag from Marcos still open. Three launch items still unticked (game ordering, Programme Analytics, MFE).
- **Game Ideation Agent.** Vision board live; 3 MRs merged, 4th in flight. NCR estimate drafted (30 rows, 7 features). Progress posted to AI Radar.
- **NCR costing** for Portfolio Optimisation + Game Ideation with Sunny — still owed to Marcos.
- **Atlas.** Planner estimate workbook rebuilt against Game Testing + RTS northstar. Discovery not yet started (5+ weeks since sizing).
- **R&D product-vending session** with Al and Serhii — targeting Fri 16 Oct.
- **Serhii onboarding.** Engineering loop scope and GitLab AI R&D group access in progress; weekly informal Friday catch-ups started.

**Blocked / needs decision**

- **GitLab queue (#42, #13, #33, #35)** — all overdue 100+ days, untouched 5+ Monday reviews. Need to re-date to Q4 or close.
- **Juan Impey's GitLab iGaming access** — outstanding since 2 Oct, Frank is the approver.
- **task-tracker CI** — `pages` job failing nightly since 15 Jun (dead runner tag, stuck_or_timeout_failure).
