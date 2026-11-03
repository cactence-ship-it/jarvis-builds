"""FRONT_SUSPENSION (FSU) - PLACEHOLDER MacPherson struts (photos E-027: strut top mounts on both
inner-wing towers), coil springs, lower arms, anti-roll bar, knuckles. Spring rates, geometry,
camber and caster are UNKNOWN; every size and point is a package guess."""
from .. import layout
from ..cad.mech import DARK, RED, STEEL, adder, block, coil, cyl, pipe

ASSEMBLY = "FRONT_SUSPENSION"
PHASE = 8


def points(r, side):
    """Hard points for one side (side -1 LH, +1 RH)."""
    x, y, z = layout.wheel_centres(r)["FL" if side < 0 else "FR"]
    s = side
    top_z, inset, iy = r.get("pkg_strut_top_z"), r.get("pkg_strut_inset"), r.get("pkg_arm_inner_y")
    return {"wheel": (x, y, z), "knuckle": (x, y - s * 120, z), "strut_low": (x + 10, y - s * 125, z + 90),
            "strut_top": (x + 30, y - s * inset - s * 30, top_z), "ball": (x, y - s * 120, z - 110),
            "pivot_f": (x - 90, s * iy, z - 80), "pivot_r": (x + 160, s * iy, z - 80)}


def build(ctx):
    base = ctx.resolver()
    add = adder(ctx, ASSEMBLY, base)
    for side, (spr, dmp, arm, knk) in ((-1, ("FSU-001", "FSU-003", "FSU-005", "FSU-009")),
                                       (1, ("FSU-002", "FSU-004", "FSU-006", "FSU-010"))):
        P = points(base, side)
        lo, top = P["strut_low"], P["strut_top"]
        mid = tuple(lo[i] + (top[i] - lo[i]) * 0.35 for i in range(3))
        upper = tuple(lo[i] + (top[i] - lo[i]) * 0.92 for i in range(3))
        add(spr, coil(mid, upper, 70, 7, 6, RED), "Coil spring (MacPherson); rate and free length UNKNOWN")
        add(dmp, [(cyl(lo, mid, 28), DARK), (cyl(mid, top, 11), STEEL)], "Strut damper; stroke UNKNOWN")
        add(arm, pipe([P["pivot_f"], P["ball"], P["pivot_r"]], 16, DARK), "Lower control arm (two-pivot shape guessed)")
        kx, ky, kz = P["knuckle"]
        add(knk, block(kx - 45, kx + 45, ky - 30, ky + 30, kz - 120, kz + 110, STEEL)
            + [(cyl((kx, ky, kz), (kx, ky + side * 60, kz), 45), STEEL)], "Knuckle and hub envelope")
    L, R = points(base, -1), points(base, 1)
    bar = [(L["ball"][0] - 40, L["ball"][1], L["ball"][2] + 10), (L["pivot_f"][0] - 120, -420, L["pivot_f"][2] - 10),
           (R["pivot_f"][0] - 120, 420, R["pivot_f"][2] - 10), (R["ball"][0] - 40, R["ball"][1], R["ball"][2] + 10)]
    add("FSU-007", pipe(bar, 11, DARK), "Anti-roll bar presence and shape UNKNOWN (suspension.front_antiroll_bar_fitted)")
    bush = []
    for P in (L, R):
        for k in ("pivot_f", "pivot_r"):
            x, y, z = P[k]
            bush.append((cyl((x - 30, y, z), (x + 30, y, z), 24), (0.1, 0.1, 0.1, 1.0)))
    add("FSU-008", bush, "Lower-arm bushings")
    tops = []
    for P in (L, R):
        x, y, z = P["strut_top"]
        tops += block(x - 55, x + 55, y - 55, y + 55, z, z + 25, STEEL)
    add("FSU-011", tops, "Strut top mounts on the towers (photos E-027); positions guessed")
    return ctx.parts
