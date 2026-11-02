"""Small geometric helpers on top of build123d (all coordinates VCS mm)."""
from __future__ import annotations

import build123d as bd
import numpy as np


def box(x0, x1, y0, y1, z0, z1) -> bd.Solid:
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(x1 - x0, y1 - y0, z1 - z0)


def thick_quad(pts, thickness: float, outward, inset: float = 0.0, gap: float = 1.5) -> bd.Solid:
    """Planar quad (4 points) shrunk by `inset`, lifted `gap` along `outward`, thickened."""
    p = np.array(pts, float)
    c = p.mean(0)
    if inset:
        p = np.array([c + (q - c) * (1 - inset / max(np.linalg.norm(q - c), 1e-9)) for q in p])
    n = np.cross(p[1] - p[0], p[2] - p[0])
    n /= np.linalg.norm(n)
    if np.dot(n, outward) < 0:
        n, p = -n, p[::-1]
    p = p + n * gap
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(*q) for q in p], close=True))
    return bd.Solid.extrude(face, bd.Vector(*(n * thickness)))


def one(shape):
    """Normalise a boolean result (Shape or ShapeList) to a single Shape."""
    if isinstance(shape, bd.ShapeList) or isinstance(shape, list):
        items = list(shape)
        if not items:
            raise ValueError("boolean operation produced no geometry")
        return items[0] if len(items) == 1 else bd.Compound(children=items)
    return shape
