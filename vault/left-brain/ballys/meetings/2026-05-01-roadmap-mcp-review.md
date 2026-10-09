---
type: meeting-note
title: "Roadmap MCP - Review"
date: 2026-05-01
project: "Roadmap Intelligence"
attendees: "Frank Enendu, Mark Webster"
source: teams-transcript
---

# Roadmap MCP - Review — 2026-05-01

## Attendees
- Frank Enendu
- Mark Webster

## Summary
Frank and Mark reviewed the UAT findings for the Roadmap Assistant tool. Mark walked through a detailed list of bugs and improvement areas from testing, including cold-start 503 errors, inaccurate progress reporting due to shallow Jira hierarchy traversal, inconsistent responses to the same prompt, and unclear persona views. They discussed architectural improvements including persona-based agents with an orchestrator and SSO integration for automatic user identification.

## Key Decisions
- The tool must not bypass the project manager when reporting bad news — it should present factual status but direct users to speak with the PM (listed via the "programme lead" Jira field) for context and next steps
- Persona detection should use SSO rather than manual selection, pulling role info automatically so the tool tailors response depth to the user
- Build individual persona agents with an orchestrator that routes queries based on user identity
- "Time logging blocked" Jira status should be treated as a done/complete status
- Mobile responsiveness downgraded from high to medium priority
- Date formatting should use UK format, not US

## Action Items
- [ ] Frank: Review the UAT workbook and this transcript, then provide Mark with a time-estimate breakdown for each issue (target: Tue/Wed May 6-7)
- [ ] Mark: Take Frank's breakdown to Al Jepps to negotiate time allocation and priority stack-ranking
- [ ] Frank: Design persona agent + orchestrator architecture
- [ ] Frank: Create a form for Mark to define each persona's requirements and tone of voice
- [ ] Frank: Fix 503 cold-start errors (critical)
- [ ] Frank: Fix Jira hierarchy traversal to go down to story/task level, not just epic level
- [ ] Frank: Ensure consistent responses — same prompt must return same sentiment
- [ ] Frank: Implement SSO-based user identity for persona routing

## Notes
Mark shared a UAT workbook with numbered issues. The main bugs discussed were: (1) PM bypass — the tool delivering project bad news without directing users to the PM, eroding the human dialogue needed for sensitive commercial conversations; (2) cold-start 503 errors making the tool unreliable; (3) false risk reporting — the tool showed 0% progress on features because it only checked epic status, not the stories underneath (e.g., 49 of 50 stories complete but epic still "in progress"); (4) inconsistent responses to identical prompts; (5) prompt parsing issues — the tool only reading the first line of multi-part questions; (6) mobile responsiveness needed for exec users on the go; (7) jargon and unclear persona labels that don't map to Bally's roles; (8) no persistent user identity across sessions.

Mark emphasized this is close to production-ready and needs refinements rather than a rebuild. Frank noted he only deployed Jay's work and hadn't yet had time to dig into improvements, but is eager to take it on given the clear business value. Frank will quantify effort for functional fixes but noted prompt accuracy tuning is harder to estimate upfront.
