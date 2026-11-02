"""WHEELS_AND_TIRES (WHL) - Phase 4. Road wheels from the (ESTIMATED) tire size."""
import build123d as bd

from .. import layout

ASSEMBLY = "WHEELS_AND_TIRES"
PHASE = 4
RUBBER = (0.06, 0.06, 0.07, 1.0)
STEEL = (0.62, 0.64, 0.66, 1.0)
IDS = {"FL": "WHL-001", "FR": "WHL-002", "RL": "WHL-003", "RR": "WHL-004"}


def wheel(t: layout.Tire):
    w, ro, ri = t.section_width, t.outer_diameter / 2, t.rim_radius
    tyre = bd.Cylinder(ro, w)
    try:
        tyre = tyre.fillet(w * 0.3, tyre.edges())
    except Exception:
        pass
    tyre = tyre.cut(bd.Cylinder(ri, w + 2))
    rim = bd.Cylinder(ri, w - 30).cut(bd.Pos(0, 0, w / 2 - 15) * bd.Cylinder(ri - 35, 60))
    return tyre, rim


def build(ctx):
    base = ctx.resolver()
    centres = layout.wheel_centres(base)
    for key, cid in IDS.items():
        r = ctx.resolver()
        r.absorb(base)
        t = layout.tire(r, "front" if key[0] == "F" else "rear")
        tyre, rim = wheel(t)
        x, y, z = centres[key]
        # Cylinder axis is Z; turn it to the lateral Y axis, outer (recessed) face outward.
        rot = bd.Rot(-90, 0, 0) if y > 0 else bd.Rot(90, 0, 0)
        place = bd.Pos(x, y, z) * rot
        ctx.add(cid, ASSEMBLY, [(place * tyre, RUBBER), (place * rim, STEEL)], r)
    return ctx.parts
