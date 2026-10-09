---
name: ingest
description: >
  Processes new source material (articles, papers, links, screenshots, data) into the vault.
  Creates structured notes, updates relevant project/research pages, maintains the index.
  Inspired by Karpathy's LLM Wiki "ingest" operation.
  Triggers: "save this article", "ingest this", "add to vault", "research this topic",
  "file this", "save for later", "read and summarize", "/ingest"
---

# Ingest — Process New Sources Into the Vault

Takes raw source material and integrates it into the vault: summarize, cross-reference,
update relevant pages, and maintain the index. This is the Karpathy "ingest" operation —
the main way new knowledge enters the system.

## Usage

When Frank shares a URL, file, paste, or screenshot:

1. **Classify** the source: article, paper, tool/library, meeting recording, data file, screenshot
2. **Store** the raw source in `vault/sources/<type>/` if it's a file
3. **Create or update** a vault note based on the content
4. **Cross-reference** with existing vault pages
5. **Update index** if a new topic or project was created

## Ingest Workflows by Source Type

### Article / Blog Post / URL
1. Fetch and read the content (WebFetch or Claude in Chrome)
2. Create `vault/research/<topic>.md` with:
   - Source URL and date accessed
   - Key takeaways (3-5 bullets, in Frank's words, not quoted)
   - Relevance to Frank's projects (link to relevant `vault/projects/*.md`)
   - Open questions or follow-ups
3. If it relates to an existing research note, update that note instead of creating a new one
4. Add entry to today's daily log

### Paper / PDF
1. Read and extract key findings
2. Create `vault/research/<paper-topic>.md` with:
   - Citation info (authors, title, year, URL)
   - Core contribution (1-2 sentences)
   - Key findings relevant to Frank's work
   - Potential applications to current projects
3. Save PDF to `vault/sources/articles/` if provided as a file

### Tool / Library Discovery
1. Create `vault/research/<tool-name>.md` with:
   - What it does (1 sentence)
   - Why it's relevant to Frank
   - Quick-start or key API details
   - Comparison with alternatives Frank already uses
2. If it could benefit an active project, add a note to that project file

### Screenshot / Image
1. Save to `vault/sources/screenshots/YYYY-MM-DD-<description>.png`
2. Create a note referencing the screenshot with context about what it shows
3. Link from relevant project or research note

### Data File (CSV, JSON)
1. Save to `vault/sources/data/<filename>`
2. Create a note describing the dataset: schema, size, source, relevance
3. Link from relevant project file

## Cross-Reference Rules

After ingesting any source:
1. Search existing vault notes for related topics (use memory_search.py if available)
2. Add links from the new note to related existing notes
3. Add links FROM related existing notes TO the new note (bidirectional)
4. If the source informs an active project decision, update that project's file
5. If the source contradicts existing vault content, flag the contradiction for Frank

## Index Updates

- New research topic → add to a research section in `portfolio/index.md` or create a `vault/research/index.md` if it doesn't exist
- New project discovered → ask Frank before creating a project file
- New tool/library → add to relevant project's "Tools" or "Dependencies" section

## Quality Rules

1. Never copy-paste large chunks of source material. Summarize in Frank's voice.
2. Always note the source URL and access date.
3. Prefer updating existing notes over creating new ones (avoid duplication).
4. If unsure where to file something, put it in `vault/ideas/` and flag for Frank.
5. Tag ingested notes with `#ingested` and the date for tracking.
