---
type: draft
channel: teams
target: AI Interlock Team
created: 2026-10-09
status: for Frank to review and paste
format_source: Frank's weekly update 2026-10-02 ("Shipped this week" / "In flight")
---

**Weekly Update — Frank**
Week commencing 5 October 2026

**Shipped this week**

- **Game DNA (Game Experience Profile).** Rubric revision 3 merged and live on the site. Capture now judges a launch by the final page state rather than intermediate events. Built the calibration review pack from Monday's review session. The words-first scoring fix is built and reviewed, MR going up today. Five parallel capture agents built and deployed — go live tonight.
- **iGaming Q4 Hackathon.** Event set up on hackathon.ballys.com with nine themes and an Open track, challenges and scoring rubric matching the vision board.
- **Casino simulator research page.** MR !137 merged — live on internal-share with the prototype, Story Mode tab and the 72-second explainer film.
- **AI Planner (Marcos, on leave).** Infra side of the Jira Cloud move done on dev and prod: planner-api and planner-api-dev now point at ballysgroup.atlassian.net with the new SSM parameters; Marcos notified we're done our part.
- **Interview Engine / AI Field Notes.** MR !54 merged and deployed. Raised the six outstanding UX handoff items as issues in the survey repo (#15 to #20) so someone else can pick them up.
- **Tech Constellation.** Dev environment live at https://constellation-dev.ai.ballys.tech with every health check passing.

**In flight**

- **Game DNA rework** from Al's 23 Sep review: numeric scores out of the embeddings, mechanics and tempo dimensions rebuilt, popularity-ordered game selection — ahead of the Product and Tech leadership presentation.
- **AI Planner #4 and #5** (Cage integration): confirming vpc00 Lambda reachability to Databricks EU prod, and getting a read-only Databricks service principal in place. Both due today.
- **rd-init.** Access gate removed in the Skills Repo (now open to everyone) — commit pending; confirmed it can go Internal in GitLab without moving repos.
- **Game Ideation + Portfolio Optimisation NCR costing** with Sunny: work-component table drafted, costing still owed to Marcos.
- **R&D comms.** 72-second overview film made and pushed to share-ai-ballys; live on internal-share once it merges to main.
- **Bally's Prototyping Platform.** Full codebase review complete; agreed to pivot to an open-source, self-hostable model with optional GitLab collaboration — plan being written.
- **R&D product vending session** with Al and Serhii — targeting Friday 16 Oct.
