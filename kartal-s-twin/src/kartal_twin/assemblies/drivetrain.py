"""DRIVETRAIN (DRV) - PLACEHOLDER propeller shaft, differential and rigid rear axle.

Rear-wheel drive with a rigid (live) rear axle (photos E-025); sizes are package guesses.
"""
from .. import layout
from ..cad.mech import DARK, STEEL, adder, cyl
from .transmission import output_point

ASSEMBLY = "DRIVETRAIN"
PHASE = 6


def build(ctx):
    base = ctx.resolver()
    w = layout.wheel_centres(base)
    xo, _, zo = output_point(base)
    dr, tr = base.get("pkg_diff_r"), base.get("pkg_axle_tube_r")
    xa = (w["RL"][0] + w["RR"][0]) / 2
    za = w["RL"][2]
    add = adder(ctx, ASSEMBLY, base)
    xn = xa - dr - 60
    add("DRV-001", [(cyl((xo, 0, zo), (xn, 0, za), 32), STEEL),
                    (cyl((xo - 10, 0, zo), (xo + 50, 0, zo), 45), DARK), (cyl((xn - 50, 0, za), (xn + 10, 0, za), 45), DARK)],
        "Propeller shaft with joints; one-piece shown, construction UNKNOWN")
    add("DRV-002", [(cyl((xa, -dr * 0.6, za), (xa, dr * 0.6, za), dr), DARK), (cyl((xa - dr - 70, 0, za), (xa, 0, za), 60), DARK)],
        "Differential housing envelope")
    yi = w["RL"][1] + 130
    add("DRV-003", [(cyl((xa, yi, za), (xa, -yi, za), tr), STEEL)],
        "Rigid rear axle tube with half-shafts (photos E-025)")
    return ctx.parts
