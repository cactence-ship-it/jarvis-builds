"""Reference-file preservation: manifest integrity and the ingest tool's guarantees."""
import csv
import importlib.util
import json
import shutil
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

from kartal_twin import PROJECT_ROOT, REFS_DIR

_spec = importlib.util.spec_from_file_location("ingest_refs", PROJECT_ROOT / "tools" / "ingest_refs.py")
ingest_refs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ingest_refs)


class ManifestIntegrity(unittest.TestCase):
    def test_manifest_rows_match_files(self):
        with open(REFS_DIR / "MANIFEST.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.assertEqual(reader.fieldnames, ingest_refs.FIELDS)
            rows = list(reader)
        for r in rows:
            p = REFS_DIR / "original" / r["stored_name"]
            if r["storage"] == "git":
                self.assertTrue(p.exists(), f"{r['ref_id']} missing from git")
            if p.exists():
                self.assertEqual(ingest_refs.sha256(p), r["sha256"], f"{r['ref_id']} was modified")
                self.assertEqual(p.stat().st_size, int(r["bytes"]))


class IngestTool(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "proj"
        (self.root / "refs").mkdir(parents=True)
        shutil.copy(PROJECT_ROOT / "project.yaml", self.root / "project.yaml")
        self.photo = self.tmp / "IMG 0001.jpg"
        self.photo.write_bytes(b"\xff\xd8\xff" + bytes(range(256)) * 40)
        self.zip = self.tmp / "Legacy.zip"
        with zipfile.ZipFile(self.zip, "w") as z:
            z.writestr("index.html", "<html></html>")
            z.writestr("kartal.json", "{}")

    def tearDown(self):
        for p in (self.root / "refs" / "original").glob("*"):
            p.chmod(stat.S_IWUSR | stat.S_IRUSR)
        shutil.rmtree(self.tmp)

    def test_copy_is_byte_identical_read_only_and_recorded(self):
        r = ingest_refs.ingest([self.photo, self.zip], root=self.root)
        self.assertEqual([x["status"] for x in r], ["ingested", "ingested"])
        stored = self.root / "refs" / "original" / r[0]["stored_name"]
        self.assertEqual(stored.read_bytes(), self.photo.read_bytes())
        self.assertFalse(stored.stat().st_mode & 0o222, "original must be read-only")
        self.assertEqual(r[0]["storage"], "local-only")     # public repo policy
        listing = json.loads((self.root / "refs" / "derived" / f"{r[1]['ref_id']}_zip_listing.json").read_text())
        self.assertIsNone(listing["first_bad_member"])
        self.assertEqual({m["name"] for m in listing["members"]}, {"index.html", "kartal.json"})

    def test_duplicate_is_not_stored_twice_and_restore_works(self):
        first = ingest_refs.ingest([self.photo], root=self.root)[0]
        self.assertEqual(ingest_refs.ingest([self.photo], root=self.root)[0]["status"], "duplicate")
        stored = self.root / "refs" / "original" / first["stored_name"]
        stored.chmod(0o644)
        stored.unlink()                                     # simulate a fresh cloud session
        again = ingest_refs.ingest([self.photo], root=self.root)[0]
        self.assertEqual((again["status"], again["ref_id"]), ("restored", first["ref_id"]))
        rows = ingest_refs.read_manifest(self.root / "refs" / "MANIFEST.csv")
        self.assertEqual(len(rows), 1)

    def test_never_overwrites(self):
        first = ingest_refs.ingest([self.photo], root=self.root)[0]
        other = self.tmp / "other.jpg"
        other.write_bytes(b"different")
        clash = self.root / "refs" / "original" / "R-0002_other.jpg"
        clash.write_bytes(b"pre-existing")
        with self.assertRaises(SystemExit):
            ingest_refs.ingest([other], root=self.root)
        self.assertEqual(clash.read_bytes(), b"pre-existing")
        self.assertEqual(first["ref_id"], "R-0001")


if __name__ == "__main__":
    unittest.main()
