---
type: concept
title: LLM Wiki + OKF — Building Knowledge That Compounds
description: Synthesis of Karpathy's LLM Wiki pattern and Google's Open Knowledge Format, and what they mean for how my second brain is built and maintained.
resource: null
tags: [knowledge-management, ai, second-brain, llm-wiki, okf, methodology]
timestamp: 2026-07-13T09:00:00Z
---

# LLM Wiki + OKF — Building Knowledge That Compounds

A synthesis of two sources ingested 2026-07-13:
[Karpathy's LLM Wiki](../sources/2026-07-13-karpathy-llm-wiki.md) and
[Google's Open Knowledge Format](../sources/2026-07-13-okf-open-knowledge-format.md).

## The one-sentence takeaway

Karpathy describes **how** to build knowledge that compounds (an LLM continuously maintains a
persistent, interlinked markdown wiki); Google's OKF defines **the shared format** that makes
such a wiki portable between tools, teams, and agents. Together they're the "why" and the
"how" of exactly what my second brain already is — and they close the loop by giving it a
standard to conform to.

## Why they belong together

| | LLM Wiki (Karpathy) | OKF (Google) |
|---|---|---|
| Nature | A *pattern / philosophy* | A *specification / format* |
| Answers | How do I maintain compounding knowledge? | How do I make it interoperable? |
| Owner of the wiki | The LLM (you curate, it maintains) | Producer-independent (human or agent) |
| Key mechanism | Ingest → Query → Lint loop | 6-field frontmatter + index.md + log.md + link graph |
| Scope | Personal, research, book, team | Any producer/consumer, cross-org |

OKF explicitly cites Karpathy's gist as the pattern it formalizes. So there's no tension: adopt
Karpathy's *workflow* and OKF's *conventions* and you get a knowledge base that is both alive
(continuously maintained) and portable (any OKF tool can read it).

## The big ideas worth keeping

1. **Compounding beats retrieval.** Don't re-derive answers from raw docs each query (RAG).
   Integrate each source into a persistent artifact once, keep it current. Cross-references and
   contradictions are resolved ahead of time, not rediscovered.
2. **Bookkeeping is the real bottleneck — and it's exactly what LLMs are good at.** Humans
   abandon wikis because maintenance outgrows value. An LLM doesn't get bored and can touch 15
   files in one pass, so maintenance cost → ~0 and the wiki survives.
3. **File good answers back.** A query answered well becomes a new concept page, so exploration
   compounds instead of vanishing into chat history. (This note is an example.)
4. **A format, not another service.** The value is in a plain, portable representation anyone
   can produce/consume — just markdown, just files, just YAML frontmatter. Lives in git next to
   what it describes.
5. **Minimal opinion, maximal interop.** Require only `type`; leave the content model open. The
   spec is the interoperability surface, not a straitjacket.
6. **The directory is a graph.** Cross-links matter as much as the documents (Memex, 1945). Wire
   every new note in; hunt orphans during lint.

## What I changed in my vault (2026-07-13)

- **Standardized frontmatter** on concepts/sources/projects/meetings — the six OKF fields
  (`type, title, description, resource, tags, timestamp`), `type` required. → schema updated.
- **Added a vault-wide [`log.md`](../../../log.md)** — append-only, greppable prefix
  `## [YYYY-MM-DD] <op> | <title>`.
- **Added a root [`index.md`](../../../index.md)** — progressive-disclosure master catalog.
- **Added `sources/` and `concepts/`** folders under `right-brain/growth/`.
- **Documented the Ingest → Query → Lint loop** explicitly in the schema.

## Open questions / next actions

- Try Google's **static HTML visualizer** on the vault to see the graph and spot orphans/hubs.
- Consider a lightweight local search (e.g. `qmd`) if the index outgrows manual navigation.
- At work: OKF is directly relevant to AI R&D (BigQuery/metadata catalogs for agents). Worth a
  separate work source note in `left-brain/ballys/sources/` if it becomes a project.

## Related

- [LLM Wiki (Karpathy)](../sources/2026-07-13-karpathy-llm-wiki.md)
- [Open Knowledge Format (OKF)](../sources/2026-07-13-okf-open-knowledge-format.md)
- Vault schema: `.claude/skills/vault-structure/SKILL.md`
