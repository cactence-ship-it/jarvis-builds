"""Side-photo scaling on synthetic data with known answers (including camera roll)."""
import importlib.util
import math
import unittest

import numpy as np

from kartal_twin import PROJECT_ROOT

_s = importlib.util.spec_from_file_location("photo_scale", PROJECT_ROOT / "tools" / "photo_scale.py")
ps = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ps)


def to_px(x_mm, z_mm, scale=0.25, roll_deg=3.0, origin=(400.0, 700.0), wheel_z=290.0):
    """Synthetic camera: VCS (X rearward, Z up) -> image pixels (y down), with roll."""
    a = math.radians(roll_deg)
    u, v = x_mm * scale, -(z_mm - wheel_z) * scale         # relative to the front wheel centre
    return [origin[0] + u * math.cos(a) - v * math.sin(a), origin[1] + u * math.sin(a) + v * math.cos(a)]


class PhotoScale(unittest.TestCase):
    def test_recovers_known_points_despite_roll(self):
        wb = 2490.0
        pts = {"front_wheel": to_px(0, 290), "rear_wheel": to_px(wb, 290),
               "ground": [to_px(-200, 0), to_px(2700, 0)], "pixel_error": 2,
               "points": {"body_profile.belt_z": to_px(1500, 955),
                          "body_profile.cowl_x": to_px(1060, 960),
                          "body_profile.b_pillar_x": to_px(1760, 1200)}}
        res = ps.solve(pts, wb)
        self.assertAlmostEqual(res["body_profile.belt_z"][0], 955, delta=0.5)
        self.assertAlmostEqual(res["body_profile.cowl_x"][0], 1060, delta=0.5)
        self.assertAlmostEqual(res["body_profile.b_pillar_x"][0], 1760, delta=0.5)
        for v, tol in res.values():
            self.assertGreater(tol, 0.02 * v * 0.99)          # perspective allowance included

    def test_rejects_non_side_quantities(self):
        pts = {"front_wheel": [0, 0], "rear_wheel": [100, 0], "ground": [[0, 10], [100, 10]],
               "points": {"body_profile.roof_width": [50, -50]}}
        with self.assertRaises(ValueError):
            ps.solve(pts, 2490)


if __name__ == "__main__":
    unittest.main()
