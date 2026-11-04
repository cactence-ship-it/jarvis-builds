#!/usr/bin/env python3
"""Write build/blender/params.json: every dimension the Blender body script uses, read through the
Resolver from the spec and placeholder assumptions (so provenance stays in one place)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from kartal_twin import PROJECT_ROOT, layout  # noqa: E402
from kartal_twin.params import Resolver  # noqa: E402

r = Resolver()
p, g, w = layout.profile(r), layout.greenhouse(r), layout.wheel_centres(r)
t, m = layout.tire(r, "front"), layout.rim(r)
keys = ["body_profile.sill_z", "body_profile.belt_z", "body_profile.nose_top_z", "body_profile.nose_bottom_z",
        "body_profile.rear_bottom_z", "body_profile.cowl_x", "body_profile.b_pillar_x", "body_profile.c_pillar_x",
        "body_profile.bumper_bottom_z", "body_profile.bumper_height", "body_profile.mirror_protrusion",
        "dimensions.overall_height_roof_rails", "arch_clearance", "paint_rgba"]
out = {"profile": p.__dict__, "greenhouse": g.__dict__, "wheels": w,
       "tire": {"od": t.outer_diameter, "width": t.section_width, "rim_r": t.rim_radius},
       "rim": {"bead_r": m.bead_seat_radius, "width": m.width_between_flanges, "flange": m.flange_height},
       "values": {k: r.get(k) for k in keys}, "provenance": dict(r.used)}
d = PROJECT_ROOT / "build" / "blender"
d.mkdir(parents=True, exist_ok=True)
(d / "params.json").write_text(json.dumps(out, indent=1, default=float))
print("wrote", d / "params.json")
