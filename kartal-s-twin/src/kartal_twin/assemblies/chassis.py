"""CHASSIS (CHS) - PLACEHOLDER floor pan with spare-wheel well, structural members, crossmembers
and mounting interfaces. Construction type (unibody or not) is UNKNOWN (body.body_construction);
the well under the LPG tank is from photos E-022/E-025, every size is a package guess.
"""
import build123d as bd

from .. import layout
from ..cad.mech import DARK, STEEL, adder, block, ring
from ..cad.shapes import box

ASSEMBLY = "CHASSIS"
PHASE = 7


def build(ctx):
    base = ctx.resolver()
    p = layout.profile(base)
    fz, cz_, wz = base.get("pkg_floor_z"), base.get("pkg_cargo_floor_z"), base.get("pkg_well_floor_z")
    fw, ry = base.get("pkg_firewall_x"), base.get("pkg_front_rail_y")
    tx, ty = base.get("lpg_system.tank_centre_x"), base.get("lpg_system.tank_centre_y")
    xa = layout.wheel_centres(base)["RL"][0]
    add = adder(ctx, ASSEMBLY, base)
    hw = p.half_width - 60
    iw = p.half_width - base.get("arch_depth") - 20          # inner width between the rear arches
    xr = p.x_tail - 60
    well_r = 330
    cargo = box(xa - 350, xr, -iw, iw, cz_ - 4, cz_) - bd.Pos(tx, ty, cz_ - 2) * bd.Cylinder(well_r, 10)
    add("CHS-001", [(box(fw - 40, xa - 350, -hw, hw, fz - 4, fz), STEEL), (cargo.solid(), STEEL),
                    (box(xa - 380, xa - 350, -iw, iw, fz, cz_), STEEL), (box(fw - 40, fw, -hw, hw, fz, 900), STEEL),
                    (ring((tx, ty, (wz + cz_) / 2), (0, 0, 1), well_r + 4, well_r, cz_ - wz), STEEL),
                    (bd.Pos(tx, ty, wz + 2) * bd.Cylinder(well_r + 4, 4), STEEL)],
        "Cabin floor, heel board, luggage floor with the spare-wheel well (photos E-022/E-025) and bulkhead; sizes guessed")
    add("CHS-002", block(p.x_nose + 120, fw + 400, -ry - 45, -ry + 45, fz + 10, fz + 110, DARK)
        + block(p.x_nose + 120, fw + 400, ry - 45, ry + 45, fz + 10, fz + 110, DARK)
        + block(fw - 50, xa - 300, -hw - 40, -hw + 20, fz - 15, fz + 80, DARK)
        + block(fw - 50, xa - 300, hw - 20, hw + 40, fz - 15, fz + 80, DARK)
        + block(xa - 380, xr, -560, -480, cz_ - 110, cz_ - 10, DARK)
        + block(xa - 380, xr, 480, 560, cz_ - 110, cz_ - 10, DARK),
        "Front rails, sills and rear rails (layout guessed; construction UNKNOWN)")
    add("CHS-003", block(-60, 60, -ry - 45, ry + 45, fz - 10, fz + 50, DARK)
        + block(fw + 500, fw + 560, -hw, hw, fz - 10, fz + 30, DARK)
        + block(xa - 380, xa - 320, -560, 560, cz_ - 110, cz_ - 30, DARK)
        + block(xr - 60, xr, -560, 560, cz_ - 110, cz_ - 10, DARK),
        "Front suspension crossmember, floor and rear crossmembers (guessed)")
    pts = [(-80, -ry, fz + 120), (-80, ry, fz + 120), (xa - 100, -560, cz_ - 130), (xa - 100, 560, cz_ - 130),
           (fw + 100, -120, fz + 30), (fw + 100, 120, fz + 30)]
    add("CHS-004", [(box(x - 25, x + 25, y - 25, y + 25, z - 25, z + 25), STEEL) for x, y, z in pts],
        "Mounting interfaces (engine, front suspension, rear links, gearbox); positions guessed")
    return ctx.parts
