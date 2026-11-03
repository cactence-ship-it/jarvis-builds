"""EXTERIOR_TRIM (EXT) - Phase 4. PLACEHOLDER bumpers, grille and mirrors."""
import build123d as bd

from .. import layout
from ..cad.shapes import box

ASSEMBLY = "EXTERIOR_TRIM"
PHASE = 4
BLACK = (0.08, 0.08, 0.09, 1.0)
CHROME = (0.78, 0.79, 0.80, 1.0)


def build(ctx):
    base = ctx.resolver()
    p = layout.profile(base)
    bz, bh = base.get("body_profile.bumper_bottom_z"), base.get("body_profile.bumper_height")
    hw, nt = p.half_width, base.get("body_profile.nose_top_z")

    def add(cid, solid, col, note=""):
        r = ctx.resolver()
        r.absorb(base)
        ctx.add(cid, ASSEMBLY, [(solid, col)], r, note)

    def bumper(x0, x1, xw0, xw1):
        """Bar plus wrap-around ends along both sides (S-series plastic bumpers, photos E-026)."""
        bar = box(x0, x1, -hw + 15, hw - 15, bz, bz + bh)
        for s in (-1, 1):
            y0, y1 = sorted((s * (hw - 20), s * (hw + 12)))
            bar = bar.fuse(box(xw0, xw1, y0, y1, bz, bz + bh))
        try:
            bar = bar.fillet(18, bar.edges().filter_by(bd.Axis.Z))
        except Exception:
            pass
        return bar.clean()
    add("EXT-001", bumper(p.x_front, p.x_nose + 20, p.x_front + 20, p.x_nose + 200), BLACK,
        "Wrap-around bumper; front face defines overall length")
    add("EXT-002", bumper(p.x_tail - 20, p.x_rear, p.x_tail - 220, p.x_rear - 20), BLACK,
        "Wrap-around bumper; rear face defines overall length")
    add("EXT-003", box(p.x_nose - 8, p.x_nose + 2, -(hw - 430), hw - 430, nt - 190, nt - 60),
        BLACK, "Grille area between headlamps")
    g = layout.greenhouse(base)
    mp = base.get("body_profile.mirror_protrusion")
    xm = g.x_belt_front + 120
    for cid, s in (("EXT-004", -1), ("EXT-005", 1)):
        y0, y1 = sorted((s * hw, s * (hw + mp)))
        add(cid, box(xm, xm + 90, y0, y1, g.z_belt - 40, g.z_belt + 80), BLACK)
    # Door handles on each door skin, near the rear edge below the beltline.
    belt, xb, xc = base.get("body_profile.belt_z"), base.get("body_profile.b_pillar_x"), base.get("body_profile.c_pillar_x")
    for cid, s, x1 in (("EXT-006", -1, xb), ("EXT-007", 1, xb), ("EXT-008", -1, xc), ("EXT-009", 1, xc)):
        y0, y1 = sorted((s * (hw - 2), s * (hw + 14)))
        add(cid, box(x1 - 190, x1 - 80, y0, y1, belt - 95, belt - 65), CHROME, "Handle position not from evidence")
    # Front wiper blades resting at the windshield base (one component, two blades).
    r = ctx.resolver()
    r.absorb(base)
    xw = g.x_belt_front - 25
    blades = [(box(xw - 12, xw, ya, yb, g.z_belt, g.z_belt + 14), BLACK)
              for ya, yb in ((-hw + 160, -60), (40, hw - 260))]
    ctx.add("EXT-015", ASSEMBLY, blades, r, "Wiper layout not from evidence")
    from ..cad.mech import cyl, pipe
    sill, rb = base.get("body_profile.sill_z"), base.get("body_profile.rear_bottom_z")
    add("EXT-010", box(p.x_tail, p.x_tail + 12, -110, 110, rb + 120, rb + 150), BLACK, "Tailgate handle bar above the plate (photos E-026); size guessed")
    r = ctx.resolver()
    r.absorb(base)
    strips = []
    for s in (-1, 1):
        y0, y1 = sorted((s * hw, s * (hw + 8)))
        strips.append((box(p.x_nose + 250, p.x_tail - 250, y0, y1, sill + 40, sill + 90), BLACK))
    ctx.add("EXT-011", ASSEMBLY, strips, r, "Lower side mouldings (photos E-026); height guessed")
    for cid, s in (("EXT-012", -1), ("EXT-013", 1)):
        r = ctx.resolver()
        r.absorb(base)
        y = s * (g.half_roof - 60)
        z = g.z_roof
        zt = r.get("dimensions.overall_height_roof_rails") - 14          # tube centre; tube top = height over rails
        feet = [(g.x_roof_front + 80, y, z), (g.x_roof_front + 80, y, zt), (g.x_roof_rear - 80, y, zt), (g.x_roof_rear - 80, y, z)]
        ctx.add(cid, ASSEMBLY, pipe(feet, 14, (0.10, 0.52, 0.50, 1.0)), r, "Body-colour roof rail (photos E-026); shape guessed")
    r = ctx.resolver()
    r.absorb(base)
    pv = (p.x_tail + 10, 0, g.z_belt + 40)
    ctx.add("EXT-016", ASSEMBLY, [(cyl(pv, (p.x_tail + 30, 260, g.z_belt + 300), 9), BLACK), (box(p.x_tail, p.x_tail + 20, -20, 20, g.z_belt + 20, g.z_belt + 60), BLACK)],
            r, "Rear wiper on the tailgate glass (photos E-026)")
    return ctx.parts
