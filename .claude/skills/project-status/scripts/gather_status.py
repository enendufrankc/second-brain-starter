#!/usr/bin/env python3
"""
Project Status Gatherer — Combines vault data with live GitLab data
to produce a portfolio-level status report.

Usage:
    python3 gather_status.py              # Full markdown report
    python3 gather_status.py --json       # JSON output
    python3 gather_status.py --project hackathon-platform  # Single project
    python3 gather_status.py --pipelines  # Include pipeline status
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# Vault and integration paths
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parent.parent.parent  # .claude/skills/project-status -> root
VAULT_DIR = PROJECT_ROOT / "vault"
INTEGRATIONS_DIR = PROJECT_ROOT / ".claude" / "scripts" / "integrations"

# GitLab config
GITLAB_URL = os.environ.get("GITLAB_URL", "https://gitlab.ballys.tech")
GITLAB_USERNAME = "frank.enendu"
TASK_TRACKER_ID = 8489

TRACKED_PROJECTS = {
    "hackathon-platform": {"gitlab_id": 8175, "issues": [13, 14]},
    "game-experience-prototype": {"gitlab_id": 8248, "issues": [11, 12]},
    "ballys-skills-repo": {"gitlab_id": 8284, "issues": []},
    "roadmap-mcp": {"gitlab_id": 8275, "issues": []},
}

# All tracked issue IDs in task-tracker
ALL_ISSUES = [11, 12, 13, 14, 15, 16, 19]


def get_token() -> str:
    """Get GitLab PAT from env or .env file."""
    token = os.environ.get("GITLAB_PAT") or os.environ.get("GITLAB_TOKEN")
    if token:
        return token
    env_files = [
        Path.cwd() / ".env",
        PROJECT_ROOT / ".env",
        Path.home() / "Documents" / "Personal" / "Second Brain Starter" / ".env",
    ]
    for f in env_files:
        if f.exists():
            for line in f.read_text().splitlines():
                line = line.strip()
                if line.startswith("GITLAB_PAT=") or line.startswith("GITLAB_TOKEN="):
                    return line.split("=", 1)[1].strip()
    return ""


def api_get(endpoint: str, params: dict = None) -> list | dict:
    """GitLab API GET request."""
    token = get_token()
    if not token:
        return []
    url = f"{GITLAB_URL}/api/v4{endpoint}"
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={"PRIVATE-TOKEN": token})
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (HTTPError, URLError) as e:
        print(f"GitLab API error: {e}", file=sys.stderr)
        return []


def read_vault_projects() -> dict:
    """Read all project files from vault/projects/."""
    projects = {}
    projects_dir = VAULT_DIR / "projects"
    if not projects_dir.exists():
        return projects
    for f in projects_dir.glob("*.md"):
        if f.name == "STATUS-DASHBOARD.md":
            continue
        name = f.stem
        content = f.read_text()
        # Extract first heading as title
        title = name
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        projects[name] = {"title": title, "file": str(f.relative_to(PROJECT_ROOT)), "content_preview": content[:500]}
    return projects


def read_recent_daily_logs(days: int = 3) -> str:
    """Read last N daily logs for context."""
    daily_dir = VAULT_DIR / "daily"
    if not daily_dir.exists():
        return ""
    logs = []
    for i in range(days):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = daily_dir / f"{d}.md"
        if log_file.exists():
            logs.append(f"### {d}\n{log_file.read_text()[:1000]}")
    return "\n\n".join(logs)


def get_gitlab_issues() -> list:
    """Fetch all open issues from task tracker."""
    issues = api_get(f"/projects/{TASK_TRACKER_ID}/issues", {
        "assignee_username": GITLAB_USERNAME,
        "state": "opened",
        "per_page": 30,
        "order_by": "due_date",
        "sort": "asc",
    })
    return issues if isinstance(issues, list) else []


def get_gitlab_pipelines(project_id: int) -> list:
    """Fetch recent pipeline status for a project."""
    pipelines = api_get(f"/projects/{project_id}/pipelines", {
        "per_page": 5,
        "order_by": "updated_at",
        "sort": "desc",
    })
    return pipelines if isinstance(pipelines, list) else []


def format_issue(issue: dict) -> dict:
    """Format a GitLab issue into a clean dict."""
    due = issue.get("due_date", None)
    status = "on_track"
    days_until = None
    if due:
        due_date = datetime.strptime(due, "%Y-%m-%d").date()
        today = datetime.now().date()
        days_until = (due_date - today).days
        if days_until < 0:
            status = "overdue"
        elif days_until == 0:
            status = "due_today"
        elif days_until <= 3:
            status = "due_soon"

    labels = issue.get("labels", [])
    project_label = next((l.split("::")[-1] for l in labels if l.startswith("project::")), "general")
    priority = next((l for l in labels if l.startswith("P")), "P?")

    return {
        "iid": issue["iid"],
        "title": issue["title"],
        "due_date": due,
        "days_until_due": days_until,
        "status": status,
        "priority": priority,
        "project": project_label,
        "milestone": issue.get("milestone", {}).get("title") if issue.get("milestone") else None,
        "url": issue.get("web_url", ""),
    }


def generate_report(project_filter: str = None, include_pipelines: bool = False) -> str:
    """Generate the full status report."""
    lines = [f"# Portfolio Status — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

    # GitLab issues
    issues = get_gitlab_issues()
    formatted = [format_issue(i) for i in issues]

    if project_filter:
        formatted = [i for i in formatted if project_filter in i["project"]]

    # Group by status
    overdue = [i for i in formatted if i["status"] == "overdue"]
    due_today = [i for i in formatted if i["status"] == "due_today"]
    due_soon = [i for i in formatted if i["status"] == "due_soon"]
    on_track = [i for i in formatted if i["status"] == "on_track"]

    if overdue:
        lines.append("## 🔴 Overdue\n")
        for i in overdue:
            lines.append(f"- **#{i['iid']}** [{i['priority']}] {i['title']}")
            lines.append(f"  Due: {i['due_date']} ({abs(i['days_until_due'])} days overdue) | Project: {i['project']}")

    if due_today:
        lines.append("\n## 🟠 Due Today\n")
        for i in due_today:
            lines.append(f"- **#{i['iid']}** [{i['priority']}] {i['title']}")
            lines.append(f"  Project: {i['project']} | Milestone: {i['milestone'] or 'None'}")

    if due_soon:
        lines.append("\n## 🟡 Due Soon (within 3 days)\n")
        for i in due_soon:
            lines.append(f"- **#{i['iid']}** [{i['priority']}] {i['title']}")
            lines.append(f"  Due: {i['due_date']} ({i['days_until_due']} days) | Project: {i['project']}")

    if on_track:
        lines.append("\n## ✅ On Track\n")
        for i in on_track:
            lines.append(f"- **#{i['iid']}** [{i['priority']}] {i['title']}")
            due_str = f"Due: {i['due_date']} ({i['days_until_due']} days)" if i['due_date'] else "No due date"
            lines.append(f"  {due_str} | Project: {i['project']}")

    if not formatted:
        lines.append("No open issues found.\n")

    # Pipelines
    if include_pipelines:
        lines.append("\n## Pipelines\n")
        for name, info in TRACKED_PROJECTS.items():
            if project_filter and project_filter not in name:
                continue
            pipelines = get_gitlab_pipelines(info["gitlab_id"])
            if pipelines:
                latest = pipelines[0]
                status_emoji = "✅" if latest["status"] == "success" else "❌" if latest["status"] == "failed" else "⏳"
                lines.append(f"- **{name}**: {status_emoji} {latest['status']} (#{latest['id']}, branch: {latest.get('ref', '?')})")
            else:
                lines.append(f"- **{name}**: No recent pipelines")

    # Vault project notes summary
    vault_projects = read_vault_projects()
    if vault_projects:
        lines.append("\n## Vault Project Notes\n")
        for name, info in vault_projects.items():
            lines.append(f"- **{info['title']}** — `{info['file']}`")

    # Recent daily log context
    recent_logs = read_recent_daily_logs(3)
    if recent_logs:
        lines.append(f"\n## Recent Activity (from daily logs)\n\n{recent_logs}")

    return "\n".join(lines)


def generate_json(project_filter: str = None, include_pipelines: bool = False) -> dict:
    """Generate JSON output."""
    issues = get_gitlab_issues()
    formatted = [format_issue(i) for i in issues]
    if project_filter:
        formatted = [i for i in formatted if project_filter in i["project"]]

    result = {
        "timestamp": datetime.now().isoformat(),
        "issues": {
            "overdue": [i for i in formatted if i["status"] == "overdue"],
            "due_today": [i for i in formatted if i["status"] == "due_today"],
            "due_soon": [i for i in formatted if i["status"] == "due_soon"],
            "on_track": [i for i in formatted if i["status"] == "on_track"],
        },
        "total": len(formatted),
    }

    if include_pipelines:
        result["pipelines"] = {}
        for name, info in TRACKED_PROJECTS.items():
            if project_filter and project_filter not in name:
                continue
            pipelines = get_gitlab_pipelines(info["gitlab_id"])
            result["pipelines"][name] = pipelines[:3] if pipelines else []

    return result


def main():
    parser = argparse.ArgumentParser(description="Gather project status across portfolio")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--project", type=str, help="Filter to specific project")
    parser.add_argument("--pipelines", action="store_true", help="Include pipeline status")
    args = parser.parse_args()

    if args.json:
        print(json.dumps(generate_json(args.project, args.pipelines), indent=2, default=str))
    else:
        print(generate_report(args.project, args.pipelines))


if __name__ == "__main__":
    main()
