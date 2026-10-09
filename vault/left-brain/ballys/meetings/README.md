---
type: meetings-index
---

# Meeting Notes — Ballys AI R&D

> Auto-populated from Teams transcripts. Each meeting note links to its parent project.

## How it works

1. In Teams, click **Record and transcribe** → **Start transcription**
2. The scheduled task `ballys-meeting-sync` runs daily at 6pm
3. It pulls new transcripts from your OneDrive Recordings folder
4. Summarizes them into structured notes with: attendees, decisions, action items
5. Saves here with frontmatter linking to the relevant project

## Recent Meetings

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Meeting",
  date AS "Date",
  project AS "Project",
  attendees AS "Attendees"
FROM "left-brain/ballys/meetings"
WHERE type = "meeting-note"
SORT date DESC
LIMIT 10
```

## Meeting Notes by Project

```dataview
TABLE WITHOUT ID
  length(rows) AS "Meetings",
  key AS "Project"
FROM "left-brain/ballys/meetings"
WHERE type = "meeting-note"
GROUP BY project AS key
SORT key ASC
```
