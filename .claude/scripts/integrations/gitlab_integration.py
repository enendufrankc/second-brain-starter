#!/usr/bin/env python3
"""
GitLab Integration — Monitors MRs, issues, pipelines, and activity
across the AI R&D group at gitlab.ballys.tech.

Usage:
    python3 gitlab_integration.py mrs          # Open MRs assigned + needing review
    python3 gitlab_integration.py issues       # Open issues assigned to me
    python3 gitlab_integration.py pipelines    # Failed pipelines across tracked projects
    python3 gitlab_integration.py activity     # Recent activity since last check
    python3 gitlab_integration.py summary      # Full summary (all of the above)
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


# Config
# GITLAB_URL may be exported for other tools with the /api/v4 suffix already on it; strip it so we never double it.
GITLAB_URL = os.environ.get("GITLAB_URL", "https://gitlab.ballys.tech").rstrip("/").removesuffix("/api/v4")
GITLAB_USERNAME = "frank.enendu"

# Tracked project IDs (AI R&D group)
TRACKED_PROJECTS = {
    8489: "task-tracker",
    8175: "hackathon-management-platform",
    8248: "game-experience-agent",
    8284: "ballys-skills-repo",
    8275: "roadmap-mcp",
}

# State file for delta polling
STATE_FILE = Path(__file__).parent.parent.parent / ".claude" / "data" / "state" / "gitlab-state.json"


def get_token() -> str:
    """Get GitLab PAT from environment or .env file."""
    token = os.environ.get("GITLAB_PAT") or os.environ.get("GITLAB_TOKEN")
    if token:
        return token

    # Try loading from .env
    env_files = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent.parent.parent / ".env",
        Path.home() / "Documents" / "Personal" / "Second Brain Starter" / ".env",
    ]
    for env_file in env_files:
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line.startswith("GITLAB_PAT="):
                    return line.split("=", 1)[1].strip()
                if line.startswith("GITLAB_TOKEN="):
                    return line.split("=", 1)[1].strip()

    print("Error: No GitLab PAT found. Set GITLAB_PAT env var or add to .env", file=sys.stderr)
    sys.exit(1)


def api_get(endpoint: str, params: dict = None) -> list | dict:
    """Make a GET request to the GitLab API."""
    token = get_token()
    url = f"{GITLAB_URL}/api/v4{endpoint}"
    if params:
        url += "?" + urlencode(params)

    req = Request(url, headers={"PRIVATE-TOKEN": token})
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        raise GitLabUnavailable(f"API error {e.code}: {endpoint}") from e
    except URLError as e:
        raise GitLabUnavailable(f"Connection error: {e.reason}") from e


class GitLabUnavailable(RuntimeError):
    """GitLab could not be reached or refused the request. Callers must not mistake this for 'no results'."""


def load_state() -> dict:
    """Load previous state for delta polling."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_check": None}


def save_state(state: dict):
    """Save current state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_my_mrs() -> str:
    """Get open MRs assigned to me and needing my review."""
    lines = ["## Open Merge Requests\n"]

    # Assigned to me
    mrs = api_get("/merge_requests", {
        "scope": "assigned_to_me",
        "state": "opened",
        "per_page": 20,
    })
    if mrs:
        lines.append("### Assigned to me")
        for mr in mrs:
            project = mr.get("references", {}).get("full", mr.get("web_url", ""))
            lines.append(f"- **!{mr['iid']}** [{mr['state']}] {mr['title']}")
            lines.append(f"  Author: {mr['author']['name']} | {mr['web_url']}")
    else:
        lines.append("### Assigned to me\nNone")

    # Needing my review
    review_mrs = api_get("/merge_requests", {
        "scope": "all",
        "reviewer_username": GITLAB_USERNAME,
        "state": "opened",
        "per_page": 20,
    })
    if review_mrs:
        lines.append("\n### Needing my review")
        for mr in review_mrs:
            lines.append(f"- **!{mr['iid']}** {mr['title']}")
            lines.append(f"  Author: {mr['author']['name']} | {mr['web_url']}")
    else:
        lines.append("\n### Needing my review\nNone")

    return "\n".join(lines)


def get_my_issues() -> str:
    """Get open issues assigned to me."""
    lines = ["## Open Issues\n"]

    issues = api_get("/issues", {
        "assignee_username": GITLAB_USERNAME,
        "state": "opened",
        "per_page": 30,
        "order_by": "due_date",
        "sort": "asc",
    })

    if not issues:
        lines.append("No open issues assigned.")
        return "\n".join(lines)

    for issue in issues:
        labels = ", ".join(issue.get("labels", []))
        due = issue.get("due_date", "No due date")
        milestone = issue.get("milestone", {})
        ms_name = milestone.get("title", "None") if milestone else "None"

        emoji = ""
        if due != "No due date":
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
            today = datetime.now().date()
            if due_date < today:
                emoji = "🔴 OVERDUE"
            elif due_date == today:
                emoji = "🟠 DUE TODAY"
            elif (due_date - today).days <= 3:
                emoji = "🟡 Due soon"

        lines.append(f"- **#{issue['iid']}** [{labels}] {issue['title']}")
        lines.append(f"  Due: {due} {emoji} | Milestone: {ms_name}")
        lines.append(f"  {issue['web_url']}")

    return "\n".join(lines)


def get_failed_pipelines() -> str:
    """Get failed pipelines across tracked projects."""
    lines = ["## Failed Pipelines\n"]
    found_failures = False

    for project_id, project_name in TRACKED_PROJECTS.items():
        pipelines = api_get(f"/projects/{project_id}/pipelines", {
            "status": "failed",
            "per_page": 3,
            "order_by": "updated_at",
            "sort": "desc",
        })
        if pipelines:
            found_failures = True
            for pipeline in pipelines:
                lines.append(f"- **{project_name}** Pipeline #{pipeline['id']} FAILED")
                lines.append(f"  Branch: {pipeline.get('ref', '?')} | {pipeline['web_url']}")

    if not found_failures:
        lines.append("All tracked project pipelines are green ✅")

    return "\n".join(lines)


def get_recent_activity() -> str:
    """Get recent activity across tracked projects."""
    state = load_state()
    last_check = state.get("last_check")
    if last_check:
        after_date = last_check
    else:
        after_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    lines = [f"## Recent Activity (since {after_date})\n"]
    found_activity = False

    for project_id, project_name in TRACKED_PROJECTS.items():
        events = api_get(f"/projects/{project_id}/events", {
            "after": after_date,
            "per_page": 10,
            "sort": "desc",
        })
        if events:
            found_activity = True
            lines.append(f"### {project_name}")
            for event in events[:5]:
                action = event.get("action_name", "unknown")
                target = event.get("target_title") or event.get("push_data", {}).get("ref", "")
                author = event.get("author", {}).get("name", "unknown")
                lines.append(f"- {author} {action} {target}")

    if not found_activity:
        lines.append("No activity across tracked projects.")

    # Update state
    state["last_check"] = datetime.now().strftime("%Y-%m-%d")
    save_state(state)

    return "\n".join(lines)


def get_full_summary() -> str:
    """Get complete GitLab summary."""
    sections = [
        "# GitLab Summary — " + datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
        get_my_issues(),
        "",
        get_my_mrs(),
        "",
        get_failed_pipelines(),
        "",
        get_recent_activity(),
    ]
    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="GitLab integration for Second Brain")
    parser.add_argument("command", choices=["mrs", "issues", "pipelines", "activity", "summary"],
                        help="What to query")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    commands = {
        "mrs": get_my_mrs,
        "issues": get_my_issues,
        "pipelines": get_failed_pipelines,
        "activity": get_recent_activity,
        "summary": get_full_summary,
    }

    try:
        result = commands[args.command]()
    except GitLabUnavailable as e:
        print(f"GitLab unavailable: {e}", file=sys.stderr)
        sys.exit(2)
    print(result)


if __name__ == "__main__":
    main()
