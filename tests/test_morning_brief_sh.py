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
