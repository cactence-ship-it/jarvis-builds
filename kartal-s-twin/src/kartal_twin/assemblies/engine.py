"""ENGINE (ENG) - PLACEHOLDER visual package of the longitudinal carburettor engine.

Arrangement from photos E-027 (longitudinal, round air cleaner on top, front radiator with an
electric fan, belt-driven accessories); every size and position is a package guess
(specs/placeholder_assumptions.yaml, pkg_*). No internal parts (crank, pistons, valves) are
modelled: there is no evidence for them.
"""
from .. import layout
from ..cad.mech import ALU, BLACK, DARK, STEEL, adder, block, cyl, disc, pipe

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
    add("ENG-001", block(x0, x1, -hw, hw, zb, zh, DARK), "Block envelope; bore, stroke and internals not modelled")
    add("ENG-002", block(x0 + 5, x1 - 5, -hw + 10, hw - 10, zh, zc, ALU), "Cylinder head envelope")
    add("ENG-003", block(x0 + 20, x1 - 20, -hw + 40, hw - 40, zc, zc + 50, BLACK), "Cam cover envelope")
    add("ENG-004", block(x0 + 30, x1 - 10, -hw + 10, hw - 10, zb - 110, zb, DARK), "Sump envelope")
    xm = (x0 + x1) / 2
    add("ENG-005", [(disc((xm, -40, zc + 135), (0, 0, 1), 150, 80), BLACK)]
        + pipe([(xm - 150, -40, zc + 135), (rx + 120, -250, zc + 60)], 40, BLACK)
        + block(xm - 120, xm + 120, -hw - 70, -hw + 10, zh - 60, zh + 40, ALU),
        "Round air cleaner on top (photos E-027) with intake duct; intake manifold on the LH side (side guessed)")
    add("ENG-006", block(x0 + 40, x1 - 40, hw, hw + 70, zh - 90, zh + 30, (0.45, 0.30, 0.20, 1.0)),
        "Exhaust manifold envelope on the RH side (side guessed)")
    add("ENG-007", block(xm - 60, xm + 60, -100, 20, zc + 20, zc + 95, ALU),
        "Carburettor envelope under the air cleaner (carburettor itself hidden in the photos)")
    rz0, rz1 = 250, 650
    add("ENG-008", block(rx - 15, rx + 15, -300, 300, rz0, rz1, BLACK)
        + [(disc((rx + 45, 0, (rz0 + rz1) / 2), (1, 0, 0), 170, 25), DARK)]
        + pipe([(rx + 15, 200, rz1 - 40), (x0 - 20, 80, zh)], 18, BLACK)
        + pipe([(rx + 15, -200, rz0 + 40), (x0 - 20, -60, cz)], 18, BLACK)
        + [(disc((x0 - 30, 0, cz + 80), (1, 0, 0), 60, 40), ALU)],
        "Radiator, electric fan (photos E-027), hoses and water pump; sizes guessed")
    add("ENG-009", [(cyl((x0 + 10, -hw - 120, zh - 20), (x0 + 120, -hw - 120, zh - 20), 62), ALU)],
        "Alternator envelope at the front of the engine; side guessed")
    add("ENG-010", [(cyl((x1 + 20, hw + 60, cz - 40), (x1 + 200, hw + 60, cz - 40), 42), DARK)],
        "Starter envelope at the bellhousing; side guessed")
    add("ENG-011", block(xm - 40, xm + 40, -hw - 80, -hw, cz - 60, cz + 20, STEEL)
        + block(xm - 40, xm + 40, hw, hw + 80, cz - 60, cz + 20, STEEL), "Two engine mounts; positions guessed")
    return ctx.parts
