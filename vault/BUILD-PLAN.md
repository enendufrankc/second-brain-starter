# Second Brain — Master Build Plan

> The roadmap for building out Frank's complete second brain.
> Created: 2026-04-14
> Last updated: 2026-04-19
> Status: Phase 1 COMPLETE ✅ (with automation caveats) — Phase 2 next

## Build Order

### Phase 1: Ballys 360 (Left Brain — Full-Time Work)
**Goal:** Give the second brain complete knowledge of every Ballys project, so it can manage, track, and surface insights across all of them.

**Steps:**
1. Walk through every project in `~/Documents/Work/` one by one
2. For each: read READMEs, key files, understand purpose/status/tech stack
3. Create vault project files for each in `left-brain/ballys/projects/`
4. Cross-reference with GitLab issues, MRs, and pipelines
5. Build a comprehensive STATUS-DASHBOARD with live health for all projects
6. Map team relationships and responsibilities
7. Set up automated monitoring (scheduled tasks for pipeline/MR/issue tracking)

**Data Sources:** Work directory, GitLab API, Teams, Outlook, Calendar

---

### Phase 2: Contracts 360 (Left Brain — Contract Work)
**Goal:** Full knowledge of every contract engagement — projects, clients, deliverables, status.

**Steps:**
1. Walk through every project in `~/Documents/Contract/` one by one
2. For each: understand the client, deliverables, tech stack, current status
3. Create per-client tracking files in `left-brain/contracts/`
4. Set up invoicing/payment tracking
5. Map deadlines and deliverables
6. Connect to relevant GitHub repos if applicable

**Data Sources:** Contract directory, GitHub (personal repos)

---

### Phase 3: Personal Projects 360 (Right Brain — Projects)
**Goal:** Full knowledge of every personal side project — what it is, where it lives, what stage it's at.

**Steps:**
1. Walk through every project in `~/Documents/Personal/` one by one
2. For each: understand purpose, tech stack, progress, next steps
3. Update `right-brain/projects/index.md` with rich detail
4. Create individual project files for active ones
5. Connect to GitHub repos (enendufrankc)
6. Prioritize — which projects deserve time vs which are dormant

**Data Sources:** Personal directory, GitHub

---

### Phase 4: Life Goals & Personal Vision (Right Brain — Vision)
**Goal:** Define what Frank wants his life to look like — yearly goals, quarterly milestones, what matters most.

**Steps:**
1. Run the yearly planning grill (structured interview across all life domains)
2. Populate VISION.md with concrete goals and milestones
3. Break down into quarterly → monthly → weekly objectives
4. Set up weekly review cadence
5. Create the yearly-planning-grill skill for future use

**Data Sources:** Conversation with Frank

---

### Phase 5: Acts of Piety (Right Brain — Norms & Faith)
**Goal:** Plan and structure Frank's spiritual practices — daily, weekly, and seasonal. This is a top priority.

**Steps:**
1. Deep conversation about Frank's faith practices, obligations, and spiritual goals
2. Build a structured daily/weekly/seasonal schedule of acts of piety
3. Integrate with calendar and daily routines
4. Set up gentle reminders and tracking
5. Create a dedicated piety planner in `right-brain/norms/`
6. Ensure work scheduling respects prayer times and spiritual commitments

**Data Sources:** Conversation with Frank

---

### Phase 6: Finance (Right Brain — Finance)
**Goal:** Complete financial clarity — earnings, expenses, budget, savings targets, path to financial freedom.

**Steps:**
1. Deep conversation about Frank's financial picture (income streams, expenses, debts, goals)
2. Set up the 50/30/20 budget framework with real numbers
3. Frank drops first month's transactions into `finance/transactions/`
4. Build the transaction analyzer script (parse CSV/PDF, categorize, report)
5. Create financial freedom roadmap with milestones
6. Set up monthly finance review cadence
7. Track contract income separately from salary

**Data Sources:** Conversation with Frank, bank statement drops

---

### Phase 7: Fitness & Working Out (Right Brain — Health)
**Goal:** Plan Frank's workout journey — routine, nutrition, tracking, progress.

**Steps:**
1. Conversation about fitness goals, current level, available time, gym access
2. Build a workout plan (or integrate an existing one)
3. Set up tracking in `right-brain/health/tracker.md`
4. Calorie/nutrition targets
5. Weekly check-in cadence
6. Connect workout schedule to calendar (block gym time)

**Data Sources:** Conversation with Frank

---

### Phase 8: YouTube Channels (Right Brain — Projects + Growth)
**Goal:** Plan and automate the launch and management of 2 YouTube channels.

**Steps:**
1. Conversation about channel topics, target audience, content strategy
2. Create a content calendar and production pipeline
3. Plan automation: scripting, scheduling, thumbnail generation, SEO
4. Set up tracking for both channels
5. Connect to YouTube API (future integration)
6. Build content idea backlog and publishing schedule

**Data Sources:** Conversation with Frank, YouTube (future integration)

---

## Current Status

| Phase | Name | Status | Notes |
|-------|------|--------|-------|
| 0 | Vault Restructure (Left/Right Brain) | DONE | Completed 2026-04-14 |
| 1 | Ballys 360 | DONE | 16 projects tracked, dashboard + deadlines + 11 scheduled tasks, 5 meeting notes, team file with 20+ contacts, CLAUDE.md cross-referenced. Caveats: automation reliability (see HEARTBEAT.md Known Issues), Outlook connectors intermittent, GitLab PAT needs renewal |
| 2 | Contracts 360 | NEXT | Start by scanning Contract directory |
| 3 | Personal Projects 360 | Pending | After Contracts |
| 4 | Life Goals & Vision | Pending | Planning grill conversation |
| 5 | Acts of Piety | Pending | High priority — Frank's top personal value |
| 6 | Finance | Pending | Earnings, expenses, financial freedom plan |
| 7 | Fitness & Working Out | Pending | Workout planning and tracking |
| 8 | YouTube Channels | Pending | 2 channels — plan and automate |

## Principles

- **Build incrementally.** Each phase is self-contained and valuable on its own.
- **Conversation first.** Phases 4-8 require deep conversations with Frank, not just scanning files.
- **Automate what repeats.** Scheduled tasks, scripts, and skills for anything that runs regularly.
- **Respect the firewall.** Ballys, contracts, and personal stay separated. No data leaks between hemispheres.
- **Frank drives.** The second brain suggests, Frank decides. Especially for personal/faith/finance.
