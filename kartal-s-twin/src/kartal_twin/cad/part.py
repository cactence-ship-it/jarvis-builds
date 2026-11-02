"""A built component: one inventory ID, one representation, one or more coloured bodies."""
from __future__ import annotations

from dataclasses import dataclass, field

from ..params import Resolver

RGBA = tuple[float, float, float, float]


@dataclass
class Part:
    component_id: str
    assembly: str
    representation: str                 # visual | cad | mechanical (D-006)
    bodies: list                        # [(build123d Solid/Compound in VCS mm, RGBA)]
    used: dict = field(default_factory=dict)
    geometry_status: str = "PLACEHOLDER"
    note: str = ""


class BuildContext:
    """Passed to every assembly builder; collects parts with derived status."""

    def __init__(self, resolver: Resolver | None = None, representation: str = "visual"):
        self.base = resolver or Resolver()
        self.representation = representation
        self.parts: list[Part] = []

    def resolver(self) -> Resolver:
        return self.base.fork()

    def add(self, component_id: str, assembly: str, bodies, r: Resolver, note: str = "") -> Part:
        part = Part(component_id, assembly, self.representation, list(bodies), dict(r.used),
                    r.geometry_status, note)
        self.parts.append(part)
        return part
