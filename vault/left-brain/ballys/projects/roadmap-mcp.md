---
project: Roadmap Intelligence
type: ballys-project
priority: P2
status: Active
criticality: Low
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/Roadmap MCP and Agent
production_url: http://roadmap-mcp-dev-alb-142014026.eu-west-1.elb.amazonaws.com/dev/chat
intended_domain: https://roadmapintelligence.ballys.tech
gitlab_issues: none
due_date: 2026-05-09
pit_sso: pending
pit_dns: pending
pit_cert: pending
last_updated: 2026-04-14
---

# Roadmap Intelligence (MCP Roadmap)

## Overview
AI-powered Jira roadmap analysis via Model Context Protocol. 30+ tools across 10 categories. Supports multiple personas (executive, portfolio manager, product manager, tech lead).

## Status
- **PIT Status:** Nothing done yet
- **In Use:** No

## Tech Stack
- FastAPI MCP server (JSON-RPC 2.0 over HTTP)
- LLM: OpenAI Gateway (Claude Sonnet 4.5), Google Gemini
- 30+ tools with progressive disclosure
- Rate limiting, circuit breaker, caching (30s-15m TTL)

## Milestones
- [x] 30+ tools built across 10 categories
- [x] Rate limiting and circuit breaker implemented
- [x] Multi-persona support (executive, portfolio, PM, tech lead)
- [ ] DNS: roadmapintelligence.ballys.tech
- [ ] SSL certificate
- [ ] SSO configuration
- [ ] User testing
- [ ] Production deploy
