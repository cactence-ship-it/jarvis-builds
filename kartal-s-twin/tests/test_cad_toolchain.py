"""CAD toolchain: build123d/OpenCascade exports are re-opened and checked independently.

An asymmetric 100 x 50 x 20 mm block with a 20 mm through-hole is used so that axis
swaps, scale errors, holes and flipped normals are all detectable.
"""
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

from kartal_twin import export_check as xc

SIZE = np.array([100.0, 50.0, 20.0])
VOLUME = 100 * 50 * 20 - math.pi * 10 ** 2 * 20


class CadToolchain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import build123d as bd
        cls.bd = bd
        cls.tmp = tempfile.TemporaryDirectory()
        d = Path(cls.tmp.name)
        cls.part = (bd.Box(*SIZE, align=(bd.Align.MIN,) * 3)
                    - bd.Pos(30, 25, 10) * bd.Cylinder(10, 20))
        cls.step, cls.stl, cls.glb = d / "t.step", d / "t.stl", d / "t.glb"
        cls.ok = (bd.export_step(cls.part, cls.step),
                  bd.export_stl(cls.part, cls.stl, tolerance=0.01, angular_tolerance=0.1),
                  bd.export_gltf(cls.part, cls.glb, binary=True))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_kernel_builds_valid_solid(self):
        self.assertTrue(self.part.is_valid)
        self.assertAlmostEqual(self.part.volume, VOLUME, delta=1e-6 * VOLUME)
        self.assertEqual(self.ok, (True, True, True))

    def test_step_reopens_identically(self):
        back = self.bd.import_step(self.step)
        self.assertTrue(back.is_valid)
        self.assertAlmostEqual(back.volume, VOLUME, delta=1e-6 * VOLUME)
        bb = back.bounding_box()
        np.testing.assert_allclose([bb.min.X, bb.min.Y, bb.min.Z], [0, 0, 0], atol=1e-6)
        np.testing.assert_allclose([bb.max.X, bb.max.Y, bb.max.Z], SIZE, atol=1e-6)

    def test_stl_is_watertight_outward_and_to_scale(self):
        tri, normals = xc.read_stl(self.stl)
        r = xc.analyse_triangles(tri, weld_tol=1e-4)
        self.assertTrue(r.watertight, r)
        self.assertTrue(r.consistent_winding, r)
        self.assertEqual(r.degenerate, 0)
        self.assertEqual(xc.stl_normal_flips(tri, normals), 0)
        self.assertGreater(r.volume, 0, "normals must point outward")
        self.assertAlmostEqual(r.volume, VOLUME, delta=2e-3 * VOLUME)
        np.testing.assert_allclose(r.size, SIZE, atol=1e-3)

    def test_glb_is_valid_metres_and_y_up(self):
        js, tri, issues = xc.read_glb(self.glb)
        self.assertEqual(issues, [])
        self.assertEqual(js["asset"]["version"], "2.0")
        r = xc.analyse_triangles(tri, weld_tol=1e-9)
        self.assertTrue(r.watertight, r)
        self.assertGreater(r.volume, 0)
        self.assertAlmostEqual(r.volume * 1e9, VOLUME, delta=2e-3 * VOLUME)   # m^3 -> mm^3
        # Measured exporter convention (E-006): glTF (x, y, z) = CAD (X, Z, -Y) * 0.001
        np.testing.assert_allclose(r.bbox_min, [0, 0, -0.05], atol=1e-6)
        np.testing.assert_allclose(r.bbox_max, [0.1, 0.02, 0], atol=1e-6)

    def test_vcs_to_gltf_mapping_is_a_proper_rotation(self):
        self.assertAlmostEqual(np.linalg.det(xc.VCS_TO_GLTF / 0.001), 1.0)
        forward_vcs = np.array([-1.0, 0, 0])            # vehicle front is -X in the VCS
        np.testing.assert_allclose(xc.VCS_TO_GLTF @ forward_vcs / 0.001, [0, 0, 1])  # glTF front +Z
        np.testing.assert_allclose(xc.VCS_TO_GLTF @ np.array([0, 0, 1.0]) / 0.001, [0, 1, 0])


if __name__ == "__main__":
    unittest.main()
