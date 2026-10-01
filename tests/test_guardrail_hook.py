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
                     "outlook_send_draft", "outlook_forward_mail",
                     "outlook_respond_to_event", "outlook_set_vacation", "outlook_delete_event"):
            self.assertEqual(run_hook(M365 + name, {})["decision"], "block", name)

    def test_event_with_attendees_blocked_without_attendees_allowed(self):
        out = run_hook(M365 + "outlook_create_event", {"attendees": ["x@y.com"]})
        self.assertEqual(out["decision"], "block")
        self.assertIn("Calendar invite", out["reason"])
        self.assertEqual(run_hook(M365 + "outlook_create_event", {"attendees": []})["decision"], "allow")
        self.assertEqual(run_hook(M365 + "outlook_create_event", {"subject": "x"})["decision"], "allow")

    def test_read_tools_still_allowed(self):
        self.assertEqual(run_hook(M365 + "chat_message_search", {"query": "*"}), {"decision": "allow"})
        self.assertEqual(run_hook("Read", {"file_path": "/etc/hosts"}), {"decision": "allow"})

    def test_teams_send_with_null_tool_input_blocked(self):
        payload = json.dumps({"tool_name": M365 + "teams_send_chat_message", "tool_input": None})
        proc = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "block")


class WriteRootTests(unittest.TestCase):
    def test_write_to_claude_memory_dir_allowed(self):
        path = "/Users/frank.enendu/.claude/projects/-Users-frank-enendu-Documents-Personal-Second-Brain-Starter/memory/note.md"
        self.assertEqual(run_hook("Write", {"file_path": path, "content": "x"}), {"decision": "allow"})

    def test_write_to_home_root_still_blocked(self):
        self.assertEqual(run_hook("Write", {"file_path": "/Users/frank.enendu/other.md", "content": "x"})["decision"], "block")


if __name__ == "__main__":
    unittest.main()
