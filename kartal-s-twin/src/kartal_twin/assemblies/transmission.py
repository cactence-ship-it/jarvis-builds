"""TRANSMISSION (TRN) - PLACEHOLDER manual gearbox behind the longitudinal engine.

Manual gearbox (floor lever, three pedals: E-024); gear count UNKNOWN; sizes are package guesses.
"""
from ..cad.mech import ALU, DARK, STEEL, adder, block, cyl, disc
from .engine import datums

ASSEMBLY = "TRANSMISSION"
PHASE = 6


def output_point(r):
    x0, x1, cz, _ = datums(r)
    return (x1 + r.get("pkg_gearbox_len"), 0.0, cz)


def build(ctx):
    base = ctx.resolver()
    x0, x1, cz, hw = datums(base)
    xo = output_point(base)[0]
    lever = base.get("pkg_gear_lever_x")
    add = adder(ctx, ASSEMBLY, base)
    xb = x1 + 170                                              # bellhousing end
    add("TRN-001", [(cyl((x1, 0, cz), (xb, 0, cz), 175), ALU), (cyl((xb, 0, cz), (xo - 60, 0, cz), 110), ALU),
                    (cyl((xo - 60, 0, cz), (xo, 0, cz), 60), ALU)],
        "Bellhousing and gearbox case envelope; 5-speed size assumed, gear count UNKNOWN")
    add("TRN-002", [(disc((x1 + 40, 0, cz), (1, 0, 0), 105, 20), DARK)]
        + [(cyl((x1 + 90, -175, cz + 60), (x1 + 90, -260, cz + 140), 10), STEEL)],
        "Clutch disc inside the bellhousing and release arm; actuation type UNKNOWN")
    add("TRN-003", [(cyl((xo - 200, 0, cz + 110), (lever, 0, cz + 110), 10), STEEL)]
        + block(xo - 230, xo - 170, -30, 30, cz + 80, cz + 140, DARK),
        "Gearshift rod from the gearbox to the floor lever (layout guessed)")
    return ctx.parts
