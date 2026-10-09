---
type: meeting-note
title: "iGaming Tech NCR (Series)"
date: 2026-08-27
project: "General AI R&D"
attendees: "Al Jepps, Sudhanva Mysore Ganesh, Frank Enendu, Kyriacos Kyriacou, Ilsan Tijhuis, Marcos Michel"
source: teams-transcript
---

# iGaming Tech NCR (Series) — 2026-08-27

## Attendees
- Al Jepps
- Sudhanva Mysore Ganesh (Sunny)
- Frank Enendu
- Kyriacos Kyriacou (KK)
- Ilsan Tijhuis
- Marcos Michel

## Summary
Two Q4 NCR candidates were presented: Sunny's Portfolio Optimization Agent (data-backed hold / enhance / withdraw plus gap analysis across games, brands, markets and segments) and Frank's Game Ideation Agent (a research agent that turns a plain-English query into an evidence-backed game design brief). Al framed the two as a single automation pipeline — portfolio gaps feed ideation, which feeds Wonder Machine and the studios — and pushed for a third component that generates prototypes and artwork. Both NCRs were judged strong in principle, with the later pipeline stages and costing still to be firmed up.

## Key Decisions
- Portfolio Optimization and Game Ideation will be packaged as one connected pipeline, with an automated shared data interface passing agreed gaps from optimization into ideation.
- Both agents stay human-in-the-loop: no autonomous decisions, and no recommendation without policy, context and cited evidence.
- Responsible gaming is dropped from the portfolio optimization scope (existing mechanisms cover it); certification is a noted consideration but will not be baked into either NCR now.
- Placement, promotion and exposure are treated as context inputs only — the optimization agent will not issue placement or promotion recommendations.
- Costing for both NCRs is taken offline into a separate session rather than done in this meeting; Sunny and Frank will do it.
- Both agents will be built as one reusable platform serving Bally's and Intralot, with pilots scoped separately (Intralot wants a narrower pilot area).
- A third pipeline element for prototype and artwork generation will be explored with the Free Play team and Gael, potentially as its own NCR.

## Action Items
- [ ] Sunny and Frank to complete the costing for both NCRs in a follow-up session (Marcos off next week; he will hand over a note that costing is due on his return).
- [ ] Al to route the portfolio optimization case to Chris for a soft dollar-value estimate and to help refine it.
- [ ] Sunny to share the portfolio optimization pack with Dez (not yet shared) and gather Intralot insights, not just data.
- [ ] Sunny to remove responsible gaming from the required-teams / scope slide.
- [ ] Sunny to factor adaptive layouts into the context model, since a game can now appear in multiple positions and placement correlates strongly with revenue.
- [ ] Sunny to fold the already-ticketed persona / game-affinity work into the segments dimension.
- [ ] Frank to firm up the demand-signal sourcing (where trend and competitor data is actually pulled from) and the later pipeline stages Al flagged as still woolly.
- [ ] KK to feed Frank input on slot data sources for upcoming and trending titles.
- [ ] Ilsan to share links to Gael's AI-generated art demos and videos in the meeting chat.
- [ ] Ilsan to bring Gael into the art and feel workstream and consider an NCR for artwork generation using the Free Play team.
- [ ] Frank to book a follow-up session in about two weeks to flesh out the combined pipeline (avoiding Ilsan's leave next week).
- [ ] Ilsan and Frank to pick up the AI hackathon thread alongside this work.

## Notes
- Current portfolio and new-game decisions are made largely on intuition; the data exists but nothing converts it into recommendations.
- Optimization agent design: policy plus context plus agent, producing portfolio intelligence (patterns) and gap analysis; outputs are hold (default), enhance, withdraw (highest evidence bar), and gap opportunity.
- Deliberately business-agnostic: intended to serve iGaming, lottery terminal menus and sports, with the optimization target set by the product (sales, GGR, etc.).
- Context includes lobby placement, commercial agreements, marketing spend, time and seasonality; framed loosely as reinforcement learning (environment, policy, objective).
- Every run is tied to evidence: data used, timeframe, patterns found and comparables.
- Validation: expert approval and action rate, historical backtest on held-out weeks, and prospective validation that the recommended action improves the chosen outcome.
- KPIs also include time to portfolio review, grounding (evidence citation rate), context coverage and the shared data interface working.
- Enhance outputs could feed contextual bandit experiments rather than direct changes.
- Pilot proposed in parallel across Intralot and Bally's, differing only in the context data gathered.
- KK's view: the real prize is building content in-house instead of paying suppliers, and rebalancing existing supplier mix on evidence; past in-house studio attempts failed for lack of exactly this insight.
- Game ideation agent reads demand signals, consumes optimization gap output, and emits a studio-ready game design brief; brief format based on a sample from Dez (concept, mechanics, gameplay, targets, comparables).
- Decision logic before any brief: reskin, extend, improve, build new, or do nothing (promote existing instead).
- Demo walked through "give me UK slot ideas for Q4": demand scan, catalogue and engine collection, gap analysis, decision logic, then three ranked options (extend scored 82 confidence), each with a generated DNA signature for later benchmarking and a build-prototype step.
- Ideation KPIs: at least 60 percent SME brief approval, cut brief creation from weeks to hours, mechanics proven against winning maths, and comparative analysis against games top personas play.
- Al challenged going full auto — with Wonder Machine plus Jelly crash game engine in place, generating playable games rather than briefs is the natural next step.
- Ilsan raised certification as a gap for real game or RTP changes, accepted as out of scope while output stops at prototypes.
- Ilsan tested the prototype and found it steered toward fishing when asked for a farming game; still rated the idea strong, especially wired into Wonder Machine plus generated art.
