"""FRONT_SUSPENSION (FSU) - PLACEHOLDER MacPherson struts (photos E-027: strut top mounts on both
inner-wing towers), coil springs, track-control arms (catalogue length E-046), struts (E-048), hub bearings (E-047), anti-roll bar, knuckles. Spring rates, geometry,
camber and caster are UNKNOWN; every size and point is a package guess."""
from .. import layout
from ..cad.mech import DARK, RED, STEEL, adder, block, coil, cyl, pipe, ring

ASSEMBLY = "FRONT_SUSPENSION"
PHASE = 8


def points(r, side):
    """Hard points for one side (side -1 LH, +1 RH)."""
    x, y, z = layout.wheel_centres(r)["FL" if side < 0 else "FR"]
    s = side
    top_z, inset = r.get("pkg_strut_top_z"), r.get("pkg_strut_inset")
    al = r.get("suspension.front_lower_arm_length")                 # E-046
    ball = (x, y - s * 120, z - 110)
    dz = 30                                                         # inner pivot 30 mm above the ball joint (guess)
    piv = (x, ball[1] - s * (al * al - dz * dz) ** 0.5, ball[2] + dz)  # transverse track-control arm, catalogue length
    return {"wheel": (x, y, z), "knuckle": (x, y - s * 120, z), "strut_low": (x + 10, y - s * 125, z + 90),
            "strut_top": (x + 30, y - s * inset - s * 30, top_z), "ball": ball,
            "pivot_f": piv, "pivot_r": piv}


def build(ctx):
    base = ctx.resolver()
    bore, rod, al = (base.get(k) for k in ("suspension.front_strut_bore", "suspension.front_strut_rod_diameter", "suspension.front_lower_arm_length"))
    base.get("suspension.front_wheel_bearing")
    add = adder(ctx, ASSEMBLY, base)
    for side, (spr, dmp, arm, knk) in ((-1, ("FSU-001", "FSU-003", "FSU-005", "FSU-009")),
                                       (1, ("FSU-002", "FSU-004", "FSU-006", "FSU-010"))):
        P = points(base, side)
        lo, top = P["strut_low"], P["strut_top"]
        mid = tuple(lo[i] + (top[i] - lo[i]) * 0.35 for i in range(3))
        upper = tuple(lo[i] + (top[i] - lo[i]) * 0.92 for i in range(3))
        add(spr, coil(mid, upper, 70, 7, 6, RED), "Coil spring (MacPherson); rate and free length UNKNOWN")
        add(dmp, [(cyl(lo, mid, bore / 2 + 10), DARK), (cyl(mid, top, rod / 2), STEEL)],
            f"Strut damper, twin tube: bore {bore} mm, rod {rod} mm (Monroe 11002 for Fiat 131, E-048, ESTIMATED LOW); "
            "outer tube wall and stroke guessed")
        add(arm, pipe([P["pivot_f"], P["ball"]], 15, DARK) + [(cyl((P["ball"][0], P["ball"][1], P["ball"][2] - 18), (P["ball"][0], P["ball"][1], P["ball"][2] + 18), 22), DARK)],
            f"Track-control arm with ball joint, {al} mm (AYD 00016 listing E-046, ESTIMATED LOW); fore-aft location "
            "by the anti-roll bar as on the Fiat 131 (bar as compression strut, ASSUMED)")
        kx, ky, kz = P["knuckle"]
        b_in, b_od, b_w = 28, 57.15, 17.462                         # E-047 (spec: suspension.front_wheel_bearing)
        add(knk, block(kx - 45, kx + 45, ky - 30, ky + 30, kz - 120, kz + 110, STEEL)
            + [(cyl((kx, ky, kz), (kx, ky + side * 60, kz), b_od / 2 + 9), STEEL),
               (ring((kx, ky + side * 40, kz), (0, 1, 0), b_od / 2, b_in / 2, b_w), (0.75, 0.72, 0.60, 1.0)),
               (cyl((kx, ky, kz), (kx, ky + side * 95, kz), b_in / 2 - 1), STEEL)],
            f"Knuckle with hub, outer taper bearing {b_in} x {b_od} x {b_w} mm (listings E-047, ESTIMATED LOW) and spindle")
    L, R = points(base, -1), points(base, 1)
    bar = [(L["ball"][0] - 40, L["ball"][1], L["ball"][2] + 10), (L["pivot_f"][0] - 120, -420, L["pivot_f"][2] - 10),
           (R["pivot_f"][0] - 120, 420, R["pivot_f"][2] - 10), (R["ball"][0] - 40, R["ball"][1], R["ball"][2] + 10)]
    add("FSU-007", pipe(bar, 11, DARK), "Anti-roll bar presence and shape UNKNOWN (suspension.front_antiroll_bar_fitted)")
    bush = []
    for P in (L, R):
        x, y, z = P["pivot_f"]
        bush.append((cyl((x - 30, y, z), (x + 30, y, z), 24), (0.1, 0.1, 0.1, 1.0)))
    add("FSU-008", bush, "Lower-arm bushings")
    tops = []
    for P in (L, R):
        x, y, z = P["strut_top"]
        tops += block(x - 55, x + 55, y - 55, y + 55, z, z + 25, STEEL)
    add("FSU-011", tops, "Strut top mounts on the towers (photos E-027); positions guessed")
    return ctx.parts
