"""EXHAUST (EXH) - PLACEHOLDER exhaust run from the manifold to the rear outlet. The rear silencer
beside the spare-wheel well is from photos E-025; route, sizes and outlet side are guesses."""
from .. import layout
from ..cad.mech import RUST, STEEL, adder, cyl, pipe
from .engine import datums

ASSEMBLY = "EXHAUST"
PHASE = 7


def build(ctx):
    base = ctx.resolver()
    p = layout.profile(base)
    x0, x1, cz, hw = datums(base)
    ey, fz = base.get("pkg_exhaust_y"), base.get("pkg_floor_z")
    sx0, sx1, sy, sz, sr = base.get("pkg_rear_silencer")
    xa, za = layout.wheel_centres(base)["RL"][0], layout.wheel_centres(base)["RL"][2]
    add = adder(ctx, ASSEMBLY, base)
    m = ((x0 + x1) / 2, hw + 40, cz + 80)
    a = (x1 + 150, ey, fz - 30)
    add("EXH-001", pipe([m, (m[0] + 60, hw + 60, cz - 120), a], 24, RUST), "Front pipe (route guessed)")
    c0, c1 = (xa - 1100, ey, fz - 40), (xa - 650, ey, fz - 40)
    add("EXH-002", [(cyl(c0, c1, 60), STEEL), (cyl((sx0, sy, sz), (sx1, sy, sz), sr), STEEL)],
        "Centre silencer (presence guessed) and rear silencer beside the spare-wheel well (photos E-025)")
    route = [a, c0]
    add("EXH-003", pipe(route, 24, RUST) + pipe([c1, (xa - 250, ey, fz - 20), (xa, ey + 120, za + 120), (sx0, sy, sz)], 24, RUST)
        + [(cyl((x, ey, fz - 30), (x, ey, fz + 10), 8), STEEL) for x in (x1 + 600, xa - 300)],
        "Pipes over the axle and rubber-hanger posts (schematic)")
    add("EXH-004", [(cyl((sx1, sy, sz), (p.x_rear - 20, sy, sz - 20), 22), RUST)], "Tailpipe to the rear (outlet side guessed)")
    return ctx.parts
