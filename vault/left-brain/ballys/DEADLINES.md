---
cssclass: dashboard
---

# ⏰ Deadline Tracker

###### All open deadlines across Ballys projects · `= date(today)`

---

> [!col-3]
>
> > [!stat] 🔴 Overdue
> > ```dataviewjs
> > const today = dv.date("today");
> > const n = dv.pages('"left-brain/ballys/projects"').where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) < today).length;
> > dv.paragraph(n);
> > ```
>
> > [!stat] 🟡 Due ≤ 7 Days
> > ```dataviewjs
> > const today = dv.date("today");
> > const week = dv.date("today").plus({days: 7});
> > const n = dv.pages('"left-brain/ballys/projects"').where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) >= today && dv.date(p.due_date) <= week).length;
> > dv.paragraph(n);
> > ```
>
> > [!stat] ⚪ No Date
> > ```dataviewjs
> > const n = dv.pages('"left-brain/ballys/projects"').where(p => p.type === "ballys-project" && !p.due_date).length;
> > dv.paragraph(n);
> > ```

---

## 📌 Hard Deadlines & Events

| Date | What | Notes |
|------|------|-------|
| **Apr 22 (TODAY)** | Hackathon prep deadline | Everything must be ready 1 week before Ignite |
| **Apr 24 (Fri)** | Hackathon idea assessment begins | Approved authors start advertising for team members |
| **Apr 25** | Portfolio Optimisation Agent scope due | #16 — define agent scope and data sources |
| **Apr 28 (Mon morning)** | All hackathon admin complete | Teams formed, ideas approved, ready to hack |
| **Apr 29-30** | Ignite Hackathon | London office, 2-day event |
| **Apr 30** | Data Analyst Agent due | #19 — pivoting to Tableau reporting agent with Dez |
| **May 9** | Roadmap MCP due | Waiting on Mark Webster testing feedback |
| **May 16** | Capex Machine due | Chris requesting Jira Cloud integration — awaiting Richard Duffy steer |

---

## 🔴 Overdue

> [!danger] Past due — action required

```dataviewjs
const today = dv.date("today");
const overdue = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) < today)
  .sort(p => p.due_date, "asc");

if (overdue.length === 0) {
  dv.paragraph("✅ Nothing overdue!");
} else {
  dv.table(
    ["Project", "Pri", "Was Due", "Overdue By", "Issues"],
    overdue.map(p => {
      const days = Math.round((today - dv.date(p.due_date)) / (1000*60*60*24));
      return [
        p.file.link,
        `<span class="badge ${p.priority?.toLowerCase()}">${p.priority}</span>`,
        p.due_date,
        `<span class="badge overdue">${days} days</span>`,
        p.gitlab_issues || "—"
      ];
    })
  );
}
```

---

## 🟡 Due This Week

> [!warning] Due within 7 days

```dataviewjs
const today = dv.date("today");
const week = dv.date("today").plus({days: 7});
const dueSoon = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) >= today && dv.date(p.due_date) <= week)
  .sort(p => p.due_date, "asc");

if (dueSoon.length === 0) {
  dv.paragraph("😎 Clear for the week.");
} else {
  dv.table(
    ["Project", "Pri", "Due", "Countdown", "Issues"],
    dueSoon.map(p => {
      const days = Math.round((dv.date(p.due_date) - today) / (1000*60*60*24));
      const label = days === 0 ? "TODAY" : days === 1 ? "TOMORROW" : `${days} days`;
      const cls = days <= 2 ? "due-soon" : "on-track";
      return [
        p.file.link,
        `<span class="badge ${p.priority?.toLowerCase()}">${p.priority}</span>`,
        p.due_date,
        `<span class="badge ${cls}">${label}</span>`,
        p.gitlab_issues || "—"
      ];
    })
  );
}
```

---

## 🟢 Due This Month

> [!info] Coming up within 30 days

```dataviewjs
const today = dv.date("today");
const week = dv.date("today").plus({days: 7});
const month = dv.date("today").plus({days: 30});
const upcoming = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) > week && dv.date(p.due_date) <= month)
  .sort(p => p.due_date, "asc");

if (upcoming.length === 0) {
  dv.paragraph("Nothing else due this month.");
} else {
  dv.table(
    ["Project", "Pri", "Due", "Status"],
    upcoming.map(p => [
      p.file.link,
      `<span class="badge ${p.priority?.toLowerCase()}">${p.priority}</span>`,
      p.due_date,
      p.status
    ])
  );
}
```

---

## ⚪ No Due Date Set

> [!question] Consider setting deadlines for these

```dataviewjs
const noDate = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project" && !p.due_date)
  .sort(p => {
    const order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3};
    return order[p.priority] ?? 4;
  }, "asc");

if (noDate.length === 0) {
  dv.paragraph("All projects have due dates set. 👏");
} else {
  dv.table(
    ["Project", "Pri", "Status"],
    noDate.map(p => [
      p.file.link,
      `<span class="badge ${p.priority?.toLowerCase()}">${p.priority}</span>`,
      p.status
    ])
  );
}
```

---

## ✅ All Open Tasks

> Unchecked `- [ ]` items from every project file.

```dataviewjs
const tasks = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project")
  .file.tasks
  .where(t => !t.completed);

if (tasks.length === 0) {
  dv.paragraph("🎉 All tasks complete!");
} else {
  dv.taskList(tasks, false);
}
```

---

---

## ✅ Recently Completed (w/c Apr 22)

- Conference Write-Up — marked complete
- Game Experience: dimensions #11 + full catalogue #12 — done, awaiting Al's review
- Hackathon Platform: Intralot rebranding — done
- GitLab PAT — renewed
- Skills Repo strategy plan — approved by Al
- M365 app registration — fixed, Outlook + Teams data flowing
- Juan Impey / Inner Source Skills Pilot — replied and resolved
- Train ticket for Ignite — raised on Support Hub

---

[← Back to Command Center](DASHBOARD.md)
