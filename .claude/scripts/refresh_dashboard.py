#!/usr/bin/env python3
"""Refresh BALLYS-360-DASHBOARD.xlsx with live GitLab data.
Usage: python3 refresh_dashboard.py
Requires: GITLAB_PAT in .env, openpyxl
"""
import json, os, sys, urllib.request
from datetime import date, datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent  # Second Brain Starter root
ENV_FILE = PROJECT_DIR / ".env"
DASHBOARD = PROJECT_DIR / "vault" / "left-brain" / "ballys" / "projects" / "BALLYS-360-DASHBOARD.xlsx"
GITLAB_URL = "https://gitlab.ballys.tech"
PROJECT_ID = 8489  # task-tracker

def load_pat():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("GITLAB_PAT="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("GITLAB_PAT")

def gitlab_get(endpoint, pat):
    url = f"{GITLAB_URL}/api/v4{endpoint}"
    req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": pat})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def main():
    pat = load_pat()
    if not pat:
        print("ERROR: No GITLAB_PAT found", file=sys.stderr)
        return 1

    try:
        issues = gitlab_get(f"/projects/{PROJECT_ID}/issues?state=opened&per_page=100", pat)
    except Exception as e:
        print(f"ERROR: GitLab API failed: {e}", file=sys.stderr)
        return 1

    today = date.today()
    frank_issues = [i for i in issues if i.get("assignee", {}) and i["assignee"].get("username") == "frank.enendu"]
    overdue = []
    due_soon = []
    p0_count = 0

    for issue in frank_issues:
        labels = issue.get("labels", [])
        if "P0" in labels:
            p0_count += 1
        dd = issue.get("due_date")
        if dd:
            due = date.fromisoformat(dd)
            days = (due - today).days
            if days < 0:
                overdue.append((issue["iid"], issue["title"], abs(days)))
            elif days <= 2:
                due_soon.append((issue["iid"], issue["title"], days))

    print(f"=== Ballys 360 Dashboard Refresh — {today.isoformat()} ===")
    print(f"Frank's open issues: {len(frank_issues)}")
    print(f"P0 issues: {p0_count}")
    print(f"Total team issues: {len(issues)}")

    if overdue:
        print("\nOVERDUE:")
        for iid, title, days in overdue:
            print(f"  #{iid} {title} — {days} days overdue")

    if due_soon:
        print("\nDUE WITHIN 48H:")
        for iid, title, days in due_soon:
            label = "TODAY" if days == 0 else f"in {days} day(s)"
            print(f"  #{iid} {title} — {label}")

    if not overdue and not due_soon:
        print("\nNo urgent deadlines.")

    print(f"\nDashboard location: {DASHBOARD}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
