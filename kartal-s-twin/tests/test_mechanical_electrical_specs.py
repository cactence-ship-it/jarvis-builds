"""Schema gate for the mechanical and electrical registers (T-024, T-025).

Written after Claude's review of 36b7b6d (agents/CLAUDE_REVIEW_T-024_T-025.md, finding 2):
specs/mechanical_subassembly_register.yaml and specs/electrical_harness_route_matrix.yaml were
read by no code and no test, so neither a silent VERIFIED promotion nor a fabricated electrical
value would have been caught.

The validators below are deliberately pure functions over the loaded documents so the negative
controls can prove each rule actually rejects a bad document. New code is Rust (D-029); these
validators live under tests/ because that is where the rule still allows Python.
"""
import copy
import unittest

import yaml

from kartal_twin import PROJECT_ROOT, spec

MECH_PATH = PROJECT_ROOT / "specs" / "mechanical_subassembly_register.yaml"
ELEC_PATH = PROJECT_ROOT / "specs" / "electrical_harness_route_matrix.yaml"

# A component is a record, not prose: an unexpected key almost always means an unquoted comma
# inside a YAML flow mapping silently split the name into extra keys.
COMPONENT_KEYS = {"id", "name", "geometry", "dimensions", "note", "fitment"}
COMPONENT_REQUIRED = {"id", "name", "geometry", "dimensions"}
ASSEMBLY_REQUIRED = {"id", "name", "architecture", "arrangement_evidence", "geometry_status",
                     "components", "blockers"}
GEOMETRY_STATES = {"PLACEHOLDER", "NONE", "DRAFT_LOCAL_FRAME_ONLY"}

ROUTE_REQUIRED = {"id", "name", "source_node", "destination_nodes", "corridor", "circuit_family",
                  "wire_gauge", "wire_colour", "fuse_rating", "connectors", "route_length",
                  "cad_status", "evidence_needed"}
ROUTE_KEYS = ROUTE_REQUIRED | {"note"}
# D-005 and the owner rule: no colour, cross-section, fuse rating, pinout or cut length may be
# inferred. Until a factory diagram arrives the only honest values are these.
ELECTRICAL_UNKNOWN_FIELDS = ("wire_gauge", "wire_colour", "fuse_rating", "connectors", "route_length")
ELECTRICAL_ALLOWED = {"UNKNOWN", "NOT_APPLICABLE"}


def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def check_mechanical(doc, evidence_ids):
    e = []
    if doc.get("schema_version") != 1:
        e.append("schema_version must be 1")
    if doc.get("vehicle") != "VEH-01":
        e.append("vehicle must be the alias VEH-01 (D-012)")
    seen = set()
    for a in doc.get("assemblies", []):
        aid = a.get("id", "?")
        missing = ASSEMBLY_REQUIRED - set(a)
        if missing:
            e.append(f"{aid}: assembly missing {sorted(missing)}")
        if a.get("geometry_status") not in GEOMETRY_STATES:
            e.append(f"{aid}: geometry_status {a.get('geometry_status')!r} not in {sorted(GEOMETRY_STATES)}")
        for ev in a.get("arrangement_evidence") or []:
            if ev not in evidence_ids:
                e.append(f"{aid}: arrangement_evidence {ev} is not in EVIDENCE_REGISTER.md")
        for c in a.get("components", []) or []:
            cid = c.get("id", "?")
            if cid in seen:
                e.append(f"duplicate component id {cid}")
            seen.add(cid)
            extra = set(c) - COMPONENT_KEYS
            if extra:
                e.append(f"{cid}: unexpected key(s) {sorted(extra)} - an unquoted comma in the "
                         f"flow mapping split the name; name is only {c.get('name')!r}")
            for k in sorted(COMPONENT_REQUIRED - set(c)):
                e.append(f"{cid}: component missing {k}")
            if "geometry" in c and c["geometry"] not in GEOMETRY_STATES:
                e.append(f"{cid}: geometry {c['geometry']!r} not in {sorted(GEOMETRY_STATES)}")
            if c.get("dimensions") != "UNKNOWN":
                e.append(f"{cid}: dimensions must stay UNKNOWN until measurements arrive, got "
                         f"{c.get('dimensions')!r}")
    if not seen:
        e.append("register declares no components")
    return e


def check_electrical(doc, evidence_ids):
    e = []
    if doc.get("schema_version") != 1:
        e.append("schema_version must be 1")
    if doc.get("vehicle") != "VEH-01":
        e.append("vehicle must be the alias VEH-01 (D-012)")
    ev = doc.get("evidence") or {}
    for key in ("factory_wiring_diagram", "loom_label_photos"):
        if key not in ev:
            e.append(f"evidence.{key} must state its receipt status")
    for ref in ev.get("arrangement_photos") or []:
        if ref not in evidence_ids:
            e.append(f"evidence.arrangement_photos {ref} is not in EVIDENCE_REGISTER.md")
    seen = set()
    for g in doc.get("route_groups", []):
        gid = g.get("id", "?")
        if gid in seen:
            e.append(f"duplicate route group id {gid}")
        seen.add(gid)
        for k in sorted(ROUTE_REQUIRED - set(g)):
            e.append(f"{gid}: route group missing {k}")
        extra = set(g) - ROUTE_KEYS
        if extra:
            e.append(f"{gid}: unexpected key(s) {sorted(extra)}")
        if g.get("cad_status") not in GEOMETRY_STATES:
            e.append(f"{gid}: cad_status {g.get('cad_status')!r} not in {sorted(GEOMETRY_STATES)}")
        for field in ELECTRICAL_UNKNOWN_FIELDS:
            if field in g and g[field] not in ELECTRICAL_ALLOWED:
                e.append(f"{gid}: {field} is {g[field]!r} - no colour, cross-section, fuse rating, "
                         f"pinout or cut length may be inferred without a factory diagram")
        if not (g.get("destination_nodes") or []):
            e.append(f"{gid}: needs at least one destination node")
        if not (g.get("evidence_needed") or []):
            e.append(f"{gid}: needs its outstanding evidence listed")
    if not seen:
        e.append("matrix declares no route groups")
    return e


class RegistersAreValid(unittest.TestCase):
    """Positive control: the committed registers satisfy every rule."""

    @classmethod
    def setUpClass(cls):
        cls.ids = set(spec.load_evidence())
        cls.mech = _load(MECH_PATH)
        cls.elec = _load(ELEC_PATH)

    def test_mechanical_register_schema(self):
        self.assertEqual([], check_mechanical(self.mech, self.ids))

    def test_electrical_matrix_schema(self):
        self.assertEqual([], check_electrical(self.elec, self.ids))

    def test_no_verified_geometry_without_primary_evidence(self):
        """Neither register may introduce a VERIFIED value: VERIFIED lives in the master spec,
        backed by a primary evidence item (D-005)."""
        for path in (MECH_PATH, ELEC_PATH):
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "VERIFIED" in line and not line.lstrip().startswith(("#", "VERIFIED:")):
                    self.fail(f"{path.name}:{lineno} introduces VERIFIED outside the status legend: {line.strip()}")

    def test_variant_gate_keeps_injection_out(self):
        gate = self.mech["variant_gate"]
        self.assertIn("carburettor", gate["required_variant"])
        self.assertTrue(any("i.e." in x for x in gate["exclude"]),
                        "the 1.6 i.e. exclusion must stay explicit")
        self.assertEqual("UNKNOWN", gate["unresolved_engine_identity"]["status"])


class NegativeControls(unittest.TestCase):
    """Each rule must actually reject a bad document, otherwise the gate is decoration."""

    @classmethod
    def setUpClass(cls):
        cls.ids = set(spec.load_evidence())
        cls.mech = _load(MECH_PATH)
        cls.elec = _load(ELEC_PATH)

    def assertRejects(self, errors, needle):
        self.assertTrue(any(needle in x for x in errors),
                        f"expected an error containing {needle!r}, got {errors}")

    def test_unquoted_comma_in_component_name_is_rejected(self):
        d = copy.deepcopy(self.mech)
        d["assemblies"][0]["components"][0]["rings and connecting rods"] = None
        self.assertRejects(check_mechanical(d, self.ids), "unquoted comma")

    def test_dimension_promotion_is_rejected(self):
        d = copy.deepcopy(self.mech)
        d["assemblies"][0]["components"][0]["dimensions"] = {"length": 350}
        self.assertRejects(check_mechanical(d, self.ids), "must stay UNKNOWN")

    def test_unknown_evidence_id_is_rejected(self):
        d = copy.deepcopy(self.mech)
        d["assemblies"][0]["arrangement_evidence"] = ["E-999"]
        self.assertRejects(check_mechanical(d, self.ids), "E-999")

    def test_duplicate_component_id_is_rejected(self):
        d = copy.deepcopy(self.mech)
        first = d["assemblies"][0]["components"][0]
        d["assemblies"][0]["components"].append(copy.deepcopy(first))
        self.assertRejects(check_mechanical(d, self.ids), "duplicate component id")

    def test_missing_component_field_is_rejected(self):
        d = copy.deepcopy(self.mech)
        d["assemblies"][0]["components"][0].pop("geometry")
        self.assertRejects(check_mechanical(d, self.ids), "missing geometry")

    def test_fabricated_wire_gauge_is_rejected(self):
        d = copy.deepcopy(self.elec)
        d["route_groups"][0]["wire_gauge"] = "2.5 mm2"
        self.assertRejects(check_electrical(d, self.ids), "may be inferred")

    def test_fabricated_fuse_rating_is_rejected(self):
        d = copy.deepcopy(self.elec)
        d["route_groups"][0]["fuse_rating"] = "15 A"
        self.assertRejects(check_electrical(d, self.ids), "may be inferred")

    def test_fabricated_route_length_is_rejected(self):
        d = copy.deepcopy(self.elec)
        d["route_groups"][0]["route_length"] = 1840
        self.assertRejects(check_electrical(d, self.ids), "may be inferred")

    def test_route_group_without_evidence_list_is_rejected(self):
        d = copy.deepcopy(self.elec)
        d["route_groups"][0]["evidence_needed"] = []
        self.assertRejects(check_electrical(d, self.ids), "outstanding evidence")


if __name__ == "__main__":
    unittest.main()
