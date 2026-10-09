#!/usr/bin/env python3
"""
Vault Lint — Health-checks the vault wiki for stale content, orphaned pages,
broken cross-references, missing index entries, and data gaps.

Inspired by Karpathy's LLM Wiki "lint" operation.

Usage:
    python3 lint_vault.py              # Report issues
    python3 lint_vault.py --fix        # Auto-fix safe issues
    python3 lint_vault.py --json       # Machine-readable output
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
VAULT_DIR = PROJECT_ROOT / "vault"

# Left-brain paths (new structure)
LEFT_BRAIN = VAULT_DIR / "left-brain" / "ballys"
RIGHT_BRAIN = VAULT_DIR / "right-brain"

# Resolve paths — fall back to old structure if new doesn't exist yet
def _resolve_work_dir(subpath):
    new = LEFT_BRAIN / subpath
    old = VAULT_DIR / subpath
    return new if new.exists() else old

PROJECTS_DIR = _resolve_work_dir("projects")
DAILY_DIR = _resolve_work_dir("daily")
MEETINGS_DIR = _resolve_work_dir("meetings")
PORTFOLIO_INDEX = _resolve_work_dir("portfolio") / "index.md"
DRAFTS_ACTIVE = _resolve_work_dir("drafts/active")
DRAFTS_EXPIRED = _resolve_work_dir("drafts/expired")

# Size limits
LIMITS = {
    "MEMORY.md": 100,
    "SOUL.md": 70,
    "USER.md": 120,
    "max_file_lines": 500,
}


class LintResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.fixes_applied = []

    def error(self, msg: str, file: str = None):
        self.errors.append({"level": "error", "message": msg, "file": file})

    def warning(self, msg: str, file: str = None):
        self.warnings.append({"level": "warning", "message": msg, "file": file})

    def note(self, msg: str, file: str = None):
        self.info.append({"level": "info", "message": msg, "file": file})

    def fixed(self, msg: str):
        self.fixes_applied.append(msg)

    def to_markdown(self) -> str:
        lines = [f"# Vault Lint Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

        if self.fixes_applied:
            lines.append(f"## Fixes Applied ({len(self.fixes_applied)})\n")
            for f in self.fixes_applied:
                lines.append(f"- ✅ {f}")
            lines.append("")

        if self.errors:
            lines.append(f"## Errors ({len(self.errors)})\n")
            for e in self.errors:
                file_ref = f" — `{e['file']}`" if e["file"] else ""
                lines.append(f"- 🔴 {e['message']}{file_ref}")
            lines.append("")

        if self.warnings:
            lines.append(f"## Warnings ({len(self.warnings)})\n")
            for w in self.warnings:
                file_ref = f" — `{w['file']}`" if w["file"] else ""
                lines.append(f"- 🟡 {w['message']}{file_ref}")
            lines.append("")

        if self.info:
            lines.append(f"## Info ({len(self.info)})\n")
            for i in self.info:
                file_ref = f" — `{i['file']}`" if i["file"] else ""
                lines.append(f"- ℹ️ {i['message']}{file_ref}")
            lines.append("")

        total = len(self.errors) + len(self.warnings) + len(self.info)
        if total == 0:
            lines.append("Vault is healthy! No issues found. 🎉")

        lines.append(f"\n**Summary:** {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info")
        return "\n".join(lines)

    def to_json(self) -> dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
            "fixes_applied": self.fixes_applied,
            "counts": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "info": len(self.info),
                "fixes": len(self.fixes_applied),
            },
        }


def check_stale_content(result: LintResult, auto_fix: bool):
    """Check for stale content across the vault."""
    today = datetime.now().date()

    # Check project files for staleness
    projects_dir = PROJECTS_DIR
    daily_dir = DAILY_DIR
    if projects_dir.exists():
        for f in projects_dir.glob("*.md"):
            if f.name == "STATUS-DASHBOARD.md":
                continue
            project_name = f.stem
            # Check if project mentioned in recent daily logs
            mentioned = False
            for i in range(7):
                d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                log_file = daily_dir / f"{d}.md"
                if log_file.exists() and project_name in log_file.read_text().lower():
                    mentioned = True
                    break
            if not mentioned:
                result.warning(f"Project '{project_name}' has no mentions in daily logs for 7+ days", str(f.relative_to(PROJECT_ROOT)))

    # Check stale drafts
    active_drafts = DRAFTS_ACTIVE
    if active_drafts.exists():
        for draft in active_drafts.glob("*.md"):
            # Extract date from filename pattern YYYY-MM-DD_...
            try:
                date_str = draft.name[:10]
                draft_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                age_days = (today - draft_date).days
                if age_days > 1:
                    if auto_fix:
                        expired_dir = DRAFTS_EXPIRED
                        expired_dir.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(draft), str(expired_dir / draft.name))
                        result.fixed(f"Moved stale draft to expired: {draft.name}")
                    else:
                        result.warning(f"Draft is {age_days} days old (should expire after 24h)", draft.name)
            except ValueError:
                pass  # Skip files that don't match naming convention

    # Check MEMORY.md for stale entries
    memory_file = VAULT_DIR / "MEMORY.md"
    if memory_file.exists():
        content = memory_file.read_text()
        # Look for dates in the past that might be stale
        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        for match in date_pattern.finditer(content):
            try:
                entry_date = datetime.strptime(match.group(), "%Y-%m-%d").date()
                if (today - entry_date).days > 14:
                    result.note(f"MEMORY.md contains date {match.group()} which is 14+ days old — consider archiving", "vault/MEMORY.md")
                    break  # Only report once
            except ValueError:
                pass


def check_orphaned_pages(result: LintResult):
    """Check for pages not referenced from anywhere."""
    # Check projects not in portfolio index
    index_file = PORTFOLIO_INDEX
    index_content = index_file.read_text().lower() if index_file.exists() else ""

    projects_dir = PROJECTS_DIR
    if projects_dir.exists():
        for f in projects_dir.glob("*.md"):
            if f.name == "STATUS-DASHBOARD.md":
                continue
            if f.stem.lower() not in index_content and f.name.lower() not in index_content:
                result.warning(f"Project '{f.stem}' not found in portfolio/index.md", str(f.relative_to(PROJECT_ROOT)))

    # Check meeting notes not referenced from daily logs
    meetings_dir = MEETINGS_DIR
    daily_dir = DAILY_DIR
    if meetings_dir.exists():
        for f in meetings_dir.glob("*.md"):
            referenced = False
            if daily_dir.exists():
                for log in daily_dir.glob("*.md"):
                    if f.stem in log.read_text():
                        referenced = True
                        break
            if not referenced:
                result.note(f"Meeting note '{f.stem}' not referenced from any daily log", str(f.relative_to(PROJECT_ROOT)))


def check_index_consistency(result: LintResult, auto_fix: bool):
    """Check portfolio index consistency."""
    index_file = PORTFOLIO_INDEX
    projects_dir = PROJECTS_DIR

    if not index_file.exists():
        result.error("portfolio/index.md does not exist", "vault/portfolio/index.md")
        return

    index_content = index_file.read_text()
    index_lower = index_content.lower()

    if projects_dir.exists():
        for f in projects_dir.glob("*.md"):
            if f.name == "STATUS-DASHBOARD.md":
                continue
            if f.stem not in index_lower:
                if auto_fix:
                    # Add placeholder entry to index
                    with open(index_file, "a") as idx:
                        idx.write(f"\n| {f.stem} | — | — | — | — |\n")
                    result.fixed(f"Added '{f.stem}' placeholder to portfolio/index.md")
                else:
                    result.warning(f"Project '{f.stem}' exists but not in portfolio/index.md", str(f.relative_to(PROJECT_ROOT)))


def check_cross_references(result: LintResult):
    """Check for broken wiki-links and missing cross-references."""
    all_files = {}
    for f in VAULT_DIR.rglob("*.md"):
        rel = str(f.relative_to(VAULT_DIR))
        all_files[rel] = f
        all_files[f.stem] = f  # Allow stem-only references

    wiki_link_pattern = re.compile(r'\[\[([^\]]+)\]\]')

    for rel_path, filepath in list(all_files.items()):
        if "/" not in rel_path:
            continue  # Skip stem-only entries
        content = filepath.read_text()
        for match in wiki_link_pattern.finditer(content):
            target = match.group(1)
            # Check if target exists (with or without .md extension)
            if target not in all_files and f"{target}.md" not in all_files and target.replace(".md", "") not in all_files:
                result.error(f"Broken wiki-link [[{target}]]", rel_path)


def check_size_limits(result: LintResult):
    """Check file size limits."""
    for name, limit in LIMITS.items():
        if name == "max_file_lines":
            continue
        filepath = VAULT_DIR / name
        if filepath.exists():
            line_count = len(filepath.read_text().splitlines())
            if line_count > limit:
                result.warning(f"{name} has {line_count} lines (limit: {limit}). Consider summarizing.", f"vault/{name}")
            elif line_count > limit * 0.8:
                result.note(f"{name} has {line_count} lines (approaching limit of {limit})", f"vault/{name}")

    # Check all vault files for max size
    max_lines = LIMITS["max_file_lines"]
    for f in VAULT_DIR.rglob("*.md"):
        line_count = len(f.read_text().splitlines())
        if line_count > max_lines:
            result.warning(f"File has {line_count} lines (limit: {max_lines}). Consider splitting.", str(f.relative_to(PROJECT_ROOT)))


def check_data_gaps(result: LintResult):
    """Check for missing daily logs and other gaps."""
    daily_dir = DAILY_DIR
    if not daily_dir.exists():
        result.error("Work daily log directory does not exist")
        return

    today = datetime.now().date()
    # Check last 7 weekdays for daily logs
    checked = 0
    d = today
    while checked < 5:
        if d.weekday() < 5:  # Weekday
            log_file = daily_dir / f"{d.strftime('%Y-%m-%d')}.md"
            if not log_file.exists():
                # Skip today if it's early
                if d != today or datetime.now().hour >= 10:
                    result.note(f"No daily log for {d.strftime('%Y-%m-%d')} (weekday)", f"vault/daily/{d.strftime('%Y-%m-%d')}.md")
            checked += 1
        d -= timedelta(days=1)

    # Check HABITS.md last reset
    habits_file = VAULT_DIR / "HABITS.md"
    if habits_file.exists():
        content = habits_file.read_text()
        if today.strftime("%Y-%m-%d") not in content and (today - timedelta(days=1)).strftime("%Y-%m-%d") not in content:
            result.note("HABITS.md may not have been reset recently", "vault/HABITS.md")


def main():
    parser = argparse.ArgumentParser(description="Vault lint — health check the wiki")
    parser.add_argument("--fix", action="store_true", help="Auto-fix safe issues")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = LintResult()

    check_stale_content(result, args.fix)
    check_orphaned_pages(result)
    check_index_consistency(result, args.fix)
    check_cross_references(result)
    check_size_limits(result)
    check_data_gaps(result)

    if args.json:
        print(json.dumps(result.to_json(), indent=2))
    else:
        print(result.to_markdown())


if __name__ == "__main__":
    main()
