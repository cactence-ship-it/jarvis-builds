"""Clearance / interference checks (T-001): exact B-rep results against analytic values."""
import math
import tempfile
import unittest
from pathlib import Path

import build123d as bd

from kartal_twin import interfaces, pipeline


def box_at(x, size=10.0):
    return bd.Pos(x, 0, size / 2) * bd.Box(size, size, size)


class Primitives(unittest.TestCase):
    def test_gap_touch_and_overlap(self):
        a = box_at(0)
        self.assertAlmostEqual(interfaces.clearance(a, box_at(25)), 15.0, places=6)
        self.assertAlmostEqual(interfaces.clearance(a, box_at(10)), 0.0, places=6)    # touching faces
        self.assertAlmostEqual(interfaces.interference_volume(a, box_at(10)), 0.0, places=6)
        self.assertAlmostEqual(interfaces.interference_volume(a, box_at(4)), 6 * 10 * 10, places=3)


class Rules(unittest.TestCase):
    RULE = [{"id": "X-1", "kind": "no_interference", "description": "t", "components": ["A", "B"],
             "min_clearance_mm": 0.0, "basis": "test"},
            {"id": "X-2", "kind": "ground_contact", "description": "t", "components": ["A"],
             "tolerance_mm": 0.01, "basis": "test"}]

    def test_detects_interference(self):
        r = interfaces.check({"A": box_at(0), "B": box_at(4)}, self.RULE)
        self.assertEqual(r[0]["status"], "FAIL")
        self.assertGreater(r[0]["measurements"][0]["interference_mm3"], 0)

    def test_touching_is_not_clearance(self):
        r = interfaces.check({"A": box_at(0), "B": box_at(10)}, self.RULE)
        self.assertEqual(r[0]["status"], "FAIL")                      # 0 mm is not > 0 mm

    def test_floating_part_fails_ground_contact(self):
        r = interfaces.check({"A": bd.Pos(0, 0, 50) * bd.Box(10, 10, 10), "B": box_at(100)}, self.RULE)
        self.assertEqual(r[1]["status"], "FAIL")

    def test_missing_geometry_is_reported_not_skipped(self):
        r = interfaces.check({"A": box_at(0)}, self.RULE)
        self.assertEqual(r[0]["status"], "NOT_EVALUATED")
        self.assertEqual(r[0]["missing"], ["B"])


class VehicleCad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        r = pipeline.run(Path(cls.tmp.name))
        cls.res = {c["id"]: c for c in r["checks"]["clearance"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_tire_clearances_match_analytic_values(self):
        from kartal_twin.params import Resolver
        r = Resolver()
        tf, tr = r.get("dimensions.front_track"), r.get("dimensions.rear_track")
        wb = r.get("dimensions.wheelbase_lh")
        od, w = 14 * 25.4 + 2 * 0.70 * 175, 175.0
        expect = {("WHL-001", "WHL-002"): tf - w, ("WHL-003", "WHL-004"): tr - w,
                  ("WHL-001", "WHL-003"): wb - od,
                  ("WHL-001", "WHL-004"): math.hypot(wb - od, tf / 2 - w / 2 + tr / 2 - w / 2)}
        got = {tuple(m["pair"]): m["clearance_mm"] for m in self.res["CL-001"]["measurements"]}
        self.assertEqual(self.res["CL-001"]["status"], "PASS")
        for pair, v in expect.items():
            self.assertAlmostEqual(got[pair], v, delta=1e-3, msg=str(pair))

    def test_unloaded_tires_touch_ground(self):
        self.assertEqual(self.res["CL-002"]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
