---
type: meeting-note
title: "Bally Intralot Prototyping Platform Discovery"
date: 2026-04-22
project: "General AI R&D"
attendees: "Frank Enendu, Bav Patel, Al Jepps"
source: teams-transcript
---

# Bally Intralot Prototyping Platform Discovery — 2026-04-22

## Attendees
- Frank Enendu
- Bav Patel
- Al Jepps

## Summary
Frank and Bav discussed the vision for an internal prototyping platform where staff can build app prototypes that follow Bally's design system, similar to tools like Lovable. Bav walked through the Stadium design system repo (Storybook-based, using MUI with design token overrides) which would serve as the source of truth for components, theming, and styling conventions.

## Key Decisions
- Stadium (the existing Storybook-based design system) will be the foundation/source of truth for the prototyping platform
- Wait approximately 2 weeks for Adam's design team to finish their current Stadium work before progressing further on the prototyping platform
- Once Adam's team completes their part, Frank's team may take over finishing the integration

## Action Items
- [ ] Bav to share access to the Stadium repo with Frank
- [ ] Frank to review the Stadium Storybook, component library, and codebase config/standards docs
- [ ] Reconvene in ~2 weeks to assess progress on Stadium and plan next steps
- [ ] Explore packaging Stadium components as an SDK for use in the prototyping platform

## Notes
The core problem being solved: people currently use Claude Code to build prototypes, but the output doesn't follow Bally's design system and they lack access to deployment infrastructure and API keys. The prototyping platform would bundle all of this together.

Bav demonstrated the Stadium Storybook showing themed components (buttons, checkboxes, radio buttons) with brand-specific palettes. The repo contains MUI component overrides using design tokens, performance standards, and code quality guidelines — all intended to feed into AI-assisted building.

The vision aligns with what Craig has also been requesting. Stadium uses an MUI theme provider with brand-switchable palettes, and the component overrides live in a packages directory with per-component variant definitions.
