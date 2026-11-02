"""Owner measurement intake: codes -> VERIFIED spec values -> geometry status DRAFT."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

from kartal_twin import PROJECT_ROOT, spec
from kartal_twin.params import Resolver, load_assumptions

_s = importlib.util.spec_from_file_location("record_measurement", PROJECT_ROOT / "tools" / "record_measurement.py")
rm = importlib.util.module_from_spec(_s)
_s.loader.exec_module(rm)


class MeasurementIntake(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        shutil.copytree(PROJECT_ROOT / "specs", self.root / "specs")
        shutil.copy(PROJECT_ROOT / "EVIDENCE_REGISTER.md", self.root / "EVIDENCE_REGISTER.md")

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_measurement_becomes_verified_and_drives_geometry(self):
        codes = rm._load("measurement_guide").codes()
        wb = next(c for c, p in codes.items() if p == "dimensions.wheelbase_lh")
        belt = next(c for c, p in codes.items() if p == "body_profile.belt_z")
        eid, changed = rm.record(self.root, {wb: 2488.0, belt: 955.0}, 5.0, "test state", "2026-11-02")
        self.assertEqual(set(changed), {"dimensions.wheelbase_lh", "body_profile.belt_z"})
        self.assertTrue((self.root / "evidence" / "measurements" / f"{eid}.yaml").exists())
        ev = spec.load_evidence(self.root / "EVIDENCE_REGISTER.md")
        s = spec.load_spec(self.root / "specs" / "kartal_s_1997.yaml")
        self.assertEqual(spec.validate_spec(s, ev), [])
        self.assertEqual(spec.status_counts(s)["VERIFIED"], 2)
        r = Resolver(s, load_assumptions(self.root / "specs" / "placeholder_assumptions.yaml"))
        self.assertEqual(r.get("body_profile.belt_z"), 955.0)          # measurement beats placeholder
        self.assertEqual(r.used["body_profile.belt_z"], "VERIFIED")

    def test_rejects_unknown_code_and_zero_tolerance(self):
        with self.assertRaises(SystemExit):
            rm.record(self.root, {"M99": 1.0}, 5.0, "x")
        with self.assertRaises(SystemExit):
            rm.record(self.root, {"M01": 4390.0}, 0.0, "x")

    def test_placeholder_cannot_bypass_spec_key(self):
        with self.assertRaises(KeyError):
            Resolver().get("belt_z")


if __name__ == "__main__":
    unittest.main()
