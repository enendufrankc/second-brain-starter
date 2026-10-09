---
cssclass: dashboard
---

# 🎯 Ballys AI R&D — Command Center

###### Frank Enendu · AI R&D · iGaming · `= date(today)`

---

> [!col-3]
>
> > [!stat] 📊 Total Projects
> > ```dataviewjs
> > const pages = dv.pages('"left-brain/ballys/projects"').where(p => p.type === "ballys-project");
> > dv.paragraph(pages.length);
> > ```
>
> > [!stat] 🔴 P0 Critical
> > ```dataviewjs
> > const p0 = dv.pages('"left-brain/ballys/projects"').where(p => p.type === "ballys-project" && p.priority === "P0");
> > dv.paragraph(p0.length);
> > ```
>
> > [!stat] ⚠️ Overdue
> > ```dataviewjs
> > const today = dv.date("today");
> > const overdue = dv.pages('"left-brain/ballys/projects"').where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) < today);
> > dv.paragraph(overdue.length);
> > ```

---

## 🚨 Alerts

> [!danger] Overdue — Needs Immediate Action
> ```dataviewjs
> const today = dv.date("today");
> const overdue = dv.pages('"left-brain/ballys/projects"')
>   .where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) < today)
>   .sort(p => p.due_date, "asc");
> 
> if (overdue.length === 0) {
>   dv.paragraph("✅ Nothing overdue — you're clear!");
> } else {
>   for (let p of overdue) {
>     const days = Math.round((today - dv.date(p.due_date)) / (1000*60*60*24));
>     dv.paragraph(`<span class="badge overdue">OVERDUE ${days}d</span> **${p.file.link}** — was due ${p.due_date} — Issues: ${p.gitlab_issues || "none"}`);
>   }
> }
> ```

> [!warning] Due This Week
> ```dataviewjs
> const today = dv.date("today");
> const weekEnd = dv.date("today").plus({days: 7});
> const dueSoon = dv.pages('"left-brain/ballys/projects"')
>   .where(p => p.type === "ballys-project" && p.due_date && dv.date(p.due_date) >= today && dv.date(p.due_date) <= weekEnd)
>   .sort(p => p.due_date, "asc");
> 
> if (dueSoon.length === 0) {
>   dv.paragraph("😎 Nothing due this week.");
> } else {
>   for (let p of dueSoon) {
>     const days = Math.round((dv.date(p.due_date) - today) / (1000*60*60*24));
>     const badge = days <= 2 ? "due-soon" : "on-track";
>     const label = days === 0 ? "TODAY" : days === 1 ? "TOMORROW" : `${days} days`;
>     dv.paragraph(`<span class="badge ${badge}">${label}</span> **${p.file.link}** — ${p.priority} — Issues: ${p.gitlab_issues || "none"}`);
>   }
> }
> ```

---

## 📌 This Week's Focus (w/c Oct 5)

> [!info] Manually updated each Monday via backlog review

- **🔴 Confirm AL 5% step landed (1 Oct) + Spain prep:** Spain at 5%, end Oct; RTP locale gap, privacy confirmation, KK content ~10 days
- **🟠 Game DNA rubric rework:** add anticipation/readability/persistence/intensity flag, 80 spins, tempo naming compliance check; then leadership presentation
- **🟠 Interview agent pilot:** pick pilot group, comms, success criteria (Al ask, 30 Sep)
- **🟠 AWS migration tool:** test on more projects, add grill-me skill, share with team
- **🔴 Adaptive Layouts budget risk:** Marcos flagged the project over budget to Al/Craig (24 Sep). Needs resolving before the 1 Oct 5% rollout.
- **🔴 Adaptive Layouts 5% rollout — 1 Oct:** Land game ordering, Programme Analytics reporting, and the one remaining MFE launch
- **🔴 Clear the GitLab queue (~20 min):** #42, #13, #33, #35 now 90–121 days overdue and untouched for five straight Monday reviews — every report built on the tracker is currently wrong
- **🟠 Game Experience Profile rework:** Al's review landed 23 Sep (~80% there) — drop numeric-score embeddings, rework mechanics/tempo, popularity-order game selection, then present to Product/Tech leadership
- **🟠 NCR costing:** Portfolio Optimisation + Game Ideation — Frank + Sunny still owe this, unchanged two weeks running
- **🟠 Atlas discovery:** 1 week of R&D Frank owns, still not started 5+ weeks after the 27 Aug sizing
- **🟠 GitLab access from this device:** Reconciliation had to run on meeting notes alone again — gitlab.ballys.tech unreachable (VPN-gated) two runs running
- **⚪ Vault hygiene:** ~11 project files still frozen at April state with stale due dates
- **Life insurance:** ~157 days overdue. 20 minutes on comparethemarket.com

_⚠️ Auto-populated by the Monday backlog review on 2026-10-05 from meeting notes (30 Sep–1 Oct) — GitLab itself was unreachable from this device. Frank was not present — confirm/correct._

---

## 📣 Comms & Outreach Pending

| What | Who | Status |
|------|-----|--------|
| Ignite Hackathon broadcast | All engineers | Sending today |
| Skills Repo broadcast email | All tech | Not sent — Al approved strategy |
| Engineering Leads showcase meeting | Engineering Leads | Not set up yet |
| Prototyping Platform — Stadium repo access | Bhav | Promised Apr 22, awaiting link |
| Game Ideation scoping catch-up | Sudhanva | Not scheduled yet |

---

## ⏳ Waiting On

| What | Who | Since | Days |
|------|-----|-------|------|
| Native event tracking → Thunderbird/MFE | Harriet Cole / Salvatore DeCicco | Aug 27 | 32 |
| Data-usage-for-personalisation Privacy form | Privacy (via Adam Bailey) | Aug 27 | 32 |
| Contentful → Atlas read/write scope | Kyriacos Kyriacou | Aug 27 | 32 |
| Slot data sources for trending titles | Kyriacos Kyriacou | Aug 27 | 32 |
| Soft dollar-value estimate on portfolio NCR | Chris (via Al) | Aug 27 | 32 |
| Harmon requirements file for Atlas discovery | Nathan / Kevin | Aug 27 | 32 |
| Al to review Game Experience dimensions w/ Dez or a slots expert | Al Jepps | Sep 23 | 5 |
| Al to return atomic-change list on Frank's mechanics/tempo code | Al Jepps | Sep 23 | 5 |
| Al to draft the commercial control-plane proposal for product | Al Jepps | Sep 25 | 3 |
| Tableau back-token fix (blocking Game Experience self-serve access) | Georgia | Sep 25 | 3 |
| Stadium repo access + Storybook link | Bhav | Apr 22 | **159** |
| Capex Machine Jira Cloud integration steer | Richard Duffy | Apr 22 | **159** |
| Roadmap MCP testing feedback | Mark Webster | May 9 | **142** |
| Tableau reporting agent collab | Dez Pazmany | Apr 17 | **164** |

_The bottom four are 4–5+ months silent. Chase or close — carrying them as "waiting" is costing nothing but telling you nothing either. Note: the long-running "Game Experience review — Al Jepps" item is now resolved — the review happened 23 Sep, replaced above by Al's follow-through asks from that same review._

---

## 🔑 Key Decisions (Recent)

- **Apr 21 — User access for AI R&D apps:** No SSO for demos/prototypes. Apps with PII or user base need passwords with self sign-up. Dedicated service principal rejected by Bartek. Al binned meeting with Bartek.
- **Apr 21 — SSO/DNS initiative deprioritised:** Dropped from P0 to P2. Replaced by user access strategy write-up.
- **Apr 22 — Prototyping Platform: Stadium is the foundation.** Bhav's "Stadium" design system (MUI-based, Storybook, brand tokens) will be the source of truth. Wait ~2 weeks for Adam's team to finish more components, then integrate. Bhav open to AI R&D team taking over extending Stadium for prototyping use case.
- **Apr 22 — Data Agent pivot:** Pivoting to automated Tableau reporting agent, working with Dez Pazmany.
- **Apr 22 — Error Analysis deprioritised:** Pipeline broken since Apr 2, not actively working on it.
- **Apr 22 — Conference Write-Up complete.**
- **Apr 22 — Skills Repo strategy approved by Al.**

---

## 📊 Project Progress

> Check off milestones inside each project file — bars update automatically.

```dataviewjs
const pages = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project")
  .sort(p => {
    const order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3};
    return order[p.priority] ?? 4;
  }, "asc");

const rows = [];
for (let p of pages) {
  const tasks = p.file.tasks;
  const total = tasks.length;
  const done = tasks.where(t => t.completed).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  
  // Pick color based on progress
  let color = "red";
  if (pct >= 75) color = "green";
  else if (pct >= 40) color = "blue";
  else if (pct >= 20) color = "orange";
  
  const bar = `<div class="progress-bar"><div class="progress-fill ${color}" style="width:${pct}%"></div></div>`;
  const priBadge = `<span class="badge ${(p.priority || "").toLowerCase()}">${p.priority || "—"}</span>`;
  
  rows.push([
    p.file.link,
    priBadge,
    `${bar} <small>${done}/${total} — ${pct}%</small>`,
    p.status
  ]);
}

dv.table(["Project", "Pri", "Progress", "Status"], rows);
```

---

## 🔥 P0 — Critical Path

```dataviewjs
const p0 = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project" && p.priority === "P0")
  .sort(p => p.due_date, "asc");

const container = dv.el("div", "", {cls: "nav-buttons"});

for (let p of p0) {
  const due = p.due_date ? p.due_date : "No date";
  dv.el("div", 
    `<strong>${p.file.link}</strong><br>` +
    `<small>${p.status}</small><br>` +
    `<small>Due: ${due}</small><br>` +
    `<small>Issues: ${p.gitlab_issues || "none"}</small>`,
    {cls: "callout", attr: {"data-callout": "p0"}}
  );
}
```

---

## 📋 All Projects

```dataviewjs
const pages = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project")
  .sort(p => {
    const order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3};
    return order[p.priority] ?? 4;
  }, "asc");

const today = dv.date("today");

dv.table(
  ["Project", "Pri", "Status", "Due", "Countdown", "Issues"],
  pages.map(p => {
    // Priority badge
    const priClass = p.priority ? p.priority.toLowerCase() : "";
    const priBadge = `<span class="badge ${priClass}">${p.priority || "—"}</span>`;
    
    // Due date with countdown
    let countdown = "—";
    let dueBadge = "—";
    if (p.due_date) {
      const dueDate = dv.date(p.due_date);
      const days = Math.round((dueDate - today) / (1000*60*60*24));
      if (days < 0) {
        countdown = `<span class="badge overdue">${Math.abs(days)}d overdue</span>`;
      } else if (days <= 2) {
        countdown = `<span class="badge due-soon">${days}d left</span>`;
      } else if (days <= 7) {
        countdown = `<span class="badge on-track">${days}d left</span>`;
      } else {
        countdown = `${days}d`;
      }
      dueBadge = p.due_date;
    }

    return [
      p.file.link,
      priBadge,
      p.status,
      dueBadge,
      countdown,
      p.gitlab_issues || "—"
    ];
  })
);
```

---

## 🏗️ PIT Infrastructure

> SSO, DNS, and SSL certificate status for external-facing apps.

```dataviewjs
const pages = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project" && p.intended_domain)
  .sort(p => {
    const order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3};
    return order[p.priority] ?? 4;
  }, "asc");

function badge(val) {
  if (!val || val === "—") return "—";
  if (val === "done") return `<span class="badge done">✅ Done</span>`;
  if (val === "pending") return `<span class="badge pending">❌ Pending</span>`;
  if (val === "ticket-raised") return `<span class="badge ticket">🎫 Ticket</span>`;
  return val;
}

dv.table(
  ["App", "Domain", "SSO", "DNS", "Cert"],
  pages.map(p => [
    p.file.link,
    p.intended_domain,
    badge(p.pit_sso),
    badge(p.pit_dns),
    badge(p.pit_cert)
  ])
);
```

---

## 🎙️ Recent Meetings

```dataviewjs
const meetings = dv.pages('"left-brain/ballys/meetings"')
  .where(p => p.type === "meeting-note")
  .sort(p => p.date, "desc")
  .slice(0, 5);

if (meetings.length === 0) {
  dv.paragraph("No meeting notes yet. Start transcribing in Teams — notes will appear here automatically.");
} else {
  dv.table(
    ["Meeting", "Date", "Project"],
    meetings.map(m => [
      m.file.link,
      m.date,
      m.project || "General"
    ])
  );
}
```

> 📁 [All Meetings](meetings/README.md) · *Auto-synced from Teams transcripts daily at 6pm*

---

## ✅ Open Tasks

> Unchecked tasks pulled from all project files.

```dataviewjs
const tasks = dv.pages('"left-brain/ballys/projects"')
  .where(p => p.type === "ballys-project")
  .file.tasks
  .where(t => !t.completed)
  .sort(t => t.text, "asc");

if (tasks.length === 0) {
  dv.paragraph("🎉 All tasks complete!");
} else {
  dv.taskList(tasks.slice(0, 15), false);
  if (tasks.length > 15) {
    dv.paragraph(`*...and ${tasks.length - 15} more. See [[DEADLINES]] for full list.*`);
  }
}
```

---

## 🔗 Quick Nav

> [!col-3]
>
> > [!nav] 🎯
> > [Deadlines](DEADLINES.md)
>
> > [!nav] 📂
> > [Portfolio](portfolio/index.md)
>
> > [!nav] 📝
> > [Build Plan](../../BUILD-PLAN.md)

> [!col-3]
>
> > [!nav] 🔧
> > [GitLab Tracker](https://gitlab.ballys.tech/igaming/ai-rd/task-tracker)
>
> > [!nav] 📚
> > [Skills Repo](https://gitlab.ballys.tech/igaming/tooling/claude-skills)
>
> > [!nav] 🏆
> > [Hackathon](https://hackathon.ballys.com)

---

> [!tip] Setup (one-time)
> 1. **Install Dataview** — Settings → Community Plugins → search "Dataview" → Install → Enable
> 2. **Enable JS queries** — Settings → Dataview → toggle on "Enable JavaScript Queries" + "Enable Inline Queries"
> 3. **Enable CSS snippet** — Settings → Appearance → CSS Snippets → reload → toggle on "dashboard"
