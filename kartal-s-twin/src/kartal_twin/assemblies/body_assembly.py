"""BODY_ASSEMBLY (BDY) - Phase 4.

Current content (all PLACEHOLDER): BDY-001 body shell envelope (lower body extruded
from a side profile, lofted greenhouse, wheel-arch cut-outs) with the closures cut out
of it as separate components: hood BDY-003, doors BDY-008..011, tailgate BDY-012, each
separated by a panel gap. Fenders, quarters and roof remain part of BDY-001 for now.
"""
import build123d as bd

from .. import layout
from ..cad.shapes import box, one

GAP = 3.0                      # panel gap, mm (visual)
SKIN = 45.0                    # depth of a closure cut into the envelope, mm

ASSEMBLY = "BODY_ASSEMBLY"
PHASE = 4


def body_shell(r) -> bd.Shape:
    p, g = layout.profile(r), layout.greenhouse(r)
    sill, nb, nt = r.get("body_profile.sill_z"), r.get("body_profile.nose_bottom_z"), r.get("body_profile.nose_top_z")
    belt, rb, cowl = r.get("body_profile.belt_z"), r.get("body_profile.rear_bottom_z"), r.get("body_profile.cowl_x")
    side = [(p.x_nose, nb), (p.x_nose, nt), (cowl, belt), (p.x_tail, belt), (p.x_tail, rb),
            (p.x_tail - 150, sill), (p.x_nose + 150, sill)]
    # Sketch in the XZ plane (VCS X, Z), extrude symmetrically across the body width.
    wire = bd.Wire.make_polygon([bd.Vector(x, 0, z) for x, z in side], close=True)
    lower = bd.Solid.extrude(bd.Face(wire), bd.Vector(0, 2 * p.half_width, 0))
    lower = bd.Pos(0, -p.half_width, 0) * lower
    try:
        vertical = lower.edges().filter_by(bd.Axis.Y)
        lower = lower.fillet(40, vertical)
    except Exception:  # fillet is cosmetic; keep the sharp envelope if OCC refuses
        pass
    bottom = bd.Pos((g.x_belt_front + g.x_belt_rear) / 2, 0, g.z_belt) * bd.Rectangle(
        g.x_belt_rear - g.x_belt_front, 2 * g.half_belt)
    top = bd.Pos((g.x_roof_front + g.x_roof_rear) / 2, 0, g.z_roof) * bd.Rectangle(
        g.x_roof_rear - g.x_roof_front, 2 * g.half_roof)
    cabin = bd.loft([bottom.face(), top.face()])
    shell = lower.fuse(cabin).clean()
    arch_r = layout.tire(r).outer_diameter / 2 + r.get("arch_clearance")
    depth = r.get("arch_depth")
    for x, y, z in layout.wheel_centres(r).values():
        side_sign = 1 if y > 0 else -1
        cyl = bd.Cylinder(arch_r, depth, rotation=(90, 0, 0))
        cut = bd.Pos(x, side_sign * (p.half_width - depth / 2 + 1), z) * cyl
        shell = one(shell.cut(cut))
    return shell


def _prism_xz(pts, y0, y1) -> bd.Solid:
    wire = bd.Wire.make_polygon([bd.Vector(x, y0, z) for x, z in pts], close=True)
    return bd.Solid.extrude(bd.Face(wire), bd.Vector(0, y1 - y0, 0))


def closure_regions(r) -> dict:
    """Region solids for each closure: (cut region, panel region shrunk by GAP)."""
    p = layout.profile(r)
    hw, sill, belt = p.half_width, r.get("body_profile.sill_z"), r.get("body_profile.belt_z")
    nt, cowl = r.get("body_profile.nose_top_z"), r.get("body_profile.cowl_x")
    xb, xc, rb = r.get("body_profile.b_pillar_x"), r.get("body_profile.c_pillar_x"), r.get("body_profile.rear_bottom_z")
    out = {}
    doors = {"BDY-008": (-1, cowl - 30, xb - 2), "BDY-009": (1, cowl - 30, xb - 2),
             "BDY-010": (-1, xb + 2, xc - 4), "BDY-011": (1, xb + 2, xc - 4)}
    for cid, (side, x0, x1) in doors.items():
        def door(g, side=side, x0=x0, x1=x1):
            ya, yb = sorted((side * (hw - SKIN), side * (hw + 5)))
            return box(x0 + g, x1 - g, ya, yb, sill + 30 + g, belt - 8 - g)
        out[cid] = (door(0), door(GAP))

    def ztop(x):
        return nt + (belt - nt) * (x - p.x_nose) / (cowl - p.x_nose)

    def hood(g):
        xa, xb_ = p.x_nose + 12 + g, cowl - 20 - g
        pts = [(xa, ztop(xa) + 5), (xb_, ztop(xb_) + 5), (xb_, ztop(xb_) - 35), (xa, ztop(xa) - 35)]
        return _prism_xz(pts, -(hw - 65 - g), hw - 65 - g)
    out["BDY-003"] = (hood(0), hood(GAP))

    def tailgate(g):
        return box(p.x_tail - SKIN, p.x_tail + 5, -(hw - 70) + g, hw - 70 - g, rb + 30 + g, belt - 10 - g)
    out["BDY-012"] = (tailgate(0), tailgate(GAP))
    return out


def build(ctx):
    r = ctx.resolver()
    paint = tuple(r.get("paint_rgba"))
    envelope = body_shell(r)
    shell = envelope
    regions = closure_regions(r)
    for cid, (cut, panel_region) in regions.items():
        shell = one(shell.cut(cut))
        pr = ctx.resolver()
        pr.absorb(r)
        ctx.add(cid, ASSEMBLY, [(one(envelope.intersect(panel_region)), paint)], pr,
                "Cut from the placeholder envelope; outline not from evidence")
    ctx.add("BDY-001", ASSEMBLY, [(shell, paint)], r,
            "Envelope minus closures; fenders, quarters and roof not yet separated")
    return ctx.parts
