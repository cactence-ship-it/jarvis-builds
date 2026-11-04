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


class MissingIntegrityFiles(unittest.TestCase):
    """ChatGPT T-018 review (bf31d4d): absent integrity files must fail, never read as clean."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        snap = self.root / "audit" / "2026-01-01"
        snap.mkdir(parents=True)
        (snap / "a.txt").write_text("a\n")
        (snap / "SHA256SUMS").write_text(hashlib.sha256(b"a\n").hexdigest() + "  a.txt\n")
        (self.root / "refs").mkdir()
        (self.root / "refs" / "MANIFEST.csv").write_text(
            "ref_id,stored_name,original_name,sha256,bytes,media_type,ingested_utc,storage,source,note\n")

    def fails(self):
        return hashes.failures(hashes.verify_project(self.root))

    def test_complete_project_passes(self):                       # positive control
        self.assertEqual(self.fails(), [])

    def test_missing_manifest_fails(self):
        (self.root / "refs" / "MANIFEST.csv").unlink()
        self.assertEqual(self.fails(), ["refs/MANIFEST.csv: MANIFEST.csv MISSING"])

    def test_manifest_without_header_fails(self):
        (self.root / "refs" / "MANIFEST.csv").write_text("")
        self.assertEqual(self.fails(), ["refs/MANIFEST.csv: MANIFEST.csv MALFORMED"])

    def test_no_audit_snapshot_fails(self):
        shutil.rmtree(self.root / "audit")
        self.assertEqual(self.fails(), ["audit: audit/<date>/SHA256SUMS MISSING"])

    def test_empty_sums_file_fails(self):
        (self.root / "audit" / "2026-01-01" / "SHA256SUMS").write_text("\n")
        self.assertEqual(self.fails(), ["audit/2026-01-01/SHA256SUMS: SHA256SUMS EMPTY"])

    def test_sums_file_passed_directly_but_absent_fails(self):
        res = hashes.verify_sums(self.root / "audit" / "nope" / "SHA256SUMS")
        self.assertEqual(res, [{"file": "SHA256SUMS", "status": "MISSING"}])


class ProjectVerification(unittest.TestCase):
    def test_repository_hashes_are_intact(self):
        res = hashes.verify_project()
        self.assertTrue(any(k.startswith("audit/") for k in res))
        self.assertEqual(hashes.failures(res), [])


if __name__ == "__main__":
    unittest.main()
