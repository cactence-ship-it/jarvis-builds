"""End-to-end build: provenance honesty, export validity, scale, axes, inventory sync."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from kartal_twin import export_check as xc
from kartal_twin import inventory, pipeline
from kartal_twin.params import Resolver, UnknownParameter


class ResolverRules(unittest.TestCase):
    def test_unknown_without_placeholder_raises(self):
        with self.assertRaises(UnknownParameter):
            Resolver().get("engine.bore")

    def test_placeholder_marks_provenance(self):
        r = Resolver()
        r.get("dimensions.front_track")
        self.assertEqual(r.used, {"dimensions.front_track": "PLACEHOLDER"})
        self.assertEqual(r.geometry_status, "PLACEHOLDER")

    def test_spec_value_beats_placeholder(self):
        base = Resolver()
        spec = copy.deepcopy(base.spec)
        spec["parameters"]["dimensions"]["front_track"].update(
            value=1400, status="ESTIMATED", confidence="LOW", tolerance=30, source=["E-001"])
        r = Resolver(spec, base.assumptions)
        self.assertEqual(r.get("dimensions.front_track"), 1400)
        self.assertEqual(r.geometry_status, "DRAFT")

    def test_estimated_only_gives_draft_never_validated(self):
        r = Resolver()
        r.get("dimensions.overall_length")
        self.assertEqual(r.geometry_status, "DRAFT")


class Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        cls.r = pipeline.run(cls.out)
        cls.parts = {p["id"]: p for p in cls.r["parts"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_no_build_errors_and_manifest_written(self):
        self.assertEqual(self.r["errors"], [])
        self.assertTrue(json.loads((self.out / "manifest.json").read_text())["parts"])

    def test_every_export_reopens_cleanly(self):
        c = self.r["checks"]
        self.assertEqual(c["step"]["solids_read"], c["step"]["solids_written"])
        self.assertLess(c["step"]["volume_rel_error"], 1e-6)
        self.assertTrue(c["step"]["valid"])
        self.assertEqual(c["stl"]["normal_flips"], 0)
        self.assertEqual(c["mesh_closed_outward"]["failed_bodies"], [])
        for k, v in c.items():
            if k.startswith("glb"):
                self.assertEqual(v["issues"], [], k)

    def test_no_part_better_than_its_evidence(self):
        for p in self.r["parts"]:
            if "PLACEHOLDER" in p["parameters"].values():
                self.assertEqual(p["geometry_status"], "PLACEHOLDER", p["id"])
            self.assertNotEqual(p["geometry_status"], "VALIDATED", p["id"])

    def test_overall_dimensions_match_spec(self):
        r = Resolver()
        lo, hi = (np.array(v) for v in self.r["checks"]["stl"]["bbox_mm"])
        self.assertAlmostEqual(hi[0] - lo[0], r.get("dimensions.overall_length"), delta=0.5)
        self.assertAlmostEqual(hi[2], r.get("dimensions.overall_height"), delta=0.5)
        self.assertAlmostEqual(lo[0], -r.get("dimensions.front_overhang"), delta=0.5)

    def test_gltf_front_is_plus_z_and_up_is_plus_y(self):
        js, tris, _ = xc.read_glb(self.out / "vehicle.glb")
        lo, hi = tris.reshape(-1, 3).min(0), tris.reshape(-1, 3).max(0)
        self.assertAlmostEqual(hi[1], Resolver().get("dimensions.overall_height") / 1000, delta=1e-3)
        self.assertGreater(hi[2], 0.5)          # front overhang ahead of the front axle (+Z)
        self.assertLess(lo[2], -3.0)            # rear of the car towards -Z
        names = [n.get("name") for n in js["nodes"]]
        self.assertIn("LGT-001", names)
        self.assertEqual(js["nodes"][0]["name"], "VEHICLE_MASTER")

    def test_inventory_records_built_geometry(self):
        inv = {c["id"]: c for _, _, c in inventory.iter_components(inventory.load_assembly())}
        for cid, p in self.parts.items():
            self.assertEqual(inv[cid]["geometry"][p["representation"]], p["geometry_status"], cid)


if __name__ == "__main__":
    unittest.main()
