"""VEHICLE_MASTER inventory structure, generated docs and assembly-module contract."""
import copy
import importlib
import unittest

from kartal_twin import INVENTORY_MD_PATH, inventory, spec
from kartal_twin.assemblies import MODULES


class Inventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ev = spec.load_evidence()
        cls.m = inventory.load_assembly()

    def test_inventory_is_valid(self):
        self.assertEqual(inventory.validate_assembly(self.m, self.ev), [])

    def test_exactly_the_17_master_assemblies(self):
        self.assertEqual(tuple(self.m["assemblies"]), inventory.ASSEMBLY_ORDER)
        self.assertEqual(len(inventory.ASSEMBLY_ORDER), 17)

    def test_markdown_is_up_to_date(self):
        self.assertEqual(INVENTORY_MD_PATH.read_text(encoding="utf-8"),
                         inventory.render_markdown(self.m))

    def test_every_assembly_has_a_builder_module(self):
        for name, asm in self.m["assemblies"].items():
            mod = importlib.import_module(MODULES[name])
            self.assertEqual((mod.ASSEMBLY, mod.PHASE), (name, asm["phase"]))
            with self.assertRaises(NotImplementedError):
                mod.build({})

    def test_no_geometry_claimed_in_phase_1(self):
        for _, _, c in inventory.iter_components(self.m):
            self.assertEqual(set(c["geometry"].values()), {"NONE"}, c["id"])

    # --- negative tests ----------------------------------------------------------------
    def _mutated(self, fn):
        m = copy.deepcopy(self.m)
        fn(m)
        return inventory.validate_assembly(m, self.ev)

    def test_detects_duplicate_id(self):
        def dup(m):
            comps = m["assemblies"]["BODY_ASSEMBLY"]["components"]
            comps.append(copy.deepcopy(comps[0]))
        self.assertTrue(any("duplicate" in e for e in self._mutated(dup)))

    def test_detects_unknown_dependency(self):
        def bad(m):
            m["assemblies"]["BODY_ASSEMBLY"]["components"][1]["dependencies"] = ["BDY-999"]
        self.assertTrue(any("BDY-999" in e for e in self._mutated(bad)))

    def test_detects_dependency_cycle(self):
        def cyc(m):
            m["assemblies"]["BODY_ASSEMBLY"]["components"][0]["dependencies"] = ["BDY-002"]
        self.assertTrue(any("cycle" in e for e in self._mutated(cyc)))

    def test_detects_unsupported_confirmation(self):
        def conf(m):
            m["assemblies"]["BODY_ASSEMBLY"]["components"][0]["fitment"] = "CONFIRMED"
        self.assertTrue(self._mutated(conf))


if __name__ == "__main__":
    unittest.main()
