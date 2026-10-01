---
name: vault-structure
description: >
  Teaches the agent Frank's vault file organization, naming conventions, and where to store
  different types of notes. The vault uses a left-brain/right-brain architecture: left brain
  for work (Ballys + contracts), right brain for personal life (vision, health, finance,
  norms, growth, relationships, projects, journal). Prevents misplaced files. Inspired by
  Karpathy's LLM Wiki schema pattern — this IS the schema document.
  Triggers: "where should I save this", "vault layout", "file organization", "create a note",
  "store this", "vault-structure", any file creation inside vault/
---

# Vault Structure — The Schema

This skill defines the canonical structure of Frank's second brain vault. Every file the agent
creates, moves, or references must follow these conventions. This is the "schema layer" from
the LLM Wiki pattern — the single source of truth for how knowledge is organized.

## Architecture: Left Brain / Right Brain

The vault is split into two hemispheres plus shared core files:

- **Left Brain** (`left-brain/`): Work — analytical, structured, professional
  - `ballys/` — Full-time role at Ballys Interactive (AI R&D)
  - `contracts/` — Freelance/contract work (firewalled per client)
- **Right Brain** (`right-brain/`): Personal — creative, aspirational, life management
  - Six life domains: vision, health, finance, norms, growth, relationships
  - Plus: personal projects, journal
- **Shared Core** (vault root): Identity files that span both hemispheres

## Directory Map

```
vault/
├── SOUL.md                    # Agent identity, style, proactivity rules
├── USER.md                    # Frank's profile, all platforms, integration config
├── MEMORY.md                  # Key decisions, active context, lessons learned
├── HEARTBEAT.md               # What scheduled tasks monitor, notification rules
├── HABITS.md                  # Daily improvement pillars, streaks, history
│
├── left-brain/                # === WORK ===
│   ├── ballys/                # Full-time: AI Software Engineer, AI R&D
│   │   ├── index.md           # Ballys overview, data sources, project list
│   │   ├── inbox/             # Raw dumps from the Teams notes-to-self chat
│   │   │   └── YYYY-MM-DD.md
│   │   ├── daily/             # LEGACY — five April ai-news files; do not add to it
│   │   ├── projects/          # One file per active project
│   │   │   └── STATUS-DASHBOARD.md
│   │   ├── meetings/          # Meeting notes
│   │   │   └── YYYY-MM-DD-<topic>.md
│   │   ├── team/              # Team context
│   │   │   └── ai-rd.md
│   │   ├── portfolio/         # Master project index
│   │   │   └── index.md
│   │   └── sources/           # Work research material
│   │       ├── articles/
│   │       ├── screenshots/
│   │       └── data/
│   │
│   └── contracts/             # Freelance/contract work
│       ├── index.md           # All contracts, invoicing, rates
│       └── <client>/          # Per-client isolation
│
├── right-brain/               # === PERSONAL ===
│   ├── vision/                # Yearly plan & life direction
│   │   └── VISION.md          # The master plan (populated via planning grill)
│   ├── goals/                 # Goal tracking (year → quarter → month → week)
│   │   └── index.md
│   ├── health/                # Wellness tracking
│   │   └── tracker.md         # Gym, calories, weight, sleep, water
│   ├── finance/               # Personal finances
│   │   ├── index.md           # Budget, financial freedom plan, 50/30/20
│   │   ├── transactions/      # Monthly bank statement drops (CSV/PDF/XLSX)
│   │   │   └── YYYY-MM/
│   │   └── reports/           # Auto-generated monthly analysis
│   │       └── YYYY-MM-summary.md
│   ├── norms/                 # Values, faith, routines, boundaries
│   │   └── index.md
│   ├── growth/                # Learning, skills, books, courses
│   │   └── index.md
│   ├── relationships/         # Family, friends, network
│   │   └── index.md
│   ├── projects/              # Personal side projects
│   │   └── index.md           # All personal projects + GitHub repos
│   └── journal/               # Private reflections (separate from work logs)
│       ├── index.md
│       └── YYYY-MM-DD.md
│
├── daily/                     # CANONICAL work daily log (append-only). Hooks, reflect,
│   ├── YYYY-MM-DD.md          #   heartbeat and the morning brief all write here.
│   └── ai-news-YYYY-MM-DD.md
└── drafts/                    # CANONICAL draft store
    ├── active/
    ├── sent/
    └── expired/
```

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Work daily log | `daily/YYYY-MM-DD.md` | `daily/2026-04-14.md` |
| AI news | `daily/ai-news-YYYY-MM-DD.md` | `daily/ai-news-2026-04-14.md` |
| Work meeting | `left-brain/ballys/meetings/YYYY-MM-DD-<topic>.md` | `left-brain/ballys/meetings/2026-04-14-qodo-review.md` |
| Work project | `left-brain/ballys/projects/<kebab-case>.md` | `left-brain/ballys/projects/hackathon-platform.md` |
| Draft reply | `drafts/active/YYYY-MM-DD_<type>_<slug>.md` | `drafts/active/2026-04-14_email_al-review.md` |
| Self-chat dump | `left-brain/ballys/inbox/YYYY-MM-DD.md` | `left-brain/ballys/inbox/2026-10-01.md` |
| Contract client | `left-brain/contracts/<client-kebab>/` | `left-brain/contracts/bizos/` |
| Personal journal | `right-brain/journal/YYYY-MM-DD.md` | `right-brain/journal/2026-04-14.md` |
| Finance report | `right-brain/finance/reports/YYYY-MM-summary.md` | `right-brain/finance/reports/2026-04-summary.md` |
| Transaction drop | `right-brain/finance/transactions/YYYY-MM/` | `right-brain/finance/transactions/2026-04/` |

## Rules

1. **Never create files outside the vault** unless explicitly asked.
2. **kebab-case** for all filenames. No spaces, no camelCase.
3. **Daily logs are append-only.** Never edit past entries. Add new timestamped entries at the bottom.
4. **MEMORY.md stays under 100 lines.** If it grows beyond that, summarize and archive.
5. **Every project must appear in its index.** Work projects in `left-brain/ballys/portfolio/index.md`, personal projects in `right-brain/projects/index.md`.
6. **Cross-reference liberally** within the same hemisphere. Cross-hemisphere links are allowed but should be explicit (e.g., career goals in right-brain linking to Ballys projects in left-brain).
7. **Firewall contracts from Ballys.** Never reference contract client names/data in Ballys files.
8. **Firewall personal from work.** Work daily logs don't contain personal reflections; journal entries don't contain work tasks.
9. **Sources go in the appropriate hemisphere.** Work articles in `left-brain/ballys/sources/`, personal reading in `right-brain/growth/`.
10. **Draft lifecycle:** `active/` → `sent/` (if Frank replies) or `expired/` (after 24h).
11. **One topic per file.** Don't create catch-all files.
12. **Frontmatter optional but encouraged** for meetings, drafts, and journal entries.
13. **Dumps are not to-dos.** Lines in inbox/ are raw capture. Only a message prefixed todo: becomes a task.

## Core Files (Loaded Every Session)

These files are injected into every conversation via the SessionStart hook. Keep them concise:

- **SOUL.md** — Agent personality, rules, left/right brain awareness. ~70 lines max.
- **USER.md** — Frank's profile, all platforms, all integration config. ~120 lines max.
- **MEMORY.md** — Active decisions, deadlines, lessons. ~100 lines max.

## Index Maintenance

- `left-brain/ballys/portfolio/index.md` — Master catalog of all Ballys work projects
- `left-brain/contracts/index.md` — All contract work with invoicing
- `right-brain/projects/index.md` — Personal projects and GitHub repos
- `right-brain/goals/index.md` — Life goals across all six domains
- `right-brain/finance/index.md` — Financial freedom tracker and budget

Daily logs serve as the **append-only log** per hemisphere. Every significant action gets a timestamped entry in the appropriate log.

## When Creating New Files

1. Determine hemisphere: Is this work (left) or personal (right)?
2. If work: Is it Ballys or contract?
3. Check this schema for the correct directory and naming convention.
4. Add cross-references to related files.
5. Update the relevant index file.
6. If it doesn't fit any category, ask Frank.

## Finance Transaction Processing

When Frank drops files into `right-brain/finance/transactions/YYYY-MM/`:
1. Parse the file (CSV, PDF, or XLSX)
2. Categorize each transaction (needs/wants/savings)
3. Compare against budget in `finance/index.md`
4. Generate monthly report in `finance/reports/YYYY-MM-summary.md`
5. Update totals and trends in `finance/index.md`
