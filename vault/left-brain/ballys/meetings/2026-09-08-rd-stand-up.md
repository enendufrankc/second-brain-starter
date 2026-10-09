---
type: meeting-note
title: "R&D - Stand up"
date: 2026-09-08
project: "Adaptive Layouts"
attendees: "Al Jepps, Frank Enendu, Sudhanva Mysore Ganesh, Marcos Michel"
source: teams-transcript
---

# R&D - Stand up — 2026-09-08

## Attendees
- Al Jepps
- Frank Enendu
- Sudhanva Mysore Ganesh (Sudhanva)
- Marcos Michel (mentioned, not confirmed present)

## Summary
Team discussed progress on Adaptive Layouts project, focusing on issues with fixed vs. dynamic section handling. Key blocker: ops team has pinned first 6 rows, preventing adaptive layout algorithms from working effectively. Discussed need to include "suggested for you" section in AI pool and monitoring/reporting readiness.

## Key Decisions
- Turn off pinned sections temporarily to test adaptive layout effectiveness
- Add "suggested for you" section to AI recommendation pool via pipeline changes
- Include monitoring/reporting updates in next status check
- Hold for consideration: redesign fixed/dynamic section decoupling to avoid tight coupling

## Action Items
- [ ] Sudhanva: Send back office tool URL to team
- [ ] Sudhanva: Share status dashboard (fixing up this hour)
- [ ] Sudhanva: Take screenshot of Virgin Games view discrepancy and drop in group chat
- [ ] Sudhanva: Investigate "suggested for you" section in Contentful and estimate work to include in AI pool
- [ ] Al Jepps: Draft message to ops team (Dez) about pinned rows issue
- [ ] Sudhanva: Report back today on estimated effort for including suggested for you section
- [ ] Sudhanva: Optimize prompts to get best matching sections for row 1

## Notes
**AWS Partnership**: Discussed ongoing business relationship with AWS—mutual benefit arrangement involving case studies and speaking engagements in exchange for credits/discounts. AWS Lambda and Fargate Lambda Cloud workspace valuable for running production loops and listening to feedback.

**Adaptive Layouts Status**:
- Terraform changes still pending; pipelines green on staging and prod
- Minor bugs being fixed (judging/flagging issues don't block testing)
- 3 missing sections reported by stakeholders from generated layouts; clarified this was based on demo app (snapshot data) not live data
- First 6 rows pinned by ops team severely limits testing effectiveness—users see most benefit from row 6+ only
- Need to unpin or make sections dynamic for proper testing

**Content Management**:
- All layouts coming from Contentful/OpenSearch
- Back office tool manages fixed vs dynamic section tagging
- Materialization every 6 hours for drafts; instant on publish
- Virgin Games showing different view than other team members (investigating environment issue—was in Prod vs Staging)

**Monitoring & Reporting**:
- OpenSearch (OPEC) working perfectly with all traces captured
- Status dashboard nearly ready (fixing exports, LLM call visibility, AI flagging review)
- All dashboards showing run status, domestic gates, LLM calls, and flagging errors

**Architecture Concerns**: Al advocating against tight coupling between fixed rows and dynamic recommendations—suggests treating fixed sections as slots that adaptive layouts flows around, rather than excluding them from algorithm entirely.
