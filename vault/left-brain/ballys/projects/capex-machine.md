---
project: Capex Machine
type: ballys-project
priority: P1
status: Planning Complete
criticality: Low
owner: Frank Enendu
gitlab_repo: capex-epic-workflow
local_path: ~/Documents/Work/AI and R&D/Capex Epic Workflow
production_url: https://d33ahnpeio0pjn.cloudfront.net/
intended_domain: https://classify-epic.ballys.tech
gitlab_issues: none
due_date: 2026-05-16
pit_sso: done
pit_dns: pending
pit_cert: pending
last_updated: 2026-04-22
---

# Capex Machine (Epic Classifier)

## Overview
AI-powered Teams bot that classifies Jira epics as CAPEX or OPEX using RAG-based policy retrieval and Claude 3 Sonnet. Reduces classification inconsistencies between Product and Finance departments through policy-grounded AI recommendations.

## Status
- **Stage:** Planning complete, ready for implementation
- **PIT Status:** SSO configured, but DNS and certificate NOT configured yet
- **In Use:** Yes (prototype)
- **Model fix:** Switched model for Chris Benstead — error resolved (Apr 15). Chris confirmed working: "Back of the net! Thanks Frank!"

## Tech Stack
- **Backend:** Python 3.11+, FastAPI, AWS Lambda (container image)
- **AI:** LLM provider abstraction (supports Gemini or OpenAI-compatible gateway — model was recently switched for Chris Benstead)
- **RAG:** FAISS index (3072-dim), boosts external policy docs by 10%. PII sanitize → retrieve → classify → restore pipeline
- **Database:** PostgreSQL RDS + Redis ElastiCache
- **Auth:** Microsoft Bot Framework
- **Infrastructure:** AWS (Lambda, API Gateway, Bedrock, OpenSearch, ElastiCache, RDS, S3)
- **IaC:** Terraform
- **Observability:** Opik
- **Testing:** pytest with 80%+ coverage requirement

## Success Metrics
- 90%+ agreement with Finance classifications
- <5s p95 latency
- 80%+ user satisfaction

## Specification
- 5 user stories, 52 functional requirements
- Constitution v1.0.0 defined

## Milestones
- [x] Planning complete
- [x] 5 user stories defined
- [x] 52 functional requirements documented
- [x] SSO configured
- [x] Constitution v1.0.0 defined
- [ ] DNS: classify-epic.ballys.tech
- [ ] SSL certificate
- [ ] Chris request: Epic AI tool Jira Cloud integration — needs steer on implementation timing given Jira Cloud migration (awaiting Richard Duffy input)
- [ ] Implementation sprint
- [ ] Testing
- [ ] Production deploy
