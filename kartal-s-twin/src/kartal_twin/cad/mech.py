"""Primitive helpers for the mechanical PLACEHOLDER package (VCS mm, D-003).

Every helper returns a list of (solid, rgba) bodies so a component can be made of several
closed solids without boolean unions (faster, always watertight per body).
"""
from __future__ import annotations

import math

import build123d as bd

from .shapes import box

STEEL = (0.55, 0.56, 0.58, 1.0)
DARK = (0.16, 0.16, 0.17, 1.0)
BLACK = (0.07, 0.07, 0.08, 1.0)
ALU = (0.72, 0.73, 0.74, 1.0)
RUST = (0.45, 0.30, 0.20, 1.0)
RED = (0.65, 0.12, 0.10, 1.0)
WIRE = (0.85, 0.55, 0.10, 1.0)
TRIM = (0.30, 0.30, 0.32, 1.0)
FABRIC = (0.55, 0.45, 0.30, 1.0)


def _v(p):
    return bd.Vector(*p)


def cyl(p0, p1, r) -> bd.Solid:
    """Solid cylinder of radius r from point p0 to point p1."""
    a, b = _v(p0), _v(p1)
    d = b - a
    if d.length < 1e-6 or r <= 0:
        raise ValueError("degenerate cylinder")
    plane = bd.Plane(origin=a, z_dir=d)
    return bd.Solid.make_cylinder(r, d.length, plane)


def ring(c, axis, r_out, r_in, t) -> bd.Solid:
    """Annulus (outer r_out, inner r_in, thickness t) centred at c with the given axis."""
    a = _v(axis).normalized()
    c = _v(c)
    plane = bd.Plane(origin=c - a * (t / 2), z_dir=a)
    outer = bd.Solid.make_cylinder(r_out, t, plane)
    return (outer - bd.Solid.make_cylinder(r_in, t, plane)).solid() if r_in > 0 else outer


def disc(c, axis, r, t) -> bd.Solid:
    return ring(c, axis, r, 0, t)


def pipe(points, r, rgba) -> list:
    """Polyline pipe: one cylinder per segment plus a sphere at every inner joint."""
    bodies = []
    for p0, p1 in zip(points, points[1:]):
        bodies.append((cyl(p0, p1, r), rgba))
    for p in points[1:-1]:
        bodies.append((bd.Pos(*p) * bd.Sphere(r), rgba))
    return bodies


def coil(p0, p1, coil_r, wire_r, turns, rgba) -> list:
    """Coil-spring look-alike: `turns` tori stacked between p0 and p1 (visual only)."""
    a, b = _v(p0), _v(p1)
    d = b - a
    out = []
    for i in range(turns):
        c = a + d * ((i + 0.5) / turns)
        plane = bd.Plane(origin=c, z_dir=d)
        out.append((plane * bd.Torus(coil_r, wire_r), rgba))
    return out


def block(x0, x1, y0, y1, z0, z1, rgba) -> list:
    return [(box(x0, x1, y0, y1, z0, z1), rgba)]


def mirror_y(points):
    return [(x, -y, z) for x, y, z in points]


def deg(a):
    return math.radians(a)


def adder(ctx, assembly: str, base):
    """add(cid, bodies, note): one component whose provenance includes the shared `base` reads."""
    def add(cid, bodies, note=""):
        r = ctx.resolver()
        r.absorb(base)
        ctx.add(cid, assembly, list(bodies), r, note)
    return add
