# Morning Brief Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Each weekday, once Frank's laptop and VPN are up, post a five-item to-do and a short AI-news message to his Teams notes-to-self chat, capture his dumps from that chat into the vault, and enforce self-chat-only sending in the guardrail hook.

**Architecture:** A launchd agent ticks every 10 minutes into a bash gate. When the gate passes, two LLM-free Python collectors (session transcripts, RSS news) plus the existing GitLab CLI write files into a run directory, then one headless `claude -p` run reads Teams, calendar and vault through the Microsoft 365 connector, composes and sends the messages, and writes the daily log, inbox file and state marker. The PreToolUse hook gains a branch that allows Teams sends only to the self-chat id.

**Tech Stack:** Python 3.14 standard library only (`urllib`, `xml.etree`, `json`), bash, macOS launchd, Claude Code CLI 2.1.286 headless mode, Microsoft 365 connector tools. Tests use `unittest` (no pytest in this environment).

**Spec:** `docs/superpowers/specs/2026-10-01-morning-brief-design.md`

## Global Constraints

- No new Python dependencies. Collectors use the standard library only.
- All new scripts live under `.claude/scripts/`; all tests under `tests/`; run with `python3 -m unittest discover -s tests -v`.
- Self-chat id: `19:c142cf69-5033-4b79-9f1b-df23832c13d9_7cb48f87-e8c5-4ac2-8858-9b5433fc0d79@unq.gbl.spaces`.
- Team chat ids: Stand up `19:meeting_OGNlZjZhMWItMDQ2OS00M2ZlLTljOTUtNzA5MWZiNjQ1NDdk@thread.v2`, Interlock `19:762ccb646d3447e7aec650273198e595@thread.v2`, Crew `19:02a862626ca54619b6babc5593aa33a3@thread.v2`.
- VPN probe: `https://gitlab.ballys.tech/api/v4/version` must answer 200 or 401 within 5 s.
- `claude` binary: `/Users/frank.enendu/.local/bin/claude`. This CLI version has no `--max-turns` flag; do not pass it.
- Daily logs are append-only. `vault/daily/` is canonical for work logs. Nothing moves.
- Transcript scope: only repos under `~/Documents/Work` and `~/Documents/Projects`.
- Weekdays only, window 06:30–11:00 local, `--force` bypasses weekday, window and marker but never the VPN probe.
- The repo guardrail hook scans every Bash command string. Write files with the Write/Edit tools, not heredocs, when content mentions destructive commands.
- Commit per task on branch `feat/morning-brief`. Stage files by name.

## Review Focus

1. A feed item with no publish date must be dropped, not crash or be treated as new. (Task 1 test `test_item_without_date_is_dropped`.)
2. A Codex or Claude session whose cwd is under `~/Documents/Contract` must never appear in the digest, even if its name contains "Work". (Task 2 test `test_contract_repo_excluded`.)
3. A Teams send with a missing or empty `chatId` must be blocked, not allowed by accident. (Task 3 test `test_teams_send_missing_chat_id_blocked`.)
4. A time like `0700` must pass the window check despite the leading zero; bash treats `0700` as octal without `10#`. (Task 6 test `test_window_accepts_leading_zero_time`.)
5. The agent's own brief, posted under Frank's account, must not be re-ingested as a dump on the next run. (Task 5 prompt: cursor advances to send time; agent messages end with `— second brain`; Task 7 manual check after two consecutive `--force` runs.)

---

### Task 1: AI news collector

**Files:**
- Create: `.claude/scripts/news_digest.py`
- Test: `tests/test_news_digest.py`
- Create: `tests/__init__.py` (empty)

**Interfaces:**
- Produces: `parse_feed(xml_bytes: bytes, source: str) -> list[dict]` where each dict is `{"source", "title", "link", "published": datetime|None}`; `filter_recent(items, hours: int, now: datetime|None) -> list[dict]`; `format_markdown(items, warnings: list[str], hours: int) -> str`; CLI `python3 .claude/scripts/news_digest.py [--hours 24] [--json]` writing markdown or JSON to stdout, exit 0 always.
- Markdown shape consumed by Task 5's prompt:

```
## <Source>
- <ISO time> | <title> | <link>
```

- [ ] **Step 1: Write the failing tests**

Create `tests/__init__.py` empty. Create `tests/test_news_digest.py`:

```python
import sys, unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".claude" / "scripts"))
import news_digest as nd

RSS = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>X</title>
<item><title>New model</title><link>https://ex.com/a</link><pubDate>Wed, 01 Oct 2026 06:00:00 GMT</pubDate></item>
<item><title>Old post</title><link>https://ex.com/b</link><pubDate>Mon, 01 Sep 2026 06:00:00 GMT</pubDate></item>
<item><title>No date</title><link>https://ex.com/c</link></item>
<item><title>Dup</title><link>https://ex.com/a</link><pubDate>Wed, 01 Oct 2026 05:00:00 GMT</pubDate></item>
</channel></rss>"""

ATOM = b"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Y</title>
<entry><title>Atom entry</title><link rel="alternate" href="https://ex.org/p"/><published>2026-10-01T07:30:00Z</published></entry>
</feed>"""

NOW = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)


class ParseTests(unittest.TestCase):
    def test_parse_rss_items(self):
        items = nd.parse_feed(RSS, "X")
        self.assertEqual(items[0]["title"], "New model")
        self.assertEqual(items[0]["link"], "https://ex.com/a")
        self.assertEqual(items[0]["published"], datetime(2026, 10, 1, 6, 0, tzinfo=timezone.utc))
        self.assertEqual(items[0]["source"], "X")

    def test_parse_atom_entry(self):
        items = nd.parse_feed(ATOM, "Y")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["link"], "https://ex.org/p")
        self.assertEqual(items[0]["published"].hour, 7)


class FilterTests(unittest.TestCase):
    def test_filter_drops_old_and_dedupes(self):
        items = nd.filter_recent(nd.parse_feed(RSS, "X"), hours=24, now=NOW)
        self.assertEqual([i["title"] for i in items], ["New model"])

    def test_item_without_date_is_dropped(self):
        items = nd.filter_recent(nd.parse_feed(RSS, "X"), hours=24 * 365, now=NOW)
        self.assertNotIn("No date", [i["title"] for i in items])

    def test_newest_first(self):
        items = nd.filter_recent(nd.parse_feed(RSS, "X") + nd.parse_feed(ATOM, "Y"), hours=24, now=NOW)
        self.assertEqual(items[0]["title"], "Atom entry")


class FormatTests(unittest.TestCase):
    def test_no_items_message(self):
        self.assertEqual(nd.format_markdown([], [], 24), "No items in the last 24 h.")

    def test_grouped_by_source_with_warnings(self):
        items = nd.filter_recent(nd.parse_feed(RSS, "X") + nd.parse_feed(ATOM, "Y"), hours=24, now=NOW)
        out = nd.format_markdown(items, ["Z: HTTPError 403"], 24)
        self.assertIn("## X\n- 2026-10-01T06:00:00+00:00 | New model | https://ex.com/a", out)
        self.assertIn("## Y\n- 2026-10-01T07:30:00+00:00 | Atom entry | https://ex.org/p", out)
        self.assertTrue(out.rstrip().endswith("Warnings:\n- Z: HTTPError 403"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_news_digest -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'news_digest'`

- [ ] **Step 3: Write the implementation**

Create `.claude/scripts/news_digest.py` with the Write tool:

```python
#!/usr/bin/env python3
"""
AI News Digest — fetch RSS/Atom feeds from primary AI sources, keep recent
items, print markdown. Standard library only, no LLM.

Usage:
    python3 .claude/scripts/news_digest.py              # last 24 h, markdown
    python3 .claude/scripts/news_digest.py --hours 48
    python3 .claude/scripts/news_digest.py --json
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen

# Primary vendors first. Anthropic has no RSS feed; the morning brief prompt
# fetches https://www.anthropic.com/news directly instead.
FEEDS = [
    ("OpenAI", "https://openai.com/news/rss.xml"),
    ("Google DeepMind", "https://deepmind.google/blog/rss.xml"),
    ("Google AI", "https://blog.google/technology/ai/rss/"),
    ("Microsoft AI", "https://blogs.microsoft.com/ai/feed/"),
    ("Hugging Face", "https://huggingface.co/blog/feed.xml"),
    ("Simon Willison", "https://simonwillison.net/atom/everything/"),
    ("Ars Technica AI", "https://arstechnica.com/ai/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
]

USER_AGENT = "Mozilla/5.0 (compatible; SecondBrain news_digest/1.0)"
ATOM = "{http://www.w3.org/2005/Atom}"
DC_DATE = "{http://purl.org/dc/elements/1.1/}date"
FETCH_TIMEOUT = 10


def fetch(url: str) -> bytes:
    req = Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.1",
    })
    with urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        return resp.read()


def parse_date(raw: str | None) -> datetime | None:
    if not raw:
        return None
    text = raw.strip()
    try:
        return parsedate_to_datetime(text).astimezone(timezone.utc)
    except (TypeError, ValueError, IndexError):
        pass
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def parse_feed(xml_bytes: bytes, source: str) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items = []
    if root.tag == ATOM + "feed":
        for entry in root.findall(ATOM + "entry"):
            link = ""
            for link_el in entry.findall(ATOM + "link"):
                if link_el.get("rel", "alternate") == "alternate":
                    link = link_el.get("href", "")
                    break
            items.append({
                "source": source,
                "title": (entry.findtext(ATOM + "title") or "").strip(),
                "link": link.strip(),
                "published": parse_date(entry.findtext(ATOM + "published") or entry.findtext(ATOM + "updated")),
            })
    else:
        for item in root.iter("item"):
            items.append({
                "source": source,
                "title": (item.findtext("title") or "").strip(),
                "link": (item.findtext("link") or "").strip(),
                "published": parse_date(item.findtext("pubDate") or item.findtext(DC_DATE)),
            })
    return [i for i in items if i["title"] and i["link"]]


def filter_recent(items: list[dict], hours: int, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=hours)
    seen = set()
    kept = []
    for item in items:
        published = item["published"]
        if published is None or published < cutoff or item["link"] in seen:
            continue
        seen.add(item["link"])
        kept.append(item)
    kept.sort(key=lambda i: i["published"], reverse=True)
    return kept


def format_markdown(items: list[dict], warnings: list[str], hours: int) -> str:
    if not items and not warnings:
        return f"No items in the last {hours} h."
    lines = []
    if not items:
        lines.append(f"No items in the last {hours} h.")
    order = [name for name, _ in FEEDS]
    sources = sorted({i["source"] for i in items}, key=lambda s: order.index(s) if s in order else len(order))
    for source in sources:
        lines.append(f"## {source}")
        for item in items:
            if item["source"] == source:
                lines.append(f"- {item['published'].isoformat()} | {item['title']} | {item['link']}")
        lines.append("")
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"- {w}" for w in warnings)
    return "\n".join(lines).rstrip()


def collect(hours: int) -> tuple[list[dict], list[str]]:
    all_items = []
    warnings = []
    for name, url in FEEDS:
        try:
            all_items.extend(parse_feed(fetch(url), name))
        except Exception as exc:  # network and parse errors are both just a skipped feed
            warnings.append(f"{name}: {exc.__class__.__name__}: {str(exc)[:80]}")
    return filter_recent(all_items, hours), warnings


def main():
    parser = argparse.ArgumentParser(description="AI news digest from RSS/Atom feeds")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    items, warnings = collect(args.hours)
    if args.json:
        payload = [{**i, "published": i["published"].isoformat()} for i in items]
        print(json.dumps({"items": payload, "warnings": warnings}, indent=2))
    else:
        print(format_markdown(items, warnings, args.hours))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_news_digest -v`
Expected: 7 tests, `OK`

- [ ] **Step 5: Validate the live feeds**

Run: `python3 .claude/scripts/news_digest.py --hours 72 | head -40`
Expected: at least five `## <Source>` headings. Known at planning time: Microsoft AI returned HTTP 403 to curl. If it still fails here, replace its tuple with `("Azure AI", "https://azure.microsoft.com/en-us/blog/feed/")` and re-run; if that also fails, delete the Microsoft line and record it in the commit message.

- [ ] **Step 6: Commit**

```bash
git add tests/__init__.py tests/test_news_digest.py .claude/scripts/news_digest.py
git commit -m "feat: add LLM-free AI news digest collector"
```

---

### Task 2: Session transcript digest

**Files:**
- Create: `.claude/scripts/sessions_digest.py`
- Test: `tests/test_sessions_digest.py`

**Interfaces:**
- Produces: `collect(claude_dir: Path, codex_dir: Path, hours: int, home: Path, now: float|None) -> list[dict]` with each dict `{"repo", "cwd", "sessions", "last_active" (epoch float), "first_ask", "last_asks": list[str], "last_assistant"}`; `format_markdown(repos: list[dict], warnings: list[str]) -> str`; CLI `python3 .claude/scripts/sessions_digest.py [--hours 36] [--json] [--claude-dir D] [--codex-dir D] [--home H]`.
- Markdown shape consumed by Task 5's prompt:

```
## <repo name>  (<n> sessions, last active HH:MM)
- First ask: <≤300 chars>
- Last asks: <≤300 chars> | <≤300 chars>
- Last assistant: <≤500 chars>
```

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sessions_digest.py`:

```python
import json, os, sys, tempfile, time, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".claude" / "scripts"))
import sessions_digest as sd


def claude_line(kind, content, cwd, ts="2026-09-30T10:00:00Z", sidechain=False):
    return json.dumps({"type": kind, "cwd": cwd, "timestamp": ts, "isSidechain": sidechain,
                       "message": {"role": kind, "content": content}})


def codex_lines(cwd, user_text, assistant_text):
    return [
        json.dumps({"type": "session_meta", "payload": {"cwd": cwd}}),
        json.dumps({"type": "response_item", "timestamp": "2026-09-30T11:00:00Z",
                    "payload": {"type": "message", "role": "developer", "content": [{"type": "input_text", "text": "<skills_instructions>x"}]}}),
        json.dumps({"type": "response_item", "timestamp": "2026-09-30T11:00:01Z",
                    "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "# AGENTS.md instructions for /x"}]}}),
        json.dumps({"type": "response_item", "timestamp": "2026-09-30T11:00:02Z",
                    "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": user_text}]}}),
        json.dumps({"type": "response_item", "timestamp": "2026-09-30T11:05:00Z",
                    "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": assistant_text}]}}),
    ]


class DigestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.claude = self.home / ".claude" / "projects"
        self.codex = self.home / ".codex" / "sessions"
        self.work = self.home / "Documents" / "Work" / "AI and R&D" / "repo-a"
        self.contract = self.home / "Documents" / "Contract" / "Work-client"
        for d in (self.claude / "slug-a", self.codex / "2026" / "10" / "01", self.work, self.contract):
            d.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path: Path, lines, age_hours=1):
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        old = time.time() - age_hours * 3600
        os.utime(path, (old, old))

    def test_claude_session_in_work_repo_is_summarised(self):
        self.write(self.claude / "slug-a" / "s1.jsonl", [
            claude_line("user", "<system-reminder>ignore me</system-reminder>", str(self.work)),
            claude_line("user", "Fix the ingest step", str(self.work), ts="2026-09-30T10:00:00Z"),
            claude_line("assistant", [{"type": "thinking", "thinking": "hmm"}, {"type": "text", "text": "Done. Next: run the tests."}], str(self.work), ts="2026-09-30T10:05:00Z"),
            claude_line("user", [{"type": "tool_result", "content": "ok"}], str(self.work)),
            claude_line("user", "Now add a flag", str(self.work), ts="2026-09-30T10:10:00Z"),
            claude_line("user", "side quest", str(self.work), sidechain=True),
        ])
        repos = sd.collect(self.claude, self.codex, hours=36, home=self.home, now=time.time())
        self.assertEqual(len(repos), 1)
        r = repos[0]
        self.assertEqual(r["repo"], "repo-a")
        self.assertEqual(r["sessions"], 1)
        self.assertEqual(r["first_ask"], "Fix the ingest step")
        self.assertEqual(r["last_asks"], ["Fix the ingest step", "Now add a flag"])
        self.assertEqual(r["last_assistant"], "Done. Next: run the tests.")

    def test_codex_session_parsed_and_noise_skipped(self):
        self.write(self.codex / "2026" / "10" / "01" / "c.jsonl", codex_lines(str(self.work), "Refactor rubric", "Rubric refactored."))
        repos = sd.collect(self.claude, self.codex, hours=36, home=self.home, now=time.time())
        self.assertEqual(repos[0]["first_ask"], "Refactor rubric")
        self.assertEqual(repos[0]["last_assistant"], "Rubric refactored.")

    def test_contract_repo_excluded(self):
        self.write(self.claude / "slug-a" / "s2.jsonl", [claude_line("user", "client work", str(self.contract))])
        self.write(self.codex / "2026" / "10" / "01" / "c2.jsonl", codex_lines(str(self.contract), "client ask", "client reply"))
        repos = sd.collect(self.claude, self.codex, hours=36, home=self.home, now=time.time())
        self.assertEqual(repos, [])

    def test_old_file_skipped(self):
        self.write(self.claude / "slug-a" / "s3.jsonl", [claude_line("user", "ancient", str(self.work))], age_hours=100)
        repos = sd.collect(self.claude, self.codex, hours=36, home=self.home, now=time.time())
        self.assertEqual(repos, [])

    def test_two_sessions_same_repo_merge(self):
        self.write(self.claude / "slug-a" / "s4.jsonl", [claude_line("user", "first", str(self.work), ts="2026-09-30T08:00:00Z")])
        self.write(self.codex / "2026" / "10" / "01" / "c3.jsonl", codex_lines(str(self.work), "second", "reply"))
        repos = sd.collect(self.claude, self.codex, hours=36, home=self.home, now=time.time())
        self.assertEqual(repos[0]["sessions"], 2)
        self.assertEqual(repos[0]["first_ask"], "first")

    def test_markdown_shape(self):
        repos = [{"repo": "repo-a", "cwd": "/x/repo-a", "sessions": 2, "last_active": 0.0,
                  "first_ask": "a", "last_asks": ["a", "b"], "last_assistant": "c"}]
        out = sd.format_markdown(repos, ["bad.jsonl: JSONDecodeError"])
        self.assertIn("## repo-a  (2 sessions, last active ", out)
        self.assertIn("- First ask: a\n- Last asks: a | b\n- Last assistant: c", out)
        self.assertIn("Warnings:\n- bad.jsonl: JSONDecodeError", out)

    def test_truncate_collapses_whitespace(self):
        self.assertEqual(sd.truncate("a   b\n\nc", 300), "a b c")
        self.assertEqual(len(sd.truncate("x" * 400, 300)), 300)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_sessions_digest -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'sessions_digest'`

- [ ] **Step 3: Write the implementation**

Create `.claude/scripts/sessions_digest.py` with the Write tool:

```python
#!/usr/bin/env python3
"""
Sessions Digest — summarise recent Claude Code and Codex transcripts per repo
so the morning brief knows what Frank was working on. No LLM.

Only repos under ~/Documents/Work and ~/Documents/Projects are included.
Contract and Personal repos are excluded so client names never reach the
work brief.

Usage:
    python3 .claude/scripts/sessions_digest.py              # last 36 h, markdown
    python3 .claude/scripts/sessions_digest.py --hours 48 --json
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

INCLUDE_PREFIXES = ("Documents/Work", "Documents/Projects")
NOISE_PREFIXES = (
    "<system-reminder>", "<command-name>", "<command-message>", "<local-command",
    "<skills_instructions>", "<environment_context>", "# AGENTS.md instructions",
    "<task-notification>", "<pasted_content",
)
TEXT_BLOCK_TYPES = ("text", "input_text", "output_text")
ASK_CHARS = 300
ASSISTANT_CHARS = 500


def truncate(text: str, limit: int) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    return collapsed[:limit]


def text_of(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [b["text"] for b in content
                 if isinstance(b, dict) and b.get("type") in TEXT_BLOCK_TYPES and b.get("text")]
        return "\n".join(parts).strip()
    return ""


def is_noise(text: str) -> bool:
    return not text or text.startswith(NOISE_PREFIXES)


def parse_claude(path: Path) -> dict | None:
    cwd = None
    users, assistants = [], []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = row.get("type")
            if kind not in ("user", "assistant"):
                continue
            cwd = cwd or row.get("cwd")
            if row.get("isSidechain"):
                continue
            text = text_of((row.get("message") or {}).get("content"))
            if is_noise(text):
                continue
            (users if kind == "user" else assistants).append((row.get("timestamp", ""), text))
    if not cwd:
        return None
    return {"cwd": cwd, "users": users, "assistants": assistants}


def parse_codex(path: Path) -> dict | None:
    cwd = None
    users, assistants = [], []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = row.get("payload") or {}
            if row.get("type") == "session_meta":
                cwd = payload.get("cwd")
                continue
            if row.get("type") != "response_item" or payload.get("type") != "message":
                continue
            text = text_of(payload.get("content"))
            role = payload.get("role")
            if role == "user" and not is_noise(text):
                users.append((row.get("timestamp", ""), text))
            elif role == "assistant" and text:
                assistants.append((row.get("timestamp", ""), text))
    if not cwd:
        return None
    return {"cwd": cwd, "users": users, "assistants": assistants}


def in_scope(cwd: str, home: Path) -> bool:
    try:
        rel = Path(cwd).resolve().relative_to(home.resolve()).as_posix()
    except ValueError:
        return False
    return rel.startswith(INCLUDE_PREFIXES)


def collect(claude_dir: Path, codex_dir: Path, hours: int, home: Path, now: float | None = None) -> list[dict]:
    now = now or time.time()
    cutoff = now - hours * 3600
    grouped: dict[str, dict] = {}
    warnings: list[str] = []

    candidates = [(p, parse_claude) for p in claude_dir.glob("*/*.jsonl")] + \
                 [(p, parse_codex) for p in codex_dir.rglob("*.jsonl")]
    for path, parser in candidates:
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if mtime < cutoff:
            continue
        try:
            parsed = parser(path)
        except Exception as exc:
            warnings.append(f"{path.name}: {exc.__class__.__name__}")
            continue
        if not parsed or not in_scope(parsed["cwd"], home):
            continue
        bucket = grouped.setdefault(parsed["cwd"], {"users": [], "assistants": [], "sessions": 0, "last_active": 0.0})
        bucket["users"].extend(parsed["users"])
        bucket["assistants"].extend(parsed["assistants"])
        bucket["sessions"] += 1
        bucket["last_active"] = max(bucket["last_active"], mtime)

    repos = []
    for cwd, bucket in grouped.items():
        users = sorted(bucket["users"], key=lambda t: t[0])
        assistants = sorted(bucket["assistants"], key=lambda t: t[0])
        if not users and not assistants:
            continue
        repos.append({
            "repo": Path(cwd).name,
            "cwd": cwd,
            "sessions": bucket["sessions"],
            "last_active": bucket["last_active"],
            "first_ask": truncate(users[0][1], ASK_CHARS) if users else "",
            "last_asks": [truncate(t, ASK_CHARS) for _, t in users[-2:]],
            "last_assistant": truncate(assistants[-1][1], ASSISTANT_CHARS) if assistants else "",
        })
    repos.sort(key=lambda r: r["last_active"], reverse=True)
    collect.warnings = warnings  # exposed for main(); tests call collect() directly
    return repos


def format_markdown(repos: list[dict], warnings: list[str]) -> str:
    if not repos:
        lines = ["No work sessions in the window."]
    else:
        lines = []
        for r in repos:
            when = datetime.fromtimestamp(r["last_active"]).strftime("%H:%M")
            lines.append(f"## {r['repo']}  ({r['sessions']} sessions, last active {when})")
            lines.append(f"- First ask: {r['first_ask']}")
            lines.append(f"- Last asks: {' | '.join(r['last_asks'])}")
            lines.append(f"- Last assistant: {r['last_assistant']}")
            lines.append("")
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"- {w}" for w in warnings)
    return "\n".join(lines).rstrip()


def main():
    parser = argparse.ArgumentParser(description="Digest recent Claude Code and Codex sessions per repo")
    parser.add_argument("--hours", type=int, default=36)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--claude-dir", type=Path, default=None)
    parser.add_argument("--codex-dir", type=Path, default=None)
    args = parser.parse_args()

    claude_dir = args.claude_dir or args.home / ".claude" / "projects"
    codex_dir = args.codex_dir or args.home / ".codex" / "sessions"
    repos = collect(claude_dir, codex_dir, args.hours, args.home)
    warnings = getattr(collect, "warnings", [])
    if args.json:
        print(json.dumps({"repos": repos, "warnings": warnings}, indent=2))
    else:
        print(format_markdown(repos, warnings))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_sessions_digest -v`
Expected: 7 tests, `OK`

- [ ] **Step 5: Run against real transcripts**

Run: `python3 .claude/scripts/sessions_digest.py --hours 48 | head -30`
Expected: headings for `game experience pipeline`, `ai-radar` and `interviewer` (yesterday's work), and no heading containing `Contract`, `lumina`, `verifynNG` or `Personal`.

- [ ] **Step 6: Commit**

```bash
git add tests/test_sessions_digest.py .claude/scripts/sessions_digest.py
git commit -m "feat: add LLM-free session transcript digest"
```

---

### Task 3: Guardrail hook connector branch

**Files:**
- Modify: `.claude/hooks/pre-tool-guardrail.py` (add constants after imports; add `check_connector_send`; call it in `main()` before the final allow)
- Test: `tests/test_guardrail_hook.py`

**Interfaces:**
- Produces: `check_connector_send(tool_name: str, tool_input: dict) -> dict | None` returning `{"decision": "allow"}`, `{"decision": "block", "reason": str}`, or `None` when the tool is not a connector send.
- Module constant `SELF_CHAT_ID` (exact value in Global Constraints).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_guardrail_hook.py`:

```python
import json, subprocess, sys, unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "pre-tool-guardrail.py"
SELF = "19:c142cf69-5033-4b79-9f1b-df23832c13d9_7cb48f87-e8c5-4ac2-8858-9b5433fc0d79@unq.gbl.spaces"
CREW = "19:02a862626ca54619b6babc5593aa33a3@thread.v2"
M365 = "mcp__claude_ai_Microsoft_365__"


def run_hook(tool_name, tool_input):
    proc = subprocess.run([sys.executable, str(HOOK)], input=json.dumps({"tool_name": tool_name, "tool_input": tool_input}),
                          capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


class ConnectorSendTests(unittest.TestCase):
    def test_teams_send_to_self_chat_allowed(self):
        self.assertEqual(run_hook(M365 + "teams_send_chat_message", {"chatId": SELF, "body": "hi"}), {"decision": "allow"})

    def test_teams_send_to_other_chat_blocked(self):
        out = run_hook(M365 + "teams_send_chat_message", {"chatId": CREW, "body": "hi"})
        self.assertEqual(out["decision"], "block")
        self.assertIn("notes-to-self", out["reason"])

    def test_teams_send_missing_chat_id_blocked(self):
        self.assertEqual(run_hook(M365 + "teams_send_chat_message", {"body": "hi"})["decision"], "block")

    def test_outlook_send_blocked(self):
        self.assertEqual(run_hook(M365 + "outlook_send_mail", {"to": ["x@y.com"]})["decision"], "block")

    def test_create_chat_and_channel_post_blocked(self):
        for name in ("teams_create_chat", "teams_send_channel_message", "teams_reply_channel_message",
                     "outlook_send_draft", "outlook_forward_mail"):
            self.assertEqual(run_hook(M365 + name, {})["decision"], "block", name)

    def test_read_tools_still_allowed(self):
        self.assertEqual(run_hook(M365 + "chat_message_search", {"query": "*"}), {"decision": "allow"})
        self.assertEqual(run_hook("Read", {"file_path": "/etc/hosts"}), {"decision": "allow"})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_guardrail_hook -v`
Expected: `test_teams_send_to_other_chat_blocked`, `test_teams_send_missing_chat_id_blocked`, `test_outlook_send_blocked`, `test_create_chat_and_channel_post_blocked` FAIL (hook currently returns allow for every unknown tool). The two allow tests pass already.

- [ ] **Step 3: Implement**

In `.claude/hooks/pre-tool-guardrail.py`, after the `sys.path.insert(...)` line, add:

```python
# Frank's Teams notes-to-self chat. The only chat the agent may post to.
SELF_CHAT_ID = "19:c142cf69-5033-4b79-9f1b-df23832c13d9_7cb48f87-e8c5-4ac2-8858-9b5433fc0d79@unq.gbl.spaces"
TEAMS_SEND_SUFFIX = "teams_send_chat_message"
ALWAYS_BLOCK_SUFFIXES = (
    "teams_create_chat",
    "teams_send_channel_message",
    "teams_reply_channel_message",
    "outlook_send_mail",
    "outlook_send_draft",
    "outlook_forward_mail",
)


def check_connector_send(tool_name: str, tool_input: dict) -> dict | None:
    """Allow Teams sends only to the self-chat; block every other outbound send."""
    if tool_name.endswith(TEAMS_SEND_SUFFIX):
        if tool_input.get("chatId") == SELF_CHAT_ID:
            return {"decision": "allow"}
        return {"decision": "block", "reason": "Teams send only allowed to Frank's notes-to-self chat"}
    if tool_name.endswith(ALWAYS_BLOCK_SUFFIXES):
        short = tool_name.rsplit("__", 1)[-1]
        return {"decision": "block", "reason": f"Outbound send blocked by guardrail ({short})"}
    return None
```

In `main()`, replace the final two lines

```python
    # All other tools: allow
    json.dump({"decision": "allow"}, sys.stdout)
```

with

```python
    connector = check_connector_send(tool_name, tool_input)
    if connector is not None:
        json.dump(connector, sys.stdout)
        return

    # All other tools: allow
    json.dump({"decision": "allow"}, sys.stdout)
```

Also update the module docstring's rule 1 to read `1. Never send emails; never send Teams messages except to Frank's own notes-to-self chat`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_guardrail_hook -v`
Expected: 6 tests, `OK`

- [ ] **Step 5: Commit**

```bash
git add tests/test_guardrail_hook.py .claude/hooks/pre-tool-guardrail.py
git commit -m "feat: enforce self-chat-only Teams sends in guardrail hook"
```

---

### Task 4: Canonical paths and schema text

**Files:**
- Modify: `.claude/scripts/heartbeat.py:39-47`
- Modify: `.claude/skills/vault-structure/SKILL.md:44-60` and `:93-101`
- Modify: `CLAUDE.md:93`

**Interfaces:**
- Produces: `heartbeat.DAILY_DIR == <project>/vault/daily` with no fallback logic.

- [ ] **Step 1: Capture current heartbeat paths**

Run: `cd .claude/scripts && python3 -c "import heartbeat; print(heartbeat.DAILY_DIR, heartbeat.DRAFTS_ACTIVE)"`
Expected: prints `.../vault/daily .../vault/drafts/active` (the fallback already fires because the left-brain dirs do not exist). This is the behaviour we are making explicit.

- [ ] **Step 2: Edit heartbeat.py**

Replace lines 39–47 (the `# Left brain (work) paths` comment through the end of the `if not DAILY_DIR.exists():` block) with:

```python
DAILY_DIR = VAULT_DIR / "daily"
DRAFTS_ACTIVE = VAULT_DIR / "drafts" / "active"
DRAFTS_EXPIRED = VAULT_DIR / "drafts" / "expired"
```

- [ ] **Step 3: Verify**

Run: `cd .claude/scripts && python3 -c "import heartbeat; print(heartbeat.DAILY_DIR.name, heartbeat.DRAFTS_ACTIVE.parent.name)" && python3 heartbeat.py --check habits | head -5`
Expected: `daily drafts` then a habits report with no traceback.

- [ ] **Step 4: Edit the vault-structure skill**

In `.claude/skills/vault-structure/SKILL.md`, in the Directory Map:

Replace the `ballys/` subtree lines for `daily/` (line 44 to the `ai-news-YYYY-MM-DD.md` line) and for `drafts/` (line 55 to the `expired/` line) so the ballys block reads:

```
│   ├── ballys/                # Full-time: AI Software Engineer, AI R&D
│   │   ├── index.md           # Ballys overview, data sources, project list
│   │   ├── inbox/             # Raw dumps from the Teams notes-to-self chat
│   │   │   └── YYYY-MM-DD.md
│   │   ├── daily/             # LEGACY — five April ai-news files; do not add to it
│   │   ├── projects/          # One file per active project
│   │   │   └── STATUS-DASHBOARD.md
│   │   ├── meetings/          # Meeting notes
│   │   │   └── YYYY-MM-DD-<topic>.md
│   │   ├── team/              # Team context
│   │   │   └── ai-rd.md
│   │   ├── portfolio/         # Master project index
│   │   │   └── index.md
│   │   └── sources/           # Work research material
│   │       ├── articles/
│   │       ├── screenshots/
│   │       └── data/
```

Replace the `[DEPRECATED — old structure, pending cleanup from Finder]` block (line 93 to the end of that subtree) with:

```
├── daily/                     # CANONICAL work daily log (append-only). Hooks, reflect,
│   ├── YYYY-MM-DD.md          #   heartbeat and the morning brief all write here.
│   └── ai-news-YYYY-MM-DD.md
└── drafts/                    # CANONICAL draft store
    ├── active/
    ├── sent/
    └── expired/
```

In the Naming Conventions table, change the three rows to:

```
| Work daily log | `daily/YYYY-MM-DD.md` | `daily/2026-04-14.md` |
| AI news | `daily/ai-news-YYYY-MM-DD.md` | `daily/ai-news-2026-04-14.md` |
| Draft reply | `drafts/active/YYYY-MM-DD_<type>_<slug>.md` | `drafts/active/2026-04-14_email_al-review.md` |
```

and add a row:

```
| Self-chat dump | `left-brain/ballys/inbox/YYYY-MM-DD.md` | `left-brain/ballys/inbox/2026-10-01.md` |
```

Add rule 13 under Rules: `13. **Dumps are not to-dos.** Lines in inbox/ are raw capture. Only a message prefixed todo: becomes a task.`

- [ ] **Step 5: Edit CLAUDE.md**

Replace the bullet starting `- **Vault migration is half-done.**` with:

```
- **Work logs live in `vault/daily/`, not `left-brain/ballys/daily/`.** The latter is legacy and holds five April files. The vault-structure skill, hooks, reflect, heartbeat and the morning brief all agree on this since 2026-10-01. Self-chat dumps go to `vault/left-brain/ballys/inbox/`.
```

- [ ] **Step 6: Commit**

```bash
git add .claude/scripts/heartbeat.py .claude/skills/vault-structure/SKILL.md CLAUDE.md
git commit -m "chore: make vault/daily the canonical work log path"
```

---

### Task 5: Headless run prompt

**Superseded:** the prompt text embedded in Step 1 below is the original. The committed `.claude/scripts/morning_brief_prompt.md` (commits 7d35d22 and 9567abe) is authoritative; it reorders news selection before composition, writes the dump cursor before sending, uses `{{NOW_ISO}}` and `{{STATE_DIR}}`, and defines append semantics. See the spec's Implementation notes.

**Files:**
- Create: `.claude/scripts/morning_brief_prompt.md`

**Interfaces:**
- Consumes: placeholders `{{RUN_DIR}}`, `{{DATE}}` (YYYY-MM-DD), `{{NOW}}` (HH:MM), `{{NOW_ISO}}` (full ISO-8601 with UTC offset, the run start), substituted by Task 6's shell script before the prompt reaches `claude -p`.
- Consumes: `digest.md` (Task 2 shape), `gitlab.md` (existing `## Open Issues` list), `news.md` (Task 1 shape) inside `{{RUN_DIR}}`.
- Produces: last stdout line `BRIEF_SENT`, `BRIEF_SENT NEWS_FAILED <reason>`, or `BRIEF_FAILED <reason>`; marker file; daily-log section; inbox file; `morning-brief-state.json`.

- [ ] **Step 1: Write the prompt file**

Create `.claude/scripts/morning_brief_prompt.md` with the Write tool, exactly:

````markdown
You are Frank's second brain running unattended at {{NOW}} on {{DATE}}. Produce today's morning brief. Follow these steps in order. Do not ask questions; if something is unavailable, note it and continue.

## Fixed ids
- SELF_CHAT (Frank's notes-to-self, the ONLY chat you may post to): `19:c142cf69-5033-4b79-9f1b-df23832c13d9_7cb48f87-e8c5-4ac2-8858-9b5433fc0d79@unq.gbl.spaces`
- R&D Stand up meeting chat: `19:meeting_OGNlZjZhMWItMDQ2OS00M2ZlLTljOTUtNzA5MWZiNjQ1NDdk@thread.v2`
- AI Interlock Team: `19:762ccb646d3447e7aec650273198e595@thread.v2`
- AI R&D Crew: `19:02a862626ca54619b6babc5593aa33a3@thread.v2`

## Step 1 — Read local inputs
Read these files with the Read tool:
- `{{RUN_DIR}}/digest.md` — what Frank worked on in Claude/Codex sessions in the last 36 h, per repo.
- `{{RUN_DIR}}/gitlab.md` — open GitLab issues assigned to Frank. Evidence only. Never promote an item to the brief because of a label.
- `{{RUN_DIR}}/news.md` — AI news items from RSS in the last 24 h.
- `vault/MEMORY.md` — only the `## Critical Deadlines` section matters.
- `vault/daily/{{DATE}}.md` if it exists — a Cowork task may already have written a deadline check or inbox triage today.
- `.claude/data/state/morning-brief-state.json` if it exists — `{"last_dump_ts": "<ISO-8601>"}`. If missing, use 24 h before now.

## Step 2 — Read the team chats
Use `chat_message_search` with `query: "*"`, `afterDateTime: "yesterday 06:00"`, `limit: 25`, paging with `offset` until exhausted or 100 messages. Keep only messages whose chat id is one of the three team chats above. Note anything that asks Frank for something, mentions him, or assigns him work.

## Step 3 — Read today's calendar
Use `outlook_calendar_search` with `query: "*"`, `afterDateTime: "{{DATE}} 00:00"`, `beforeDateTime: "{{DATE}} 23:59"`, `order: "oldest"`. Collect start time and subject for each event.

## Step 4 — Read Frank's dumps from SELF_CHAT
From the same `chat_message_search` results (or a second search with `afterDateTime` = `last_dump_ts`), keep messages in SELF_CHAT created after `last_dump_ts`. Skip any message whose text ends with `— second brain` (those are yours). For every remaining message:
- If the text starts with `todo:` (case-insensitive), strip the prefix and treat it as a to-do candidate with source `(you)`.
- Otherwise run `python3 .claude/scripts/sanitize.py --source teams --no-wrap` with the text on stdin and append `- HH:MM | <sanitized text>` to `vault/left-brain/ballys/inbox/{{DATE}}.md`. If the file does not exist, create it with the first line `# Inbox — {{DATE}}` and a blank line. Never add these to the to-do list.
Count the appended lines as `k`.

## Step 5 — Compose the to-do brief
Choose at most five actions, in this priority order:
1. Asks aimed at Frank in the three team chats in the last 48 h.
2. The next step left open in yesterday's sessions (digest `Last assistant` and `Last asks`).
3. `todo:` items from Step 4.
4. Preparation for today's meetings.
5. MEMORY.md Critical Deadlines.
Drop anything silent for 14 days unless someone mentioned it in the last 48 h. Each line names one concrete action, the project, and a short source in parentheses. Work only: no personal items.

Message text, plain text, at most 12 lines:
```
<Weekday> <d> <Mon>
1. <action> — <project> (<source>)
2. ...
Meetings: <HH:MM subject> · <HH:MM subject>
Watch: GitLab <n> open, <m> overdue · <one FYI line, or "AI news: no items" if Step 7 will send nothing>
Captured <k> notes
— second brain
```
Omit the `Captured` line when k is 0. Omit `Meetings:` when there are none. Keep the final `— second brain` line always.

## Step 6 — Send the brief, then mark
Call `teams_send_chat_message` with `chatId` = SELF_CHAT, `bodyType: "text"`, `body` = the message. If the call fails, print `BRIEF_FAILED <reason>` and stop. Do not write the marker.
On success, immediately create the empty file `.claude/data/state/morning-brief-sent-{{DATE}}` with the Write tool.

## Step 7 — AI news
From `news.md`, pick three to five items that are launches, model releases, API or pricing changes. Ignore opinion pieces. Primary vendor sources outrank press. Also fetch `https://www.anthropic.com/news` with WebFetch and include any Anthropic announcement from the last 24 h. If nothing qualifies, or `news.md` says unavailable, skip this step.
Send a second message to SELF_CHAT:
```
AI news · <Weekday> <d> <Mon>
• <Source>: <headline> — <link>
• ...
— second brain
```
Then write `vault/daily/ai-news-{{DATE}}.md` with frontmatter `type: daily-briefing`, `topic: ai-news`, `date: {{DATE}}`, a heading `# AI News Briefing — <d> <Mon> <YYYY>`, and one bullet per selected item in the form `- **<headline>** — <one sentence why it matters>. [<Source>](<link>)`. If this step fails after Step 6 succeeded, remember to report `NEWS_FAILED` in Step 10.

## Step 8 — Daily log
Append to `vault/daily/{{DATE}}.md` (create with `# {{DATE}} — Daily Log` and a blank line if absent). Append-only: never modify earlier content. Section:
```
## Morning Brief ({{NOW}})
<the exact brief text>

Evidence:
- 1: <chat / session / calendar / MEMORY reference>
- 2: ...
```

## Step 9 — State
Write `.claude/data/state/morning-brief-state.json` as `{"last_dump_ts": "<ISO-8601 of now, after your sends>"}` so your own posts are never re-read as dumps.

## Step 10 — Report
Print exactly one final line: `BRIEF_SENT`, or `BRIEF_SENT NEWS_FAILED <reason>` if Step 7 failed.
````

- [ ] **Step 2: Sanity-check placeholders**

Run: `grep -o '{{[A-Z_]*}}' .claude/scripts/morning_brief_prompt.md | sort | uniq -c`
Expected: exactly four placeholder names: `{{DATE}}`, `{{NOW}}`, `{{NOW_ISO}}`, `{{RUN_DIR}}`. (The prompt content was revised in Task 5's fix round 1; see the SDD ledger rulings dated 2026-10-01.)

- [ ] **Step 3: Commit**

```bash
git add .claude/scripts/morning_brief_prompt.md
git commit -m "feat: add morning brief headless prompt"
```

---

### Task 6: Gate and runner script

**Files:**
- Create: `.claude/scripts/morning_brief.sh`
- Test: `tests/test_morning_brief_sh.py`

**Interfaces:**
- Consumes: Task 1, 2 CLIs; `gitlab_integration.py issues`; Task 5 prompt with `{{RUN_DIR}}`, `{{DATE}}`, `{{NOW}}`.
- Test hooks via environment: `MB_STATE_DIR` (state dir override), `MB_DATE` (YYYY-MM-DD), `MB_FAKE_NOW` (HHMM), `MB_FAKE_NOW_ISO` (ISO-8601 override), `MB_FAKE_DOW` (1–7), `MB_SKIP_VPN=1`, `MB_SKIP_CLAUDE=1` (stop after gather, print `DRY_RUN`), `MB_CLAUDE_BIN`.
- Log lines are `YYYY-MM-DD HH:MM:SS | <message>`; skip reasons are literally `skip: weekend`, `skip: outside window (HHMM)`, `skip: already sent today`, `skip: VPN down (probe <code>)`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_morning_brief_sh.py`:

```python
import os, subprocess, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude" / "scripts" / "morning_brief.sh"


def run(env_extra, *args):
    env = {**os.environ, **env_extra}
    proc = subprocess.run(["bash", str(SCRIPT), *args], capture_output=True, text=True, env=env, cwd=ROOT)
    return proc.returncode, proc.stdout + proc.stderr


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = {"MB_STATE_DIR": self.tmp.name, "MB_DATE": "2026-10-01", "MB_SKIP_VPN": "1", "MB_SKIP_CLAUDE": "1"}

    def tearDown(self):
        self.tmp.cleanup()

    def test_weekend_skips(self):
        rc, out = run({**self.base, "MB_FAKE_DOW": "6", "MB_FAKE_NOW": "0800"})
        self.assertEqual(rc, 0); self.assertIn("skip: weekend", out)

    def test_outside_window_skips(self):
        rc, out = run({**self.base, "MB_FAKE_DOW": "3", "MB_FAKE_NOW": "1130"})
        self.assertEqual(rc, 0); self.assertIn("skip: outside window", out)

    def test_window_accepts_leading_zero_time(self):
        rc, out = run({**self.base, "MB_FAKE_DOW": "3", "MB_FAKE_NOW": "0700"})
        self.assertEqual(rc, 0); self.assertIn("DRY_RUN", out)

    def test_already_sent_skips(self):
        Path(self.tmp.name, "morning-brief-sent-2026-10-01").touch()
        rc, out = run({**self.base, "MB_FAKE_DOW": "3", "MB_FAKE_NOW": "0800"})
        self.assertEqual(rc, 0); self.assertIn("skip: already sent today", out)

    def test_force_bypasses_gates_but_gathers(self):
        Path(self.tmp.name, "morning-brief-sent-2026-10-01").touch()
        rc, out = run({**self.base, "MB_FAKE_DOW": "7", "MB_FAKE_NOW": "0300"}, "--force")
        self.assertEqual(rc, 0); self.assertIn("DRY_RUN", out)
        run_dir = Path(self.tmp.name, "run-2026-10-01")
        for name in ("digest.md", "gitlab.md", "news.md"):
            self.assertTrue((run_dir / name).exists(), name)
            self.assertGreater((run_dir / name).stat().st_size, 0, name)

    def test_vpn_down_skips(self):
        env = {**self.base, "MB_FAKE_DOW": "3", "MB_FAKE_NOW": "0800", "MB_PROBE_URL": "http://127.0.0.1:9/"}
        env.pop("MB_SKIP_VPN")
        rc, out = run(env)
        self.assertEqual(rc, 0); self.assertIn("skip: VPN down", out)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_morning_brief_sh -v`
Expected: all 6 FAIL (script does not exist; bash reports `No such file`).

- [ ] **Step 3: Write the script**

Create `.claude/scripts/morning_brief.sh` with the Write tool (the content mentions nothing the Bash guardrail scans for, but use Write anyway):

```bash
#!/bin/bash
# Morning brief runner. Design: docs/superpowers/specs/2026-10-01-morning-brief-design.md
# launchd calls this every 10 minutes. It exits fast unless the gate passes,
# then gathers inputs and runs one headless Claude session that posts to Teams.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

STATE_DIR="${MB_STATE_DIR:-$PROJECT_DIR/.claude/data/state}"
TODAY="${MB_DATE:-$(date +%Y-%m-%d)}"
NOW_HHMM="${MB_FAKE_NOW:-$(date +%H%M)}"
NOW_HM="${NOW_HHMM:0:2}:${NOW_HHMM:2:2}"
NOW_ISO="${MB_FAKE_NOW_ISO:-$(date +%Y-%m-%dT%H:%M:%S%z)}"
DOW="${MB_FAKE_DOW:-$(date +%u)}"
PROBE_URL="${MB_PROBE_URL:-https://gitlab.ballys.tech/api/v4/version}"
CLAUDE_BIN="${MB_CLAUDE_BIN:-$HOME/.local/bin/claude}"
MARKER="$STATE_DIR/morning-brief-sent-$TODAY"
RUN_DIR="$STATE_DIR/run-$TODAY"
PROMPT_FILE="$SCRIPT_DIR/morning_brief_prompt.md"

FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1

log() { printf '%s | %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

mkdir -p "$STATE_DIR"

if (( FORCE == 0 )); then
  if (( DOW >= 6 )); then log "skip: weekend"; exit 0; fi
  if (( 10#$NOW_HHMM < 630 || 10#$NOW_HHMM > 1100 )); then log "skip: outside window ($NOW_HHMM)"; exit 0; fi
  if [[ -e "$MARKER" ]]; then log "skip: already sent today"; exit 0; fi
fi

if [[ "${MB_SKIP_VPN:-0}" != "1" ]]; then
  code="$(curl -s -o /dev/null -m 5 -w '%{http_code}' "$PROBE_URL" || true)"
  case "$code" in
    200|401) ;;
    *) log "skip: VPN down (probe ${code:-000})"; exit 0 ;;
  esac
fi

mkdir -p "$RUN_DIR"
find "$STATE_DIR" -path "$STATE_DIR/run-*" -type f -mtime +7 -delete 2>/dev/null || true
find "$STATE_DIR" -mindepth 1 -maxdepth 1 -type d -name 'run-*' -empty -delete 2>/dev/null || true

log "gather: sessions digest"
python3 .claude/scripts/sessions_digest.py --hours 36 > "$RUN_DIR/digest.md" 2>>"$RUN_DIR/gather.err" \
  || echo "Session digest unavailable." > "$RUN_DIR/digest.md"

log "gather: gitlab"
python3 .claude/scripts/integrations/gitlab_integration.py issues > "$RUN_DIR/gitlab.md" 2>>"$RUN_DIR/gather.err" \
  || echo "GitLab unavailable: check GITLAB_PAT." > "$RUN_DIR/gitlab.md"

log "gather: news"
if ! python3 .claude/scripts/news_digest.py --hours 24 > "$RUN_DIR/news.md" 2>>"$RUN_DIR/gather.err" \
   || ! grep -q '^- ' "$RUN_DIR/news.md"; then
  echo "AI news unavailable." > "$RUN_DIR/news.md"
fi

if [[ "${MB_SKIP_CLAUDE:-0}" == "1" ]]; then
  log "DRY_RUN: gather complete in $RUN_DIR"
  exit 0
fi

if [[ ! -x "$CLAUDE_BIN" ]]; then log "fail: claude binary not found at $CLAUDE_BIN"; exit 1; fi

prompt="$(sed -e "s|{{RUN_DIR}}|$RUN_DIR|g" -e "s|{{DATE}}|$TODAY|g" -e "s|{{NOW}}|$NOW_HM|g" -e "s|{{NOW_ISO}}|$NOW_ISO|g" "$PROMPT_FILE")"

log "run: claude -p"
set +e
out="$("$CLAUDE_BIN" -p "$prompt" --output-format text \
  --allowedTools "Read" "Write" "Edit" "Bash(python3 .claude/scripts/sanitize.py:*)" \
    "WebFetch(domain:www.anthropic.com)" \
    "mcp__claude_ai_Microsoft_365__chat_message_search" \
    "mcp__claude_ai_Microsoft_365__read_resource" \
    "mcp__claude_ai_Microsoft_365__outlook_calendar_search" \
    "mcp__claude_ai_Microsoft_365__teams_send_chat_message" \
  2>>"$RUN_DIR/claude.err")"
rc=$?
set -e
printf '%s\n' "$out" > "$RUN_DIR/claude.out"

if (( rc == 0 )) && grep -q 'BRIEF_SENT' <<<"$out"; then
  touch "$MARKER"
  log "done: brief sent ($(tail -n 1 <<<"$out"))"
  exit 0
fi
log "fail: rc=$rc, see $RUN_DIR/claude.out and claude.err"
exit 1
```

Then: `chmod +x .claude/scripts/morning_brief.sh`

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_morning_brief_sh -v`
Expected: 6 tests, `OK`. The `--force` test takes a few seconds because the news collector hits the network.

- [ ] **Step 5: Commit**

```bash
git add tests/test_morning_brief_sh.py .claude/scripts/morning_brief.sh
git commit -m "feat: add morning brief gate and runner script"
```

---

### Task 7: launchd agent, deploy scripts, first live run

**Files:**
- Create: `deploy/com.secondbrain.morning-brief.plist`
- Modify: `deploy/install.sh` (PLISTS array, line ~137) and `deploy/status.sh` (PLISTS array, line ~196)
- Modify: `CLAUDE.md` Commands section

**Interfaces:**
- Consumes: Task 6 script path.

- [ ] **Step 1: Write the plist**

Create `deploy/com.secondbrain.morning-brief.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.secondbrain.morning-brief</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/frank.enendu/Documents/Personal/Second Brain Starter/.claude/scripts/morning_brief.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/Users/frank.enendu/Documents/Personal/Second Brain Starter</string>
    <key>StandardOutPath</key>
    <string>/Users/frank.enendu/Documents/Personal/Second Brain Starter/.claude/data/logs/morning-brief.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/frank.enendu/Documents/Personal/Second Brain Starter/.claude/data/logs/morning-brief-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/Users/frank.enendu/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>/Users/frank.enendu</string>
    </dict>
</dict>
</plist>
```

Run: `plutil -lint deploy/com.secondbrain.morning-brief.plist`
Expected: `OK`

- [ ] **Step 2: Register in deploy scripts**

In `deploy/install.sh`, add `"com.secondbrain.morning-brief.plist"` as the last element of the `PLISTS=(` array, and add to the "Next steps" echo block the line `echo "  6. Morning brief posts to Teams the first weekday tick after 06:30 with VPN up"`.

In `deploy/status.sh`, add `"com.secondbrain.morning-brief"` as the last element of its `PLISTS=(` array.

- [ ] **Step 3: Dry run end to end without sending**

Run: `MB_SKIP_CLAUDE=1 bash .claude/scripts/morning_brief.sh --force && ls -la .claude/data/state/run-$(date +%Y-%m-%d)/ && head -20 .claude/data/state/run-$(date +%Y-%m-%d)/digest.md`
Expected: `DRY_RUN` log line; three files; digest shows yesterday's repos.

- [ ] **Step 4: First live run**

Confirm Frank has made the SOUL.md edit (or re-granted the read). Then:

Run: `bash .claude/scripts/morning_brief.sh --force; echo "rc=$?"; tail -3 .claude/data/state/run-$(date +%Y-%m-%d)/claude.out`
Expected: `done: brief sent (BRIEF_SENT)`, `rc=0`. Frank confirms two messages in his Teams self-chat, both ending `— second brain`. Check: `ls .claude/data/state/morning-brief-sent-$(date +%Y-%m-%d)`, `grep -c "Morning Brief" vault/daily/$(date +%Y-%m-%d).md` is 1, `ls vault/daily/ai-news-$(date +%Y-%m-%d).md`.

If `claude.err` shows a tool denied, check the tool name against the `--allowedTools` list in Task 6; if it shows the guardrail blocked a send, the `chatId` was wrong: fix the prompt, not the hook.

- [ ] **Step 5: Second forced run must not re-ingest the brief**

Type one test line in the self-chat such as `idea: test dump from Frank`, wait a minute, then re-run `bash .claude/scripts/morning_brief.sh --force`.
Expected: `vault/left-brain/ballys/inbox/$(date +%Y-%m-%d).md` contains the test line once and does not contain the brief text or `— second brain`. Two new messages in the chat. Delete the test line from the inbox file afterwards if desired.

- [ ] **Step 6: Install and observe one real tick**

Run:

```bash
cp deploy/com.secondbrain.morning-brief.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.secondbrain.morning-brief.plist
sleep 5; tail -2 .claude/data/logs/morning-brief.log; launchctl list | grep secondbrain
```

Expected: log ends with `skip: already sent today` (RunAtLoad fired immediately) and `com.secondbrain.morning-brief` appears in the list. Then `./deploy/status.sh` shows the plist loaded.

- [ ] **Step 7: Document commands in CLAUDE.md**

In the Commands section of `CLAUDE.md`, after the "Proactive systems" block, add:

```markdown
Morning brief (launchd ticks every 10 min; gate is weekday, 06:30–11:00, not sent today, VPN up):

```bash
bash .claude/scripts/morning_brief.sh --force        # run now regardless of gate (VPN still required)
MB_SKIP_CLAUDE=1 bash .claude/scripts/morning_brief.sh --force   # gather only, no send
python3 .claude/scripts/sessions_digest.py --hours 36
python3 .claude/scripts/news_digest.py --hours 24
tail -f .claude/data/logs/morning-brief.log
```

Tests (unittest, no pytest installed):

```bash
python3 -m unittest discover -s tests -v
```
```

Also change the sentence `There is no app to build and no test suite.` to `There is no app to build. The only tests are the unittest suite under tests/ for the morning-brief scripts and the guardrail hook.`

- [ ] **Step 8: Full test run and commit**

Run: `python3 -m unittest discover -s tests -v 2>&1 | tail -3`
Expected: `OK` with 26 tests.

```bash
git add deploy/com.secondbrain.morning-brief.plist deploy/install.sh deploy/status.sh CLAUDE.md
git commit -m "feat: schedule morning brief via launchd and document commands"
```

---

### Task 8: Spec alignment and wrap-up

**Files:**
- Modify: `docs/superpowers/specs/2026-10-01-morning-brief-design.md`

- [ ] **Step 1: Record the implementation deltas in the spec**

Append a section:

```markdown
## Implementation notes (2026-10-01)

- `claude` 2.1.286 has no `--max-turns`; the run is bounded by the prompt's step list instead.
- Teams `read_resource` reads a single message by id, so `chat_message_search` is the primary chat reader.
- Run dir, date and time reach the prompt by `{{RUN_DIR}}`, `{{DATE}}`, `{{NOW}}` substitution, not environment variables.
- Agent posts are authored by Frank's account. Re-ingestion is prevented by advancing `last_dump_ts` to the send time and by the `— second brain` trailer.
- Anthropic has no RSS feed; the prompt fetches anthropic.com/news directly.
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/specs/2026-10-01-morning-brief-design.md
git commit -m "docs: record morning brief implementation deltas"
```

- [ ] **Step 3: Hand back**

Report to Frank: branch `feat/morning-brief`, commits, the two messages he received, and the reminder to retire the Cowork AI News task after one clean week. Merging is his call.
