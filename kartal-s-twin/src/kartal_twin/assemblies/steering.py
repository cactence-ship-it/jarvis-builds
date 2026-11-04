"""STEERING (STR) - PLACEHOLDER steering-gear envelope, linkage and tie rods for an LHD car with
hydraulic power assistance (photos E-024, E-027). Gear TYPE (rack or recirculating ball) is UNKNOWN,
so the gear is a neutral envelope; points are guesses. Column = INT-004, wheel = INT-003."""
from ..cad.mech import ALU, DARK, STEEL, adder, block, cyl, pipe
from .front_suspension import points

ASSEMBLY = "STEERING"
PHASE = 8


def build(ctx):
    base = ctx.resolver()
    L, R = points(base, -1), points(base, 1)
    sw = base.get("pkg_steering_wheel")
    fw = base.get("pkg_firewall_x")
    add = adder(ctx, ASSEMBLY, base)
    gx, gz = L["wheel"][0] + 140, L["wheel"][2] + 40
    add("STR-001", block(gx - 60, gx + 60, -300, 300, gz - 45, gz + 45, ALU),
        "Steering gear ENVELOPE: rack or recirculating ball is UNKNOWN (steering.steering_gear_type); power assisted (E-027)")
    add("STR-002", pipe([(gx, -260, gz + 45), (fw - 150, sw[1], gz + 200), (fw - 20, sw[1], sw[2] - 260)], 14, STEEL),
        "Intermediate shaft from the gear to the column (layout guessed)")
    for cid, P, s in (("STR-003", L, -1), ("STR-004", R, 1)):
        kx, ky, kz = P["knuckle"]
        add(cid, [(cyl((gx, s * 290, gz), (kx + 110, ky - s * 10, gz), 12), STEEL)], "Tie rod (geometry guessed)")
    add("STR-005", block(gx - 30, gx + 30, -330, -290, gz - 70, gz + 70, DARK) + block(gx - 30, gx + 30, 290, 330, gz - 70, gz + 70, DARK),
        "Gear mounting points (guessed)")
    return ctx.parts
