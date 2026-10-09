---
project: Jira Documentation Agent
type: ballys-project
priority: P2
status: Prototype
criticality: Low
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/Jira Documentation Agent
gitlab_repo: jira-doc-agent
gitlab_issues: none
last_updated: 2026-04-14
---

# Jira Documentation Agent

## Overview
LLM-driven agent that automatically generates formal, audit-friendly user-story documentation from Jira data. Reduces manual documentation effort, improves consistency across delivery programmes, and satisfies audit/governance requirements. Uses Google ADK with a multi-agent architecture — delivery report agent, data tools, and progress tools.

## Status
- **Stage:** Prototype — validated with mocked Jira data
- **PDR:** Draft strawman written for stakeholder alignment
- **In Use:** No (pending live Jira API connection)

## Tech Stack
- Python 3.11+, FastAPI, Google ADK, Google GenAI
- Frontend: Vanilla JS with SSE streaming
- Output: PDF via ReportLab
- Deployment: Docker Compose, Render.com
- IaC: Terraform

## Key Features
- Extracts epics, user stories, acceptance criteria, status, and ownership from Jira
- Generates structured, audit-ready Word/PDF documentation
- Multi-agent pipeline: data extraction → analysis → report generation
- Supports multiple output formats via shared data pipeline

## Milestones
- [x] PDR/strawman document written
- [x] Multi-agent architecture designed
- [x] Prototype with mocked Jira data
- [x] PDF report generation working
- [ ] Live Jira API integration
- [ ] Real delivery programme validation
- [ ] Production deploy
