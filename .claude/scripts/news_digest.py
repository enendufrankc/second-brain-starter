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
        lines.extend(f"Warning: {w}" for w in warnings)
    return "\n".join(lines).rstrip()


def collect(hours: int) -> tuple[list[dict], list[str]]:
    all_items = []
    warnings = []
    for name, url in FEEDS:
        try:
            all_items.extend(parse_feed(fetch(url), name))
        except Exception as exc:  # network and parse errors are both just a skipped feed
            warnings.append(f"{name}: {exc.__class__.__name__}: {' '.join(str(exc).split())[:80]}")
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
