"""The private results path, end to end and offline: encrypt_results.sh on the runner,
then collect.sh on your machine (with a stand-in for the GitHub CLI)."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAKE_GH = """#!/usr/bin/env bash
# Stands in for the GitHub CLI: the run's artifacts are already in $FAKE_ARTIFACTS
case "$1 $2" in
  "repo view") echo "someone/app" ;;
  "run download") mkdir -p "$5" && cp -R "$FAKE_ARTIFACTS"/. "$5"/ ;;
  *) echo "unexpected gh call: $*" >&2; exit 1 ;;
esac
"""
REPORT = "Settings: the device name is cut to 'Secret C...'\n"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, check=True, **kw)


def new_key(path):
    run(["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048", "-out", str(path)])
    return path


@unittest.skipUnless(shutil.which("openssl") and shutil.which("bash"), "needs openssl and bash")
class ResultsPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.key = new_key(cls.tmp / "private.pem")
        # The runner: a checkout with the public key and one persona's results
        cls.runner = cls.tmp / "runner"
        (cls.runner / "results" / "noah").mkdir(parents=True)
        run(["openssl", "pkey", "-in", str(cls.key), "-pubout", "-out", str(cls.runner / "results_public.pem")])
        (cls.runner / "results/noah/report.md").write_text(REPORT, encoding="utf-8")
        (cls.runner / "results/noah/findings.json").write_text(json.dumps(
            {"score": 6, "issues": [{"title": "Device name cut", "severity": "minor", "screen": "Settings"}]}))
        cls.encrypt = run(["bash", str(ROOT / "scripts/encrypt_results.sh"), "noah"], cwd=cls.runner)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_runner_uploads_only_ciphertext(self):
        enc = self.runner / "results.enc"
        self.assertEqual(sorted(p.name for p in enc.iterdir()), ["noah.key.bin", "noah.tgz.enc"])
        self.assertFalse((self.runner / "results.tgz").exists())
        self.assertNotIn(b"Secret C", (enc / "noah.tgz.enc").read_bytes())
        # The AES key is only printed inside a mask command, which GitHub hides from the log
        self.assertTrue(all(line.startswith("::add-mask::") for line in self.encrypt.stdout.splitlines()))

    def test_collect_decrypts_and_writes_the_summary(self):
        shutil.copytree(self.runner / "results.enc", self.tmp / "artifacts" / "results-noah")
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(FAKE_GH)
        (bin_dir / "gh").chmod(0o755)
        env = dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
                   FAKE_ARTIFACTS=str(self.tmp / "artifacts"), SUMMARY_GROUPING="0")
        out = self.tmp / "run"
        res = subprocess.run(["bash", str(ROOT / "scripts/collect.sh"), "123", str(self.key), str(out)],
                             cwd=self.tmp, env=env, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertEqual((out / "noah/results/noah/report.md").read_text(encoding="utf-8"), REPORT)
        self.assertIn("| minor | Device name cut | 1 (noah) | Settings |",
                      (out / "SUMMARY.md").read_text(encoding="utf-8"))

    def test_another_key_cannot_open_it(self):
        other = new_key(self.tmp / "other.pem")
        res = subprocess.run(["openssl", "pkeyutl", "-decrypt", "-inkey", str(other), "-pkeyopt",
                              "rsa_padding_mode:oaep", "-in", str(self.runner / "results.enc/noah.key.bin")],
                             capture_output=True)
        self.assertNotEqual(res.returncode, 0)


@unittest.skipUnless(shutil.which("openssl") and shutil.which("bash"), "needs openssl and bash")
class SecondReader(unittest.TestCase):
    """results_agent_public.pem wraps the same key for a second reader; each key opens
    the results through collect.sh, and the owner's path is unchanged."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.owner = new_key(self.tmp / "owner.pem")
        self.agent = new_key(self.tmp / "agent.pem")
        runner = self.tmp / "runner"
        (runner / "results" / "noah").mkdir(parents=True)
        run(["openssl", "pkey", "-in", str(self.owner), "-pubout", "-out", str(runner / "results_public.pem")])
        run(["openssl", "pkey", "-in", str(self.agent), "-pubout", "-out", str(runner / "results_agent_public.pem")])
        (runner / "results/noah/report.md").write_text(REPORT, encoding="utf-8")
        run(["bash", str(ROOT / "scripts/encrypt_results.sh"), "noah"], cwd=runner)
        self.enc = runner / "results.enc"
        shutil.copytree(self.enc, self.tmp / "artifacts" / "results-noah")
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(FAKE_GH)
        (bin_dir / "gh").chmod(0o755)
        self.env = dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
                        FAKE_ARTIFACTS=str(self.tmp / "artifacts"), SUMMARY_GROUPING="0")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def collect(self, key, out):
        return subprocess.run(["bash", str(ROOT / "scripts/collect.sh"), "123", str(key), str(self.tmp / out)],
                              cwd=self.tmp, env=self.env, capture_output=True, text=True)

    def test_both_keys_open_the_results(self):
        self.assertEqual(sorted(p.name for p in self.enc.iterdir()),
                         ["noah.agent-key.bin", "noah.key.bin", "noah.tgz.enc"])
        for key, out in ((self.owner, "by-owner"), (self.agent, "by-agent")):
            res = self.collect(key, out)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertEqual((self.tmp / out / "noah/results/noah/report.md").read_text(encoding="utf-8"), REPORT)

    def test_a_third_key_opens_nothing(self):
        res = self.collect(new_key(self.tmp / "other.pem"), "by-other")
        self.assertNotEqual(res.returncode, 0)
        self.assertFalse((self.tmp / "by-other/noah/results").exists())


if __name__ == "__main__":
    unittest.main()
