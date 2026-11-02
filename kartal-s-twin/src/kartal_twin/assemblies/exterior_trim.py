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
    return ctx.parts
