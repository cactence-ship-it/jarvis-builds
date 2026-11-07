"""BRAKING (BRK) - PLACEHOLDER brake envelopes and hydraulic layout. Front discs (E-032/E-037) and rear
drums (E-025/E-042) sized from parts listings and the Fiat 131 catalogue (ESTIMATED LOW). Master cylinder and booster
at the LH bulkhead (LHD, E-024); lines and cables are schematic routes, not measured."""
from .. import layout
from ..cad.mech import ALU, DARK, STEEL, adder, cyl, disc, pipe, ring

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
    dd, dt = base.get("brakes.front_disc_diameter"), base.get("brakes.front_disc_thickness")      # E-037
    rd, rw = base.get("brakes.rear_drum_diameter"), base.get("brakes.rear_drum_width")            # E-042
    for cid, key in (("BRK-004", "FL"), ("BRK-005", "FR")):
        x, y, z = w[key]
        s = 1 if y > 0 else -1
        yc = y - s * 60
        add(cid, [(disc((x, yc, z), (0, 1, 0), dd / 2, dt), STEEL),
                  (disc((x, yc + s * 12, z), (0, 1, 0), 70, 18), DARK),                         # hat
                  (cyl((x + 55, yc - 22, z + 75), (x + 55, yc + 22, z + 75), 38), DARK)],          # caliper
            f"Front disc {dd} mm x {dt} mm (aftermarket listings E-037, ESTIMATED LOW) with a single-piston "
            "sliding caliper behind the axle line (caliper size and position guessed)")
    for cid, key in (("BRK-006", "RL"), ("BRK-007", "RR")):
        x, y, z = w[key]
        s = 1 if y > 0 else -1
        yc = y - s * 70
        add(cid, [(ring((x, yc, z), (0, 1, 0), rd / 2 + 10, rd / 2, rw), DARK),
                  (disc((x, yc + s * (rw / 2 + 3), z), (0, 1, 0), rd / 2 + 10, 6), DARK),             # drum face
                  (disc((x, yc - s * (rw / 2 + 3), z), (0, 1, 0), rd / 2 + 4, 6), STEEL)],             # back plate
            f"Rear drum {rd} mm x {rw} mm (Fiat 131 catalogue E-042, ESTIMATED LOW); wall thickness and back plate guessed")
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
