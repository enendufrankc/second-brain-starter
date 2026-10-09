---
type: meeting-notes
title: AI R&D weekly update — 5 to 9 October 2026
source: teams
date: 2026-10-09
channel: AI Interlock Team
participants: [Frank Enendu, Al Jepps, Sudhanva Mysore Ganesh, Serhii Tupikin]
tags: [weekly-update, ai-rd]
timestamp: 2026-10-09
---

# AI R&D Weekly Update — 5 to 9 October 2026

> Team members' raw updates, position as of Friday morning 9 October.

## Sudhanva

- Initial report on hybrid personalization done.
- Continuing work on benchmarking tool on the 40 agents tasks collected.

## Frank

- **Game DNA.**
  - Rubric revision 3 merged and shown on the site.
  - Capture now judges a launch by the final page state.
  - Calibration review pack built from the 5 Oct review.
  - Words-first scoring fix built and reviewed, MR going up today.
  - 5 parallel capture agents built and deployed, go live tonight.
- **iGaming Q4 Hackathon.** Event set up on hackathon.ballys.com with nine themes and an Open track.

## Al — Adaptive Layouts & programme

- **Adaptive Layouts.** Latest rollout record reports an increase to 10% treatment and 10% control across UK ventures on 8 October. Commercial uplift remains to be established. Prepared the GenAI Sync deep dive, covering personalisation, operating costs, evaluation, A/B testing, and the proposed next phase with contextual bandits. Next: review the commercial results before agreeing further exposure, and finish and rehearse the deep dive.
- **Hybrid personalisation.** Completed three rounds of research into placing personal rows using each player's history. The report supports separate preferences for Recently Played and Because You Played; one combined score for all personal rows did not hold up. The latest offline ranking predicted the favourite row type for 70.5% of players, versus 43.6% for a common ordering. The check period was reused, so this needs fresh validation. Predicted lobby gains are model estimates; nothing has changed in the live lobby. Next: check the ranking on fresh data and agree a controlled live test.
- **AI Training.** Launched shared learning events: automatic discovery, list and calendar views, search and filters, calendar downloads, event creation and editing. Contributors can prefill an event from a web page, review details, and publish. Moved events into one shared store; live checks confirmed saved edits survive redeployment and discovery preserves manual corrections. Released shared primers for skills and readable public articles, with source links, automated content review, retained versions, feedback. The Error Analysis primer is live. Next: resolve the broad-discovery timeout, complete outstanding live ownership checks. Infographics, quick quizzes, broader interactive exercises in development.
- **Community and Radar event integration.** Built and tested a shared-events calendar for Community and a rotating "This week's events" panel for Radar. Both unreleased. Community is intended to be the main event-editing surface; its sign-in and editor still need implementation. Next: complete Community sign-in and editing, then review and release both integrations.
- **AWS collaboration.** Built out the AgentCore workshop environment: agent runtime, model gateway, tool registry, tool gateways. Stacks deployed; agent connections to shared gateways and some policy checks unfinished. Made the Q4 hackathon proposal available in the AWS collaboration area and prepared an availability email for the three locations (draft; dates and AWS involvement not confirmed). Next: finish workshop integrations and evaluation exercises, then agree hackathon dates.
- **Research discovery and adoption.** Improved the Research homepage: clearer purpose statement, keyboard navigation fixes, clearer Radar markers, corrected prototype links. Published the R&D adoption proposal, making promotion and Product uptake part of the work. Next: each team member selects three pieces of work and prepares a product card and short communication plan.
- **AI attribution.** Packaged and trialled the AI commit-attribution plugin, covering Codex commit co-authors and GitLab MR labels. Local installation and rollback passed; wider rollout and Linux validation outstanding. Next: validate in fresh developer sessions, complete Linux validation.
- **Intralot access.** Prepared the four-site VPN access pilot, allocated static addresses. Deployment awaits Intralot's routing change. Next: deploy and verify once Intralot confirms routes.

## Serhii

- Ran multiple SWE-bench experiments to evaluate Factory's implementation quality, independent QA, repair loops, worker skills, parallel execution. Compared Factory checks with official benchmark results and investigated disagreements.
- Improved verification reliability: corrected skipped-QA reporting, preserved attachment content, added regression comparisons, clearer failure states.
- Developed worker skills for repository assessment, task understanding, implementation, testing, delivery handoff.
- Added acceptance contracts and sourced context packets, including dashboard views for requirements, context, revision-controlled updates.
- Moved from separate Codex/Claude chat + browser dashboard toward one terminal interface using Toad: chat, project navigation, agent monitoring, diffs, results. Redesigned terminal experience with project overviews, developer/QA activity, runtime and token metrics, estimated costs. Updated Software Factory web interface and branding.
- Simplified installation/onboarding with make install, automatic startup, clearer setup errors, model/backend selection, updated docs.
- Researched next stage of autonomy: persistent objectives, planning, task delegation, integration, recovery, GitLab issue processing. Improving Factory autonomy and testing on more demanding tasks so it resolves issues without human feedback.

## Open items for Frank (from this update)

- Marcos's AI Planner #4/#5 due 9 Oct (Cage integration — not mentioned in this update).
- Juan Impey's GitLab access approval still outstanding.
- Weekly update posting to AI Interlock.
