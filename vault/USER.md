# USER — Frank Enendu

## Profile

- **Name:** Frank Enendu
- **Email:** frank.enendu@ballysinternational.com
- **Role:** AI Software Engineer — AI R&D, Ballys Interactive (iGaming division)
- **Timezone:** GMT/BST (UK-based)
- **Working hours:** ~9 AM - 7 PM
- **Manager:** Al Jepps (alastair.jepps@ballysinternational.com)
- **Teammates:** Sudhanva Mysore Ganesh (s.mysoreganesh@ballys.com)
- **Projects directory:** /Users/frank.enendu/Documents/Projects
- **Second Brain:** /Users/frank.enendu/Documents/Personal/Second Brain Starter
- **Personal:** New father (baby born ~early Apr 2026), returned from paternity leave Apr 7
- **Wife:** Nnenna Enendu (age 28), not currently working
- **Age:** 31
- **Address:** Apartment 106, Doodson House, Dearmans Place, Salford, M3 5FN
- **Bank:** Lloyds (Classic account ending 3660)
- **Financial goal:** Net worth £1,000,000 by December 2032 (5-phase plan active)
- **Finance tracker:** vault/right-brain/finance/index.md
- **Elder brother:** Ebuka (Nigeria) — cosmetics business partner

## Platforms

### Microsoft Teams
- **Primary group chat:** AI R&D (thread: `19:02a862626ca54619b6babc5593aa33a3@thread.v2`)
- **Key contacts:** Al Jepps (manager), Sudhanva Mysore Ganesh (teammate), Lynn Murphy (admin/travel), Sherrine (coordination), Miguel Caron (hackathon org)
- **Monitor:** AI R&D group chat + all individual/DM conversations
- **Calendar:** Teams/Outlook Calendar — meetings, conferences, deadlines

### Outlook (Microsoft 365)
- **Use for:** Email management, calendar, draft replies to important messages
- **Shares auth with:** Teams (same Microsoft Entra app)
- **Common senders:** Al Jepps (team comms), Juan Impey (Inner Source pilot), Splunk alerts (noise — can be filtered)

### GitLab (Self-Hosted)
- **Instance:** gitlab.ballys.tech
- **Group:** igaming/ai-rd
- **Username:** frank.enendu
- **Task tracker project ID:** 8489
- **PAT:** stored in `.env` as `GITLAB_PAT`
- **Monitor:** Open MRs (assigned + review requested), issues, failed pipelines, boards
- **Issue board:** "Development" board (ID: 223)
- **Labels:** P0, P1, P2 priorities + `project::*` scoped labels

### GitHub
- **Username:** enendufrankc
- **Repos:** 82 repositories
- **Side projects:** govwatch.uk, bizOS, gstack
- **PAT:** stored in `.env` as `github_PAT`

### Obsidian
- **Vault location:** /Users/frank.enendu/Documents/Personal/Second Brain Starter/vault
- **Use for:** Notes, meeting records, project tracking, memory, AI news briefings
- **Plugins needed:** Daily Notes

### Cloud Storage
- OneDrive (work) / Google Drive (personal)

## Active R&D Projects (Work)

| Project | Local Path | GitLab Repo ID | Tracker Issues |
|---------|-----------|----------------|----------------|
| Hackathon Management Platform | `hackathon-management-platform` | 8175 | #13, #14 |
| Game Experience Prototype | `game_experience_agent` | 8248 | #11, #12 |
| R&D Prototype SSO/DNS | (shared infra) | — | #15 |
| Portfolio Optimisation Agent | — | — | #16 |
| Data Agent | — | — | #19 |
| Ballys Skills Repo | `R&D Skills Repo` | 8284 | — |
| Roadmap MCP | `Roadmap MCP + Agent` | 8275 | — |

## Other GitLab Projects (AI R&D Group)

evaluations-error-analysis, game-experience-pipeline, llm-router, prompts-library, ai-rd (group-level)

## Contract Work

| Client/Project | Local Path | Type |
|----------------|-----------|------|
| AI Business OS for SMEs | `~/Documents/Contract/AI Business OS for SMEs` | Full-stack (FastAPI + React + Terraform) |
| CaseReviewer | `~/Documents/Contract/CaseReviewer` | AI case review tool |
| Govwatch | `~/Documents/Contract/Govwatch` | Data analysis (Jupyter) |
| Tunnel Light (Lumina) | `~/Documents/Contract/Tunnel Light` | Project |

## Personal Projects

| Project | Local Path | Description |
|---------|-----------|-------------|
| Personal Copilot | `~/Documents/Personal/Personal-Copilot-Main` | AI-first personal planner (React Native + FastAPI) — Phase 2-3 of 6 |
| App Reviewer | `~/Documents/Personal/App Reviewer` | App review tool |
| SafeAI | `~/Documents/Personal/SafeAI` | AI safety project |
| FavAI | `~/Documents/Personal/FavAI` | Favourite AI tools |
| frankenendu.github.io | `~/Documents/Personal/frankenendu.github.io` | Personal website/portfolio |
| Agent Lib | `~/Documents/Personal/Agent Lib` | Agent library |
| EDC | `~/Documents/Personal/EDC` | Personal tools |

## Side Projects (GitHub)

- **govwatch.uk** — Government accountability platform
- **bizOS** — AI-powered business operating system for SMEs
- **gstack** — Personal tech stack/toolkit

## Drafting Criteria

### Draft a reply when:
- Email from a teammate or manager asking a direct question
- Teams DM that requires a substantive response (not just "ok" or emoji)
- GitLab MR comment requesting changes or clarification

### Skip drafting when:
- Automated notifications (CI/CD, bot messages, Splunk alerts)
- FYI-only emails (newsletters, announcements)
- Messages already replied to
- Group chat messages that are general discussion (not directed at Frank)

## Personal Emails

- **Gmail:** (to be connected — personal primary)
- **Yahoo Mail:** (to be connected — personal secondary)

## Integration Config

### Left Brain (Work)
- **GitLab PAT:** in `.env` as `GITLAB_PAT` — gitlab.ballys.tech
- **M365 connector:** Read-only (email search, calendar search, Teams chat search, read_resource)
- **Work directory:** `~/Documents/Work/` (mounted in Cowork via ~/Documents)
- **Claude in Chrome:** Available for browser-based actions (Outlook, Teams Web, GitLab UI, Support Hub)

### Right Brain (Personal)
- **GitHub PAT:** in `.env` as `github_PAT` — github.com/enendufrankc
- **Gmail:** (pending connection)
- **Yahoo Mail:** (pending connection)
- **Finance:** Transaction drops in `vault/right-brain/finance/transactions/`

### Shared
- **Documents mount:** `~/Documents` (full access — Work, Contract, Personal folders)
