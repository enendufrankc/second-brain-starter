---
type: meeting-note
title: Games Ops Process Show and Tell With Frank
date: 2026-04-24
time: "09:00-10:00"
project: Games Ops AI Discovery
attendees: Frank Enendu, Nathan Maddock, Kaan Onur
organiser: Kyriacos Kyriacou
---

# Games Ops Process Show and Tell — 24 Apr 2026

**Attendees:** Frank Enendu, Nathan Maddock, Kaan Onur (Kyriacos set it up but didn't attend)

**Purpose:** Games Ops walked Frank through their end-to-end game release process to identify AI/automation opportunities.

## What Games Ops Actually Does

The team manages setup, testing, and release of third-party casino/slot games across all Ballys ventures (Jackpot Joy, Double Bubble, Virgin, Monopoly, Rainbow Riches, etc.). For each game release, they manually configure three separate systems in sequence:

1. **Cabo (Infinity platform)** — create the game record with wallet code, software IDs, RTP, jackpot status
2. **Game ID Sheet (Excel)** — log the new game ID and Cabo code in a master spreadsheet (~10,000 entries)
3. **Contentful** — configure the wallet (Cashier Game Config), build the Game Model V2 with metadata, create per-venture Site Game entries

Then they test on staging, and if it works, duplicate everything to production. Additional workflows include Hasbro approvals for Monopoly-brand games, UKGC certificate submissions, and game asset creation via Figma.

## The Pain Points

The core problem is **scale meets manual process.** Building one game is manageable, but they regularly face batches of 20-30, and for new market launches (Greece) they need to set up ~2,000 games. Every field across every system is typed or pasted by hand. There's no copy button between Cabo staging and production (they've been asking for years). Provider data formats are inconsistent across hundreds of providers. Confluence crashed under the volume, forcing a move to Excel. Designers are a bottleneck for game tile assets.

As Nathan put it: "Does it hit your soul a bit, Frank, to watch all this manual data entry?"

## AI Opportunities Identified

1. **Automate data transfer between platforms** — Jira to Cabo to Excel to Contentful. Frank confirmed this is "100% doable" via APIs
2. **Kill the Excel sheet** — replace with automated lookup/database
3. **Cabo stage-to-production duplication** — Nathan already tested this with Claude Cowork and it worked
4. **Hasbro approval pipeline** — Nathan suggested using N8N to auto-submit to the Hasbro portal
5. **Provider data harvesting** — use Cowork/Chrome to scrape provider portals for game info and assets
6. **Image/asset batch processing** — resize game logos with correct bounding boxes and transparent PNGs
7. **AI-assisted metadata collection** — either scrape from providers or build a standardised form for testers
8. **Jira daily task planner** — connect AI to Jira board to generate prioritised daily task lists
9. **Launch URL extraction** — Cowork found URLs via network traffic inspection in seconds (takes them much longer manually)
10. **Third-party ticket generation** — auto-generate tickets to different provider systems when game issues arise

Frank's overarching principle: "Human is not supposed to be copying over data. It's supposed to observe, review, and approve."

## Systems and Tools Used

| Tool/System | Purpose |
|---|---|
| Cabo (Stage + Production) | Infinity game configuration — game codes, software IDs, RTP |
| Infinity | Game aggregation/integration platform connecting providers to Ballys backend |
| Contentful | CMS for wallet config, Game Model V2, Site Game entries, lobby building |
| The Wallet | Financial transaction system — no wallet entry = players can't bet |
| Jira | Ticketing — Product team fills in game details for Games Ops |
| Excel (Game ID Sheet) | Master spreadsheet tracking ~10,000 game IDs and codes |
| Hasbro Zone Portal | External portal for Monopoly-brand game approvals |
| UKGC Website | UK Gambling Commission — certificates/refs must be added |
| Figma | Game tile asset creation with correct sizing |
| Claude Cowork | AI assistant — team got access days before this meeting |
| Monday.com | Attempted for task/filter management, didn't fully work out |
| N8N | Pipeline/automation tool candidate |
| SharePoint | Destination for storing harvested game assets |

## Action Items

- [ ] **Kaan** to send Frank detailed documentation of Games Ops processes
- [ ] **Nathan** to invite Frank to watch a live asset build session next week (15 mins)
- [ ] **Frank** to schedule follow-up meeting (suggested next Friday) to walk team through practical Cowork usage
- [ ] **Nathan** to suggest Jira daily planner idea to Cindy on the team
- [ ] **Frank** to research image batch processing tools for transparent PNGs
- [ ] **Frank** in London Tue-Wed for Ignite; Kaan will be in office Tuesday

## Key Quotes

- "All done manually" — Kaan (on filling in Cabo fields)
- "We've been hoping for a duplicate button for a while" — Nathan (on Cabo stage-to-production)
- "The paying process is the quantity" — Kaan (on the main pain point)
- "For Greece, we've got like 2000 games" — Kaan (illustrating scale)
- "On that, we're on 10,000" — Kaan (total games in the ID sheet)
- "That's why Confluence died of death a long time ago" — Nathan
- "Does it hit your soul a bit, Frank, to watch all this manual data entry?" — Nathan
- "Everything that you're copying over can be automated, that is 100% doable" — Frank
- "The Excel is going to go away easily" — Frank
- "Human is not supposed to be copying over data" — Frank
- "It's hard to visualize until we can see it happening" — Kaan (on trusting automation)
- "Fill a form but don't click submit, you understand?" — Frank (on human-in-the-loop approach)
