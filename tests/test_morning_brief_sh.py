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
        self.base = {"MB_STATE_DIR": self.tmp.name, "MB_DATE": "2026-10-01", "MB_SKIP_VPN": "1", "MB_SKIP_CLAUDE": "1", "MB_SKIP_GATHER": "1"}

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
        env = {**self.base, "MB_FAKE_DOW": "7", "MB_FAKE_NOW": "0300"}
        env.pop("MB_SKIP_GATHER")
        rc, out = run(env, "--force")
        self.assertEqual(rc, 0); self.assertIn("DRY_RUN", out)
        run_dir = Path(self.tmp.name, "run-2026-10-01")
        for name in ("digest.md", "gitlab.md", "news.md"):
            self.assertTrue((run_dir / name).exists(), name)
            self.assertGreater((run_dir / name).stat().st_size, 0, name)

    def test_vpn_down_skips(self):
        env = {**self.base, "MB_FAKE_DOW": "3", "MB_FAKE_NOW": "0800", "MB_PROBE_URL": "http://127.0.0.1:9/"}
        env.pop("MB_SKIP_VPN")
        rc, out = run(env)
        self.assertEqual(rc, 0); self.assertIn("skip: VPN down (probe 000)", out)

    def test_window_boundaries(self):
        test_cases = [
            ("0629", "skip: outside window"),
            ("0630", "DRY_RUN"),
            ("1100", "DRY_RUN"),
            ("1101", "skip: outside window"),
        ]
        for time_str, expected in test_cases:
            with self.subTest(time=time_str):
                rc, out = run({**self.base, "MB_FAKE_DOW": "3", "MB_FAKE_NOW": time_str})
                self.assertEqual(rc, 0)
                self.assertIn(expected, out)

    def test_force_still_probes_vpn(self):
        env = {**self.base, "MB_FAKE_DOW": "7", "MB_FAKE_NOW": "0300", "MB_PROBE_URL": "http://127.0.0.1:9/"}
        env.pop("MB_SKIP_VPN")
        rc, out = run(env, "--force")
        self.assertEqual(rc, 0); self.assertIn("skip: VPN down (probe 000)", out)


class ClaudeRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.fake_claude = ROOT / "tests" / "fake_claude.sh"
        self.argv_file = Path(self.tmp.name) / "argv.txt"
        self.base = {
            "MB_STATE_DIR": self.tmp.name,
            "MB_DATE": "2026-10-01",
            "MB_SKIP_VPN": "1",
            "MB_FAKE_DOW": "3",
            "MB_FAKE_NOW": "0800",
            "MB_CLAUDE_BIN": str(self.fake_claude),
            "FAKE_CLAUDE_ARGV": str(self.argv_file),
            "MB_SKIP_GATHER": "1",
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_success_writes_marker_and_exits_zero(self):
        rc, out = run({**self.base, "FAKE_CLAUDE_MODE": "ok"})
        self.assertEqual(rc, 0)
        self.assertIn("done: brief sent", out)
        marker = Path(self.base["MB_STATE_DIR"], "morning-brief-sent-2026-10-01")
        self.assertTrue(marker.exists())

    def test_nonzero_exit_leaves_no_marker(self):
        rc, out = run({**self.base, "FAKE_CLAUDE_MODE": "fail"})
        self.assertEqual(rc, 1)
        self.assertIn("fail: rc=1", out)
        marker = Path(self.base["MB_STATE_DIR"], "morning-brief-sent-2026-10-01")
        self.assertFalse(marker.exists())

    def test_exit_zero_without_sentinel_leaves_no_marker(self):
        rc, out = run({**self.base, "FAKE_CLAUDE_MODE": "notoken"})
        self.assertEqual(rc, 1)
        marker = Path(self.base["MB_STATE_DIR"], "morning-brief-sent-2026-10-01")
        self.assertFalse(marker.exists())

    def test_sentinel_must_be_last_line(self):
        rc, out = run({**self.base, "FAKE_CLAUDE_MODE": "midtoken"})
        self.assertEqual(rc, 1)
        marker = Path(self.base["MB_STATE_DIR"], "morning-brief-sent-2026-10-01")
        self.assertFalse(marker.exists())

    def test_state_dir_placeholder_substituted(self):
        run({**self.base, "FAKE_CLAUDE_MODE": "ok"})
        argv = self.argv_file.read_text()
        self.assertIn(self.tmp.name, argv)
        self.assertNotIn("{{STATE_DIR}}", argv)

    def test_placeholders_substituted_and_tools_passed(self):
        rc, out = run({**self.base, "FAKE_CLAUDE_MODE": "ok"})
        self.assertEqual(rc, 0)
        argv_content = self.argv_file.read_text()
        self.assertNotIn("{{", argv_content)
        self.assertIn("run-2026-10-01", argv_content)
        self.assertIn("--allowedTools", argv_content)
        self.assertIn("--setting-sources", argv_content)
        self.assertIn("project", argv_content)
        self.assertIn("--disallowedTools", argv_content)
        self.assertIn("mcp__claude_ai_Microsoft_365__teams_send_chat_message", argv_content)

    def test_missing_binary_fails_with_log(self):
        env = {**self.base, "MB_CLAUDE_BIN": str(Path(self.tmp.name) / "nope")}
        rc, out = run(env)
        self.assertEqual(rc, 1)
        self.assertIn("fail: claude binary not found", out)

    def test_watchdog_kills_hung_claude(self):
        rc, out = run({**self.base, "FAKE_CLAUDE_MODE": "hang", "MB_CLAUDE_TIMEOUT": "2"})
        self.assertEqual(rc, 1)
        marker = Path(self.base["MB_STATE_DIR"], "morning-brief-sent-2026-10-01")
        self.assertFalse(marker.exists())
        claude_err = Path(self.base["MB_STATE_DIR"], "run-2026-10-01", "claude.err")
        self.assertTrue(claude_err.exists())
        self.assertIn("watchdog: killed claude", claude_err.read_text())

    def test_watchdog_is_cancelled_after_normal_exit(self):
        rc, out = run({**self.base, "FAKE_CLAUDE_MODE": "ok", "MB_CLAUDE_TIMEOUT": "20"})
        self.assertEqual(rc, 0)
        # Verify watchdog process is cleaned up: pgrep should find no "sleep 20" process
        pgrep_result = subprocess.run(["pgrep", "-f", "sleep 20"], capture_output=True)
        self.assertEqual(pgrep_result.returncode, 1, "watchdog sleep process should not be running")


if __name__ == "__main__":
    unittest.main()
