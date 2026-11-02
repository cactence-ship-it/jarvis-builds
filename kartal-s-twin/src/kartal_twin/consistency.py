"""Dimensional consistency checks between spec parameters (T-013, D-021).

Rules are pure relations (identities and inequalities) from specs/consistency_rules.yaml.
Every input is an interval [value - tolerance, value + tolerance]; worst case is applied
(review of T-013 by ChatGPT, 2026-11-02):

* inequality (less_than, at_most, sum_at_most, relative_difference_below):
  PASS only if the condition holds for EVERY point of the intervals;
  FAIL if it is violated for every point; otherwise INDETERMINATE (the uncertainty
  is too large to decide - better measurements needed).
* identity (sum_equals): PASS if the intervals can be reconciled (they overlap),
  FAIL if they cannot - an identity can only be checked for consistency.
* any UNKNOWN input: NOT_EVALUATED - never silently passed.
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
    rw = _value("wheels_tires.wheel_rim_width", params, {})
    if rw is not None:
        out["rim_width_mm"] = (rw[0] * 25.4, rw[1] * 25.4)
    tr, sw = _value("dimensions.rear_track", params, {}), out.get("tire_section_width_rear")
    if tr is not None and sw is not None:   # free space between the inner faces of the rear tires
        out["rear_tire_inner_gap"] = (tr[0] - sw[0], tr[1] + sw[1])
    vol = _tank_volume(params)
    if vol is not None:
        out["lpg_tank_internal_volume"] = vol
    return out


def _tank_volume(params: dict):
    """Geometric water capacity (L) of the simplified tank, with a worst-case tolerance from
    the corners of the input intervals (volume rises with D and h, falls with opening and wall)."""
    from .layout import ToroidalTank
    keys = ("lpg_system.tank_outer_diameter", "lpg_system.tank_central_opening_diameter",
            "lpg_system.tank_height", "lpg_system.tank_wall_thickness")
    vals = [_value(k, params, {}) for k in keys]
    if any(v is None for v in vals):
        return None
    (D, tD), (d, td), (h, th), (w, tw) = vals

    def vol(D, d, h, w):
        return ToroidalTank.volume_l(D - 2 * w, d + 2 * w, h - 2 * w)
    nom = vol(D, d, h, w)
    hi = vol(D + tD, max(d - td, 0.0), h + th, max(w - tw, 0.0))
    lo = vol(D - tD, d + td, h - th, w + tw)
    return nom, max(hi - nom, nom - lo)


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
        if r["kind"] == "sum_equals":
            total = sum(vals[k][0] for k in r["terms"])
            slack = sum(vals[k][1] for k in r["terms"]) + vals[r["equals"]][1]
            ref = vals[r["equals"]][0]
            status = "PASS" if abs(total - ref) <= slack else "FAIL"
            res.update(lhs=total, rhs=ref, combined_tolerance=slack)
        else:
            # Reduce every inequality to "x <= y" (or "x < y") on intervals x = [x-, x+], y = [y-, y+].
            if r["kind"] == "sum_at_most":
                x = sum(vals[k][0] for k in r["terms"])
                tx = sum(vals[k][1] for k in r["terms"])
                y, ty = vals[r["at_most"]]
                strict = False
            elif r["kind"] == "relative_difference_below":
                (a, ta), (b, tb) = vals[r["a"]], vals[r["b"]]
                x, tx = abs(a - b), ta + tb           # |a - b| lies in [diff - tx, diff + tx]
                y, ty = r["limit"] * max(a, b), r["limit"] * max(ta, tb)
                strict = True                         # "below" = strictly less than the limit
            elif r["kind"] in ("less_than", "at_most"):
                (x, tx), (y, ty) = vals[r["a"]], vals[r["b"]]
                strict = r["kind"] == "less_than"
            else:  # positive: 0 < a
                (y, ty), x, tx = vals[r["a"]], 0.0, 0.0
                strict = True
            worst_hi, best_lo = x + tx, y - ty          # condition must hold for x+ against y-
            best_x, worst_y = max(x - tx, 0.0) if r["kind"] == "relative_difference_below" else x - tx, y + ty
            holds_everywhere = worst_hi < best_lo if strict else worst_hi <= best_lo
            violated_everywhere = best_x >= worst_y if strict else best_x > worst_y
            status = "PASS" if holds_everywhere else "FAIL" if violated_everywhere else "INDETERMINATE"
            res.update(lhs=x, rhs=y, combined_tolerance=tx + ty, margin_worst_case=best_lo - worst_hi)
        res["status"] = status
        out.append(res)
    return out
