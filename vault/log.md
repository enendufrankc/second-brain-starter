# Vault Log

> Vault-wide chronological record (append-only). One line per significant event.
> Prefix format: `## [YYYY-MM-DD] <op> | <title>` — greppable: `grep "^## \[" log.md | tail -5`.
> Ops: ingest · query · lint · schema · admin

## [2026-07-13] schema | Adopt OKF-aligned conventions
Upgraded the vault schema (`vault-structure` skill) with standardized OKF frontmatter (type/title/description/resource/tags/timestamp), root `index.md` + `log.md` conventions, cross-linking-as-graph, and an explicit Ingest→Query→Lint loop. Added `sources/` and `concepts/` folders under `right-brain/growth/`. Note: updated skill delivered as a copy for Frank to install via Settings (skill file is read-only in-session).

## [2026-07-13] ingest | LLM Wiki (Andrej Karpathy)
Filed source note `right-brain/growth/sources/2026-07-13-karpathy-llm-wiki.md`. The pattern this vault is built on: LLM incrementally maintains a persistent, interlinked markdown wiki (ingest/query/lint), instead of re-deriving via RAG.

## [2026-07-13] ingest | Open Knowledge Format (OKF)
Filed source note `right-brain/growth/sources/2026-07-13-okf-open-knowledge-format.md`. Google's open spec formalizing the LLM-wiki pattern into a portable format (markdown + YAML frontmatter, index.md, log.md, link graph). Explicitly cites Karpathy's gist.

## [2026-07-13] query | Synthesis: LLM Wiki + OKF
Filed concept note `right-brain/growth/concepts/llm-wiki-and-okf.md` synthesizing both sources and recording the vault changes made today.
