# AI R&D Weekly Update — Style Guide & Progress Archive

> Extracted from Al Jepps' **Weekly Update 2026.docx** (SharePoint), covering 9 Jan – 9 Oct 2026.
> Purpose: teach any agent how to write Frank's AI R&D section in the iGaming weekly update, and provide the full progress arc for context.

---

## 1. Document Structure (Al's format)

The iGaming weekly update is a **Word doc** with these fixed sections:

```
iGaming Weekly Update DD/MM/YYYY

Executive Summary
  [one paragraph per team — DFG, Solaris, Bingo, AI R&D, Infinity, Nightwatch, Thunderbird, Athena, Live Dealer]

Upcoming Releases & Milestones
  [bullet list, with an AI R&D sub-list]

Links to Demos & Prototypes:
  [bullets]

Development Deep-Dive
  [team sections, each with Completed: / In Progress: sub-lists]
  
  Adaptive Layouts (AI R&D)
    Completed:
      • ...
    In Progress:
      • ...
  
  Data Agent + Game Experience (AI R&D)
    Completed:
      • ...
    In Progress:
      • ...
  
  AI Transformation tracker (AI R&D)
    ...

Issues, Blockers & Risks
  Immediate Blockers:
  Potential Risks:
  External Dependencies:

Next Week's Focus
  Primary Objective:
    AI R&D – [one-liner focus areas]
  Key Deliverables:

Team & Capacity
  [who's off, hiring, etc.]
```

## 2. Executive Summary — AI R&D Paragraph Style

**Length:** 2–5 sentences, 40–120 words. One paragraph, no bullets.

**Voice:** Confident, evidence-based, delivery-focused. Not promotional. Uses specific metrics and named deliverables. No hedging language ("hopefully", "we believe") — state what happened.

**Structure pattern (learned from 30+ weeks):**

1. **Lead with the biggest win or milestone** of the week (shipped, went live, demoed, presented).
2. **Name the workstream** explicitly: "Adaptive Layouts", "Game Experience Agent", "AI Radar", "AI Transformation Tracker", "Hackathon Platform", "AI Field Notes / Interview Engine", "AI Tooling / Developer Tooling", "Bally's Skills Repo".
3. **Attach a concrete metric** where possible: game counts, cluster numbers, pipeline status, user percentages, MR numbers.
4. **If something is blocked or at risk**, state it plainly at the end of the paragraph, not at the start.
5. **If nothing shipped**, lead with what advanced: "progressed on", "moved forward", "focused on".

**Tense:** Past tense for done work. Present continuous for in-flight ("is rolling out", "is underway"). Future only in the Next Week's Focus.

**Common phrasings (from the corpus):**

| Action | Phrasing |
|---|---|
| Shipped to prod | "shipped to production", "is now live", "went live", "deployed to production" |
| Milestone hit | "hit a major milestone", "cleared its last pre-staging gate", "now has a published go-live plan" |
| Pipeline green | "pipelines are green", "AI Pipelines are green in staging and production" |
| Demo/presentation | "demoed at PLT/TLT", "presented at the Tech Series", "demoed to commercial" |
| Handover | "on the Nightwatch handover path", "handover to the Nightwatch team is done" |
| A/B / rollout | "live for 1% of users", "moved from synthetic to production validation" |
| Agent/tool built | "built from scratch in one week", "now covers the full Loop" |
| Collaboration | "working with Intralot on", "joint Hackathon proposal" |
| Risk/blocker | "commercial uplift remains unproven", "SME review time... tracked as owned actions" |
| No big win | "focused on go-live readiness this week", "progressed on three fronts" |

## 3. Deep-Dive Section Conventions

The AI R&D deep-dive has **evolved over time**. Current (Oct 2026) standard sections:

| Section | What goes in it |
|---|---|
| **Adaptive Layouts (AI R&D)** | Frank's R&D work: clustering, pipelines, back-office, evaluations, go-live gates |
| **Data Agent + Game Experience (AI R&D)** | Game DNA capture, profiling, dimensions, evaluation engine, NCR |
| **AI Transformation tracker (AI R&D)** | Radar, Tracker App, MCP integration, portfolio management |
| *(as needed)* Game Ideation, Hackathon, Skills Repo, AI Tooling, Interview Engine |

Each has **Completed:** and **In Progress:** bullet lists. Items are:
- **One line per deliverable**, ≤ 20 words if possible
- **Include MR/issue numbers** where relevant
- **Include metrics**: "146 games processed", "9→5 dimensions", "50 clusters"
- **No vague items**: not "continued work" or "made progress" — say what specifically

## 4. Next Week's Focus — AI R&D Line

Format: `AI R&D – [2–4 focus areas separated by commas]`

Examples from the corpus:
- `AI R&D – AI agents discovery, progress Hackathon testing & Adaptive Layouts`
- `AI R&D – Adaptive layouts, AI radar, Game ideation and Prototyping platform`
- `AI R&D – Model benchmarks, workshop and Game ideation`
- `AI R&D – Adaptive Layouts, AI Agents & Roadmap agent`
- `AI R&D – Adaptive layouts quality improvement, go-live plan`

## 5. Progress Arc (9 Jan – 9 Oct 2026)

### Adaptive Layouts — the dominant arc
| Week | Status |
|---|---|
| Jan | ADR Global Section Catalog proposed; schema population pipeline (9× LLM reduction) |
| Feb | E2E demo running; clustering on 1M dataset → 50 clusters; CX team approved personas |
| Mar | Contentful sync + recommender MRs raised; back-office tool started; auto-clustering research |
| Apr | Production debugging; back-office tool architecture; Claude Code vs Pi agent experiment |
| May | Back-office tool built; Pi multi-agent orchestration; MCP integration for Tracker+Radar |
| Jun | Back-office handover to Nightwatch; lobby lambda build starts |
| Jul | Go-live plan published (6 gates); LLMOps/Opik tracing; evaluation harness designed |
| Aug | Final MR up with evaluations + gates; SME review; error analysis live |
| Sep | **LIVE at 1%**; monitoring green; A/B results: no stat-sig difference (commercial uplift unproven) |
| Oct | 5% UK step approved 1 Oct; Spain 5% ~end Oct; budget flag from Marcos |

### Game Experience Agent / Game DNA
| Week | Status |
|---|---|
| Jan–Feb | Manual profiling → AI analysis validation; 30→115→1000+ games |
| Mar–Apr | Dimensionality decompression 9→5/6; full-catalogue profiling |
| May–Jun | Capture pipeline built (85% on experiment sample) |
| Jul–Aug | Nightly video capture: 156→264 games filmed |
| Sep | 76 games validated; £10.31m GP projection modelled |
| Oct | Al's review: ~80% there; rework rubric dims + drop numeric embeddings |

### AI Radar / Transformation Tracker
| Week | Status |
|---|---|
| Mar | Tracker shipped to prod (built in 1 week); 7 views, KPI tracking |
| Apr–May | Radar deployed; MCP integration; streaming chatbot + Opik |
| Jun | Location/Area filters; Portfolio Pulse MCP; Vision Board beta |
| Jul | Auto Jira epic creation; portfolio pruning process |
| Aug | Follow/unfollow; lifecycle tooling; Game Ops as first product |

### Hackathon Platform
| Week | Status |
|---|---|
| Jan | MVP V1 deployed; proposal submitted |
| Feb | UAT done; Team Arena feature |
| Mar–Apr | Infra migration; Ignite prep |
| May | Ignite ran (London); submissions analysed |
| Oct | Q4 Hackathon event created on hackathon.ballys.com |

### AI Tooling / Developer Tooling
| Week | Status |
|---|---|
| Feb | Claude Code first cohort; Skills Repo built |
| Mar | Skills Repo live with website; SSO/DNS for prototypes |
| Jun | AI Gateway + Claude Code rollout to ~230 engineers |
| Jul | Model benchmarking workbench |
| Aug | Engineering Loop covers full Loop; iGaming pitch deck ready |

### Interview Engine / AI Field Notes
| Week | Status |
|---|---|
| Jul | 6 interviews complete; live public website |
| Aug | Hardened practice assessor; automated rubric capture |
| Oct | 6 UX handoff issues raised; !54 merged and deployed |

### Game Ideation Agent
| Week | Status |
|---|---|
| Feb | Brainstorming started |
| Jun | Plan approved, in build |
| Jul | Stakeholder conversations; NCR next |
| Aug | NCR presented at Tech Series |
| Oct | Vision board live; 3 MRs merged; NCR estimate drafted |

---

## 6. Frank's Teams Chat Format (simpler)

In the **AI Interlock Teams channel**, Frank uses a different, shorter format (not the Word doc):

```
**Weekly Update — Frank**
Week commencing [date]

**Shipped this week**
- **[Project].** [What shipped, with metric/MR if relevant]

**In flight**
- **[Project].** [What's in progress, what's blocking]

**Blocked / needs decision**
- [Item requiring Frank or someone else's input]
```

This is **Frank's own format**, not Al's. The Word doc is Al's iGaming-wide update that goes to senior stakeholders; the Teams message is Frank's R&D-team-internal update.

---

_Extracted 9 Oct 2026 from `/Users/frank.enendu/Downloads/Weekly Update 2026.docx`_
= 40 weeks of AI R&D updates, Jan–Oct 2026._
