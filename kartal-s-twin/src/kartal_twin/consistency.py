"""Dimensional consistency checks between spec parameters (T-013, D-021).

Rules are pure relations (identities and inequalities) from specs/consistency_rules.yaml.
Tolerances of the inputs are combined worst-case, so a rule FAILs only when the values
cannot be reconciled within their stated uncertainty. Rules with an UNKNOWN input are
NOT_EVALUATED - never silently passed.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from . import PROJECT_ROOT
from .spec import iter_parameters

RULES_PATH = PROJECT_ROOT / "specs" / "consistency_rules.yaml"
KINDS = ("sum_equals", "sum_at_most", "relative_difference_below", "less_than", "at_most", "positive")


def load_rules(path: Path = RULES_PATH) -> list[dict]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["rules"]


def _derived(params: dict) -> dict:
    """Quantities derived from other parameters (value, tolerance) - e.g. tire section width."""
    out = {}
    for axle in ("front", "rear"):
        p = params.get(f"wheels_tires.tire_size_{axle}")
        if p and p["status"] != "UNKNOWN" and isinstance(p["value"], str):
            try:
                width = float(p["value"].split("/")[0])
                aspect = float(p["value"].split("/")[1].split("R")[0]) / 100
            except (ValueError, IndexError):
                continue
            out[f"tire_section_width_{axle}"] = (width, 0.0)
            rim = params.get("wheels_tires.wheel_rim_diameter")
            if rim and rim["status"] != "UNKNOWN" and rim["value"] is not None:
                r_mm = float(rim["value"]) * 25.4 / 2 + width * aspect
                out[f"tire_radius_{axle}"] = (r_mm, float(rim["tolerance"] or 0.0) * 25.4 / 2)
    return out


def _value(key: str, params: dict, derived: dict):
    if key in derived:
        return derived[key]
    p = params.get(key)
    if p is None:
        raise KeyError(f"unknown parameter {key}")
    if p["status"] == "UNKNOWN" or p["value"] is None:
        return None
    return float(p["value"]), float(p["tolerance"] or 0.0)


def evaluate(spec: dict, rules: list[dict] | None = None) -> list[dict]:
    params = dict(iter_parameters(spec))
    derived = _derived(params)
    out = []
    for r in rules if rules is not None else load_rules():
        if r["kind"] not in KINDS:
            raise ValueError(f"{r['id']}: unknown kind {r['kind']}")
        keys = (r.get("terms") or []) + [r[k] for k in ("equals", "at_most", "a", "b") if k in r]
        vals = {k: _value(k, params, derived) for k in keys}
        res = {"id": r["id"], "description": r["description"]}
        missing = [k for k, v in vals.items() if v is None]
        if missing:
            res.update(status="NOT_EVALUATED", missing=missing)
            out.append(res)
            continue
        if r["kind"] in ("sum_equals", "sum_at_most"):
            total = sum(vals[k][0] for k in r["terms"])
            tol = sum(vals[k][1] for k in r["terms"])
            ref_key = r.get("equals") or r.get("at_most")
            ref, rtol = vals[ref_key]
            slack = tol + rtol
            ok = abs(total - ref) <= slack if r["kind"] == "sum_equals" else total <= ref + slack
            res.update(lhs=total, rhs=ref, combined_tolerance=slack)
        elif r["kind"] == "relative_difference_below":
            (a, ta), (b, tb) = vals[r["a"]], vals[r["b"]]
            diff = abs(a - b)
            ok = diff <= r["limit"] * max(a, b) + ta + tb
            res.update(lhs=diff, rhs=r["limit"] * max(a, b), combined_tolerance=ta + tb)
        elif r["kind"] in ("less_than", "at_most"):
            (a, ta), (b, tb) = vals[r["a"]], vals[r["b"]]
            ok = (a < b + ta + tb) if r["kind"] == "less_than" else (a <= b + ta + tb)
            res.update(lhs=a, rhs=b, combined_tolerance=ta + tb)
        else:  # positive
            a, ta = vals[r["a"]]
            ok = a + ta > 0
            res.update(lhs=a, rhs=0.0, combined_tolerance=ta)
        res["status"] = "PASS" if ok else "FAIL"
        out.append(res)
    return out
