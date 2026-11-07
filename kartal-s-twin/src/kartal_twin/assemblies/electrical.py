"""ELECTRICAL (ELE) - PLACEHOLDER electrical ARCHITECTURE: battery, fuse box, relays, ignition,
lighting and instrument branches, main looms, connectors and ground points as SCHEMATIC routes.
No pinout, wire colour, gauge or circuit data is modelled or implied (none exists as evidence).
Battery in the engine bay from photos E-027; every position is a guess."""
import build123d as bd

from .. import layout
from ..cad.mech import DARK, STEEL, WIRE, adder, block, cyl, pipe
from .engine import datums

ASSEMBLY = "ELECTRICAL"
PHASE = 9


def build(ctx):
    base = ctx.resolver()
    p = layout.profile(base)
    x0, x1, cz, hw = datums(base)
    bx0, bx1, by0, by1, bz0, bz1 = base.get("pkg_battery")
    fw, fz, hr = base.get("pkg_firewall_x"), base.get("pkg_floor_z"), base.get("pkg_harness_r")
    dx0, dx1, dz0, dz1 = base.get("pkg_dash")
    sy = base.get("pkg_steering_wheel")[1]
    add = adder(ctx, ASSEMBLY, base)
    bl, bw, bh = (base.get(k) for k in ("electrical.battery_case_length", "electrical.battery_case_width", "electrical.battery_case_height"))  # E-043
    bcx, bcy = (bx0 + bx1) / 2, (by0 + by1) / 2                       # keep the photo-based position (pkg_battery)
    bx0, bx1, by0, by1, bz1 = bcx - bw / 2, bcx + bw / 2, bcy - bl / 2, bcy + bl / 2, bz0 + bh
    add("ELE-001", block(bx0, bx1, by0, by1, bz0, bz1, (0.75, 0.76, 0.78, 1.0))
        + [(cyl((bcx, by0 + 30, bz1), (bcx, by0 + 30, bz1 + 18), 9), (0.65, 0.12, 0.10, 1.0)),
           (cyl((bcx, by1 - 30, bz1), (bcx, by1 - 30, bz1 + 18), 8), DARK)],
        f"12 V battery {bl} x {bw} x {bh} mm, İnci Formul A L2 case (E-043, ESTIMATED LOW: the label is only partly "
        "readable, 60 or 72 Ah); terminals at the case ends; position from photos E-027")
    fb = (dx0 + 60, -620, dz0 - 40)
    add("ELE-002", block(fb[0] - 60, fb[0] + 60, fb[1] - 80, fb[1] + 80, fb[2] - 30, fb[2] + 30, (0.25, 0.30, 0.55, 1.0)), "Fuse box under the LH dash (position guessed)")
    add("ELE-003", block(fw - 80, fw - 20, 300, 420, 700, 760, DARK), "Relay group at the bulkhead (guessed)")
    add("ELE-004", [(cyl((x1 - 60, -40, cz + 300), (x1 - 60, -40, cz + 380), 35), DARK),
                    (cyl((fw - 200, -520, 620), (fw - 200, -520, 720), 32), (0.25, 0.25, 0.27, 1.0))]
        + [b for i in range(4) for b in pipe([(x1 - 60, -40, cz + 380), (x0 + 60 + i * 115, -hw + 30, cz + 300)], 4, (0.1, 0.1, 0.1, 1.0))],
        "Ignition: distributor, coil and HT leads (type UNKNOWN, electrical.ignition_type)")
    head = [(p.x_nose + 60, s * (p.half_width - 120), 620) for s in (-1, 1)]
    tail = [(p.x_tail - 60, s * (p.half_width - 80), 600) for s in (-1, 1)]
    light = pipe([head[0], (-500, 0, 640), head[1]], hr * 0.6, WIRE) + pipe([(-500, 0, 640), (fw - 30, -500, 760)], hr * 0.6, WIRE)
    light += pipe([tail[0], (p.x_tail - 60, 0, 620), tail[1]], hr * 0.6, WIRE)
    add("ELE-005", light, "Lighting branches to head and tail lamps (schematic)")
    add("ELE-006", pipe([(dx1, sy, dz1 - 100), (fw + 40, sy - 100, dz0), (fw - 30, -300, 760), (x1, -hw - 20, cz + 150)], hr * 0.6, WIRE),
        "Instrument branch and engine sensors (schematic)")
    main = pipe([(bx0, by0, bz1), (-400, 400, 700), (fw - 30, 380, 760), (fw - 30, -500, 760), (fb[0], fb[1], fb[2])], hr, WIRE)
    main += pipe([(fb[0], fb[1], fb[2]), (fw + 200, -p.half_width + 90, fz + 40), (fw + 900, -500, fz + 40), (p.x_tail - 300, -500, fz + 250), tail[0]], hr, WIRE)
    add("ELE-007", main, "Main looms: engine bay, bulkhead, LH sill to the rear (routing schematic)")
    con = [(bd.Pos(*q) * bd.Box(50, 30, 30), DARK) for q in (head[0], head[1], tail[0], tail[1], (fw - 30, 380, 760), (fw - 30, -500, 760))]
    add("ELE-008", con, "Connector positions (schematic)")
    gnd = [(bd.Pos(*q) * bd.Sphere(14), STEEL) for q in ((bx0 - 20, by0 + 40, bz0), (x1, hw + 20, cz), (fw - 10, 0, 800), (p.x_tail - 120, 0, 600))]
    add("ELE-009", gnd, "Ground (earth) points (schematic)")
    return ctx.parts
