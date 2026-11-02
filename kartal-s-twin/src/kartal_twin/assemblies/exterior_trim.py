"""EXTERIOR_TRIM (EXT) - Phase 4. PLACEHOLDER bumpers, grille and mirrors."""
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

    add("EXT-001", box(p.x_front, p.x_nose + 20, -hw + 15, hw - 15, bz, bz + bh), BLACK,
        "Bumper bar; front face defines overall length")
    add("EXT-002", box(p.x_tail - 20, p.x_rear, -hw + 15, hw - 15, bz, bz + bh), BLACK,
        "Bumper bar; rear face defines overall length")
    add("EXT-003", box(p.x_nose - 8, p.x_nose + 2, -(hw - 430), hw - 430, nt - 190, nt - 60),
        BLACK, "Grille area between headlamps")
    g = layout.greenhouse(base)
    mp = base.get("body_profile.mirror_protrusion")
    xm = g.x_belt_front + 120
    for cid, s in (("EXT-004", -1), ("EXT-005", 1)):
        y0, y1 = sorted((s * hw, s * (hw + mp)))
        add(cid, box(xm, xm + 90, y0, y1, g.z_belt - 40, g.z_belt + 80), BLACK)
    return ctx.parts
