---
project: AI R&D Tracker
type: ballys-project
priority: P1
status: Active
criticality: Low
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/AI R&D Tracker
gitlab_repo: task-tracker
gitlab_issues: "#7"
due_date: 2026-04-11
last_updated: 2026-04-22
---

# AI R&D Tracker (Task Tracker)

## Overview
GitLab-integrated task management for the AI R&D team. Syncs between local todo.md and GitLab issues. 6 reusable skills for task management.

## Tech Stack
- Python, GitLab API, shell scripts, CSV generation
- Skills: /sync, /create, /my-tasks, /team-board, /weekly-summary, /comment
- Session hooks for end-of-day reminders
- CI/CD: GitLab Pages

## Note
GitLab PAT expiring imminently — email warning received Apr 11 ("tokens will expire in 7 days or less", i.e. ~Apr 18). A new PAT was created Apr 3 but the old one is still in use. Needs renewal urgently to keep API sync working.

## Milestones
- [x] GitLab API integration
- [x] 6 reusable skills built
- [x] CSV generation
- [x] GitLab PAT regeneration ✅ 2026-04-22
- [ ] CI/CD pipeline
- [ ] Team adoption and training
