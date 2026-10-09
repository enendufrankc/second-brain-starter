---
project: Bally's Prototyping Platform
type: ballys-project
priority: P1
status: Active
criticality: Medium
owner: Frank Enendu
gitlab_issues: none
due_date:
last_updated: 2026-04-22
---

# Bally's Prototyping Platform

## Overview
Browser-based prototyping tool for Bally's — built on Pi, inspired by Bolt/Lovable but stripped down to what the business needs. Pre-loaded with all Bally's assets (lobby designs, game screens, etc.), connected to internal data sources. Conversational or drag-and-drop building with one-click deploy. Allows anyone in the business to build working mock-ups of ideas before writing tickets, so engineering gets click-through concepts instead of meeting descriptions.

## Status
- **Stage:** Waiting — Bhav's team working on Stadium design system, revisit in ~2 weeks (w/c May 4)
- **Docs:** Ballys-Prototyping-Platform-Brief.docx, RFC-001-Ballys-Prototyping-Platform.docx
- **Key dependency:** Stadium design system (Bhav + Adam's team)

## Discovery Meeting (Apr 22 — Frank, Bhav, Al)

### Key Outcomes
- **Stadium is the source of truth.** Bhav's team has a design system called "Stadium" — it contains all the rules, tokens, and components that define how Bally's products look. This is the foundation the prototyping platform should build on.
- **MUI-based component library exists.** Stadium uses MUI (Material UI) as the base, with custom overrides per brand. Components (buttons, checkboxes, radio buttons, etc.) are themed using design system tokens. Variants (primary, secondary) are defined and mapped to colour palettes.
- **Storybook available.** Bhav has a Storybook instance showing all components with brand theming. He's sharing repo access + Storybook link with Frank.
- **Adam's team actively building.** Adam (design team) is pushing to get more components into Stadium. Bhav suggested waiting 1-2 weeks for them to make more progress before Frank integrates.
- **Aligned vision.** Bhav confirmed they want the same thing — AI-assisted building using actual components (not lookalikes), so prototypes are production-grade code that developers can use directly.
- **Potential handoff.** Bhav mentioned his team struggles for time and suggested once Adam's bits are done, the AI R&D team could take over finishing/extending Stadium for the prototyping use case.
- **Use case validated.** Bhav recognised the Jackpot Joy overlay example — product people prototyping features on top of existing platforms. Craig Staples had asked for the same thing.

### What Bhav Is Providing
- Repo access to Stadium (MUI provider, component overrides, design tokens, Storybook)
- Engines file with code-based config, component usage docs, performance standards
- AI context docs — Bhav was already planning to create docs that tell AI "remember this, remember that" when building

### Architecture Insight
- Stadium repo structure: `packages/provider/` → MUI theme provider; `config/index` → palette/colour assignments; `components/` → MUI overrides (e.g. MUI Button with brand variants); tokens from design system feed into all of this
- Single page apps using MUI as base
- Can be packaged as an SDK/npm package

## Context
- Frank messaged Bhav directly (Apr 21) and shared detailed ask in group chat with Al
- Al asked about user access approach for AI R&D apps — conclusion: no SSO for demos/prototypes, self sign-up with passwords for apps with PII/user base

## Milestones
- [x] Initial concept and brainstorming
- [x] Platform brief document written
- [x] RFC-001 document written
- [x] Meeting scheduled with Bhav and Al
- [x] Discovery meeting with Bhav ✅ 2026-04-22
- [x] Bhav sharing Stadium repo access + Storybook link ✅ 2026-04-22
- [ ] Get access to Stadium repo and explore components/tokens/Storybook
- [ ] Wait for Adam's team progress on Stadium (~2 weeks, revisit w/c May 4)
- [ ] Evaluate integrating Stadium SDK into prototyping platform
- [ ] Define auth approach (per Al's tiered access decision)
- [ ] Core platform scaffold with Stadium components
- [ ] Brand theming integration (multi-brand support via Stadium tokens)
- [ ] Data source connections
- [ ] Internal pilot / user testing (Jackpot Joy overlay as test case)
- [ ] Production deploy
