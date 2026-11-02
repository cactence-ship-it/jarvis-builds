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
    return ctx.parts


def build_cad(ctx):
    r = ctx.resolver()
    t = layout.toroidal_tank(r)
    ctx.add(TANK_ID, ASSEMBLY, [(tank_shell(t), TANK_COLOUR)], r,
            f"LPG toroidal tank shell {t.outer_diameter:.0f} x {t.height:.0f} mm, opening "
            f"{t.opening_diameter:.0f} mm, wall {t.wall:g} mm; internal volume {t.internal_volume_l:.2f} L "
            f"(simplified stadium section); LOCAL frame, not placed in the vehicle (position UNKNOWN); "
            "mounting, multivalve, filler and lines not modelled", placed=False)
    return ctx.parts
