"""REAR_SUSPENSION (RSU) - PLACEHOLDER parts around the rigid rear axle (photos E-025: axle tube
and a transverse locating rod). Spring TYPE (coil or leaf) is UNKNOWN, so the springs are neutral
envelopes; the two trailing links are ASSUMED (link layout not evidenced). Sizes are guesses."""
from .. import layout
from ..cad.mech import DARK, STEEL, adder, block, cyl

ASSEMBLY = "REAR_SUSPENSION"
PHASE = 8


def build(ctx):
    base = ctx.resolver()
    w = layout.wheel_centres(base)
    xa, za = w["RL"][0], w["RL"][2]
    sy, tr, cz_ = base.get("pkg_rear_spring_y"), base.get("pkg_axle_tube_r"), base.get("pkg_cargo_floor_z")
    dmin, dmax = base.get("suspension.rear_damper_length_compressed"), base.get("suspension.rear_damper_length_extended")
    add = adder(ctx, ASSEMBLY, base)
    for s, spr, dmp, hub in ((-1, "RSU-001", "RSU-003", "RSU-007"), (1, "RSU-002", "RSU-004", "RSU-008")):
        y = s * sy
        add(spr, [(cyl((xa, y, za + tr), (xa, y, cz_ - 110), 75), (0.55, 0.55, 0.60, 1.0))],
            "Spring ENVELOPE only: coil or leaf is UNKNOWN (suspension.rear_spring_type)")
        lo, up = (xa + 70, s * (sy + 70), za - 30), (xa + 150, s * (sy + 25), cz_ - 120)   # guessed eyes
        d = [b - a for a, b in zip(lo, up)]
        n = sum(v * v for v in d) ** 0.5
        L = (dmin + dmax) / 2                                           # mid-stroke eye-to-eye (E-044)
        u = [v / n for v in d]
        top = tuple(a + v * L for a, v in zip(lo, u))
        body = tuple(a + v * (dmin - 40) for a, v in zip(lo, u))
        add(dmp, [(cyl(lo, body, 25), DARK), (cyl(body, top, 10), STEEL)],
            f"Telescopic damper drawn at mid stroke, eye-to-eye {L:.0f} mm between {dmin} and {dmax} mm "
            "(Fiat 131 saloon KYB 343142, E-044, ESTIMATED LOW); lower eye guessed, upper eye follows the length")
        hy = w["RL" if s < 0 else "RR"][1] - s * 110
        add(hub, [(cyl((xa, hy, za), (xa, hy + s * 40, za), 70), STEEL)], "Axle end / hub flange envelope")
    links = [(cyl((xa + 60, -sy + 40, za + 20), (xa + 90, sy + 80, za + 90), 15), DARK)]
    for s in (-1, 1):
        links.append((cyl((xa - 20, s * (sy - 60), za - 60), (xa - 520, s * (sy - 40), za - 30), 18), DARK))
    add("RSU-005", links, "Transverse locating rod (photos E-025) and two trailing links (ASSUMED)")
    bush = []
    for s in (-1, 1):
        for x, y, z in ((xa - 520, s * (sy - 40), za - 30), (xa - 20, s * (sy - 60), za - 60)):
            bush.append((cyl((x, y - 25, z), (x, y + 25, z), 22), (0.1, 0.1, 0.1, 1.0)))
    add("RSU-006", bush, "Link bushings")
    mnt = []
    for x, y, z in ((xa - 540, -sy + 40, za + 10), (xa - 540, sy - 40, za + 10), (xa + 90, sy + 80, za + 130),
                    (xa + 150, -(sy + 25), cz_ - 120), (xa + 150, sy + 25, cz_ - 120)):
        mnt += block(x - 25, x + 25, y - 25, y + 25, z - 25, z + 25, STEEL)
    add("RSU-009", mnt, "Body-side mounting points (guessed)")
    return ctx.parts
