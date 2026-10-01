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
