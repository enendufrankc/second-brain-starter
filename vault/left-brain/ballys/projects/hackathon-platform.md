---
project: Hackathon Management Platform
type: ballys-project
priority: P0
status: Production
criticality: High
owner: Frank Enendu
local_path: ~/Documents/Work/Hackathons/Hackathon V2
production_url: https://hackathon.ballys.com
intended_domain: https://hackathon.ballys.com
gitlab_issues: "#13, #14"
due_date: 2026-04-17
pit_sso: done
pit_dns: done
pit_cert: done
pit_myapp: pending
last_updated: 2026-05-25
---

# Hackathon Management Platform

## Overview
AI-powered hackathon management platform — idea submission to winner selection. Smart duplicate detection (pgvector), skill-based team formation, two-stage evaluation, People's Choice voting, innovation pipeline to graduate winning ideas.

## Status
- **Production:** Live at https://hackathon.ballys.com
- **PIT Status:** SSO configured, DNS and certificate attached. App NOT in My App yet.
- **In Use:** Yes — company-wide
- **Next Event:** Ignite Hackathon (Apr 29-30)
- **Business Travel:** TB-13831 approved by Al Jepps (Apr 16)

## Urgent
- **Issue #13 (Migrate to scalable infrastructure) — OVERDUE (was Apr 17)**
- Scoring system currently hardcoded — Al requested it be made dynamic so organisers control criteria during event creation
- Ignite Apr 29-30 — **9 days away**
- **Email domain mismatch bug:** Eduardo couldn't see Ruben's idea — role was assigned to @gamesys.com but user authenticated with @ballysinternational.com (Entra AD). Frank fixed Eduardo's manually (Fri Apr 17) but general fix still needed before Ignite to avoid same issue with other users
- Prototyping session with Craig Staples today (Mon Apr 20, 9:30 AM) — Al set up to help Craig prototype features

## Tech Stack
- **Frontend:** React 18 + TypeScript + Vite + TailwindCSS, Zustand, Headless UI
- **Backend:** FastAPI 0.110+, SQLAlchemy 2.0 async, Alembic, Celery 5.3+
- **Database:** PostgreSQL 16 + pgvector
- **Cache/Queue:** Redis 7
- **AI:** Google Gemini 2.0 Flash
- **Auth:** Microsoft Entra ID via MSAL
- **Infra:** AWS EC2 t3.medium, ALB, S3, SSM, Docker Compose, Nginx
- **CI/CD:** GitLab CI
- **Observability:** Opik

## Key Features
- Multi-event support, AI idea processing, RBAC, team formation
- Multi-channel notifications (email, in-app, Teams)
- Evaluation: assessors > reviewers > judges > consensus
- People's Choice Arena (Elo rating)

## Strategic Direction (from MEMORY.md, Apr 14)
- RFC created for "Intralot Lab" Phase 3 — always-on innovation registry (hackathons as one module)
- Platform name: "Bally Intralot Lab"
- Buyer: CTO/CDO/AI transformation owner
- Two-phase strategy: Phase 1 (no dev — config + seeding + adoption), Phase 2 (showcase gallery, recognition, analytics)
- Phase 2 gaps: upvotes/views, contributor profiles, showcase gallery, lightweight forms, per-person analytics, comments
- Adoption plan: seed 20-30 projects before launch, get executive sponsor
- Pre-build intent submissions required (duplicate detection before effort)

## Milestones
- [x] Core platform built and deployed
- [x] SSO configured via Entra ID
- [x] DNS and certificate attached
- [x] Multi-event support live
- [x] People's Choice Arena implemented
- [ ] Get app added to My App portal
- [ ] Migrate to scalable infrastructure (#13) — **DUE APR 17**
- [x] Make scoring system dynamic (currently hardcoded) — Al Jepps request
- [x] Ignite Hackathon setup and dry run (Apr 29-30) (#14)
- [x] Add Ignite to Outlook calendar
- [x] Rebranding: Ballys → Intralot ✅ 2026-04-22
- [x] Send Ignite Hackathon broadcast message ✅ 2026-04-22
- [ ] Get app listed on AccessHub
- [x] Post-Ignite retrospective and v3 planning ✅ 2026-05-05 (post-mortem done, scoring finalized)
- [ ] #41 IGNITE Showcase on S3 + CloudFront (assigned by Al, May 7) — IGNITE-blocking
