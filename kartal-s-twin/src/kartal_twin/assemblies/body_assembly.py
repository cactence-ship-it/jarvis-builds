"""BODY_ASSEMBLY (BDY) - Phase 4.

Current content: BDY-001 body shell as a single PLACEHOLDER envelope (lower body
extruded from a side profile, lofted greenhouse, wheel-arch cut-outs). Individual
panels (doors, hood, fenders...) are not split out yet.
"""
import build123d as bd

from .. import layout

ASSEMBLY = "BODY_ASSEMBLY"
PHASE = 4


def body_shell(r) -> bd.Shape:
    p, g = layout.profile(r), layout.greenhouse(r)
    sill, nb, nt = r.get("sill_z"), r.get("nose_bottom_z"), r.get("nose_top_z")
    belt, rb, cowl = r.get("belt_z"), r.get("rear_bottom_z"), r.get("cowl_x")
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
        shell = shell.cut(cut)
    return shell


def build(ctx):
    r = ctx.resolver()
    paint = tuple(r.get("paint_rgba"))
    ctx.add("BDY-001", ASSEMBLY, [(body_shell(r), paint)], r,
            "Single envelope solid; panels not yet separated")
    return ctx.parts
