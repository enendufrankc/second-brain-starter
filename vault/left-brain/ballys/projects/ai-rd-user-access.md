---
project: AI R&D User Access Strategy
type: ballys-project
priority: P1
status: Not Started
criticality: Medium
owner: Frank Enendu
gitlab_issues: none
due_date:
last_updated: 2026-04-22
---

# AI R&D User Access Strategy

## Overview
Write-up requested by Al Jepps (Apr 21) on user access approach for all AI R&D apps. Replaces the previous SSO/DNS initiative which was deprioritised after Bartek confirmed a dedicated service principal isn't possible.

## Decision Context (from Teams group chat, Apr 21)
- **Dedicated service principal** for AI R&D: rejected by Bartek
- **Entra SSO on all apps:** not happening
- **Al's preferred approach:** Unique logins with self sign-up, everything needs passwords
- **Tiered model agreed:**
  - Concept demos / prototypes → no auth needed
  - Apps with PII, user actions, or a real user base (e.g. Capex Machine) → passwords with self sign-up required
- Al binned the meeting with Bartek
- Sudhanva to add to task tracker

## Milestones
- [ ] Draft user access strategy document
- [ ] Define which apps fall into each tier
- [ ] Propose self sign-up implementation approach
- [ ] Review with Al and Sudhanva
- [ ] Finalise and share
