"""End-to-end build: provenance honesty, export validity, scale, axes, inventory sync."""
import copy
import json
import math
import re
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
        # Independent of current data: force the record to UNKNOWN so the placeholder is used.
        base = Resolver()
        spec = copy.deepcopy(base.spec)
        spec["parameters"]["dimensions"]["front_track"].update(
            value=None, status="UNKNOWN", confidence="NONE", tolerance=None, source=[])
        r = Resolver(spec, base.assumptions)
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


class EngineeringCad(unittest.TestCase):
    """D-016: the CAD representation uses evidence only (no placeholders)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.r = pipeline.run(Path(cls.tmp.name))
        cls.cad = {p["id"]: p for p in cls.r["parts"] if p["representation"] == "cad"}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_cad_resolver_refuses_placeholders(self):
        with self.assertRaises(UnknownParameter):
            Resolver(allow_placeholders=False).get("body_profile.belt_z")

    TIRES = ["WHL-001", "WHL-002", "WHL-003", "WHL-004"]

    def test_tire_envelopes_are_draft_without_placeholders(self):
        self.assertTrue(set(self.TIRES) <= set(self.cad))
        for p in self.cad.values():                      # every CAD part, incl. rims and LPG tank
            self.assertEqual(p["geometry_status"], "DRAFT")
            self.assertNotIn("PLACEHOLDER", p["parameters"].values())

    def test_step_volume_and_position_match_the_designation(self):
        r = Resolver()
        m = re.fullmatch(r"(\d{3})/(\d{2}) R(\d{2})", r.get("wheels_tires.tire_size_front"))
        w, aspect, rim_in = float(m.group(1)), int(m.group(2)) / 100, float(m.group(3))
        od = rim_in * 25.4 + 2 * aspect * w                   # e.g. 185/70 R14 -> 614.6 mm
        vol = math.pi / 4 * (od ** 2 - (rim_in * 25.4) ** 2) * w
        c = self.r["checks"]["cad"]
        for cid in self.TIRES:
            self.assertTrue(c[cid]["valid"])
            self.assertAlmostEqual(c[cid]["volume_mm3"], vol, delta=vol * 1e-9)
        lo, hi = (np.array(v) for v in c["WHL-002"]["bbox_mm"])   # front right
        self.assertAlmostEqual((lo[1] + hi[1]) / 2, r.get("dimensions.front_track") / 2, delta=1e-6)
        self.assertAlmostEqual(hi[2] - lo[2], od, delta=1e-6)
        lo, hi = (np.array(v) for v in c["WHL-003"]["bbox_mm"])   # rear left
        self.assertAlmostEqual((lo[0] + hi[0]) / 2, r.get("dimensions.wheelbase_lh"), delta=1e-6)
        self.assertEqual(c["_assembly"]["solids_read"], c["_assembly"]["solids_written"])


class Reproducibility(unittest.TestCase):
    def test_two_builds_give_identical_cad_step_and_glb(self):
        # Engineering CAD STEP files and the GLB are byte-reproducible. The coloured visual
        # vehicle.step is not: OCCT writes its colour/style records in varying order, so it is
        # compared geometrically instead (same solids, same volume).
        # Each build runs in its own process, as an auditor would run it: OCCT numbers
        # assembly-usage records with a per-process counter.
        import subprocess
        import sys
        from kartal_twin import PROJECT_ROOT
        code = ("import sys; sys.path.insert(0, 'src'); from pathlib import Path; "
                "from kartal_twin import pipeline; pipeline.run(Path(sys.argv[1]))")
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for d in (a, b):
                subprocess.run([sys.executable, "-c", code, d], cwd=PROJECT_ROOT, check=True)
            ra, rb = (json.loads((Path(d) / "manifest.json").read_text()) for d in (a, b))
            for f in ("vehicle.glb", "cad/vehicle_cad.step", "cad/WHL-001.step", "cad/WHL-004.step"):
                self.assertEqual(ra["files"][f]["sha256"], rb["files"][f]["sha256"], f)
            sa, sb = ra["checks"]["step"], rb["checks"]["step"]
            self.assertEqual(sa["solids_read"], sb["solids_read"])
            self.assertLess(abs(sa["volume_rel_error"] - sb["volume_rel_error"]), 1e-9)

    def test_manifest_lists_only_this_runs_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            stale = Path(d) / "cad" / "OLD-999.step"
            stale.parent.mkdir()
            stale.write_text("stale")
            r = pipeline.run(Path(d))
            self.assertFalse(stale.exists())
            self.assertNotIn("cad/OLD-999.step", r["files"])
            self.assertTrue(all(not k.startswith("delivery") for k in r["files"]))


class WheelbaseAsymmetry(unittest.TestCase):
    """Review finding (ChatGPT, T-001): left/right wheelbases must not be averaged."""

    def _resolver(self, lh, rh, allow=True):
        base = Resolver()
        spec = copy.deepcopy(base.spec)
        for k, v in (("wheelbase_lh", lh), ("wheelbase_rh", rh)):
            spec["parameters"]["dimensions"][k].update(value=v, status="ESTIMATED", confidence="LOW",
                                                       tolerance=10, source=["E-009"])
        return Resolver(spec, base.assumptions, allow_placeholders=allow)

    def test_cad_rear_wheels_use_their_own_side(self):
        from kartal_twin.assemblies.wheels_and_tires import cad_wheel_centres
        c = cad_wheel_centres(self._resolver(2480.0, 2500.0, allow=False))
        self.assertEqual((c["RL"][0], c["RR"][0]), (2480.0, 2500.0))
        self.assertEqual((c["FL"][0], c["FR"][0]), (0.0, 0.0))
        self.assertLess(c["RL"][1], 0)
        self.assertGreater(c["RR"][1], 0)

    def test_visual_rear_wheels_use_their_own_side(self):
        from kartal_twin import layout
        c = layout.wheel_centres(self._resolver(2480.0, 2500.0))
        self.assertEqual((c["RL"][0], c["RR"][0]), (2480.0, 2500.0))
