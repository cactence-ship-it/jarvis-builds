#!/usr/bin/env python3
"""Turn pixel points marked on a SIDE-PROFILE photo into VCS millimetres (Phase 2).

    python tools/photo_scale.py points.yaml [--apply E-0xx]

points.yaml (pixel coordinates, image y grows downwards):
    front_wheel: [x, y]          # front wheel centre
    rear_wheel:  [x, y]          # rear wheel centre
    ground: [[x, y], [x, y]]     # two points on the ground line (tyre contact patches)
    points:                      # spec parameter -> pixel point
      body_profile.belt_z: [x, y]
      body_profile.cowl_x: [x, y]
    pixel_error: 3               # optional, px (default 3)

Scale = wheelbase (from the spec) / pixel distance between the wheel centres. X is measured
rearward from the front wheel centre along the wheel-centre line, Z upward from the ground
line, so camera roll is removed. *_x parameters take X, *_z parameters take Z.

Results are photo-derived ESTIMATES: tolerance = pixel error (both ends, scale-converted)
combined with a lens/perspective allowance (default 2 % of the value) and the wheelbase
tolerance. --apply writes them as ESTIMATED with the given PHOTO evidence ID, but never
replaces a VERIFIED value or an estimate with a smaller tolerance.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import yaml

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS.parent / "src"))
from kartal_twin.spec import iter_parameters, load_spec  # noqa: E402

PERSPECTIVE = 0.02


def solve(pts: dict, wheelbase: float, wheelbase_tol: float = 0.0,
          perspective: float = PERSPECTIVE) -> dict[str, tuple[float, float]]:
    f, r = np.array(pts["front_wheel"], float), np.array(pts["rear_wheel"], float)
    g0, g1 = (np.array(p, float) for p in pts["ground"])
    px_err = float(pts.get("pixel_error", 3))
    axis = r - f
    scale = wheelbase / np.linalg.norm(axis)               # mm per pixel
    ux = axis / np.linalg.norm(axis)                        # rearward direction in the image
    gd = (g1 - g0) / np.linalg.norm(g1 - g0)
    up = np.array([gd[1], -gd[0]])                          # normal to the ground line
    if up[1] > 0:                                           # image y grows downwards: 'up' must point to -y
        up = -up
    out = {}
    for pid, p in (pts.get("points") or {}).items():
        p = np.array(p, float)
        if pid.endswith("_x"):
            v = float((p - f) @ ux * scale)
        elif pid.endswith("_z"):
            v = float((p - g0) @ up * scale)
        else:
            raise ValueError(f"{pid}: only *_x or *_z parameters can be read from a side photo")
        tol = math.sqrt(2 * (px_err * scale) ** 2 + (perspective * abs(v)) ** 2
                        + (abs(v) * wheelbase_tol / wheelbase) ** 2)
        out[pid] = (round(v, 1), round(max(tol, 1.0), 1))
    return out


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pts = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    params = dict(iter_parameters(load_spec()))
    wb = params["dimensions.wheelbase_lh"]
    if wb["value"] is None:
        sys.exit("wheelbase is UNKNOWN - cannot scale the photo")
    res = solve(pts, wb["value"], wb["tolerance"] or 0.0)
    eid = sys.argv[sys.argv.index("--apply") + 1] if "--apply" in sys.argv else None
    spec_set = None
    if eid:
        s = importlib.util.spec_from_file_location("spec_set", TOOLS / "spec_set.py")
        spec_set = importlib.util.module_from_spec(s)
        s.loader.exec_module(spec_set)
    for pid, (v, tol) in res.items():
        cur = params.get(pid)
        action = "report"
        if cur is None:
            action = "SKIP (not a spec parameter)"
        elif eid:
            better = cur["status"] == "UNKNOWN" or (cur["status"] == "ESTIMATED" and
                                                    (cur["tolerance"] or 1e9) > tol)
            if cur["status"] == "VERIFIED" or not better:
                action = f"keep existing {cur['status']} ±{cur['tolerance']}"
            else:
                spec_set.set_param(pid, {"value": v, "status": "ESTIMATED", "confidence": "LOW",
                                         "tolerance": tol, "source": [eid],
                                         "notes": f"From side photo {eid} via tools/photo_scale.py "
                                                  f"(scale from wheelbase; ±{tol} mm incl. perspective)."})
                action = "APPLIED as ESTIMATED"
        print(f"{pid:32s} {v:9.1f} ± {tol:6.1f} mm   {action}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
