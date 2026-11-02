"""Dimensional consistency rules (T-013): they must catch entry errors, not just pass."""
import copy
import unittest

from kartal_twin import consistency, spec


def setp(s, pid, value, tol=5.0, status="VERIFIED"):
    g, k = pid.split(".")
    s["parameters"][g][k].update(value=value, status=status, confidence="HIGH",
                                 tolerance=tol, source=["E-001"])


class Consistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = spec.load_spec()

    def _res(self, s):
        return {r["id"]: r for r in consistency.evaluate(s)}

    def test_current_spec_has_no_failures(self):
        self.assertNotIn("FAIL", {r["status"] for r in consistency.evaluate(self.base)})

    def test_unknown_inputs_are_not_evaluated(self):
        r = self._res(self.base)["DC-001"]
        self.assertEqual(r["status"], "NOT_EVALUATED")
        self.assertIn("dimensions.front_overhang", r["missing"])

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

    def test_arch_must_clear_the_tire(self):
        s = copy.deepcopy(self.base)
        setp(s, "dimensions.wheel_centre_to_arch_fl", 340.0)       # radius 300.3 +/- 12.7 -> clears
        self.assertEqual(self._res(s)["DC-012"]["status"], "PASS")
        setp(s, "dimensions.wheel_centre_to_arch_fl", 250.0)       # below the tire radius
        self.assertEqual(self._res(s)["DC-012"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
