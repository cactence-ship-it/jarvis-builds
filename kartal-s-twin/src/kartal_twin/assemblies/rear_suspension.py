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
    ll, lu = base.get("suspension.rear_lower_link_length"), base.get("suspension.rear_upper_link_length")   # E-056/E-057
    links, ends = [], []
    for s in (-1, 1):
        ra = (xa - 20, s * (sy - 60), za - 70)                      # lower arm axle bracket (guessed)
        fa = (ra[0] - (ll * ll - 60 * 60) ** 0.5, s * (sy - 40), ra[2] + 60)   # 617 mm forward, 60 mm up
        rb = (xa - 30, s * 160, za + 95)                            # upper arm on the axle casing top (guessed)
        fb = (rb[0] - (lu * lu - 40 * 40) ** 0.5, s * 200, rb[2] + 40)
        links += [(cyl(ra, fa, 17), DARK), (cyl(rb, fb, 14), DARK)]
        ends += [ra, fa, rb, fb]
    pr = [(xa + 60, -sy + 40, za + 20), (xa + 90, sy + 80, za + 90)]
    links.append((cyl(pr[0], pr[1], 15), DARK))
    add("RSU-005", links,
        f"Four links and Panhard rod: two lower trailing arms {ll} mm and two short upper arms {lu} mm (Fiat 131 parts, "
        "E-056/E-057, ESTIMATED LOW; Kartal fit not confirmed), Panhard rod length UNKNOWN (photo E-025 shows a "
        "transverse rod); all mounting points guessed")
    bush = [(cyl((x, y - 25, z), (x, y + 25, z), 22), (0.1, 0.1, 0.1, 1.0)) for x, y, z in ends + pr]
    add("RSU-006", bush, "Link and Panhard bushings at the link ends")
    mnt = []
    for x, y, z in [e for i, e in enumerate(ends) if i % 2 == 1] + [pr[1], (xa + 150, -(sy + 25), cz_ - 120), (xa + 150, sy + 25, cz_ - 120)]:
        mnt += block(x - 25, x + 25, y - 25, y + 25, z - 25, z + 25, STEEL)
    add("RSU-009", mnt, "Body-side mounting points (forward link ends, Panhard body end, damper tops; guessed)")
    return ctx.parts
