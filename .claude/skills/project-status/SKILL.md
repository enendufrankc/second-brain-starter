---
name: project-status
description: >
  Gathers status across all of Frank's R&D projects: reads vault/projects/*.md, queries GitLab
  for recent MRs/issues/pipelines, checks daily logs for recent updates. Produces a portfolio-level
  status report. Triggers: "project status", "portfolio status", "what's the state of my projects",
  "status report", "sprint status", "how are things going", "/project-status"
---

# Project Status — Portfolio-Level Status Gatherer

Produces a cross-project status report by combining vault data with live GitLab data.

## Usage

Run the gather script, then format the output for Frank:

```bash
python3 .claude/skills/project-status/scripts/gather_status.py
```

Or with options:
```bash
# JSON output for programmatic use
python3 .claude/skills/project-status/scripts/gather_status.py --json

# Only specific projects
python3 .claude/skills/project-status/scripts/gather_status.py --project hackathon-platform

# Include pipeline status
python3 .claude/skills/project-status/scripts/gather_status.py --pipelines
```

## What It Gathers

### From GitLab (live)
- Open issues assigned to Frank (with due dates, milestones, labels)
- Open MRs (assigned + review requested)
- Recent pipeline status (last 5 per tracked project)
- Overdue/due-soon markers

### From Vault (local)
- `vault/projects/*.md` — current project descriptions and notes
- `vault/portfolio/index.md` — master project list
- `vault/daily/` — last 3 daily logs for recent context
- `vault/projects/STATUS-DASHBOARD.md` — previous dashboard state

## Output Format

The script outputs a markdown status report. The agent should:

1. Run the script to get raw data
2. Read `vault/projects/STATUS-DASHBOARD.md` for previous state
3. Identify what changed since last check
4. Present to Frank as a concise briefing:
   - Projects with urgent items first (overdue, due today)
   - Then active items (due this week)
   - Then upcoming items (due later)
   - Flag any blockers or cross-project dependencies

## After Gathering

- Update `vault/projects/STATUS-DASHBOARD.md` with current state
- Append a status check entry to today's daily log
- If any deadlines shifted, update `vault/MEMORY.md`

## Frank's Tracked Projects

| Project | GitLab Repo ID | Key Issues |
|---------|---------------|------------|
| Hackathon Management Platform | 8175 | #13, #14 |
| Game Experience Prototype | 8248 | #11, #12 |
| R&D Prototype SSO/DNS | — | #15 |
| Portfolio Optimisation Agent | — | #16 |
| Data Agent | — | #19 |
| Ballys Skills Repo | 8284 | — |
| Roadmap MCP | 8275 | — |

Task tracker project: **8489** (where issues live)
