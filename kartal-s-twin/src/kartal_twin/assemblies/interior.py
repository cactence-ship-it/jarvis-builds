"""INTERIOR (INT) - PLACEHOLDER cockpit and cabin: dashboard, cluster, aftermarket sport steering
wheel (LHD), column, three pedals, floor gear lever, handbrake, console, seats, door cards, headliner,
carpets, trim and luggage floor covering. Arrangement from photos E-024; every size is a guess."""
import build123d as bd

from .. import layout
from ..cad.mech import BLACK, DARK, FABRIC, STEEL, TRIM, adder, block, cyl, disc
from ..cad.shapes import box

ASSEMBLY = "INTERIOR"
PHASE = 5


def build(ctx):
    base = ctx.resolver()
    p, g = layout.profile(base), layout.greenhouse(base)
    dx0, dx1, dz0, dz1 = base.get("pkg_dash")
    sx, sy, sz, sr = base.get("pkg_steering_wheel")
    fx0, fx1, yi, yo, cz0, cz1, bt = base.get("pkg_front_seat")
    rx0, rx1, ryo, rz0, rz1, rbt = base.get("pkg_rear_seat")
    px, pyl, pyr, pz0, pz1 = base.get("pkg_pedals")
    fz, cfz, fw = base.get("pkg_floor_z"), base.get("pkg_cargo_floor_z"), base.get("pkg_firewall_x")
    glx, hbx = base.get("pkg_gear_lever_x"), base.get("pkg_handbrake_x")
    xb, xc = base.get("body_profile.b_pillar_x"), base.get("body_profile.c_pillar_x")
    hw = p.half_width - 45
    xa = layout.wheel_centres(base)["RL"][0]
    arch_r = layout.tire(base, "rear").outer_diameter / 2 + base.get("arch_clearance")
    ax0, atop = xa - arch_r, layout.wheel_centres(base)["RL"][2] + arch_r
    iw = p.half_width - base.get("arch_depth") - 20          # inner width between the rear arches
    add = adder(ctx, ASSEMBLY, base)
    add("INT-001", block(dx0, dx1, -hw + 20, hw - 20, dz0, dz1, BLACK), "Dashboard envelope")
    add("INT-002", block(dx1 - 10, dx1 + 30, sy - 170, sy + 170, dz1 - 160, dz1 - 30, DARK), "Instrument cluster face (speedometer, tachometer: E-024)")
    tilt = (-0.55, 0, 0.83)
    c = bd.Vector(sx, sy, sz)
    add("INT-003", [(bd.Plane(origin=c, z_dir=tilt) * bd.Torus(sr, 16), (0.85, 0.80, 0.65, 1.0)),
                    (disc((sx, sy, sz), tilt, 45, 30), DARK)]
        + [(cyl((sx, sy, sz), (sx + 0.55 * 0.0, sy + dy * sr * 0.95, sz + dz * sr * 0.95), 10), STEEL) for dy, dz in ((1, 0), (-1, 0), (0, -1))],
        "Aftermarket three-spoke sport wheel, beige rim (E-024); size guessed")
    add("INT-004", [(cyl((fw - 20, sy, sz - 260), (sx + 20, sy, sz - 15), 22), DARK)], "Steering column (angle guessed)")
    peds = []
    for y in (pyl, (pyl + pyr) / 2, pyr):
        peds += [(cyl((px, y, pz1), (px + 90, y, pz0), 9), STEEL), (box(px + 70, px + 100, y - 35, y + 35, pz0, pz0 + 80), BLACK)]
    add("INT-005", peds, "Clutch, brake and accelerator pedals (three pedals, E-024)")
    add("INT-006", [(cyl((glx, 0, fz + 150), (glx + 60, 0, fz + 450), 9), STEEL), (bd.Pos(glx + 62, 0, fz + 470) * bd.Sphere(28), BLACK),
                    (box(glx - 60, glx + 60, -60, 60, fz + 120, fz + 160), BLACK)], "Floor gear lever with boot (E-024)")
    add("INT-007", [(cyl((hbx, 0, fz + 210), (hbx + 220, 0, fz + 330), 14), BLACK)], "Handbrake lever between the seats (position guessed)")
    add("INT-008", block(dx1 - 40, hbx + 260, -120, 120, fz, fz + 200, BLACK), "Centre console / tunnel cover")
    for cid, s in (("INT-009", -1), ("INT-010", 1)):
        y0, y1 = sorted((s * yi, s * yo))
        add(cid, block(fx0, fx1, y0, y1, cz0, cz1, FABRIC) + block(fx1 - 110, fx1, y0 + 20, y1 - 20, cz1, bt, FABRIC)
            + block(fx1 - 90, fx1 - 30, (y0 + y1) / 2 - 110, (y0 + y1) / 2 + 110, bt, bt + 180, FABRIC),
            "Front seat with aftermarket cover (E-024); size guessed")
    add("INT-011", block(rx0, rx1, -ryo, ryo, rz0, rz1, FABRIC) + block(rx1 - 110, rx1, -ryo, ryo, rz1, rbt, FABRIC), "Rear bench (E-024)")
    runners = []
    for s in (-1, 1):
        for yy in (yi + 60, yo - 60):
            runners += block(fx0 - 40, fx1, s * yy - 15, s * yy + 15, fz, cz0, STEEL)
    add("INT-012", runners, "Seat runners and frames (guessed)")
    doors = {"INT-013": (-1, fw + 80, xb), "INT-014": (1, fw + 80, xb), "INT-015": (-1, xb + 20, xc), "INT-016": (1, xb + 20, xc)}
    for cid, (s, x0, x1) in doors.items():
        y0, y1 = sorted((s * (hw - 10), s * hw))
        grey = (0.70, 0.71, 0.72, 1.0)
        if x1 > ax0:   # rear door: the lower card stops at the wheel arch
            bodies = block(x0, ax0 - 20, y0, y1, fz + 60, g.z_belt - 10, grey) + block(ax0 - 20, x1 - 20, y0, y1, atop + 20, g.z_belt - 10, grey)
        else:
            bodies = block(x0, x1 - 20, y0, y1, fz + 60, g.z_belt - 10, grey)
        add(cid, bodies, "Door card (grey, E-024)")
    ctl = []
    for s, x in ((-1, xb - 250), (1, xb - 250), (-1, xc - 250), (1, xc - 250)):
        y0, y1 = sorted((s * (hw - 40), s * (hw - 10)))
        ctl += block(x, x + 150, y0, y1, g.z_belt - 260, g.z_belt - 200, BLACK)
    add("INT-017", ctl, "Inner handles and window controls (schematic)")
    add("INT-018", block(g.x_roof_front + 40, g.x_roof_rear - 40, -g.half_roof + 40, g.half_roof - 40, g.z_roof - 50, g.z_roof - 40, (0.80, 0.80, 0.78, 1.0)),
        "Headliner (E-024)")
    add("INT-019", block(fw, ax0 - 20, -hw + 20, hw - 20, fz, fz + 8, (0.20, 0.20, 0.22, 1.0)), "Carpets / floor mats")
    trim = []
    for s in (-1, 1):
        y0, y1 = sorted((s * (g.half_belt - 30), s * (g.half_belt - 10)))
        yp0, yp1 = sorted((s * (g.half_roof - 50), s * (g.half_roof - 30)))      # pillars lean inward with the greenhouse
        trim += block(xb - 40, xb + 40, yp0, yp1, g.z_belt, g.z_roof - 60, TRIM) + block(xc, p.x_tail - 80, y0, y1, atop + 20, g.z_belt, TRIM)
    add("INT-020", trim, "Pillar and luggage-side trim (schematic)")
    tx, ty = base.get("lpg_system.tank_centre_x"), base.get("lpg_system.tank_centre_y")
    mat = box(rx1, p.x_tail - 60, -iw, iw, cfz, cfz + 6) - bd.Pos(tx, ty, cfz + 3) * bd.Cylinder(340, 10)
    add("INT-021", [(mat.solid(), (0.12, 0.30, 0.33, 1.0))], "Luggage floor covering with the well opening (photos E-022)")
    return ctx.parts
