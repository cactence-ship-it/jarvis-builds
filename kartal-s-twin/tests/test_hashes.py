"""SHA-256 verification (T-018): every failure mode must be detected."""
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from kartal_twin import hashes


class SnapshotVerification(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        (self.d / "cad").mkdir()
        (self.d / "cad" / "a.step").write_text("ISO-10303-21;\nEND-ISO-10303-21;\n")
        (self.d / "b.json").write_text('{"x": 1}\n')
        lines = [f"{hashlib.sha256((self.d / f).read_bytes()).hexdigest()}  {f}" for f in ("cad/a.step", "b.json")]
        (self.d / "SHA256SUMS").write_text("\n".join(lines) + "\n")

    def status(self):
        return {e["file"]: e["status"] for e in hashes.verify_sums(self.d / "SHA256SUMS")}

    def test_intact_snapshot_is_ok(self):
        self.assertEqual(set(self.status().values()), {"OK"})

    def test_modified_file_is_mismatch(self):
        (self.d / "cad" / "a.step").write_text("ISO-10303-21;\nTAMPERED\n")
        self.assertEqual(self.status()["cad/a.step"], "MISMATCH")

    def test_missing_file_is_missing(self):
        (self.d / "b.json").unlink()
        self.assertEqual(self.status()["b.json"], "MISSING")

    def test_corrupt_line_is_malformed(self):
        with open(self.d / "SHA256SUMS", "a") as f:
            f.write("not-a-hash  c.txt\n")
        self.assertIn("MALFORMED", self.status().values())

    def test_path_escape_is_rejected(self):
        with open(self.d / "SHA256SUMS", "a") as f:
            f.write("0" * 64 + "  ../outside.txt\n" + "0" * 64 + "  /etc/passwd\n")
        st = self.status()
        self.assertEqual((st["../outside.txt"], st["/etc/passwd"]), ("UNSAFE_PATH", "UNSAFE_PATH"))

    def test_failures_lists_only_problems(self):
        (self.d / "b.json").unlink()
        f = hashes.failures({"x/SHA256SUMS": hashes.verify_sums(self.d / "SHA256SUMS")})
        self.assertEqual(f, ["x/SHA256SUMS: b.json MISSING"])


class ProjectVerification(unittest.TestCase):
    def test_repository_hashes_are_intact(self):
        res = hashes.verify_project()
        self.assertTrue(any(k.startswith("audit/") for k in res))
        self.assertEqual(hashes.failures(res), [])


if __name__ == "__main__":
    unittest.main()
