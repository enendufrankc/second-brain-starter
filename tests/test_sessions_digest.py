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
