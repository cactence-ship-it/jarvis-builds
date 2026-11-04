"""Assembly interface and clearance checks on CAD solids (D-018).

Exact B-rep computations through OpenCascade (BRepExtrema distance, boolean common for
interference volume) - not mesh approximations. Rules live in specs/clearance_rules.yaml.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

import yaml

from . import PROJECT_ROOT

RULES_PATH = PROJECT_ROOT / "specs" / "clearance_rules.yaml"
KINDS = ("no_interference", "ground_contact")


def load_rules(path: Path = RULES_PATH) -> list[dict]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["rules"]


def clearance(a, b) -> float:
    """Minimum distance between two shapes in mm (0.0 when touching or intersecting)."""
    return float(a.distance_to(b))


def interference_volume(a, b) -> float:
    """Volume of the intersection of two solids in mm^3 (0.0 when disjoint)."""
    common = a.intersect(b)
    if common is None:
        return 0.0
    items = list(common) if not hasattr(common, "volume") else [common]
    return float(sum(getattr(s, "volume", 0.0) for s in items))


def check(shapes: dict[str, object], rules: list[dict] | None = None) -> list[dict]:
    """Evaluate every rule against the given {component_id: solid} map.

    Returns one result per rule with status PASS / FAIL / NOT_EVALUATED (a component the
    rule needs has no CAD geometry yet - reported, never silently skipped).
    """
    results = []
    for rule in rules if rules is not None else load_rules():
        if rule["kind"] not in KINDS:
            raise ValueError(f"{rule['id']}: unknown rule kind {rule['kind']}")
        missing = [c for c in rule["components"] if c not in shapes]
        res = {"id": rule["id"], "kind": rule["kind"], "description": rule["description"],
               "components": rule["components"], "measurements": []}
        if missing:
            res.update(status="NOT_EVALUATED", missing=missing)
            results.append(res)
            continue
        ok = True
        if rule["kind"] == "no_interference":
            for a, b in combinations(rule["components"], 2):
                d = clearance(shapes[a], shapes[b])
                vol = interference_volume(shapes[a], shapes[b]) if d == 0.0 else 0.0
                passed = d > rule["min_clearance_mm"] and vol == 0.0
                ok &= passed
                res["measurements"].append({"pair": [a, b], "clearance_mm": round(d, 4),
                                            "interference_mm3": round(vol, 4), "pass": passed})
        elif rule["kind"] == "ground_contact":
            for c in rule["components"]:
                zmin = float(shapes[c].bounding_box().min.Z)
                passed = abs(zmin) <= rule["tolerance_mm"]
                ok &= passed
                res["measurements"].append({"component": c, "z_min_mm": round(zmin, 4), "pass": passed})
        res["status"] = "PASS" if ok else "FAIL"
        results.append(res)
    return results
