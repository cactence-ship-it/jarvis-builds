"""Complete-vehicle PLACEHOLDER package (owner master directive 2026-11-03).

* every inventory component has visual geometry, except a short list with a stated reason;
* the mechanical package never claims more than PLACEHOLDER (no evidence-based geometry);
* cabin and engine-bay parts stay inside the body envelope (they once spilled into the rear
  wheel-arch cut-outs - caught by this check).
"""
import unittest

from kartal_twin import inventory
from kartal_twin.pipeline import build_parts

NOT_BUILT = {  # component -> reason it has no separate visual geometry yet
    "BDY-002": "roof is part of the body envelope BDY-001", "BDY-004": "part of BDY-001", "BDY-005": "part of BDY-001",
    "BDY-006": "part of BDY-001", "BDY-007": "part of BDY-001", "EXT-014": "seals not modelled",
    "FUL-007": "LPG filler location UNKNOWN (lpg_system.filler_location)",
}
MECH = ("ENGINE", "TRANSMISSION", "DRIVETRAIN", "CHASSIS", "FRONT_SUSPENSION", "REAR_SUSPENSION", "STEERING",
        "BRAKING", "EXHAUST", "ELECTRICAL", "INTERIOR")
INSIDE = ("INT-", "LGT-010", "ENG-001", "ENG-002", "ENG-003", "ENG-005", "ENG-007", "ENG-008", "ELE-001",
          "ELE-002", "ELE-003", "ELE-005", "ELE-006", "ELE-007", "FUL-013")


class FullVehicle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parts, cls.skipped = build_parts()
        cls.parts = {p.component_id: p for p in parts}

    def test_no_assembly_skipped(self):
        self.assertEqual(self.skipped, [])

    def test_every_component_has_visual_geometry_or_a_reason(self):
        inv = [c["id"] for _, _, c in inventory.iter_components(inventory.load_assembly())]
        missing = sorted(set(inv) - set(self.parts) - set(NOT_BUILT))
        self.assertEqual(missing, [])
        self.assertEqual(sorted(set(NOT_BUILT) & set(self.parts)), [], "NOT_BUILT list is stale")

    def test_mechanical_package_is_placeholder_only(self):
        for p in self.parts.values():
            if p.assembly in MECH:
                with self.subTest(cid=p.component_id):
                    self.assertEqual(p.geometry_status, "PLACEHOLDER")
                    self.assertIn("PLACEHOLDER", p.used.values())

    def test_cabin_and_engine_bay_parts_inside_the_body(self):
        env = [s for cid in ("BDY-001", "BDY-003", "BDY-008", "BDY-009", "BDY-010", "BDY-011", "BDY-012")
               for s, _ in self.parts[cid].bodies]
        shell = env[0]
        for s in env[1:]:
            shell = shell.fuse(s)
        for cid, p in self.parts.items():
            if not cid.startswith(INSIDE):
                continue
            out = tot = 0.0
            for s, _ in p.bodies:
                tot += s.volume
                o = s.cut(shell)
                out += sum(x.volume for x in (o if isinstance(o, list) else [o]) if hasattr(x, "volume"))
            with self.subTest(cid=cid):
                self.assertLessEqual(out / tot, 0.01, f"{cid}: {out / tot:.1%} outside the body envelope")


if __name__ == "__main__":
    unittest.main()
