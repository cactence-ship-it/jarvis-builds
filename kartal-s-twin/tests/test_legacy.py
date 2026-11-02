"""Legacy archive analyser on synthetic archives (the real ZIP has not been received)."""
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from kartal_twin import PROJECT_ROOT

_s = importlib.util.spec_from_file_location("analyze_legacy", PROJECT_ROOT / "tools" / "analyze_legacy.py")
al = importlib.util.module_from_spec(_s)
_s.loader.exec_module(al)

THREE = {"metadata": {"version": 4.5, "type": "Object"},
         "geometries": [{"uuid": "g1", "type": "BoxGeometry", "width": 4.4, "height": 1.2, "depth": 1.6},
                        {"uuid": "g2", "type": "BufferGeometry",
                         "data": {"attributes": {"position": {"itemSize": 3, "type": "Float32Array",
                                                              "array": [0, 0, 0, 1, 0, 0, 0, 1, 0]}}}}],
         "object": {"type": "Group", "name": "Kartal", "children": [
             {"type": "Mesh", "name": "govde", "geometry": "g1"},
             {"type": "Mesh", "name": "far_sol", "geometry": "g2"},
             {"type": "Group", "name": "bos_grup"}]}}


class LegacyAnalyser(unittest.TestCase):
    def _zip(self, members):
        d = Path(tempfile.mkdtemp())
        p = d / "Kartal_S_Studyo.zip"
        with zipfile.ZipFile(p, "w") as z:
            for name, text in members.items():
                z.writestr(name, text)
        return p

    def test_threejs_objects_classified(self):
        html = '<script src="three.min.js"></script><script>new THREE.CylinderGeometry(1,1,2)</script>' \
               '<img src="data:image/jpeg;base64,AAAA">'
        rep = al.analyse_zip(self._zip({"index.html": html, "kartal.json": json.dumps(THREE)}))
        s = al.summary(rep)
        self.assertEqual(s["objects"], 4)
        self.assertEqual(s["by_geometry_kind"], {"NO_GEOMETRY": 2, "PROCEDURAL": 1, "MESH": 1})
        self.assertEqual(s["procedural_calls_in_html"], 1)
        self.assertTrue(any("embedded image" in w for w in rep["warnings"]))
        self.assertIn("| /Kartal/govde | Mesh | PROCEDURAL BoxGeometry |", al.to_markdown(rep))

    def test_generic_json_named_lists(self):
        doc = {"parts": [{"name": "kapi", "verts": []}, {"name": "tampon"}]}
        rep = al.analyse_zip(self._zip({"kartal.json": json.dumps(doc)}))
        self.assertEqual(rep["json"]["kartal.json"]["format"], "generic JSON")
        self.assertEqual(rep["json"]["kartal.json"]["named_lists"][0]["count"], 2)


if __name__ == "__main__":
    unittest.main()
