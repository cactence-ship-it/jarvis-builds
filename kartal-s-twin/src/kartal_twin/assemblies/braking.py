"""BRAKING (BRK) - PLACEHOLDER brake envelopes and hydraulic layout. Front brake TYPE is UNKNOWN
(neutral envelope); rear drums are ESTIMATED from one photo (E-025). Master cylinder and booster
at the LH bulkhead (LHD, E-024); lines and cables are schematic routes, not measured."""
from .. import layout
from ..cad.mech import ALU, DARK, STEEL, adder, cyl, disc, pipe

ASSEMBLY = "BRAKING"
PHASE = 8


def build(ctx):
    base = ctx.resolver()
    w = layout.wheel_centres(base)
    br, fw, fz = base.get("pkg_brake_r"), base.get("pkg_firewall_x"), base.get("pkg_floor_z")
    hb = base.get("pkg_handbrake_x")
    add = adder(ctx, ASSEMBLY, base)
    mx, my, mz = fw - 120, -380, 700
    add("BRK-001", [(cyl((mx - 140, my, mz), (mx, my, mz), 30), ALU), (cyl((mx - 90, my, mz + 30), (mx - 90, my, mz + 80), 35), (0.8, 0.8, 0.7, 1.0))],
        "Master cylinder with reservoir at the LH bulkhead (position guessed)")
    add("BRK-002", [(disc((mx + 60, my, mz), (1, 0, 0), 110, 110), DARK)], "Brake booster (servo) envelope; fitment UNKNOWN (brakes.brake_booster_fitted)")
    for cid, key, note in (("BRK-004", "FL", "Front brake ENVELOPE: disc or drum is UNKNOWN (brakes.front_brake_type)"),
                           ("BRK-005", "FR", "Front brake ENVELOPE: disc or drum is UNKNOWN (brakes.front_brake_type)"),
                           ("BRK-006", "RL", "Rear drum brake (ESTIMATED from photo E-025); size guessed"),
                           ("BRK-007", "RR", "Rear drum brake (ESTIMATED from photo E-025); size guessed")):
        x, y, z = w[key]
        s = 1 if y > 0 else -1
        add(cid, [(disc((x, y - s * 45, z), (0, 1, 0), br, 45 if key[0] == "R" else 22), DARK if key[0] == "R" else STEEL)], note)
    lines = []
    for key in ("FL", "FR", "RL", "RR"):
        x, y, z = w[key]
        s = 1 if y > 0 else -1
        route = [(mx - 140, my, mz - 40), (fw - 60, my, fz + 140)]
        route += [(x + 60, y - s * 160, z + 60)] if key[0] == "F" else [(x - 400, -60, fz + 30), (x - 30, 0, z + 60), (x, y - s * 120, z + 40)]
        lines += pipe(route, 4, STEEL)
    add("BRK-003", lines, "Brake-line routes (schematic)")
    cables = []
    for key in ("RL", "RR"):
        x, y, z = w[key]
        s = 1 if y > 0 else -1
        cables += pipe([(hb, 0, fz + 20), (x - 300, s * 300, fz + 10), (x - 40, y - s * 110, z - 30)], 4, DARK)
    add("BRK-008", cables, "Parking-brake cables from the lever to the rear brakes (schematic)")
    return ctx.parts
