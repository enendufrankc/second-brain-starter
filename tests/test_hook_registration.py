import json, unittest
from pathlib import Path

SETTINGS = Path(__file__).resolve().parents[1] / ".claude" / "settings.json"


class HookRegistrationTests(unittest.TestCase):
    def test_pretooluse_guardrail_registered(self):
        entries = json.loads(SETTINGS.read_text())["hooks"]["PreToolUse"]
        commands = [h.get("command", "") for e in entries for h in e.get("hooks", [])]
        self.assertTrue(any("pre-tool-guardrail.py" in c for c in commands), commands)


if __name__ == "__main__":
    unittest.main()
