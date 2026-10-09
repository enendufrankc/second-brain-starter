---
type: meeting-note
title: "Adaptive Layouts - UAT Testing Set Up"
date: 2026-09-08
project: "Adaptive Layouts"
attendees: "Juan Impey, Al Jepps, Craig Staples, Dean Richards, Adam Bailey, Samuel Milner, Kyriacos Kyriacou, Thomas Heighway, Craig Walker"
source: teams-transcript
---

# Adaptive Layouts - UAT Testing Set Up — 2026-09-08

## Attendees
- Juan Impey (presenter)
- Al Jepps
- Craig Staples
- Dean Richards
- Adam Bailey
- Samuel Milner
- Kyriacos Kyriacou
- Thomas Heighway
- Craig Walker
- Plus additional attendees

## Summary
Juan walked team through UAT testing setup for adaptive layouts. Pipeline is all green in production. Created Chrome extension to simplify testing across different clusters without needing specific member IDs. Contentful contains static sections; back office app (built by Freddie) manages fixed/dynamic designation; adaptive layouts app generates AI recommendations that substitute into dynamic rows.

## Key Decisions
- Use Chrome extension for cluster switching instead of member ID insertion
- Use staging for Google Analytics and LCA data testing with insertable member data
- Automated testing completed for all ventures, platforms, and client platforms
- Control/treatment groups testable via cluster ID + variant parameter

## Action Items
- [ ] Juan: Drop Chrome extension setup link in chat (and conference page)
- [ ] Juan: Provide zip file on conference page for those unable to download from GitLab
- [ ] Juan: Investigate why Virgin Games Chrome extension not refreshing between clusters
- [ ] Juan: Investigate two discrepancies in automated testing
- [ ] Juan: Create Contentful export for team without access to content management tools
- [ ] Juan: Provide list of expected sections so testers know what to look for

## Notes
**UAT Testing Approach**:
- Pipeline complete and green in production—ready for testing
- Chrome extension acts like Requestly, allowing cluster ID selection without member ID insertion
- Works across all 22 clusters currently in production
- Control/treatment/unaffected groups supported for A/B testing

**System Setup**:
- **Contentful**: Contains all static sections configured for production
- **Back Office App** (built by Freddie): Marks sections as fixed vs dynamic per cluster (currently all same across clusters, but per-cluster customization possible)
- **Adaptive Layouts App** (built by Sudhanva): Generates AI recommendations that populate dynamic slots
- **Lobby Preview**: Shows expected AI-generated rows for each cluster

**Testing Flow**:
1. Install Chrome extension from GitLab or conference page
2. Search cluster ID + variant to enable treatment group (shows adaptive layouts)
3. Refresh page to see AI-generated rows substituted
4. Switch between clusters (22 available) and ventures
5. Cross-reference generated content against Contentful/back office configuration
6. Control/Unaffected options show static lobby for baseline comparison
7. Turn off extension after testing to avoid unexpected behavior elsewhere

**Issues Identified**:
- Two discrepancies found in automated testing (to be investigated)
- Virgin Games Chrome extension not refreshing when switching clusters (needs troubleshooting)
- Some attendees lack access to Contentful or back office app—export needed

**Support**: Juan offering to expand Chrome extension functionality if tested features don't fit current capabilities.
