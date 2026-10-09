---
type: meeting-note
title: "Serhii Onboarding"
date: 2026-09-23
project: "General"
attendees: "Frank Enendu, Sudhanva Mysore Ganesh"
source: teams-transcript
---

# Serhii Onboarding — 2026-09-23

## Attendees
- Frank Enendu
- Sudhanva Mysore Ganesh (Sonny)

## Summary
Frank and Sonny worked out what Serhii needs in his first days: access paths, the R&D tech estate, and where knowledge lives. The conversation then drifted into what a "software factory" actually is and how a harness around GitLab issues might work, before landing on a proposal for a weekly informal engineer catch-up.

## Key Decisions
- HR/IT handle laptop and email; R&D covers Support Hub, Access Hub, AI Gateway, Claude, Cursor, GitLab and AWS
- Serhii requests the GenAI AWS account via Access Hub; Databricks skipped for now as he won't need it initially
- No deep repo walkthrough needed — everything he works on will be new
- Start a weekly informal engineer catch-up (Friday afternoon, not 4pm), roughly an hour, to share what people are working on and what's trending

## Action Items
- [ ] Frank: Find and send Sonny the infra skill Al built for AI Transformation Infra
- [ ] Frank: Walk Serhii through Access Hub, Teams/Outlook, GitLab and the repo standards
- [ ] Sudhanva: Ask for Serhii to be added to the shared mailbox, the GitLab R&D team and the R&D team generally
- [ ] Sudhanva: Prepare a stack summary for Serhii — OpenTofu/Terraform, WAF, restricted IPs, CloudFront front ends, Lambda/ECS back ends
- [ ] Frank/Sonny: Point Serhii at Confluence (older material), share.ballys.ai and the AI R&D infra repo
- [ ] Frank/Sonny: Share Al's list of current R&D projects with Serhii
- [ ] Frank/Sonny: Set up the recurring Friday engineer catch-up once Serhii starts

## Notes
**Naming issue** — The "AI Transformation Infra" project is misnamed; it holds all R&D infrastructure, not just transformation work.

**Infrastructure as code** — Neither is certain Serhii has Terraform/IaC experience. Sonny's concern is that AI will confidently generate over-engineered Terraform (S3 lifecycle rules and similar) that R&D doesn't need. Frank pointed to Al's infra skill, which constrains generation to the team's actual patterns — new to Sonny. Frank rates OpenTofu highly for module structure and for being able to inspect resources in the repo rather than in the AWS console.

**Software factory** — Neither was fully clear on the definition. Sonny's version: hand it a ticket, it plans, codes, tests and opens a merge request. Frank's version: a harness customising Claude Code with the team's own skills. Sonny sketched an orchestrator Lambda that picks up a GitLab issue, routes to a model based on ticket size, builds the repo, creates a worktree, does the work and opens an MR. He'd previously tested micro VMs for this and doesn't think they fit. Frank's view is that the prerequisite is a solid SDLC with strong end-to-end testing and CI/CD hooks.

**Tooling comparison** — Frank uses the Google approach over the Claude one, noting the Claude version wants an intent folder (index.md, aspect.md) that gets populated before a feature session starts, then hands off.

**Weekly catch-up rationale** — Sonny is fully remote and wants more contact; both noted this session spent ~50 minutes on topics other than onboarding, which is exactly the value. Agreed weekly rather than fortnightly given the pace of change.
