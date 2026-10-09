---
type: source
title: Open Knowledge Format (OKF)
description: Google Cloud's open spec that formalizes the LLM-wiki pattern into a portable, vendor-neutral format — markdown + YAML frontmatter, index.md, log.md, cross-links as a graph.
resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
tags: [knowledge-management, ai, second-brain, okf, standards, interoperability]
timestamp: 2026-07-13T09:00:00Z
---

# Open Knowledge Format (OKF v0.1)

**Source:** Google Cloud Blog, 12 Jun 2026 (Sam McVeety & Amir Hormati) — [link](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
**Spec/repo:** [github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
**Ingested:** 2026-07-13 · **Why it matters:** Formalizes the exact pattern my vault uses, so my knowledge can become portable/interoperable.

## What it is

OKF is an **open specification** that formalizes the [LLM-wiki pattern](2026-07-13-karpathy-llm-wiki.md)
into a portable, vendor-neutral format for the metadata, context, and curated knowledge modern
AI systems need. **v0.1** represents knowledge as a directory of markdown files with YAML
frontmatter plus a small set of agreed conventions — so wikis written by one producer can be
consumed by any agent without a translation layer.

Deliberately tiny. No compression scheme, no runtime, no SDK. An OKF bundle is:

- **Just markdown** — readable in any editor, renders on GitHub, indexable by any search tool.
- **Just files** — ship as a tarball, host in any git repo, mount on any filesystem.
- **Just YAML frontmatter** — for the few structured fields that must be queryable.

If you've used Obsidian, Notion, Hugo, or the CLAUDE.md/AGENTS.md family, the shape is familiar.

## The problem it solves

Organizational knowledge (table schemas, metric definitions, runbooks, join paths, deprecation
notices) lives fragmented across catalogs, wikis, shared drives, code comments, and senior
engineers' heads. Every vendor has its own catalog, SDK, and knowledge-graph schema; nothing is
portable. So every agent builder re-solves context-assembly from scratch and knowledge stays
siloed. The answer isn't another service — it's a **format**: anyone can produce (no SDK),
anyone can consume (no integration), it survives moving between systems, lives in version
control next to the code, and is readable by humans and parseable by agents (same file).

## How the format works

A **bundle** is a directory of markdown files representing **concepts** (tables, datasets,
metrics, playbooks, runbooks, APIs — anything). One concept = one file; the file path is its
identity. Each concept has a small YAML frontmatter block + a markdown body:

```yaml
---
type: BigQuery Table
title: Orders
description: One row per completed customer order.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, revenue]
timestamp: 2026-05-28T14:30:00Z
---
```

The six fields: **type, title, description, resource, tags, timestamp**. Concepts link to each
other with normal markdown links, turning the directory into a **graph** richer than the folder
tree. Bundles may include `index.md` (progressive disclosure as agents navigate) and `log.md`
(chronological change history). The full v0.1 spec fits on one page.

## Three design principles

1. **Minimally opinionated** — the only required field is `type`. Everything else (what types
   exist, what other fields, what body sections) is left to the producer. The spec defines the
   *interoperability surface*, not the content model.
2. **Producer/consumer independence** — who writes ≠ who reads. A human-authored bundle can be
   read by an agent; an export pipeline's bundle can be browsed in a visualizer; one LLM's
   bundle queried by another. The format is the contract; tooling on each end is swappable.
3. **Format, not platform** — not tied to any cloud, DB, model, or agent framework; never needs
   a proprietary account/SDK. Value comes from how many parties speak it, not who owns it.

## What Google shipped with it

- An **enrichment agent** that walks a BigQuery dataset, drafts an OKF concept doc per table/view, then a second LLM pass crawls docs to add citations, schemas, join paths.
- A **static HTML visualizer** — turns any bundle into an interactive graph in one self-contained file; no backend, no data leaves the page.
- **Three sample bundles** (GA4 e-commerce, Stack Overflow, Bitcoin public datasets).
- Google's **Knowledge Catalog** updated to ingest OKF and serve it to agents.

These are proofs of concept — nothing about the format requires their specific agent, LLM, or HTML/graph viewer.

## How this applies to my vault

My vault is effectively a personal OKF bundle. Adopting the six-field frontmatter, keeping
`index.md`/`log.md`, and cross-linking as a graph makes it portable to any OKF tool (e.g. that
static visualizer) at near-zero cost — and enforces consistency I was doing loosely before.
Changes made 2026-07-13: standardized frontmatter in the schema, added root `index.md` + `log.md`,
added `sources/` and `concepts/` under growth. See [LLM Wiki + OKF](../concepts/llm-wiki-and-okf.md).

## Related

- [LLM Wiki (Karpathy)](2026-07-13-karpathy-llm-wiki.md) — the pattern OKF formalizes.
- [LLM Wiki + OKF — synthesis](../concepts/llm-wiki-and-okf.md)
