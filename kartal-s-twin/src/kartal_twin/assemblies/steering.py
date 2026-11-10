"""STEERING (STR) - PLACEHOLDER steering-gear envelope, linkage and tie rods for an LHD car with
hydraulic power assistance (photos E-024, E-027). Rack-and-pinion (ESTIMATED, E-038/E-039); tie-rod
length from listings (E-045); points are guesses. Column = INT-004, wheel = INT-003."""
import build123d as bd

from ..cad.mech import ALU, DARK, STEEL, adder, block, cyl, pipe, ring
from .front_suspension import points


def bd_sphere(c, r):
    return bd.Pos(*c) * bd.Sphere(r)


ASSEMBLY = "STEERING"
PHASE = 8


def build(ctx):
    base = ctx.resolver()
    L, R = points(base, -1), points(base, 1)
    sw = base.get("pkg_steering_wheel")
    fw = base.get("pkg_firewall_x")
    add = adder(ctx, ASSEMBLY, base)
    gx, gz = L["wheel"][0] + 140, L["wheel"][2] + 40
    trl = base.get("steering.tie_rod_length")                        # E-045
    base.get("steering.steering_gear_type")                          # rack-and-pinion, ESTIMATED (E-038/E-039)
    ends = {}
    for s in (-1, 1):
        P = L if s < 0 else R
        kx, ky, kz = P["knuckle"]
        outer = (kx + 110, ky - s * 10, gz)                          # steering-arm ball joint (guessed)
        dx = gx - outer[0]
        ends[s] = (outer, (gx, outer[1] - s * (trl * trl - dx * dx) ** 0.5, gz))
    half = abs(ends[1][1][1]) - 70                                  # housing ends 70 mm inside the inner joints (boots)
    boots = []
    for s in (-1, 1):
        for k in range(5):
            yb = s * (half + 10 + k * 12)
            boots.append((ring((gx, yb, gz), (0, 1, 0), 30 if k % 2 == 0 else 22, 0, 10), (0.05, 0.05, 0.05, 1.0)))
    add("STR-001", [(cyl((gx, -half, gz), (gx, half, gz), 28), ALU),
                    (cyl((gx, -half + 60, gz), (gx - 40, -half + 60, gz + 110), 30), ALU),        # pinion housing (LHD)
                    (cyl((gx, -half - 70, gz), (gx, half + 70, gz), 11), STEEL)] + boots,
        "Rack-and-pinion gear (type ESTIMATED from parts listings E-039, Fiat 131 E-038), power assisted (pump "
        "in owner photos); housing length follows the catalogue tie-rod length; boots and pinion angle guessed")
    add("STR-002", pipe([(gx - 40, -half + 60, gz + 110), (fw - 150, sw[1], gz + 200), (fw - 20, sw[1], sw[2] - 260)], 14, STEEL),
        "Intermediate shaft from the pinion to the column (layout guessed)")
    for cid, s in (("STR-003", -1), ("STR-004", 1)):
        outer, inner = ends[s]
        add(cid, [(cyl(inner, outer, 9), STEEL), (bd_sphere(outer, 16), DARK), (bd_sphere(inner, 14), DARK)],
            f"Tie rod {trl} mm, M14x1.5 (listings E-045, ESTIMATED LOW) with inner and outer ball joints")
    add("STR-005", block(gx - 30, gx + 30, -330, -290, gz - 70, gz + 70, DARK) + block(gx - 30, gx + 30, 290, 330, gz - 70, gz + 70, DARK),
        "Gear mounting points (guessed)")
    return ctx.parts
