"""Geometry builders - one module per VEHICLE_MASTER assembly (contract only in Phase 1).

Each module exposes ASSEMBLY, PHASE and build(spec). build() must read every dimension
from specs/kartal_s_1997.yaml and must refuse to build from UNKNOWN parameters.
"""

MODULES = {
    "BODY_ASSEMBLY": "kartal_twin.assemblies.body_assembly",
    "EXTERIOR_TRIM": "kartal_twin.assemblies.exterior_trim",
    "GLAZING": "kartal_twin.assemblies.glazing",
    "LIGHTING": "kartal_twin.assemblies.lighting",
    "INTERIOR": "kartal_twin.assemblies.interior",
    "ENGINE": "kartal_twin.assemblies.engine",
    "TRANSMISSION": "kartal_twin.assemblies.transmission",
    "DRIVETRAIN": "kartal_twin.assemblies.drivetrain",
    "CHASSIS": "kartal_twin.assemblies.chassis",
    "FRONT_SUSPENSION": "kartal_twin.assemblies.front_suspension",
    "REAR_SUSPENSION": "kartal_twin.assemblies.rear_suspension",
    "STEERING": "kartal_twin.assemblies.steering",
    "BRAKING": "kartal_twin.assemblies.braking",
    "FUEL_SYSTEM": "kartal_twin.assemblies.fuel_system",
    "EXHAUST": "kartal_twin.assemblies.exhaust",
    "ELECTRICAL": "kartal_twin.assemblies.electrical",
    "WHEELS_AND_TIRES": "kartal_twin.assemblies.wheels_and_tires",
}
