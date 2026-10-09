---
project: Tableau MCP Agent
type: ballys-project
priority: P2
status: Active
criticality: Low
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/New Tableau MCP Agent
gitlab_issues: none
due_date: 2026-05-23
last_updated: 2026-04-14
---

# Tableau MCP Agent

## Overview
Full-stack Tableau AI workspace with natural language querying. Three-service monorepo: Next.js frontend, FastAPI backend, Node-based Tableau MCP server. Dashboard extension UI for embedded Tableau.

## Tech Stack
- Frontend: Next.js 15+, React 18, TypeScript, Vite, TailwindCSS, Zustand
- Backend: FastAPI, Python 3.12+, LangGraph
- MCP Server: Node.js (TypeScript), stdio transport
- Infra: AWS Terraform
- Observability: Opik

## Milestones
- [x] Next.js frontend scaffold
- [x] FastAPI backend scaffold
- [x] MCP server scaffold
- [ ] LangGraph integration
- [ ] Tableau API connection
- [ ] Testing and validation
- [ ] Production deploy
