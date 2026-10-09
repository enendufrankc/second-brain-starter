---
name: meeting-notes
description: >
  Standardized meeting note template. Auto-files to vault/meetings/YYYY-MM-DD-<topic>.md.
  Extracts action items and appends to relevant vault/projects/*.md files.
  Triggers: "meeting notes", "take notes", "meeting summary", "standup notes",
  "what happened in the meeting", "/meeting-notes"
---

# Meeting Notes — Capture and File

Creates structured meeting notes following Frank's format, files them correctly, and extracts
action items to the right project files.

## Quick Start

When Frank says "take meeting notes" or similar:

1. Ask for (or infer from calendar): meeting title, attendees, date
2. Create the file at `vault/meetings/YYYY-MM-DD-<topic>.md` using the template
3. As Frank provides info, fill in sections
4. After the meeting, extract action items and append to relevant project files
5. Add a timestamped entry to today's daily log referencing the meeting

## Template

Use the template at `${CLAUDE_SKILL_DIR}/references/template.md` as the starting structure.

## Filing Rules

1. **Filename:** `vault/meetings/YYYY-MM-DD-<topic>.md` where `<topic>` is kebab-case, 3-5 words max
2. **Cross-reference:** Link to relevant project files with `[[projects/project-name]]`
3. **Action items:** After capturing notes, append each action item to the relevant `vault/projects/*.md` file under an "## Action Items" section
4. **Daily log:** Add entry like `## HH:MM — Meeting: <title>` to today's daily log with a link to the full notes
5. **MEMORY.md:** If any key decisions were made, add them to MEMORY.md under "## Key Decisions"

## Action Item Format

```markdown
- [ ] **<owner>**: <action> (due: <date or "TBD">) — from [[meetings/YYYY-MM-DD-topic]]
```

## For Calendar Events

If the meeting came from Frank's calendar, the agent can pre-populate:
- Title from calendar event subject
- Attendees from event participants
- Time from event start/end
- Location from event location field
