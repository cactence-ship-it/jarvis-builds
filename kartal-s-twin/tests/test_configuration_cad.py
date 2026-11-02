"""Owner configuration 2026-11-02 (D-026): data classes, engine-variant separation, steel rims,
provisional 185/70 R14 tire geometry and the parametric toroidal LPG tank.

Analytic checks are written here independently of the builders where possible (ISO tire
designation arithmetic, the classical torus volume 2*pi^2*R*r^2, Pappus for the rim section),
and compared with OpenCascade volumes of the built solids.
"""
import copy
import math
import tempfile
import unittest
from pathlib import Path

from kartal_twin import configuration, consistency, interfaces, layout, pipeline, spec
from kartal_twin.assemblies import fuel_system, wheels_and_tires
from kartal_twin.params import Resolver
from kartal_twin.spec import Evidence


class TireGeometry(unittest.TestCase):
    def test_outer_diameter_from_designation(self):
        # OD = rim diameter (in) * 25.4 + 2 * aspect * section width
        self.assertAlmostEqual(layout.Tire(185, 0.70, 14).outer_diameter, 355.6 + 259.0, places=9)   # 614.6
        self.assertAlmostEqual(layout.Tire(175, 0.70, 14).outer_diameter, 355.6 + 245.0, places=9)   # 600.6

    def test_cad_envelope_volume_matches_designation(self):
        t = layout.Tire(185, 0.70, 14)
        expect = math.pi / 4 * (t.outer_diameter ** 2 - 355.6 ** 2) * 185
        self.assertAlmostEqual(wheels_and_tires.tire_envelope(t).volume, expect, delta=expect * 1e-9)


class RimGeometry(unittest.TestCase):
    R = layout.Rim(14, 5.5, 17.5, 3.0, 4.0)

    def test_derived_dimensions(self):
        self.assertAlmostEqual(self.R.bead_seat_radius, 177.8)
        self.assertAlmostEqual(self.R.width_between_flanges, 139.7)
        self.assertAlmostEqual(self.R.outer_radius, 195.3)
        self.assertAlmostEqual(self.R.overall_width, 145.7)

    def test_cad_volume_matches_analytic_section(self):
        m, pi = self.R, math.pi
        rb, t, w, g, d = m.bead_seat_radius, m.steel, m.width_between_flanges, m.flange_height, m.disc
        barrel = pi * (rb ** 2 - (rb - t) ** 2) * (w + 2 * t)
        flanges = 2 * pi * ((rb + g) ** 2 - rb ** 2) * t          # part of each flange outside the barrel
        disc = pi * (rb - t) ** 2 * d                             # part of the disc inside the barrel
        expect = barrel + flanges + disc
        self.assertAlmostEqual(wheels_and_tires.rim_solid(m).volume, expect, delta=expect * 1e-6)

    def test_rim_fits_inside_the_tire(self):
        t = layout.Tire(185, 0.70, 14)
        self.assertLess(self.R.outer_radius, t.outer_diameter / 2)
        self.assertLess(self.R.overall_width, t.section_width)
        self.assertAlmostEqual(self.R.bead_seat_radius, t.rim_radius)   # same nominal diameter

    def test_non_positive_values_are_rejected(self):
        for bad in ({"width_in": 0}, {"flange_height": -1}, {"steel": 0}, {"disc": -4}, {"diameter_in": 0}):
            kw = dict(diameter_in=14, width_in=5.5, flange_height=17.5, steel=3, disc=4) | bad
            with self.assertRaises(ValueError, msg=str(bad)):
                layout.Rim(**kw)


class TankGeometry(unittest.TestCase):
    def test_circular_section_equals_classical_torus(self):
        # opening chosen so the section is a circle: width (600-240)/2 = 180 = height
        D, d, h = 600.0, 240.0, 180.0
        R, r = (D + d) / 4, h / 2
        self.assertAlmostEqual(layout.ToroidalTank.volume_l(D, d, h), 2 * math.pi ** 2 * R * r ** 2 / 1e6, places=9)

    def test_stadium_volume_by_hand(self):
        # 600 x 180, opening 130: width 235, area (235-180)*180 + pi*90^2, centroid radius 182.5
        area = 55 * 180 + math.pi * 90 ** 2
        self.assertAlmostEqual(layout.ToroidalTank.volume_l(600, 130, 180), 2 * math.pi * 182.5 * area / 1e6, places=9)

    def test_cad_volumes_match_pappus(self):
        t = layout.ToroidalTank(600, 180, 130, 3)
        outer, inner, shell = fuel_system.tank_outer(t), fuel_system.tank_inner(t), fuel_system.tank_shell(t)
        self.assertAlmostEqual(outer.volume / 1e6, t.external_volume_l, delta=t.external_volume_l * 1e-6)
        self.assertAlmostEqual(inner.volume / 1e6, t.internal_volume_l, delta=t.internal_volume_l * 1e-6)
        self.assertAlmostEqual(shell.volume / 1e6, t.external_volume_l - t.internal_volume_l, delta=1e-5)
        bb = shell.bounding_box()
        self.assertAlmostEqual(bb.max.X - bb.min.X, 600, delta=1e-6)
        self.assertAlmostEqual(bb.max.Z - bb.min.Z, 180, delta=1e-6)
        self.assertAlmostEqual(bb.min.Z, 0.0, delta=1e-9)                # local frame: underside at Z = 0

    def test_parametric_not_fixed(self):
        a, b = layout.ToroidalTank(600, 180, 130, 3), layout.ToroidalTank(600, 200, 130, 3)
        self.assertGreater(b.internal_volume_l, a.internal_volume_l)
        self.assertAlmostEqual(fuel_system.tank_outer(b).bounding_box().max.Z, 200, delta=1e-6)

    def test_invalid_geometry_is_rejected(self):
        for kw in ({"outer_diameter": 0}, {"height": -180}, {"opening_diameter": 600}, {"wall": 0},
                   {"wall": 95}, {"height": 300}):
            args = dict(outer_diameter=600, height=180, opening_diameter=130, wall=3) | kw
            with self.assertRaises(ValueError, msg=str(kw)):
                layout.ToroidalTank(**args)

    def test_usable_lpg_at_fill_limit(self):
        self.assertAlmostEqual(layout.usable_lpg_l(40, 80), 32.0)
        with self.assertRaises(ValueError):
            layout.usable_lpg_l(40, 120)


def _set(s, pid, value, tol, status="ESTIMATED", conf="LOW"):
    g, k = pid.split(".")
    s["parameters"][g][k].update(value=value, tolerance=tol, status=status, confidence=conf, source=["E-018"])


class CapacityVersusGeometry(unittest.TestCase):
    """DC-018 with pinned inputs (tight tolerances) so PASS / FAIL / INDETERMINATE are all reachable."""

    def _dc018(self, capacity, cap_tol=1.0):
        s = copy.deepcopy(spec.load_spec())
        for pid, v in (("tank_outer_diameter", 600), ("tank_height", 180),
                       ("tank_central_opening_diameter", 130), ("tank_wall_thickness", 3)):
            _set(s, f"lpg_system.{pid}", v, 0.1)
        _set(s, "lpg_system.tank_nominal_capacity", capacity, cap_tol, conf="HIGH")
        return {r["id"]: r for r in consistency.evaluate(s)}["DC-018"]

    def test_small_capacity_fits(self):
        self.assertEqual(self._dc018(35)["status"], "PASS")

    def test_capacity_above_geometry_fails(self):
        r = self._dc018(40)                       # 40 - 1 = 39 L > 38.24 L + small tolerance
        self.assertEqual(r["status"], "FAIL")
        self.assertAlmostEqual(r["rhs"], layout.ToroidalTank(600, 180, 130, 3).internal_volume_l, places=9)

    def test_overlap_is_indeterminate(self):
        self.assertEqual(self._dc018(38.3)["status"], "INDETERMINATE")


class EngineVariant(unittest.TestCase):
    RULES = {"engine_variant_exclusions": {"carburettor": {"E-009": "injection page"}}}

    def _spec(self, fuel_system, src):
        s = copy.deepcopy(spec.load_spec())
        s["parameters"]["engine"]["fuel_system_type"].update(value=fuel_system)
        s["parameters"]["engine"]["max_power"].update(source=src)
        return s

    def test_injection_source_rejected_for_carburettor_engine(self):
        errs = configuration.check(self._spec("carburettor", ["E-009"]), self.RULES)
        self.assertEqual(len(errs), 1)
        self.assertIn("engine.max_power", errs[0])

    def test_same_source_allowed_for_other_variant(self):
        self.assertEqual(configuration.check(self._spec("multi-point injection", ["E-009"]), self.RULES), [])

    def test_live_spec_is_carburettor_and_clean(self):
        s = spec.load_spec()
        self.assertEqual(s["parameters"]["engine"]["fuel_system_type"]["value"], "carburettor")
        self.assertEqual(configuration.check(s), [])


class DataClasses(unittest.TestCase):
    EV = {"U": Evidence("U", "owner", "USER_STATEMENT", "REPORTED"),
          "D": Evidence("D", "doc", "DOCUMENT", "RECEIVED"),
          "M": Evidence("M", "tape", "MEASUREMENT", "RECORDED"),
          "L": Evidence("L", "book", "LITERATURE", "REPORTED"),
          "A": Evidence("A", "assumption", "ASSUMPTION", "REPORTED")}

    def cls(self, status, conf, src):
        return spec.data_class({"status": status, "confidence": conf, "source": src}, self.EV)

    def test_mapping(self):
        self.assertEqual(self.cls("UNKNOWN", "NONE", []), "UNKNOWN")
        self.assertEqual(self.cls("VERIFIED", "HIGH", ["M"]), "MEASURED")
        self.assertEqual(self.cls("VERIFIED", "HIGH", ["D", "U"]), "DOCUMENT_CONFIRMED")
        self.assertEqual(self.cls("ESTIMATED", "HIGH", ["U", "L"]), "USER_CONFIRMED")
        self.assertEqual(self.cls("ESTIMATED", "MEDIUM", ["U"]), "ESTIMATED")      # inferred, not stated
        self.assertEqual(self.cls("ESTIMATED", "MEDIUM", ["L"]), "SOURCE_SUPPORTED")
        self.assertEqual(self.cls("ESTIMATED", "LOW", ["L"]), "ESTIMATED")          # aggregator cap (D-020)
        self.assertEqual(self.cls("ESTIMATED", "LOW", ["A"]), "ESTIMATED")

    def test_assumption_only_value_must_be_low_confidence(self):
        s = copy.deepcopy(spec.load_spec())
        s["parameters"]["lpg_system"]["tank_wall_thickness"].update(confidence="MEDIUM")
        errs = spec.validate_spec(s, spec.load_evidence())
        self.assertTrue(any("tank_wall_thickness" in e and "ASSUMPTION" in e for e in errs), errs)

    def test_no_owner_assumption_is_shown_as_confirmed(self):
        ev = spec.load_evidence()
        for pid, p in spec.iter_parameters(spec.load_spec()):
            kinds = {ev[e].type for e in p["source"]}
            if kinds and kinds <= {"ASSUMPTION"}:
                with self.subTest(pid=pid):
                    self.assertEqual(spec.data_class(p, ev), "ESTIMATED")


class BuiltConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.r = pipeline.run(Path(cls.tmp.name))
        cls.cad = {p["id"]: p for p in cls.r["parts"] if p["representation"] == "cad"}
        cls.cl = {c["id"]: c for c in cls.r["checks"]["clearance"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_no_build_errors(self):
        self.assertEqual(self.r["errors"], [])

    def test_rims_built_placed_and_inside_their_tires(self):
        for cid in ("WHL-006", "WHL-007", "WHL-008", "WHL-009"):
            self.assertEqual(self.cad[cid]["geometry_status"], "DRAFT")
            self.assertTrue(self.cad[cid]["placed_in_vehicle"])
        for rid in ("CL-003", "CL-004", "CL-005", "CL-006", "CL-007"):
            self.assertEqual(self.cl[rid]["status"], "PASS", rid)

    def test_tank_is_draft_unplaced_and_exported(self):
        c = self.r["checks"]["cad"]
        self.assertEqual(self.cad["FUL-005"]["geometry_status"], "DRAFT")
        self.assertFalse(self.cad["FUL-005"]["placed_in_vehicle"])
        self.assertTrue(c["FUL-005"]["valid"])
        self.assertLess(c["FUL-005"]["volume_rel_error"], 1e-6)
        placed = sum(1 for p in self.cad.values() if p["placed_in_vehicle"])
        self.assertEqual(c["_assembly"]["solids_written"], placed)        # tank kept out of the assembly
        self.assertEqual(c["_assembly"]["solids_read"], placed)

    def test_tank_clearance_rules_are_blocked_not_passed(self):
        for rid in ("CL-008", "CL-009", "CL-010", "CL-011", "CL-012"):
            self.assertEqual(self.cl[rid]["status"], "NOT_EVALUATED", rid)
            self.assertIn("FUL-005", self.cl[rid]["missing"])
            self.assertIn("UNKNOWN", self.cl[rid]["blocked_by"])

    def test_visual_tank_is_placeholder(self):
        vis = [p for p in self.r["parts"] if p["id"] == "FUL-005" and p["representation"] == "visual"]
        self.assertEqual(len(vis), 1)
        self.assertEqual(vis[0]["geometry_status"], "PLACEHOLDER")


class WithinBoxRule(unittest.TestCase):
    def test_pass_and_fail(self):
        import build123d as bd
        rule = [{"id": "X", "kind": "within_bbox", "description": "", "components": ["in", "out"]}]
        big, small = bd.Box(10, 10, 10), bd.Box(2, 2, 2)
        self.assertEqual(interfaces.check({"in": small, "out": big}, rule)[0]["status"], "PASS")
        self.assertEqual(interfaces.check({"in": big, "out": small}, rule)[0]["status"], "FAIL")


class NewParametersArePositive(unittest.TestCase):
    def test_numeric_wheel_and_lpg_values_positive(self):
        for pid, p in spec.iter_parameters(spec.load_spec()):
            coordinate = pid.endswith(("_x", "_y", "_z"))             # positions may be 0 or negative
            if pid.split(".")[0] in ("wheels_tires", "lpg_system") and p["status"] != "UNKNOWN" \
                    and isinstance(p["value"], (int, float)) and not coordinate:
                with self.subTest(pid=pid):
                    self.assertGreater(p["value"], 0)
                    self.assertGreater(p["tolerance"], 0)

    def test_resolver_reads_them_without_placeholders(self):
        r = Resolver(allow_placeholders=False)
        layout.rim(r)
        layout.toroidal_tank(r)
        self.assertNotIn("PLACEHOLDER", r.used.values())


if __name__ == "__main__":
    unittest.main()
