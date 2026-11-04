"""Regression gate on engineering CAD (T-015): a fresh build must reproduce the latest audit
snapshot byte for byte (CAD STEP export is deterministic, D-016). An intended geometry change
must come with a new dated snapshot in audit/<date>/ (D-017)."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from kartal_twin import PROJECT_ROOT

AUDIT = sorted(p for p in (PROJECT_ROOT / "audit").iterdir() if p.is_dir())[-1]


def sums(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text().splitlines():
        h, name = line.split(maxsplit=1)
        out[name.strip()] = h
    return out


class GoldenCad(unittest.TestCase):
    def test_snapshot_is_internally_consistent(self):
        for name, h in sums(AUDIT / "SHA256SUMS").items():
            self.assertEqual(hashlib.sha256((AUDIT / name).read_bytes()).hexdigest(), h, name)

    def test_fresh_build_reproduces_snapshot_cad(self):
        code = ("import sys; sys.path.insert(0, 'src'); from pathlib import Path; "
                "from kartal_twin import pipeline; pipeline.run(Path(sys.argv[1]))")
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable, "-c", code, d], cwd=PROJECT_ROOT, check=True)
            files = json.loads((Path(d) / "manifest.json").read_text())["files"]
        for name, h in sums(AUDIT / "SHA256SUMS").items():
            if name.startswith("cad/"):
                self.assertEqual(files[name]["sha256"], h, f"{name} differs from {AUDIT.name} snapshot")


if __name__ == "__main__":
    unittest.main()
