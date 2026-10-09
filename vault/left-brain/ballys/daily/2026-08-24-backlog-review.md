# Weekly Backlog Review — Monday 24 Aug 2026

**Frank not present.** Step 3 (interview) and step 5 (apply updates) were skipped — updating milestones without Frank's confirmation would fabricate state. No project file was modified.

**Delta vs 10 Aug run:** +14 days on every overdue counter (no run/report was generated 17 Aug, so this covers a two-week gap). Zero vault edits in 91 days (last project-file edit was `hackathon-platform.md` on 25 May; `STATUS-DASHBOARD.md` last touched 1 Jun). Nothing else changed.

---

## Scope scanned

18 files with `type: ballys-project`. **87 open milestones** (unchanged). 13 have a due date — **all 13 are still overdue.** 5 have no due date at all.

## Overdue

| Project | Pri | Status | Was due | Overdue |
|---|---|---|---|---|
| ai-rd-tracker | P1 | Active | 2026-04-11 | 135d |
| game-experience-prototype | P0 | Awaiting Review | 2026-04-16 | 130d |
| ballys-skills-repo | P1 | Active Development | 2026-04-17 | 129d |
| conference-writeup | P1 | Complete | 2026-04-17 | 129d |
| hackathon-platform | P0 | Production | 2026-04-17 | 129d |
| rd-prototype-sso-dns | P2 | Deprioritised | 2026-04-20 | 126d |
| portfolio-optimisation-agent | P0 | Scoping | 2026-04-25 | 121d |
| data-analyst-agent | P1 | Active | 2026-04-30 | 116d |
| error-analysis | P2 | Deprioritised | 2026-05-09 | 107d |
| roadmap-mcp | P2 | Active | 2026-05-09 | 107d |
| capex-machine | P1 | Planning Complete | 2026-05-16 | 100d |
| tableau-mcp-agent | P2 | Active | 2026-05-23 | 93d |
| video-analysis | P3 | Validation Phase | 2026-05-30 | 86d |

## No due date

`ai-rd-user-access` (P1, Not Started, 5 open) · `ballys-prototyping-platform` (P1, Active, 9 open — most open items in the vault) · `game-ideation-agent` (P2, Concept, 6 open) · `jira-documentation-agent` (P2, Prototype, 3 open) · `rd-catalogue` (P3, Early Development, 4 open)

## Data-quality problems (unchanged, ~12 weeks running)

1. Every due date is stale — the dashboard's "Overdue" panel is 100% noise; one re-dating pass would restore its signal.
2. `conference-writeup` is `status: Complete` with 4 open milestones. Status/checkboxes disagree.
3. Deprioritised P2s (`rd-prototype-sso-dns`, `error-analysis`) still contribute 10 open items to dashboard totals. Consider archiving.
4. Al's 21 Apr access decision ("no SSO for demos") never propagated — nine SSO/DNS/SSL milestones across four project files are still open.
5. `hackathon-platform` shows `status: Production` while #13 and #41 remain unchecked.

## Long-silent dependencies

- **Al Jepps — Game Experience review:** waiting since 22 Apr (~18 weeks).
- **Bhav — Stadium repo access + Storybook link:** promised 22 Apr, silent ~124 days. Blocks Prototyping Platform (9 open items).
- **Mark Webster, Richard Duffy, Dez Pazmany:** all last touched in April.

## Personal (from MEMORY.md)

- **Life insurance:** was ~104 days overdue as of 10 Aug; now ~118 days overdue, unconfirmed. Single-income family, wife and infant son.
- **Finance reviews:** blocked 4 consecutive months (Apr–Jul statements never uploaded). The 1 Sep review is due in a week — will be a 5th consecutive block unless statements are uploaded or the format changes.

---

## Recommendation

Unchanged from the last several runs: **pause, delete, or re-scope this scheduled task.** It has now produced ~12 weeks of identical unattended reports with zero vault movement — the interview step this task depends on never happens because Frank isn't in a live session on Monday mornings. Two paths forward: (a) re-point it at GitLab activity so it can report real signal without needing Frank present, or (b) switch it to a passive report-only mode (drop the AskUserQuestion interview) until a live session resets the backlog.

**If Frank gets 30 minutes this week:** life insurance (20 min, protects the family) → chase Al on Game Experience review (unblocks a P0) → chase Bhav for Stadium access (unblocks 9 items) → one bulk re-dating pass on frontmatter → upload Apr–Aug bank statements before the 1 Sep review.
