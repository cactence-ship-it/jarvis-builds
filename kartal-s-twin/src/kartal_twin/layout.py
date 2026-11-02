"""Shared vehicle layout derived from the spec (+ placeholders), in VCS millimetres.

Every function takes a Resolver, so provenance of every derived number is recorded.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .params import Resolver


@dataclass(frozen=True)
class Tire:
    section_width: float
    aspect: float
    rim_diameter_in: float

    @property
    def outer_diameter(self) -> float:
        return self.rim_diameter_in * 25.4 + 2 * self.section_width * self.aspect

    @property
    def rim_radius(self) -> float:
        return self.rim_diameter_in * 25.4 / 2


def tire(r: Resolver, axle: str = "front") -> Tire:
    size = r.get(f"wheels_tires.tire_size_{axle}")
    m = re.fullmatch(r"\s*(\d{3})/(\d{2})\s*R\s*(\d{2})\s*", str(size))
    if not m:
        raise ValueError(f"cannot parse tire size {size!r}")
    rim = r.get("wheels_tires.wheel_rim_diameter")
    if int(m.group(3)) != int(rim):
        raise ValueError(f"tire size {size} conflicts with rim diameter {rim} in")
    return Tire(float(m.group(1)), int(m.group(2)) / 100, float(rim))


def wheel_centres(r: Resolver) -> dict[str, tuple[float, float, float]]:
    """Centres of the four road wheels: FL, FR, RL, RR (LH = -Y)."""
    wb = (r.get("dimensions.wheelbase_lh") + r.get("dimensions.wheelbase_rh")) / 2
    out = {}
    for axle, x, track in (("F", 0.0, r.get("dimensions.front_track")),
                           ("R", wb, r.get("dimensions.rear_track"))):
        t = tire(r, "front" if axle == "F" else "rear")
        z = t.outer_diameter / 2 - r.get("tire_static_deflection")
        out[axle + "L"] = (x, -track / 2, z)
        out[axle + "R"] = (x, track / 2, z)
    return out


@dataclass(frozen=True)
class Profile:
    x_front: float      # front extremity (bumper face)
    x_rear: float       # rear extremity (bumper face)
    x_nose: float       # body front face
    x_tail: float       # body rear face
    half_width: float
    height: float


def profile(r: Resolver) -> Profile:
    length = r.get("dimensions.overall_length")
    fo = r.get("dimensions.front_overhang")
    bp = r.get("body_profile.bumper_protrusion")
    x_front = -fo
    x_rear = x_front + length
    return Profile(x_front, x_rear, x_front + bp, x_rear - bp,
                   r.get("dimensions.overall_width_body") / 2, r.get("dimensions.overall_height"))


@dataclass(frozen=True)
class Greenhouse:
    """Lofted cabin between the beltline section and the roof section."""
    x_belt_front: float
    x_belt_rear: float
    x_roof_front: float
    x_roof_rear: float
    half_belt: float
    half_roof: float
    z_belt: float
    z_roof: float

    def side_point(self, x_bottom: float, x_top: float, u: float, side: int):
        """Point on the side glass plane (side = +1 RH, -1 LH) at height fraction u."""
        x = x_bottom + (x_top - x_bottom) * u
        y = side * (self.half_belt + (self.half_roof - self.half_belt) * u)
        return (x, y, self.z_belt + (self.z_roof - self.z_belt) * u)


def greenhouse(r: Resolver) -> Greenhouse:
    p = profile(r)
    return Greenhouse(r.get("body_profile.cowl_x"), p.x_tail - r.get("tail_rear_inset"),
                      r.get("body_profile.windshield_top_x"), p.x_tail - r.get("body_profile.roof_rear_inset"),
                      p.half_width - r.get("greenhouse_inset_belt"),
                      r.get("body_profile.roof_width") / 2,
                      r.get("body_profile.belt_z"), p.height)
