---
name: vault-lint
description: >
  Health-checks the vault wiki for stale content, orphaned pages, broken cross-references,
  missing index entries, and data gaps. Inspired by Karpathy's LLM Wiki "lint" operation.
  Triggers: "lint vault", "vault health", "check vault", "stale content", "orphaned pages",
  "vault maintenance", "clean up vault", "/vault-lint"
---

# Vault Lint — Wiki Health Check

Runs a health check across the entire vault to catch rot, inconsistencies, and gaps.
Directly inspired by Karpathy's LLM Wiki lint operation: find contradictions, stale claims,
orphaned pages, and data gaps.

## Usage

```bash
python3 .claude/skills/vault-lint/scripts/lint_vault.py
python3 .claude/skills/vault-lint/scripts/lint_vault.py --fix    # auto-fix safe issues
python3 .claude/skills/vault-lint/scripts/lint_vault.py --json   # machine-readable output
```

## What It Checks

### 1. Stale Content
- Projects in `vault/projects/` with no updates in daily logs for 7+ days
- MEMORY.md entries referencing past dates or completed items
- Draft replies in `drafts/active/` older than 24 hours (should be expired)
- HABITS.md not reset today

### 2. Orphaned Pages
- Files in `vault/projects/` not listed in `portfolio/index.md`
- Meeting notes not referenced from any daily log
- Research notes not linked from any project file

### 3. Index Consistency
- Projects in `portfolio/index.md` that don't have a corresponding `projects/*.md` file
- Projects in `projects/` missing from `portfolio/index.md`
- STATUS-DASHBOARD.md out of sync with individual project files

### 4. Cross-Reference Integrity
- Broken `[[wiki-links]]` pointing to non-existent files
- Project files that should reference each other (shared dependencies) but don't
- Meeting notes mentioning projects but not linking to them

### 5. Data Gaps
- Days with no daily log entry
- Projects with no recent GitLab activity check
- Team members mentioned in notes but not in `team/ai-rd.md`

### 6. Size Limits
- MEMORY.md over 100 lines (needs summarization)
- SOUL.md over 60 lines
- USER.md over 95 lines
- Any single file over 500 lines (should be split)

## Output

Reports findings in three severity levels:

- **Error** — broken references, missing required files, data inconsistencies
- **Warning** — stale content, orphaned pages, approaching size limits
- **Info** — suggestions for better cross-referencing, gaps that could be filled

## Auto-Fix (--fix)

Safe auto-fixes the script can apply:
- Move stale drafts from `active/` to `expired/`
- Add missing projects to `portfolio/index.md` (with placeholder entry)
- Reset HABITS.md for today if not yet reset
- Remove completed items from MEMORY.md that are older than 7 days

Unsafe fixes are reported but require Frank's approval:
- Deleting orphaned files
- Rewriting stale project descriptions
- Merging duplicate entries
