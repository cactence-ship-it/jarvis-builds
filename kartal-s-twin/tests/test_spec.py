"""Master spec + evidence register integrity, including proof that fabrication is rejected."""
import copy
import unittest

from kartal_twin import spec


class SpecIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ev = spec.load_evidence()
        cls.spec = spec.load_spec()

    def test_evidence_register_is_valid(self):
        self.assertGreaterEqual(len(self.ev), 1)
        self.assertEqual(spec.validate_evidence(self.ev), [])

    def test_master_spec_is_valid(self):
        self.assertEqual(spec.validate_spec(self.spec, self.ev), [])

    def test_no_verified_values_without_received_evidence(self):
        # Phase 1: nothing has been received yet, so nothing may be VERIFIED.
        self.assertEqual(spec.status_counts(self.spec)["VERIFIED"], 0)

    def test_units_and_coordinate_system_declared(self):
        self.assertEqual(self.spec["units"]["length"], "mm")
        cs = self.spec["coordinate_system"]
        self.assertEqual((cs["x"]["axis"], cs["y"]["axis"], cs["z"]["axis"]),
                         ("longitudinal", "lateral", "vertical"))

    # --- negative tests: each fabrication pattern must be caught -------------------------
    def _errors_after(self, **changes):
        s = copy.deepcopy(self.spec)
        s["parameters"]["dimensions"]["wheelbase_lh"].update(changes)
        return spec.validate_spec(s, self.ev)

    def test_rejects_unknown_with_a_number(self):
        self.assertTrue(self._errors_after(value=2500))

    def test_rejects_verified_from_owner_statement_only(self):
        errs = self._errors_after(value=2500, status="VERIFIED", confidence="HIGH",
                                  tolerance=1, source=["E-001"])
        self.assertTrue(any("RECEIVED PHOTO/DOCUMENT/MEASUREMENT" in e for e in errs))

    def test_rejects_estimate_without_tolerance(self):
        errs = self._errors_after(value=2500, status="ESTIMATED", confidence="LOW", source=["E-001"])
        self.assertTrue(any("tolerance" in e for e in errs))

    def test_rejects_unregistered_evidence(self):
        errs = self._errors_after(value=2500, status="ESTIMATED", confidence="LOW",
                                  tolerance=50, source=["E-999"])
        self.assertTrue(any("E-999" in e for e in errs))

    def test_rejects_missing_field(self):
        s = copy.deepcopy(self.spec)
        del s["parameters"]["dimensions"]["wheelbase_lh"]["source"]
        self.assertTrue(spec.validate_spec(s, self.ev))

    def test_accepts_properly_sourced_estimate(self):
        self.assertEqual(self._errors_after(value=2500, status="ESTIMATED", confidence="LOW",
                                            tolerance=50, source=["E-001"]), [])


if __name__ == "__main__":
    unittest.main()
