---
project: Error Analysis
type: ballys-project
priority: P2
status: Active — shared analysis backbone (merge landed 2026-09-25)
criticality: Medium
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/Error Analysis
production_url: https://d2lv9gmcz9m4c3.amplifyapp.com
gitlab_issues: none
due_date:
pit_sso: pending
pit_dns: pending
pit_cert: pending
last_updated: 2026-09-28
---

# Error Analysis

> ⚠️ **Refreshed 2026-09-28** by the weekly backlog review from this week's R&D stand-ups (22–25 Sep). This project had been marked Deprioritised with a broken pipeline since April; this week's meeting notes show it back in active use as the shared tool other projects (starting with Game Experience Profile) feed into. Frank was not present to confirm — the "pipeline failed on main since Apr 2" note below is left as the last confirmed state of the underlying code; nothing in this week's notes explicitly confirms the pipeline itself was fixed, only that Frank is actively merging changes into it and it is receiving live traces. Verify at the next live review.

## Overview
Multi-tenant serverless platform for analyzing AI agent trace data. Identifies and categorizes failure modes with clustering, statistics, and trend tracking. As of this week, this is the team's **single shared error-analysis system** — the Game Experience Profile project's own eval/tagging UI is being folded into it via API rather than run as a second tool.

## Tech Stack
- Frontend: Next.js 15.5, React 19, AWS Amplify (SSR)
- Backend: Python 3.11 Lambda (22+ handlers), API Gateway
- Auth: AWS Cognito + JWT
- Data: DynamoDB single-table design, S3 for trace files
- IaC: Terraform

## Note (last confirmed state, unverified since)
Pipeline FAILED on main since Apr 2 (last commit: `feat: add project reset endpoint and UI button`). Still broken as of Apr 16. This week's stand-ups show active merges and live trace ingestion, which implies it works, but no note explicitly says the Apr 2 failure was resolved — confirm with Frank.

## Milestones
- [x] Next.js frontend completed
- [x] Lambda backend with 22+ handlers
- [x] DynamoDB single-table design
- [x] Cognito authentication configured
- [x] Terraform IaC
- [x] New eval tab added, collecting a golden dataset for prompt tuning (2026-09-23)
- [x] Frank's traces reworked to fit the error-analysis format — only minor changes needed (2026-09-23)
- [x] Merged error-analysis changes so it feeds the priority list built in the eval tab (2026-09-25)
- [ ] Expose the API methods Game Experience Profile needs, incl. managing its own data source
- [ ] Render captured video in the input-data pane (for Game Experience Profile)
- [ ] DNS: error-analysis.ballys.tech
- [ ] SSL certificate
- [ ] SSO configuration
- [ ] Bug fixes and refinements
- [ ] Production hardening

## Sources
- [2026-09-22 — R&D Stand up](../meetings/2026-09-22-rd-stand-up.md)
- [2026-09-23 — R&D Stand up](../meetings/2026-09-23-rd-stand-up.md)
- [2026-09-23 — Game Exp Pipeline Update](../meetings/2026-09-23-game-exp-pipeline-update.md)
- [2026-09-25 — R&D Stand up](../meetings/2026-09-25-rd-stand-up.md)
