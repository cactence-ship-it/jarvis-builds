"""DRIVETRAIN (DRV) - PLACEHOLDER propeller shaft, differential and rigid rear axle.

Rear-wheel drive with a rigid (live) rear axle (photos E-025); sizes are package guesses.
"""
from .. import layout
from ..cad.mech import DARK, STEEL, adder, cyl, disc, ring
from .transmission import output_point
from ..cad.shapes import box


def block_c(c, lx, ly, lz):
    return box(c[0] - lx / 2, c[0] + lx / 2, c[1] - ly / 2, c[1] + ly / 2, c[2] - lz / 2, c[2] + lz / 2)


ASSEMBLY = "DRIVETRAIN"
PHASE = 6


def build(ctx):
    base = ctx.resolver()
    w = layout.wheel_centres(base)
    xo, _, zo = output_point(base)
    dr, tr = base.get("pkg_diff_r"), base.get("pkg_axle_tube_r")
    xa = (w["RL"][0] + w["RR"][0]) / 2
    za = w["RL"][2]
    add = adder(ctx, ASSEMBLY, base)
    xn = xa - dr - 60
    tod = base.get("drivetrain.propshaft_tube_od")                  # E-056
    god, gth = base.get("drivetrain.flex_coupling_od"), base.get("drivetrain.flex_coupling_thickness")
    base.get("drivetrain.propshaft_construction")
    cup, span = 23.8, 61.2                                          # drivetrain.ujoint_cross (E-056)
    xc = xo + (xn - xo) * 0.45                                      # centre bearing at 45 % (guess)
    zc = zo + (za - zo) * 0.45

    def ujoint(x, z):
        return [(cyl((x, -span / 2, z), (x, span / 2, z), cup / 2), STEEL), (cyl((x, 0, z - span / 2), (x, 0, z + span / 2), cup / 2), STEEL)]
    add("DRV-001", [(disc((xo + gth / 2 + 5, 0, zo), (1, 0, 0), god / 2, gth), (0.08, 0.08, 0.08, 1.0)),          # guibo
                    (cyl((xo + gth + 5, 0, zo), (xc - 40, 0, zc), tod / 2), STEEL),                              # front shaft
                    (block_c((xc, 0, zc - 10), 100, 165, 97), DARK),                                             # centre bearing + bracket
                    (cyl((xc + 40, 0, zc), (xn - 30, 0, za), tod / 2), STEEL)]                                   # rear shaft
        + ujoint(xc + 25, zc) + ujoint(xn - 15, za),
        f"Two-piece propeller shaft (E-056, ESTIMATED LOW): flexible coupling {god} x {gth} mm at the gearbox, front "
        f"shaft, centre bearing, rear shaft, crosses {cup} x {span} mm; tube {tod} mm; bearing position guessed")
    add("DRV-002", [(cyl((xa, -dr * 0.6, za), (xa, dr * 0.6, za), dr), DARK), (cyl((xa - dr - 70, 0, za), (xa, 0, za), 60), DARK),
                    (disc((xn + 10, 0, za), (1, 0, 0), 46, 12), STEEL)],
        "Differential housing with pinion nose and drive flange; final drive 4.10 (E-031/E-056); housing size guessed")
    yi = w["RL"][1] + 130
    sl = base.get("drivetrain.axle_shaft_length")
    base.get("drivetrain.rear_wheel_bearing")
    bodies = [(cyl((xa, yi, za), (xa, -yi, za), tr), STEEL)]
    for s in (-1, 1):
        ye = s * abs(w["RL"][1] - 20)
        bodies.append((ring((xa, ye, za), (0, 1, 0), 32.5, 15, 21), (0.75, 0.72, 0.60, 1.0)))             # 30 x 65 x 21 bearing
        bodies.append((cyl((xa, ye, za), (xa, s * 60, za), 12), (0.40, 0.40, 0.42, 1.0)))   # half-shaft to the diff side gear (U-018)
    add("DRV-003", bodies,
        f"Rigid rear axle tube, half-shafts drawn from the wheel bearing to the differential (the quoted {sl} mm, E-056, "
        "does not fit the 1327 mm track: U-018) and wheel bearings 30 x 65 x 21 (E-056); tube radius guessed")
    return ctx.parts
