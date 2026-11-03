"""WHEELS_AND_TIRES (WHL) - Phase 4. Road wheels from the (ESTIMATED) tire size.

CAD: WHL-001..004 tire design envelopes, WHL-006..009 pressed-steel rims (simplified section).
"""
import build123d as bd

from .. import layout

ASSEMBLY = "WHEELS_AND_TIRES"
PHASE = 4
RUBBER = (0.06, 0.06, 0.07, 1.0)
STEEL = (0.62, 0.64, 0.66, 1.0)
BLACK_STEEL = (0.08, 0.08, 0.09, 1.0)        # owner: black pressed-steel wheels (E-017)
IDS = {"FL": "WHL-001", "FR": "WHL-002", "RL": "WHL-003", "RR": "WHL-004"}
RIM_IDS = {"FL": "WHL-006", "FR": "WHL-007", "RL": "WHL-008", "RR": "WHL-009"}


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
        ctx.add(cid, ASSEMBLY, [(place * tyre, RUBBER)], r, "Tire (smooth envelope: tread pattern not modelled)")
        rr = ctx.resolver()
        rr.absorb(base)
        m = layout.rim(rr)
        s = 1 if y > 0 else -1
        valve = bd.Pos(x, y + s * 20, z + m.bead_seat_radius - 25) * bd.Rot(90, 0, 0) * bd.Cylinder(5, 40)
        ctx.add(RIM_IDS[key], ASSEMBLY, [(bd.Pos(x, y, z) * bd.Rot(90, 0, 0) * rim_solid(m), BLACK_STEEL), (valve, (0.1, 0.1, 0.1, 1.0))], rr,
                "Pressed-steel rim (simplified section) with valve stem (valve angle guessed)")
    r = ctx.resolver()
    r.absorb(base)
    t = layout.tire(r, "rear")
    m = layout.rim(r)
    sx, sy = r.get("pkg_spare_wheel")
    zc = r.get("pkg_cargo_floor_z") + t.outer_diameter / 2
    tyre, _ = wheel(t)
    ctx.add("WHL-005", ASSEMBLY, [(bd.Pos(sx, sy, zc) * bd.Rot(90, 0, 0) * tyre, RUBBER),
                                  (bd.Pos(sx, sy, zc) * bd.Rot(90, 0, 0) * rim_solid(m), BLACK_STEEL)], r,
            "Spare wheel standing loose in the luggage compartment (photos E-022); position guessed")
    return ctx.parts


# ----------------------------------------------------------------------------- CAD (D-016)
def tire_envelope(t: layout.Tire) -> bd.Solid:
    """Design envelope from the size designation only: annulus of outer diameter OD,
    bead-seat diameter (rim diameter) and nominal section width. Shoulder radius, tread,
    sidewall bulge and the rim are NOT modelled (no evidence)."""
    w, ro, ri = t.section_width, t.outer_diameter / 2, t.rim_radius
    return bd.Cylinder(ro, w).cut(bd.Cylinder(ri, w + 2)).solid()


def rim_solid(m: layout.Rim) -> bd.Solid:
    """Revolved simplified steel wheel, axis = Z, centred on the rim centre plane:
    barrel (bead-seat radius, inward by the steel thickness) between the flanges, two J flanges
    of the given height, and a flat disc on the centre plane. NOT modelled (no evidence): drop
    centre well, bead humps, vent holes, PCD / bolt holes, centre bore, offset ET (the disc is
    placed on the centre plane, which is not a claim that ET = 0)."""
    rb, t, w = m.bead_seat_radius, m.steel, m.width_between_flanges
    barrel = bd.Cylinder(rb, w + 2 * t) - bd.Cylinder(rb - t, w + 2 * t + 2)
    flange = bd.Cylinder(m.outer_radius, t) - bd.Cylinder(rb - t, t + 2)
    disc = bd.Cylinder(rb - t / 2, m.disc)                     # overlaps the barrel by t/2: one solid
    body = barrel + bd.Pos(0, 0, (w + t) / 2) * flange + bd.Pos(0, 0, -(w + t) / 2) * flange + disc
    return body.clean().solid()


def cad_wheel_centres(r) -> dict[str, tuple[float, float, float]]:
    """Unloaded design position: wheel centre at the free radius above the ground plane
    (no static deflection - that value has no evidence)."""
    out = {}
    for key, (x, y) in layout.axle_positions(r).items():
        t = layout.tire(r, "front" if key[0] == "F" else "rear")
        out[key] = (x, y, t.outer_diameter / 2)
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
        rr = ctx.resolver()
        rr.absorb(base)
        m = layout.rim(rr)
        ctx.add(RIM_IDS[key], ASSEMBLY, [(bd.Pos(x, y, z) * bd.Rot(90, 0, 0) * rim_solid(m), BLACK_STEEL)], rr,
                f"Pressed-steel rim {m.width_in:g}J x {m.diameter_in:g} (simplified section): flange tip "
                f"diameter {2*m.outer_radius:.1f} mm, overall width {m.overall_width:.1f} mm; well, vent "
                "holes, PCD, centre bore and offset ET not modelled")
    return ctx.parts
