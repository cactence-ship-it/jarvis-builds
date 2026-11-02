"""Dimensional consistency rules (T-013) with strict worst-case interval semantics.

Revised after ChatGPT's CHANGES_REQUESTED (c665cfb): an inequality PASSes only when it holds
over the whole uncertainty range, FAILs when violated everywhere, otherwise INDETERMINATE.
"""
import copy
import unittest

from kartal_twin import consistency, spec


def setp(s, pid, value, tol=5.0, status="VERIFIED"):
    g, k = pid.split(".")
    s["parameters"][g][k].update(value=value, status=status, confidence="HIGH",
                                 tolerance=tol, source=["E-001"])


R_FRONT = 14 * 25.4 / 2 + 175 * 0.70        # 300.3 mm free radius from 175/70 R14
R_TOL = 1 * 25.4 / 2                          # 12.7 mm from the rim-diameter tolerance (+/-1 in)


class Consistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = spec.load_spec()

    def _res(self, s):
        return {r["id"]: r for r in consistency.evaluate(s)}

    def _arch(self, value, tol):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.wheel_centre_to_arch_fl", value, tol)
        return self._res(s)["DC-012"]

    # --- current data -------------------------------------------------------------------
    def test_current_spec_has_no_failures(self):
        self.assertNotIn("FAIL", {r["status"] for r in consistency.evaluate(self.base)})

    def test_unknown_inputs_are_not_evaluated(self):
        r = self._res(self.base)["DC-001"]
        self.assertEqual(r["status"], "NOT_EVALUATED")
        self.assertIn("dimensions.front_overhang", r["missing"])
        self.assertEqual(self._res(self.base)["DC-012"]["status"], "NOT_EVALUATED")

    # --- tire radius vs wheel-arch clearance (worst case) -----------------------------------
    def test_clearance_safe_over_whole_range(self):
        # arch lower bound 340-5 = 335 > tire upper bound 300.3+12.7 = 313.0
        r = self._arch(340.0, 5.0)
        self.assertEqual(r["status"], "PASS")
        self.assertGreater(r["margin_worst_case"], 0)

    def test_nominally_positive_but_bands_overlap(self):
        # nominal 310 > 300.3, but 310-5 = 305 < 313.0 -> cannot be decided
        self.assertEqual(self._arch(310.0, 5.0)["status"], "INDETERMINATE")

    def test_definitely_insufficient(self):
        # arch upper bound 250+5 = 255 < tire lower bound 300.3-12.7 = 287.6
        self.assertEqual(self._arch(250.0, 5.0)["status"], "FAIL")

    def test_exact_less_than_boundaries(self):
        upper = R_FRONT + R_TOL                    # tire radius upper bound
        self.assertEqual(self._arch(upper + 5.0 + 0.01, 5.0)["status"], "PASS")
        self.assertEqual(self._arch(upper + 5.0, 5.0)["status"], "INDETERMINATE")   # strict '<' fails at equality

    # --- sum_at_most boundaries (front track + tire width <= body width) ---------------------
    def _track(self, track, t_tol, width, w_tol):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.front_track", track, t_tol)
        setp(s, "dimensions.overall_width_body", width, w_tol)
        return self._res(s)["DC-004"]["status"]

    def test_sum_at_most_boundaries(self):
        # x = track + 175, worst x+ = track + 175 + t_tol ; best y- = width - w_tol
        self.assertEqual(self._track(1400, 10, 1600, 10), "PASS")      # 1585 <= 1590
        self.assertEqual(self._track(1405, 10, 1600, 10), "PASS")      # 1590 <= 1590 (non-strict)
        self.assertEqual(self._track(1406, 10, 1600, 10), "INDETERMINATE")
        self.assertEqual(self._track(1446, 10, 1600, 10), "FAIL")      # x- 1611 > y+ 1610

    # --- relative_difference_below is strict ('below' the limit) ------------------------------
    def _wb(self, lh, rh, tol):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.wheelbase_lh", lh, tol)
        setp(s, "dimensions.wheelbase_rh", rh, tol)
        return self._res(s)["DC-003"]

    def test_relative_difference_exact_limit_is_not_pass(self):
        # zero tolerance: |2500 - 2475| = 25 = 1 % of 2500 exactly -> equality must not PASS
        r = self._wb(2475.0, 2500.0, 0.0)
        self.assertNotEqual(r["status"], "PASS")
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(self._wb(2475.01, 2500.0, 0.0)["status"], "PASS")   # just below the limit
        self.assertEqual(self._wb(2474.0, 2500.0, 0.0)["status"], "FAIL")    # just above

    def test_relative_difference_tolerance_band(self):
        # diff 10 +/- 10 against limit 25.0 +/- 0.05: worst 20 < 24.95 -> PASS
        self.assertEqual(self._wb(2490.0, 2500.0, 5.0)["status"], "PASS")
        # diff 20 +/- 10: worst 30 > 24.95 but best 10 < 25.05 -> INDETERMINATE
        self.assertEqual(self._wb(2480.0, 2500.0, 5.0)["status"], "INDETERMINATE")

    # --- unit mix-ups ---------------------------------------------------------------------------
    def test_metre_entry_is_caught(self):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.wheelbase_lh", 2.49, 0.005)            # entered in metres
        self.assertEqual(self._res(s)["DC-003"]["status"], "FAIL")

    def test_centimetre_track_is_caught(self):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.overall_length", 4396)
        setp(s, "dimensions.overall_width_body", 164.2, 1.0)        # width in cm
        self.assertEqual(self._res(s)["DC-004"]["status"], "FAIL")

    # --- entry errors (kept from the first version) -----------------------------------------
    def test_length_identity_pass_and_fail(self):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.overall_length", 4396)
        setp(s, "dimensions.wheelbase_lh", 2490)
        setp(s, "dimensions.front_overhang", 830)
        setp(s, "dimensions.rear_overhang", 1076)
        self.assertEqual(self._res(s)["DC-001"]["status"], "PASS")
        setp(s, "dimensions.rear_overhang", 1176)                   # 100 mm typo
        self.assertEqual(self._res(s)["DC-001"]["status"], "FAIL")

    def test_centimetre_entry_is_caught(self):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.wheelbase_lh", 249.0)                  # entered in cm by mistake
        self.assertEqual(self._res(s)["DC-003"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
