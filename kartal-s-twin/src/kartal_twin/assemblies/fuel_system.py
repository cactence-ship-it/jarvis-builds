"""FUEL_SYSTEM (FUL) - petrol system FUL-001..004 (no geometry yet) and the separate LPG
system FUL-005..014 (D-026). Only the LPG tank FUL-005 has geometry so far.

* CAD: toroidal tank shell in its OWN local frame (axis = Z through the tank centre, underside
  at Z = 0), built from ESTIMATED parameters -> DRAFT. Its position in the vehicle is UNKNOWN
  (lpg_system.tank_centre_x/y, tank_base_z), so it is exported alone and kept out of the vehicle
  assembly and clearance checks (placed = False). Mounting, multivalve, filler and lines are
  NOT modelled.
* Visual: the same outer shape at a placeholder position in the luggage compartment.
This is a digital-twin preparation model, not an installation drawing for LPG equipment.
"""
import build123d as bd

from .. import layout

ASSEMBLY = "FUEL_SYSTEM"
PHASE = 7
TANK_ID = "FUL-005"
TANK_COLOUR = (0.78, 0.80, 0.82, 1.0)


def _ring(D: float, d: float, h: float, z0: float = 0.0) -> bd.Solid:
    """Stadium-section ring: radial width (D-d)/2 >= h, revolved about Z, underside at z0."""
    w, rc = (D - d) / 2, (D + d) / 4
    sec = bd.Plane.XZ * bd.Pos(rc, z0 + h / 2) * (bd.SlotOverall(w, h) if w > h + 1e-9 else bd.Circle(h / 2))
    return bd.revolve(sec, bd.Axis.Z).solid()


def tank_outer(t: layout.ToroidalTank) -> bd.Solid:
    return _ring(t.outer_diameter, t.opening_diameter, t.height)


def tank_inner(t: layout.ToroidalTank) -> bd.Solid:
    w = t.wall
    return _ring(t.outer_diameter - 2 * w, t.opening_diameter + 2 * w, t.height - 2 * w, w)


def tank_shell(t: layout.ToroidalTank) -> bd.Solid:
    return (tank_outer(t) - tank_inner(t)).solid()


def build(ctx):
    r = ctx.resolver()
    t = layout.toroidal_tank(r)
    x, y, z = (r.get("lpg_system.tank_centre_x"), r.get("lpg_system.tank_centre_y"),
               r.get("lpg_system.tank_base_z"))
    ctx.add(TANK_ID, ASSEMBLY, [(bd.Pos(x, y, z) * tank_outer(t), TANK_COLOUR)], r,
            f"LPG toroidal tank {t.outer_diameter:.0f} x {t.height:.0f} mm, PLACEHOLDER position")
    _visual_package(ctx, r, (x, y, z), t)
    return ctx.parts


def _visual_package(ctx, base, tank, t):
    """PLACEHOLDER petrol system (FUL-001..004) and LPG kit parts (FUL-006, FUL-008..014). Schematic
    routes only; the LPG filler FUL-007 is not drawn because its location is UNKNOWN. This is a
    digital-twin picture, never installation guidance for gas equipment."""
    from ..cad.mech import ALU, DARK, RED, STEEL, adder, block, cyl, disc, pipe
    from .engine import datums
    p = layout.profile(base)
    x0, x1, cz, hw = datums(base)
    px0, px1, py0, py1, pz0, pz1 = base.get("pkg_petrol_tank")
    fw, fz = base.get("pkg_firewall_x"), base.get("pkg_floor_z")
    add = adder(ctx, ASSEMBLY, base)
    tx, ty, tz = tank
    xm = (x0 + x1) / 2
    add("FUL-001", block(px0, px1, py0, py1, pz0, pz1, DARK), "Petrol tank beside the spare-wheel well (photos E-025); envelope guessed")
    add("FUL-002", pipe([((px0 + px1) / 2, py1, pz0 + 20), (fw + 300, -p.half_width + 140, fz - 20), (fw - 100, -hw - 120, cz + 120), (xm, -60, cz + 330)], 4, STEEL),
        "Petrol feed line (route schematic)")
    add("FUL-003", pipe([((px0 + px1) / 2, py0 + 40, pz1), (2900, -p.half_width + 60, 780)], 22, DARK)
        + [(disc((2900, -p.half_width + 25, 780), (0, 1, 0), 45, 15), DARK)], "Filler neck to the cap on the LH rear quarter (photos E-026)")
    add("FUL-004", block(x0 + 60, x0 + 140, -hw - 70, -hw, cz + 120, cz + 200, ALU), "Fuel pump envelope; mechanical or electric UNKNOWN")
    ox = tx - t.opening_diameter / 2 + 25
    add("FUL-006", block(ox - 35, ox + 35, ty - 50, ty + 50, tz + 20, tz + 120, (0.80, 0.68, 0.35, 1.0)) + [(cyl((ox, ty, tz + 120), (ox, ty, tz + 170), 28), RED)],
        "ALBIEN multivalve with 12 V solenoid in the central opening (photos E-022/E-023); size guessed")
    add("FUL-008", pipe([(ox, ty, tz + 60), (tx - 200, 450, fz + 140), (fw + 200, 450, fz - 10), (fw - 80, 420, 560)], 4, (0.72, 0.45, 0.20, 1.0)),
        "LPG high-pressure line (route schematic, side guessed)")
    add("FUL-009", [(cyl((fw - 80, 420, 560), (fw - 80, 420, 660), 25), RED)], "LPG solenoid valve with filter (position guessed)")
    add("FUL-010", [(disc((fw - 160, -150, 640), (1, 0, 0), 85, 70), ALU)], "LPG vaporiser/regulator; a round coolant-heated unit near the bulkhead is visible (E-027), identity unconfirmed")
    add("FUL-011", [(disc((xm, -40, cz + 310), (0, 0, 1), 60, 15), ALU)], "LPG gas-air mixer ring under the air cleaner (not visible; kit type UNKNOWN)")
    add("FUL-012", [(cyl((xm - 90, -150, cz + 260), (xm - 30, -150, cz + 260), 18), RED)], "Petrol cut-off solenoid (presence UNKNOWN)")
    sw = base.get("pkg_steering_wheel")
    dx1 = base.get("pkg_dash")[1]
    add("FUL-013", block(dx1 - 5, dx1 + 10, sw[1] + 230, sw[1] + 280, 700, 730, DARK), "Petrol/LPG changeover switch on the dash (position guessed)")
    add("FUL-014", block(tx - 60, tx + 60, ty - 140, ty + 140, tz - 10, tz + 5, STEEL) + [(disc((tx, ty, tz + t.height - 20), (0, 0, 1), t.opening_diameter / 2 + 30, 6), DARK)],
        "Mounting brackets through the well floor and the black centre cover (photos E-022/E-025); sizes guessed")


def build_cad(ctx):
    r = ctx.resolver()
    t = layout.toroidal_tank(r)
    ctx.add(TANK_ID, ASSEMBLY, [(tank_shell(t), TANK_COLOUR)], r,
            f"LPG toroidal tank shell {t.outer_diameter:.0f} x {t.height:.0f} mm, opening "
            f"{t.opening_diameter:.0f} mm, wall {t.wall:g} mm; internal volume {t.internal_volume_l:.2f} L "
            f"(simplified stadium section); LOCAL frame, not placed in the vehicle (position UNKNOWN); "
            "mounting, multivalve, filler and lines not modelled", placed=False)
    return ctx.parts
