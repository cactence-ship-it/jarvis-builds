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
    hub = bd.Pos(0, 0, w / 2 - 40) * bd.Cylinder(ri * 0.38, 30)       # hub cap (placeholder)
    return tyre, rim.fuse(hub).clean()


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


# ----------------------------------------------------------------------------- CAD (D-016)
def tire_envelope(t: layout.Tire) -> bd.Solid:
    """Design envelope from the size designation only: annulus of outer diameter OD,
    bead-seat diameter (rim diameter) and nominal section width. Shoulder radius, tread,
    sidewall bulge and the rim are NOT modelled (no evidence)."""
    w, ro, ri = t.section_width, t.outer_diameter / 2, t.rim_radius
    return bd.Cylinder(ro, w).cut(bd.Cylinder(ri, w + 2)).solid()


def cad_wheel_centres(r) -> dict[str, tuple[float, float, float]]:
    """Unloaded design position: wheel centre at the free radius above the ground plane
    (no static deflection - that value has no evidence)."""
    wb = (r.get("dimensions.wheelbase_lh") + r.get("dimensions.wheelbase_rh")) / 2
    out = {}
    for axle, x, track in (("F", 0.0, r.get("dimensions.front_track")),
                           ("R", wb, r.get("dimensions.rear_track"))):
        t = layout.tire(r, "front" if axle == "F" else "rear")
        out[axle + "L"] = (x, -track / 2, t.outer_diameter / 2)
        out[axle + "R"] = (x, track / 2, t.outer_diameter / 2)
    return out


def build_cad(ctx):
    base = ctx.resolver()
    centres = cad_wheel_centres(base)
    for key, cid in IDS.items():
        r = ctx.resolver()
        r.absorb(base)
        t = layout.tire(r, "front" if key[0] == "F" else "rear")
        x, y, z = centres[key]
        solid = bd.Pos(x, y, z) * bd.Rot(90, 0, 0) * tire_envelope(t)
        ctx.add(cid, ASSEMBLY, [(solid, RUBBER)], r,
                f"Tire design envelope {t.section_width:.0f}/{t.aspect*100:.0f} R{t.rim_diameter_in:.0f}: "
                f"OD {t.outer_diameter:.1f} mm, bead seat {2*t.rim_radius:.1f} mm; rim, shoulders and "
                "static deflection not modelled; unloaded position")
    return ctx.parts
