---
type: meeting-note
title: "Interview — Senior AI Engineer (AI/ML R&D)"
date: 2026-08-14
project: "General"
attendees: "Frank Enendu, Sudhanva Mysore Ganesh, Serhii (candidate)"
source: teams-transcript
---

# Interview — Senior AI Engineer (AI/ML R&D) — 2026-08-14

## Attendees
- Frank Enendu
- Sudhanva Mysore Ganesh
- Serhii (candidate)

## Summary
Technical interview (1h 4m) for the Senior AI Engineer role in AI/ML R&D. Candidate walked through his AI writing engine ("Second Draft") at Cardinal 40 and an earlier computer-vision project for public transport, then took a system design question on ticket categorisation. Second half was candidate questions about how the R&D team works.

## Key Decisions
- Take-home assignment is the next stage, but format not yet agreed — Frank noted it still needs an idea, HR input and Al's approval
- No decision made on start date; deferred to HR

## Action Items
- [ ] Frank / HR: Reach out to candidate with outcome and next steps
- [ ] Frank: Agree take-home assignment scope with Al and HR before issuing
- [ ] Frank: Confirm expected start date with HR

## Notes
- Candidate background: ~4.5 yrs — computer vision/GPU work at a transport-tech startup (YOLOv3, ~500GB/day, 220 buses), now leading two branches at Cardinal 40 (AI writing engine + thought-leadership research published in Axios)
- Stack: Go backend, React front end, Python microservices, Pinecone vector DB, MySQL/Postgres, Heroku + Railway hosting, Langfuse tracing with a custom observability wrapper for non-engineers
- Strong on prompt-hash/cosine-similarity caching, LLM-as-judge, regression detection via similarity thresholds; mentioned DSPy for prompt optimisation
- Gaps: no Terraform / infra-as-code experience, limited direct AWS (Heroku only) — said he'd be happy to certify; little MCP or custom-skill authoring
- Workflow: Codex over Claude Code, markdown files for task/research/results tracking, PR + AI code review with manual review, opinionated on minimal tests for throwaway scripts and TDD for production
- Design answer: sequential agent pipeline first (metadata extraction → scoring → CMS tool-call agent → classifier), evolve to orchestrator only where failures justify it; would benchmark model-per-agent combinations
- Team context shared with candidate: full AWS account, VPC restrictions, GenAI/SecOps approval flow for new tools, 271 prototypes awaiting deployment (clearing ~50% in six months framed as success), yearly company-wide hackathon on Frank's platform
- Candidate is Manchester-based
