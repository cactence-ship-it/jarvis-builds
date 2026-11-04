"""GLAZING (GLZ) - Phase 4. PLACEHOLDER glass panels on the lofted greenhouse."""
from .. import layout
from ..cad.shapes import thick_quad

ASSEMBLY = "GLAZING"
PHASE = 4
GLASS = (0.16, 0.22, 0.28, 0.6)
T = 5.0


def build(ctx):
    base = ctx.resolver()
    g = layout.greenhouse(base)
    m = base.get("pillar_width")
    xb, xc = base.get("body_profile.b_pillar_x"), base.get("body_profile.c_pillar_x")
    gf, gr = (g.x_belt_front, g.x_roof_front), (g.x_belt_rear, g.x_roof_rear)

    def add(cid, quad, outward):
        r = ctx.resolver()
        r.absorb(base)
        ctx.add(cid, ASSEMBLY, [(thick_quad(quad, T, outward, inset=m), GLASS)], r)

    zb, zt = g.z_belt, g.z_roof
    add("GLZ-001", [(gf[0], -g.half_belt, zb), (gf[0], g.half_belt, zb),
                    (gf[1], g.half_roof, zt), (gf[1], -g.half_roof, zt)], (-1, 0, 0.3))
    add("GLZ-002", [(gr[0], -g.half_belt, zb), (gr[0], g.half_belt, zb),
                    (gr[1], g.half_roof, zt), (gr[1], -g.half_roof, zt)], (1, 0, 0.3))
    windows = {  # (front edge bottom/top x, rear edge bottom/top x)
        "front": (gf, (xb, xb)),
        "rear": ((xb, xb), (xc, xc)),
        "quarter": ((xc, xc), gr),
    }
    ids = {("front", -1): "GLZ-003", ("front", 1): "GLZ-004", ("rear", -1): "GLZ-005",
           ("rear", 1): "GLZ-006", ("quarter", -1): "GLZ-007", ("quarter", 1): "GLZ-008"}
    for (name, side), cid in ids.items():
        (fb, ft), (rb_, rt) = windows[name]
        quad = [g.side_point(fb, ft, 0, side), g.side_point(rb_, rt, 0, side),
                g.side_point(rb_, rt, 1, side), g.side_point(fb, ft, 1, side)]
        add(cid, quad, (0, side, 0))
    return ctx.parts
