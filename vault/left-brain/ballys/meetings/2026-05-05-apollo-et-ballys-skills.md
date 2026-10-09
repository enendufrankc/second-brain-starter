---
type: meeting-note
title: "Apollo et Ballys Skills"
date: 2026-05-05
project: "Ballys Skills Repo"
attendees: "Frank Enendu, Volodymyr Pivoshenko"
source: teams-transcript
---

# Apollo et Ballys Skills — 2026-05-05

## Attendees
- Frank Enendu
- Volodymyr Pivoshenko

## Summary
Frank and Volodymyr discussed integrating Apollo (a package manager for skills and MCPs built by the Vitruvian team) with the Ballys Skills platform. Apollo handles declarative distribution, versioning, and syncing of skills across teams via config files, while Ballys Skills Hub is the centralized discovery/publishing platform. Both agreed the tools complement each other and should be consolidated.

## Key Decisions
- Apollo will serve as the distribution/installation backend for the Ballys Skills platform, replacing direct NPX install commands
- A base config with common Ballys skills (e.g. branding) will be created that all teams inherit from via Apollo's planned "extend" feature
- External skills referenced in Apollo configs will go through a "skill gate" security check before installation

## Action Items
- [ ] Frank to send Volodymyr access to the Ballys Skills repo so he can evaluate Apollo integration points
- [ ] Volodymyr to prioritize the config "extend" feature so teams can inherit a base Ballys skills config
- [ ] Volodymyr to implement skill gate (security scanning for external skills)
- [ ] Both to coordinate with Wanis on pre-installing skills into Cloud Cowork instances
- [ ] Both to align on joint promotion of the platforms to avoid user confusion between Apollo and Ballys Skills
- [ ] Sonny's agentic framework comparison report to be shared once ready (covers LangChain, LangGraph, Llama, Pydantic AI, OpenAI, Google ADK, Anthropic)

## Notes
- Apollo works as a declarative config: list skills/MCPs in a YAML config, run `apollo sync`, and everything installs/updates/removes automatically
- Apollo registers a hook on agent startup (Cursor, Claude Code) to auto-sync skills on launch
- Vitruvian team already has multiple teams using Apollo with team-specific configs
- Apollo collects minimal telemetry (who installed, what configs, what version) — more detailed tracking needs approval from leadership due to sensitivity
- Ballys Skills platform includes CI pipeline with LLM-as-judge evaluation for submitted skills via merge requests
- Frank uses Google ADK for agent framework; Sonny is completing a cross-framework comparison for Ballys standardization
