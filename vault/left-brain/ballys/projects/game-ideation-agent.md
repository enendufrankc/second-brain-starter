---
project: Game Ideation Intelligence Platform
type: ballys-project
priority: P1
status: NCR presented — costing outstanding
criticality: High
owner: Frank Enendu
local_path: ~/Documents/Work/AI and R&D/Game Ideation Agent Experiment
gitlab_issues: "#35"
last_updated: 2026-09-21
---

# Game Ideation Intelligence Platform

> ⚠️ **Refreshed 2026-09-21** by the weekly backlog review from the 27 Aug iGaming Tech NCR. Frank was not present to confirm. Priority raised P2 → P1 and criticality Medium → High because this is now half of a presented Q4 NCR pipeline, not a side experiment — revert if that reads wrong.

## Overview
Multi-agent system built on Google ADK and A2A (Agent-to-Agent) protocol that accelerates the game concept pipeline from weeks to hours. Researches market trends, generates game concepts, and scores them for financial viability and regulatory compliance — delivering business-ready briefs.

## Status
- **Stage:** NCR presented 27 Aug 2026 and judged strong in principle. A research agent that turns a plain-English query into an evidence-backed game design brief.
- **In Use:** No
- **Packaged with Portfolio Optimisation** as one connected Q4 pipeline — portfolio gaps feed ideation, which feeds Wonder Machine and the studios. Al pushed for a third component generating prototypes and artwork.
- **Blocker:** GitLab #35 (scoping session with Sudhanva) is ~110 days overdue.
- **Related:** Game Experience Profile, Portfolio Optimisation Agent, Adaptive Layouts, iPOP

## Tech Stack
- Google ADK (orchestrator), A2A protocol for agent communication
- MCP for data access
- Connects existing agents: Game Experience, Adaptive Layouts, iPOP
- New specialist agents: market research, concept creation, validation

## Key Features
- Connects existing Ballys/Intralot agents into unified A2A network
- Produces Game Briefs with concept, mechanics, and commercial scores
- Supports both iGaming and Fast Play through domain-specific agents
- Human-in-the-loop design — AI proposes, humans decide

## Design Principles
- Speed over perfection — deliver briefs fast, humans refine
- Evidence over intuition — recommendations grounded in data
- Built in-house, not vendor
- Google ADK as standard framework

## Milestones
- [x] Architecture blueprint document written
- [x] Workshop deck presented (Bally's Intralot AI Agents Workshop)
- [x] Agent profiles defined
- [x] NCR presented to iGaming Tech alongside Portfolio Optimisation (2026-08-27)
- [ ] Complete NCR costing in a follow-up session (Frank + Sunny — due on Marcos's return)
- [ ] Firm up demand-signal sourcing — where trend and competitor data is actually pulled from (Frank)
- [ ] Firm up the later pipeline stages Al flagged as still woolly (Frank)
- [ ] Get KK's input on slot data sources for upcoming and trending titles
- [ ] Book the follow-up session (~2 weeks out) to flesh out the combined pipeline
- [ ] Define the shared data interface passing agreed gaps from optimisation into ideation
- [ ] Explore prototype/artwork generation as a third pipeline element with the Free Play team and Gael
- [ ] Scoping session with Sudhanva (#35 — ~110 days overdue)
- [ ] Write up the game ideation project plan, share with Al, add to tracker (from 4 Jun 1:1)
- [ ] Prototype orchestrator with Google ADK
- [ ] Connect Game Experience Agent via A2A
- [ ] Market research agent implementation
- [ ] Concept generation agent implementation
- [ ] End-to-end pipeline validation
- [ ] Production deployment

## Sources
- [2026-08-27 — iGaming Tech NCR](../meetings/2026-08-27-igaming-tech-ncr.md)
- [2026-06-04 — Frank's 1:1 with Al](../meetings/2026-06-04-franks-1-2-1.md)
