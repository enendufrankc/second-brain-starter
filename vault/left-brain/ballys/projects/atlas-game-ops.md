---
project: Atlas (Game Ops)
type: ballys-project
priority: P1
status: Discovery
criticality: Medium
owner: Frank Enendu
gitlab_issues: none
due_date:
last_updated: 2026-09-21
---

# Atlas (Game Ops)

> ⚠️ **Reconstructed 2026-09-21** by the weekly backlog review from the 27 Aug t-shirt sizing session. Frank was not present to confirm. Scope, sizing and owner assignment need his check.

## Overview
Game Ops automation agent. Currently three separate runners to be merged behind a single router, with a production-grade rewrite to follow. Reads from and writes to Contentful; deployed on AWS Fargate. Sized in the Game Ops / Atlas t-shirt estimation sessions alongside Kyriacos Kyriacou and Nathan.

## Status
- **Stage:** Discovery — sizing done, scope gap not yet pinned down
- **In Use:** Internal runs only
- **Known issue:** Fargate deployment is laggy with a blurred picture versus sharp local runs; single-task scaling unproven

## Milestones
- [x] T-shirt sizing session 2 completed with Game Ops (2026-08-27)
- [ ] Run Atlas discovery (1 week, R&D) — pin down the gap between Atlas today and what Kyriacos and Nathan want, plus additional business/QA use cases
- [ ] Obtain the existing requirements file given to Harmon covering Game Ops and QA (ask Nathan or Kevin) as discovery input
- [ ] Confirm with Kyriacos exactly what data Atlas reads from and writes to Contentful, to estimate the integration
- [ ] Bring Kevin into discovery and testing, including the pain points he hit with HRAdmin (with Ilsan)
- [ ] Merge the three Atlas runners into one runner with a router (~3 weeks, Game Ops)
- [ ] Write production-grade Atlas code (1 week, R&D) after the merge
- [ ] Get infra advice on the AWS/Fargate deployment — lag/blur versus local, and whether the single Fargate task can be scaled
- [ ] Tidy up the t-shirt sizing draft — sizing figures were AI-generated and need a human pass (Marcos rounds up)
- [ ] Post each sized item into the meeting chat
- [ ] Open question: which team delivers Atlas — to be recommended by attendees at the requirements meeting

## Sources
- [2026-08-27 — T-shirt Size Estimation, Game Ops Atlas Session 2](../meetings/2026-08-27-t-shirt-size-estimation-game-ops-atlas-session-2.md)
- [2026-08-25 — R&D Stand up](../meetings/2026-08-25-rd-stand-up.md)
