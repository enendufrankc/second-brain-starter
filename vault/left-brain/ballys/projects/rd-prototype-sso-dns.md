---
project: R&D Prototype SSO/DNS
type: ballys-project
priority: P2
status: Deprioritised
criticality: Low
owner: Frank Enendu
gitlab_issues: "#15"
due_date: 2026-04-20
last_updated: 2026-04-22
---

# R&D Prototype SSO/DNS

## Overview
Cross-cutting infrastructure initiative to get SSO (Microsoft Entra ID), DNS (*.ballys.tech), and SSL certificates configured for all R&D prototypes. PIT (Platform Infrastructure Team) dependency — each app needs a ticket raised for DNS + cert + SSO integration.

## Status
- **Scope:** Covers Error Analysis, Roadmap Intelligence, Data Analyst Agent, Game Experience Profile, Ballys Skills Repo, Capex Machine
- **PIT Status:** Tickets raised for some apps, most still pending
- **Blocking:** Several prototypes can't go to production without this
- **PIT-9889:** Escalated via Nicholas Cutajar → Jean Paul Gatt (meeting set up Apr 15 3:30pm)
- **SSO/DNS meeting:** Wed Apr 15 4PM "Adding SSO and DNS to R&D P" — Al pushed back on self-service approach, connect next week

## Apps Requiring SSO/DNS/Cert

| App | Domain | SSO | DNS | Cert |
|-----|--------|-----|-----|------|
| Error Analysis | error-analysis.ballys.tech | pending | pending | pending |
| Roadmap Intelligence | roadmapintelligence.ballys.tech | pending | pending | pending |
| Data Analyst Agent | dataagent.ballys.tech | pending | pending | pending |
| Game Experience Profile | gameexperienceprofile.ballys.tech | pending | pending | pending |
| Ballys Skills Repo | agent-skills.ballys.tech | pending | ticket-raised | ticket-raised |
| Capex Machine | classify-epic.ballys.tech | done | pending | pending |

## Milestones
- [x] Identify all apps needing SSO/DNS/cert
- [x] Raise PIT tickets for Skills Repo DNS/cert
- [ ] Raise PIT tickets for remaining apps
- [ ] SSO configuration for all prototypes (#15)
- [ ] DNS records attached for all apps
- [ ] SSL certificates issued for all apps
- [ ] Verify end-to-end access for each app
