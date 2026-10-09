---
type: source
title: LLM Wiki (Andrej Karpathy)
description: The pattern this second brain is built on — an LLM incrementally builds and maintains a persistent, interlinked markdown wiki instead of re-deriving answers via RAG each query.
resource: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
tags: [knowledge-management, ai, second-brain, llm-wiki, methodology]
timestamp: 2026-07-13T09:00:00Z
---

# LLM Wiki — Andrej Karpathy

**Source:** [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
**Ingested:** 2026-07-13 · **Why it matters:** This is the blueprint my whole vault follows.

## Core idea

Most LLM+document workflows are RAG: upload files, retrieve chunks at query time, generate an
answer. The model rediscovers knowledge from scratch on every question — nothing accumulates.

The LLM Wiki flips this. The LLM **incrementally builds and maintains a persistent wiki** — a
structured, interlinked set of markdown files that sits between you and the raw sources. Adding
a source doesn't just index it; the LLM reads it, extracts the key points, and *integrates* it:
updating entity pages, revising summaries, flagging contradictions, strengthening the synthesis.
Knowledge is compiled once and kept current, not re-derived per query.

Key line: **the wiki is a persistent, compounding artifact.** Cross-references already exist,
contradictions are already flagged, the synthesis already reflects everything read.

> "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

You own sourcing, exploration, and asking good questions. The LLM does the grunt work —
summarizing, cross-referencing, filing, bookkeeping.

## Three layers

- **Raw sources** — immutable curated documents (articles, papers, data). Source of truth; the LLM reads but never edits them.
- **The wiki** — LLM-generated, LLM-owned markdown: summaries, entity/concept pages, comparisons, an overview, a synthesis.
- **The schema** — a config doc (CLAUDE.md / AGENTS.md) telling the LLM how the wiki is structured and what workflows to follow. This is what makes the LLM a disciplined maintainer rather than a generic chatbot. → *In my vault this is the `vault-structure` skill.*

## Operations

- **Ingest** — drop a source, LLM reads it, discusses takeaways, writes a summary page, updates index, updates related pages, appends to the log. One source may touch 10–15 pages.
- **Query** — ask against the wiki; LLM reads relevant pages and answers with citations. **Good answers get filed back as new pages** so explorations compound.
- **Lint** — periodic health-check: contradictions, stale claims, orphan pages, missing pages/cross-refs, data gaps to fill with search.

## Indexing & logging

- **index.md** — content-oriented catalog: every page with a link + one-line summary, by category. Read first when answering. Works well up to ~100 sources / hundreds of pages without embedding-based RAG.
- **log.md** — chronological, append-only. Consistent prefix (`## [2026-04-02] ingest | Title`) makes it greppable: `grep "^## \[" log.md | tail -5`.

## Why it works

The tedious part of a knowledge base isn't reading or thinking — it's the *bookkeeping*
(updating cross-refs, keeping summaries current, flagging contradictions). Humans abandon wikis
because maintenance grows faster than value. LLMs don't get bored, don't forget a cross-reference,
and can touch 15 files in one pass. Maintenance cost → near zero, so the wiki stays alive.

Related in spirit to Vannevar Bush's **Memex (1945)** — a private, curated store with associative
trails between documents. The part Bush couldn't solve was who does the maintenance. The LLM does.

## Tips worth adopting

- Obsidian **Web Clipper** to pull web articles into raw sources as markdown.
- Download images locally so the LLM can view them (read text first, then images separately).
- Obsidian **graph view** to spot hubs and orphans; **Dataview** to query frontmatter; **Marp** for slides from wiki content.
- Optional CLI search (e.g. `qmd`, local BM25/vector) once the index file alone isn't enough.
- It's just a git repo of markdown → free version history, branching, collaboration.

## How this applies to my vault

My second brain already implements this pattern. Gaps this source highlights, now addressed:
standardized frontmatter, a vault-wide `log.md` and root `index.md`, and an explicit
ingest/query/lint loop. See the synthesis: [LLM Wiki + OKF](../concepts/llm-wiki-and-okf.md).

## Related

- [Open Knowledge Format (OKF)](2026-07-13-okf-open-knowledge-format.md) — Google's formalization of this exact pattern into a portable spec.
- [LLM Wiki + OKF — synthesis](../concepts/llm-wiki-and-okf.md)
