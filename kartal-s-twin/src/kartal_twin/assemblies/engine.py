"""ENGINE (ENG) - PLACEHOLDER visual package of the longitudinal carburettor engine (rev 2, 2026-11-07:
ribbed block, timing cover, plug leads, runners, radiator tanks, fan blades, belt drive, D-037).

Arrangement from photos E-027 (longitudinal, round air cleaner on top, front radiator with an
electric fan, belt-driven accessories); every size and position is a package guess
(specs/placeholder_assumptions.yaml, pkg_*). No internal parts (crank, pistons, valves) are
modelled: there is no evidence for them.
"""
import math

import build123d as bd

from .. import layout
from ..cad.mech import ALU, BLACK, DARK, STEEL, adder, block, cyl, disc, pipe, ring

IRON = (0.30, 0.30, 0.31, 1.0)       # cast-iron block colour (visual only)
RUBBER = (0.05, 0.05, 0.05, 1.0)
PLASTIC = (0.10, 0.10, 0.11, 1.0)


def _hull(points):
    """Convex hull (monotone chain) of 2-D points, counter-clockwise."""
    pts = sorted(set(points))
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def belt(x, pulleys, r_belt, rgba, n=10):
    """Accessory belt in the plane X = x wrapped around pulleys [(y, z, r)]: the convex hull of the
    pulley rims, as a closed pipe. Visual routing only; a hull cannot show serpentine back-bends."""
    rim = [(round(y + r * math.cos(2 * math.pi * k / n), 2), round(z + r * math.sin(2 * math.pi * k / n), 2))
           for y, z, r in pulleys for k in range(n)]
    h = _hull(rim)
    return pipe([(x, y, z) for y, z in h + h[:1]], r_belt, rgba)


def fan(c, r_hub, r_tip, blades, rgba):
    """Axial fan (axis X): hub disc plus `blades` flat blades pitched 25 degrees."""
    out = [(disc(c, (1, 0, 0), r_hub, 30), rgba)]
    span = r_tip - r_hub
    for k in range(blades):
        blade = (bd.Pos(*c) * bd.Rot(360 * k / blades, 0, 0) * bd.Pos(0, 0, r_hub + span / 2)
                 * bd.Rot(0, 0, 25) * bd.Box(4, 48, span))
        out.append((blade, rgba))
    return out

ASSEMBLY = "ENGINE"
PHASE = 6


def datums(r):
    x0, ln, cz, hw = (r.get(k) for k in ("pkg_engine_x0", "pkg_engine_len", "pkg_crank_z", "pkg_block_half_w"))
    return x0, x0 + ln, cz, hw


def build(ctx):
    base = ctx.resolver()
    x0, x1, cz, hw = datums(base)
    rx = base.get("pkg_radiator_x")
    layout.profile(base)
    add = adder(ctx, ASSEMBLY, base)
    zb, zh, zc = cz - 100, cz + 200, cz + 300                      # sump top, deck, head top
    xm = (x0 + x1) / 2
    pitch = (x1 - x0) / 4                                           # four cylinders (E-029)
    xf = x0 - 40                                                    # accessory-drive plane, front of block
    # ENG-001 block: cast-iron body, four cylinder-pitch ribs per side, front timing-belt cover.
    ribs = []
    for i in range(5):
        xr = x0 + i * pitch
        for sgn in (-1, 1):
            ribs += block(xr - 6, xr + 6, sgn * hw - (8 if sgn < 0 else 0), sgn * hw + (8 if sgn > 0 else 0), zb + 10, zh - 10, IRON)
    add("ENG-001", block(x0, x1, -hw, hw, zb, zh, IRON) + ribs
        + block(x0 - 30, x0, -70, 70, cz - 20, zc + 20, PLASTIC),
        "Block: cast-iron body with ribs at the cylinder pitch of a 4-cylinder (E-029) and the front "
        "timing-belt cover (Fiat SOHC belt drive, black cover visible in owner photos); bore, stroke "
        "and internals not modelled (no evidence)")
    plugs = [(cyl((x0 + (i + 0.5) * pitch, hw - 10, zh + 60), (x0 + (i + 0.5) * pitch, hw + 25, zh + 60), 11), PLASTIC)
             for i in range(4)]
    add("ENG-002", block(x0 + 5, x1 - 5, -hw + 10, hw - 10, zh, zc, ALU) + plugs,
        "Cylinder head (aluminium) with four spark-plug leads on the exhaust side (side guessed)")
    add("ENG-003", block(x0 + 20, x1 - 20, -hw + 40, hw - 40, zc, zc + 30, PLASTIC)
        + block(x0 + 35, x1 - 35, -hw + 55, hw - 55, zc + 30, zc + 50, PLASTIC)
        + [(cyl((x0 + 60, hw - 80, zc + 50), (x0 + 60, hw - 80, zc + 75), 30), (0.85, 0.83, 0.75, 1.0))],
        "Cam cover with oil-filler cap at the front (light cap visible in owner photos)")
    add("ENG-004", block(x0 + 30, x1 - 10, -hw + 10, hw - 10, zb - 60, zb, DARK)
        + block(x0 + 120, x1 - 20, -hw + 30, hw - 30, zb - 130, zb - 60, DARK),
        "Sump: stepped (deep rear well, typical); depth guessed")
    add("ENG-005", [(disc((xm, -40, zc + 135), (0, 0, 1), 150, 80), BLACK)]
        + pipe([(xm - 150, -40, zc + 135), (rx + 120, -250, zc + 60)], 40, BLACK)
        + block(xm - 120, xm + 120, -hw - 70, -hw + 10, zh - 60, zh + 40, ALU),
        "Round air cleaner on top (photos E-027) with intake duct; intake manifold on the LH side (side guessed)")
    runners = [(cyl((x0 + (i + 0.5) * pitch, hw - 5, zh - 30), (x0 + (i + 0.5) * pitch, hw + 60, zh - 70), 18), (0.45, 0.30, 0.20, 1.0))
               for i in range(4)]
    add("ENG-006", runners + pipe([(x0 + 0.5 * pitch, hw + 60, zh - 70), (x1 - 0.5 * pitch, hw + 60, zh - 70),
                                   (x1 + 40, hw + 40, zb - 40)], 24, (0.45, 0.30, 0.20, 1.0)),
        "Exhaust manifold: four runners into a collector on the RH side (side guessed)")
    add("ENG-007", block(xm - 60, xm + 60, -100, 20, zc + 20, zc + 95, ALU),
        "Carburettor envelope under the air cleaner (carburettor itself hidden in the photos)")
    cw, ch, cd = (base.get(k) for k in ("engine.radiator_core_width", "engine.radiator_core_height", "engine.radiator_core_depth"))  # E-041
    rzm = 450                                                       # radiator centre height (guess)
    rz0, rz1, hwc = rzm - ch / 2, rzm + ch / 2, cw / 2
    rfan = rx + cd / 2 + 45
    fr = min(ch / 2 - 8, 150)                                       # fan must fit the core height
    add("ENG-008", block(rx - cd / 2, rx + cd / 2, -hwc, hwc, rz0, rz1, (0.20, 0.20, 0.21, 1.0))        # core
        + block(rx - cd / 2 - 8, rx + cd / 2 + 8, -hwc - 45, -hwc, rz0 - 15, rz1 + 15, PLASTIC)          # LH tank
        + block(rx - cd / 2 - 8, rx + cd / 2 + 8, hwc, hwc + 45, rz0 - 15, rz1 + 15, PLASTIC)            # RH tank
        + [(cyl((rx, hwc + 22, rz1 + 15), (rx, hwc + 22, rz1 + 40), 16), STEEL),
           (disc((rx, hwc + 22, rz1 + 45), (0, 0, 1), 28, 10), STEEL)]                                   # filler neck + cap
        + [(ring((rfan, 0, rzm), (1, 0, 0), fr + 12, fr + 4, 45), PLASTIC)]                              # fan shroud
        + fan((rfan, 0, rzm), 38, fr, 7, PLASTIC)
        + [(cyl((rfan + 20, 0, rzm), (rfan + 75, 0, rzm), 45), DARK)]                                   # fan motor
        + pipe([(rx + cd / 2 + 8, hwc + 22, rz1 - 30), (rx + 160, hwc, rz1 - 10), (x0 - 120, 120, zh + 40), (x0 - 10, 60, zh + 40)], 19, RUBBER)
        + pipe([(rx + cd / 2 + 8, -hwc - 22, rz0 + 30), (rx + 180, -hwc, rz0 + 20), (xf - 40, -90, cz + 40), (xf, 0, cz + 150)], 19, RUBBER)
        + [(disc((xf, 0, cz + 150), (1, 0, 0), 55, 18), ALU)],                                    # water-pump pulley
        f"Radiator core {cw} x {ch} x {cd} mm (2-row aluminium, plastic side tanks; aftermarket M131 1.6 listing E-041, "
        "ESTIMATED LOW), filler cap on the RH tank (owner photos), electric fan sized to the core with shroud and motor, "
        "hoses and water-pump pulley (positions guessed)")
    pulleys = [(0, cz, 65), (0, cz + 150, 55), (-hw - 120, zh - 20, 35), (200, zh + 50, 60)]
    add("ENG-009", [(cyl((x0 + 10, -hw - 120, zh - 20), (x0 + 120, -hw - 120, zh - 20), 62), ALU),
                    (disc((xf, -hw - 120, zh - 20), (1, 0, 0), 35, 18), STEEL),
                    (cyl((xf + 20, 200, zh + 50), (x0 + 120, 200, zh + 50), 50), ALU),
                    (disc((xf, 200, zh + 50), (1, 0, 0), 60, 18), STEEL),
                    (disc((xf, 0, cz), (1, 0, 0), 65, 22), STEEL)]
        + belt(xf, pulleys, 5, RUBBER),
        "Alternator (LH, side guessed) and accessory belt drive: crank, water-pump, alternator and "
        "power-steering pump pulleys (PS pump and belt visible in owner photos); belt shown as the "
        "hull of the pulleys")
    add("ENG-010", [(cyl((x1 + 20, hw + 60, cz - 40), (x1 + 200, hw + 60, cz - 40), 42), DARK),
                    (cyl((x1 + 140, hw + 60, cz - 40), (x1 + 200, hw + 60, cz + 20), 28), DARK)],
        "Starter with solenoid at the bellhousing; side guessed")
    add("ENG-011", block(xm - 40, xm + 40, -hw - 80, -hw, cz - 60, cz + 20, STEEL)
        + block(xm - 40, xm + 40, hw, hw + 80, cz - 60, cz + 20, STEEL)
        + [(cyl((xm, -hw - 40, cz - 60), (xm, -hw - 40, cz - 100), 30), RUBBER),
           (cyl((xm, hw + 40, cz - 60), (xm, hw + 40, cz - 100), 30), RUBBER)],
        "Two engine mounts with rubber bushes; positions guessed")
    return ctx.parts
