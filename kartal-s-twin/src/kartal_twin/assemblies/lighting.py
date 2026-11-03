"""LIGHTING (LGT) - Phase 4. PLACEHOLDER lamp lenses on the front and rear faces.

Lamp shapes and positions are NOT known for VEH-01; simple rectangles mark where the
lamp groups are expected, to be replaced from the owner photos (Phase 2/4).
"""
from .. import layout
from ..cad.shapes import box

ASSEMBLY = "LIGHTING"
PHASE = 4
WHITE = (0.92, 0.93, 0.95, 1.0)
AMBER = (0.98, 0.62, 0.10, 1.0)
RED = (0.75, 0.05, 0.05, 1.0)


def build(ctx):
    base = ctx.resolver()
    p = layout.profile(base)
    nt, hw = base.get("body_profile.nose_top_z"), p.half_width
    belt = base.get("body_profile.belt_z")
    d = 10.0                                       # lens stands proud of the face
    lamps = [  # cid, x-face, sign of x outward, y range (RH; mirrored for LH), z range, colour
        ("LGT-001", p.x_nose, -1, -1, (hw - 420, hw - 160), (nt - 190, nt - 60), WHITE),
        ("LGT-002", p.x_nose, -1, 1, (hw - 420, hw - 160), (nt - 190, nt - 60), WHITE),
        ("LGT-003", p.x_nose, -1, -1, (hw - 150, hw - 50), (nt - 190, nt - 60), AMBER),
        ("LGT-004", p.x_nose, -1, 1, (hw - 150, hw - 50), (nt - 190, nt - 60), AMBER),
        ("LGT-007", p.x_tail, 1, -1, (hw - 230, hw - 40), (belt - 380, belt - 60), RED),
        ("LGT-008", p.x_tail, 1, 1, (hw - 230, hw - 40), (belt - 380, belt - 60), RED),
    ]
    for cid, xf, sx, side, (ya, yb), (za, zb), col in lamps:
        r = ctx.resolver()
        r.absorb(base)
        x0, x1 = sorted((xf - sx * 2, xf + sx * d))
        y0, y1 = sorted((side * ya, side * yb))
        ctx.add(cid, ASSEMBLY, [(box(x0, x1, y0, y1, za, zb), col)], r,
                "Position/shape not from evidence")
    g = layout.greenhouse(base)
    rb = base.get("body_profile.rear_bottom_z")
    extra = [("LGT-005", [(box(320, 380, -hw - 4, -hw + 1, nt - 140, nt - 110), AMBER)], "Side repeater (position guessed)"),
             ("LGT-006", [(box(320, 380, hw - 1, hw + 4, nt - 140, nt - 110), AMBER)], "Side repeater (position guessed)"),
             ("LGT-009", [(box(p.x_tail + 2, p.x_tail + 14, -60, 60, rb + 95, rb + 115), WHITE)], "Licence-plate lamp in the handle bar (guessed)"),
             ("LGT-010", [(box(g.x_roof_front + 40, g.x_roof_front + 240, -110, 110, g.z_roof - 90, g.z_roof - 50), (0.15, 0.15, 0.16, 1.0)),
                          (box(g.x_roof_front + 80, g.x_roof_front + 200, -80, 80, g.z_roof - 94, g.z_roof - 90), WHITE)],
              "Overhead console with lamp (photos E-024)")]
    for cid, bodies, note in extra:
        r = ctx.resolver()
        r.absorb(base)
        ctx.add(cid, ASSEMBLY, bodies, r, note)
    return ctx.parts
