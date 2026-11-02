"""Minimal, dependency-free GLB writer for the Android viewer.

One node per component (name = component ID, extras = metadata), grouped under one node
per assembly under VEHICLE_MASTER. Vertices are converted VCS mm -> glTF m (D-003).
Per-face smooth normals keep CAD creases sharp but curved faces smooth.
"""
from __future__ import annotations

import json
import struct

import numpy as np

from .export_check import VCS_TO_GLTF


def tessellate(shape, tol: float = 0.5, ang: float = 0.3):
    """Return (positions (n,3) VCS mm, normals (n,3), indices (m,3)) with per-face normals."""
    pos, nrm, idx, off = [], [], [], 0
    for face in shape.faces():
        verts, tris = face.tessellate(tol, ang)
        if not tris:
            continue
        v = np.array([(p.X, p.Y, p.Z) for p in verts], float)
        t = np.array(tris, np.int64)
        fn = np.cross(v[t[:, 1]] - v[t[:, 0]], v[t[:, 2]] - v[t[:, 0]])
        vn = np.zeros_like(v)
        for k in range(3):
            np.add.at(vn, t[:, k], fn)
        ln = np.linalg.norm(vn, axis=1, keepdims=True)
        vn = np.divide(vn, ln, out=np.zeros_like(vn), where=ln > 0)
        pos.append(v); nrm.append(vn); idx.append(t + off); off += len(v)
    if not pos:
        return np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3), np.int64)
    return np.concatenate(pos), np.concatenate(nrm), np.concatenate(idx)


class GlbBuilder:
    def __init__(self):
        self.js = {"asset": {"version": "2.0", "generator": "kartal_twin.gltf_writer"},
                   "scene": 0, "scenes": [{"name": "VEHICLE_MASTER", "nodes": [0]}],
                   "nodes": [{"name": "VEHICLE_MASTER", "children": []}],
                   "meshes": [], "materials": [], "accessors": [], "bufferViews": [],
                   "buffers": [{"byteLength": 0}]}
        self.bin = bytearray()
        self._groups: dict[str, int] = {}
        self._materials: dict[tuple, int] = {}

    def _view(self, data: bytes, target: int) -> int:
        while len(self.bin) % 4:
            self.bin.append(0)
        self.js["bufferViews"].append({"buffer": 0, "byteOffset": len(self.bin),
                                       "byteLength": len(data), "target": target})
        self.bin += data
        return len(self.js["bufferViews"]) - 1

    def _accessor(self, arr: np.ndarray, ctype: int, typ: str, target: int, minmax: bool) -> int:
        a = {"bufferView": self._view(arr.tobytes(), target), "componentType": ctype,
             "count": int(arr.shape[0]), "type": typ}
        if minmax:
            a["min"] = arr.min(0).astype(float).tolist()
            a["max"] = arr.max(0).astype(float).tolist()
        self.js["accessors"].append(a)
        return len(self.js["accessors"]) - 1

    def _material(self, rgba) -> int:
        key = tuple(round(float(c), 4) for c in rgba)
        if key not in self._materials:
            m = {"name": "rgba_" + "_".join(f"{c:.2f}" for c in key),
                 "pbrMetallicRoughness": {"baseColorFactor": list(key), "metallicFactor": 0.1,
                                          "roughnessFactor": 0.55}, "doubleSided": False}
            if key[3] < 1.0:
                m["alphaMode"] = "BLEND"
            self.js["materials"].append(m)
            self._materials[key] = len(self.js["materials"]) - 1
        return self._materials[key]

    def _group(self, name: str) -> int:
        if name not in self._groups:
            self.js["nodes"].append({"name": name, "children": []})
            self._groups[name] = len(self.js["nodes"]) - 1
            self.js["nodes"][0]["children"].append(self._groups[name])
        return self._groups[name]

    def add_part(self, name: str, group: str, bodies, extras: dict, tol=0.5, ang=0.3) -> int:
        prims = []
        for shape, rgba in bodies:
            p, n, i = tessellate(shape, tol, ang)
            if not len(i):
                continue
            p = (p @ VCS_TO_GLTF.T).astype(np.float32)
            n = (n @ (VCS_TO_GLTF.T / 0.001)).astype(np.float32)
            prims.append({"attributes": {"POSITION": self._accessor(p, 5126, "VEC3", 34962, True),
                                         "NORMAL": self._accessor(n, 5126, "VEC3", 34962, False)},
                          "indices": self._accessor(i.astype(np.uint32).reshape(-1, 1), 5125,
                                                    "SCALAR", 34963, False),
                          "material": self._material(rgba), "mode": 4})
        self.js["meshes"].append({"name": name, "primitives": prims})
        self.js["nodes"].append({"name": name, "mesh": len(self.js["meshes"]) - 1, "extras": extras})
        node = len(self.js["nodes"]) - 1
        self.js["nodes"][self._group(group)]["children"].append(node)
        return node

    def write(self, path) -> None:
        while len(self.bin) % 4:
            self.bin.append(0)
        self.js["buffers"][0]["byteLength"] = len(self.bin)
        j = json.dumps(self.js, separators=(",", ":")).encode()
        j += b" " * ((4 - len(j) % 4) % 4)
        total = 12 + 8 + len(j) + 8 + len(self.bin)
        with open(path, "wb") as f:
            f.write(struct.pack("<4sII", b"glTF", 2, total))
            f.write(struct.pack("<II", len(j), 0x4E4F534A) + j)
            f.write(struct.pack("<II", len(self.bin), 0x004E4942) + bytes(self.bin))
