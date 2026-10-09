---
project: Data Analyst Agent
type: ballys-project
priority: P1
status: Active
criticality: Low
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/Data Analyst Agent
production_url: https://main.devqiqmi3hnvs.amplifyapp.com/
intended_domain: https://dataagent.ballys.tech
gitlab_issues: "#19"
due_date: 2026-04-30
pit_sso: pending
pit_dns: pending
pit_cert: pending
last_updated: 2026-04-22
---

# Data Analyst Agent

## Overview
Multi-agent AI system for natural language analysis of CSV data. 8 specialized agents (understanding, code generation, execution, validation, visualization, chart validation). Auto-generates pandas code, executes in sandbox, creates Seaborn/Matplotlib charts with AI vision validation.

## Status
- **PIT Status:** Nothing done yet
- **In Use:** No

## Recent (Apr 17-20)
- **Dez Pazmany** wants a Tableau dashboard summariser feature — needs access to 10+ dashboards each morning, currently checking manually. Needs a PAT from Giorgia. Al offered his PAT as fallback.
- Frank agreed to work with Dez on the summariser feature. Discussed in "Al and Dez" group chat (Fri Apr 17).
- Dez getting set up on AI Fridays — Frank helping him get started properly.

## Tech Stack
- Python 3.13+, FastAPI, Claude Agent SDK, LiteLLM, Opik
- Frontend: Vanilla JS with SSE streaming
- Execution: Restricted sandbox
- Deployment: Render.com / AWS Lightsail

## Milestones
- [x] 8 specialized agents built
- [x] Sandbox execution working
- [x] Chart generation with AI validation
- [ ] Pivot: Automated Tableau reporting agent (new req from Dez Pazmany / Chris)
- [ ] Agentic harness implementation (#19)
- [ ] DNS: dataagent.ballys.tech
- [ ] SSL certificate
- [ ] SSO configuration
- [ ] Production deploy
