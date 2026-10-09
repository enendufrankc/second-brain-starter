---
type: backlog-review
title: Weekly Backlog Review — 2026-08-10
description: Automated Monday backlog review. Frank not present (10th consecutive run). No milestone confirmations obtained; no project files changed.
resource: vault/left-brain/ballys/daily/2026-08-10-backlog-review.md
tags: [ballys, backlog, review, automated]
timestamp: 2026-08-10
---

# Weekly Backlog Review — Monday 10 Aug 2026

**Frank not present.** This is the **10th consecutive Monday** the review has run unattended. Step 3 (interview) and step 5 (apply updates) were skipped — updating milestones without Frank's confirmation would fabricate state. No project file was modified.

**Delta vs 3 Aug run:** +7 days on every overdue counter. Zero vault edits since 6 May 2026 (**96 days**). Nothing else changed.

---

## Scope scanned

18 files with `type: ballys-project`. **87 open milestones.** 13 have a due date — **all 13 are overdue.** 5 have no due date at all.

## Overdue (all dates are stale frontmatter, not confirmed slippage)

| Project | Pri | Status | Was due | Overdue |
|---|---|---|---|---|
| ai-rd-tracker | P1 | Active | 2026-04-11 | 121d |
| game-experience-prototype | P0 | Awaiting Review | 2026-04-16 | 116d |
| ballys-skills-repo | P1 | Active Development | 2026-04-17 | 115d |
| conference-writeup | P1 | Complete | 2026-04-17 | 115d |
| hackathon-platform | P0 | Production | 2026-04-17 | 115d |
| rd-prototype-sso-dns | P2 | Deprioritised | 2026-04-20 | 112d |
| portfolio-optimisation-agent | P0 | Scoping | 2026-04-25 | 107d |
| data-analyst-agent | P1 | Active | 2026-04-30 | 102d |
| error-analysis | P2 | Deprioritised | 2026-05-09 | 93d |
| roadmap-mcp | P2 | Active | 2026-05-09 | 93d |
| capex-machine | P1 | Planning Complete | 2026-05-16 | 86d |
| tableau-mcp-agent | P2 | Active | 2026-05-23 | 79d |
| video-analysis | P3 | Validation Phase | 2026-05-30 | 72d |

## No due date

`ai-rd-user-access` (P1, Not Started, 5 open) · `ballys-prototyping-platform` (P1, Active, 9 open — most open items in the vault) · `game-ideation-agent` (P2, Concept, 6 open) · `jira-documentation-agent` (P2, Prototype, 3 open) · `rd-catalogue` (P3, Early Development, 4 open)

## Data-quality problems (unchanged, 10 weeks running)

1. **Every due date is stale.** The dashboard's "Overdue" panel is 100% noise — it flags all 13 dated projects, so it carries no signal. One re-dating pass would restore it.
2. **`conference-writeup`** is `status: Complete` with 4 open milestones, including "Complete remaining 13 session write-ups". Either the status or the checkboxes are wrong.
3. **Deprioritised P2s still counted.** `rd-prototype-sso-dns` and `error-analysis` contribute 10 open items to dashboard totals despite being dropped. Archive them.
4. **Al's 21 Apr access decision never propagated.** Nine SSO/DNS/SSL milestones across `data-analyst-agent`, `error-analysis`, `roadmap-mcp`, `rd-prototype-sso-dns` and `game-experience-prototype` are open, but the decision was "no SSO for demos". Most of these should be struck, not done.
5. **`hackathon-platform`** shows `status: Production` while #13 (infra migration) and #41 (IGNITE showcase on S3+CloudFront) are still unchecked.

## Long-silent dependencies

- **Al Jepps — Game Experience review:** waiting since 22 Apr (~16 weeks). This is a P0 blocked on one review.
- **Bhav — Stadium repo access + Storybook link:** promised 22 Apr, silent ~110 days. Blocks the whole Prototyping Platform (9 open items).
- **Mark Webster** (Roadmap MCP testing), **Richard Duffy** (Capex Machine / Jira Cloud steer), **Dez Pazmany** (Tableau collab): all last touched in April.

## Personal (from MEMORY.md)

- **Life insurance: ~104 days overdue.** Single-income family, wife and infant son. ~20 minutes on comparethemarket.com. Flagged in every review since May.
- **Finance review blocked 4 months straight** (Apr–Jul statements never uploaded). Next review 1 Sep — will be a 5th consecutive block unless statements land or the format switches to an auto bank-feed / no-statements Q&A.

---

## Recommendation

**Pause or delete this scheduled task.** Ten identical unattended reports have produced zero vault changes. The task is designed around a live interview it never gets, and each run adds a file to `daily/` while dropping the signal-to-noise of the dashboard further. Better options: (a) re-point it at GitLab activity so it can report real movement without Frank, or (b) turn it off until a live session resets the backlog.

**If Frank gets 30 minutes this week**, the highest-leverage sequence is: buy life insurance (20 min, protects the family) → chase Al on the Game Experience review (1 message, unblocks a P0) → chase Bhav for Stadium access (1 message, unblocks 9 items) → one bulk re-dating pass on frontmatter.
