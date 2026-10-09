---
type: meeting-note
title: "T-Shirt size estimation: Game Ops, Atlas: session 2"
date: 2026-08-27
project: "General AI R&D"
attendees: "Marcos Michel, Kyriacos Kyriacou, Frank Enendu, Ilsan Tijhuis, Iona Lloyd, Gabor Csomak"
source: teams-transcript
---

# T-Shirt size estimation: Game Ops, Atlas: session 2 — 2026-08-27

## Attendees
- Marcos Michel (organiser)
- Kyriacos Kyriacou
- Frank Enendu
- Ilsan Tijhuis
- Iona Lloyd
- Gabor Csomak

## Summary
Marcos ran a T-shirt sizing session across two initiatives: the remaining Game Ops automation features and Atlas. The Game Asset Harvester was re-sized down to less than small (one sprint, one person), while the Game Build tool was parked until Juan Impey returns, since he is expected to own it via Thunderbird. Most of the call was Frank walking through seven Atlas work items — discovery, merging the three runners, production-grade code, testing, QA test, infra/security/scaling and integrations — with sizes and owners assigned across R&D, Game Ops, PIT and Thunderbird, closing with a dependency map.

## Key Decisions
- Game Asset Harvester re-sized to less than small: one sprint, one person, remaining work is only uploading to GitLab so anyone can check out and run it locally. QA is considered done once a fresh machine can run it.
- Game Build ("Game Ops Game Build") left unsized and parked until Juan Impey is back on Tuesday; Thunderbird is the expected owner.
- Scope discipline agreed: land the first two features to prove the Game Ops hub works, rather than sizing the full 13-feature list now.
- A Confluence page will be created as single source of truth for all 13 Game Ops features (name, description, current form, owner, next step).
- Atlas stays hosted as-is in the R&D space; not treated as a work item.
- Atlas discovery: very small, one week, one person, R&D.
- The three Atlas agents (RTS runner, TestRail runner, game capture) merge into one runner behind a router: Game Ops, three weeks, small, one person.
- Production-grade code: one week, R&D, dependent on the runner merge.
- "QA" item renamed to "testing" (one sprint, one person, done incrementally); a separate "QA test" item added for the Content QA team.
- Infra/security/scaling kept as one item, sized small for Platform Infrastructure (PIT), and split into a discovery part and a development part.
- Confluence integration dropped; integrations are Contentful and Jira only. Jira is easy (API calls, R&D, one sprint).
- Contentful integration split into its own item, sized medium or larger, assigned to Thunderbird because Contentful is critical infra.
- Dependency map: discovery → development, with infra finish-to-finish against development, integration hand-in-hand with development, and main testing last.
- All sizes are provisional T-shirt sizes to be refined later.

## Action Items
- [ ] Marcos Michel — send Kyriacos the links previously sent to Naif for the two features.
- [ ] Kyriacos Kyriacou — build the Confluence single-source-of-truth page for the 13 Game Ops features (name, description, current form, owner, next step), using Claude.
- [ ] Iona Lloyd — take over the workstream next week while Marcos is on holiday; wants a roadmap/Gantt view of sized, blocked and progressed features.
- [ ] Juan Impey — on return Tuesday, analyse the Game Build skill (scope and complexity of folding it into the Game Ops hub) and confirm Thunderbird ownership.
- [ ] Juan Impey — refine the Contentful integration sizing for Atlas.
- [ ] Marcos Michel — revisit Game Build sizing with Juan next week.
- [ ] Frank Enendu — run Atlas discovery (1 week, R&D): pin down the gap between Atlas today and what Kyriacos and Nate want, plus additional business/QA use cases.
- [ ] Frank Enendu — ask Nathan or Kevin for the existing requirements file given to Harmon covering Game Ops and QA, as an input to discovery.
- [ ] Frank Enendu — merge the three Atlas runners into one runner with a router (Game Ops, ~3 weeks).
- [ ] Frank Enendu — write the production-grade Atlas code (1 week, R&D) after the merge.
- [ ] Frank Enendu — post each sized item into the meeting chat.
- [ ] Frank Enendu / Ilsan Tijhuis — bring Kevin into Atlas discovery and testing, including the pain points he hit with HRAdmin.
- [ ] Ilsan Tijhuis — involve the Content QA team as a separate testing item (provider integrations, games validation, regression).
- [ ] Frank Enendu — get infra advice on the AWS/Fargate deployment (laggy, blurred picture vs sharp local runs) and whether the single Fargate task can be scaled.
- [ ] Ilsan Tijhuis — raise the AWS setup/scaling question with Al Jepps and PIT together.
- [ ] Gabor Csomak — potentially help with the platform-infrastructure sizing.
- [ ] Kyriacos Kyriacou — explain exactly what data Atlas will read from and write to Contentful so Frank can estimate the integration.
- [ ] Kyriacos Kyriacou and Nate — continue ongoing Atlas performance testing in parallel with development.
- [ ] Marcos Michel — keep Thunderbird/Nightwatch in the loop on the Contentful work.

## Notes
- Naming confusion over the second Game Ops feature (Building Tool / Game Build) was itself an argument for the Confluence list.
- Game Build is an existing beefy skill that builds a game, configures Contentful and drives the Jira ticket process; it touches production so must move into the hub for auditability.
- Iona flagged governance risk: 13 features tracked only in a meeting chat.
- Kyriacos framed the Game Ops hub as a blueprint other teams could replicate as their own audited productionised zone.
- Atlas already works and is stood up; roughly seven gaps remain to reach what Kyriacos and Nate want.
- Frank floated 3–5 weeks for Nate on the runner merge; agreed 3 weeks as the estimate.
- Atlas is useful to Content QA for provider/game integration validation and regression; Kevin and Carolina have seen it and like it.
- Overlap noted between Atlas and Kevin's Harmon work — Marcos suggested the two tools may merge.
- Infra risk: local runs are fast and sharp, the AWS deployment is laggy with blurred picture; runners currently on a single Fargate task with unknown scaling path.
- Ilsan warned most infra elapsed time is waiting on PIT, which is awkward to estimate.
- Gabor argued for walking-skeleton delivery — proper infra first to avoid "works on my machine" — noting it can run in parallel rather than as a hard dependency.
- Contentful treated as critical infra: past incidents where a Contentful update took the whole site down.
- Main Atlas Contentful use case: game testing pulls metadata and pushes it into Contentful.
- Meeting record metadata still carries the earlier series subject ("Game Swipe, Game Ops, Atlas", 14 Aug); Game Swipe was not discussed in this session.
