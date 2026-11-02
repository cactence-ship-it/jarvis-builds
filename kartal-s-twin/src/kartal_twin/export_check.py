"""Independent re-open checks for exported meshes (STL, GLB).

Pure numpy - deliberately does NOT use the CAD kernel that wrote the file, so a
broken exporter cannot hide its own errors. Used by the toolchain tests now and by
the Phase 11 export pipeline later.
"""
from __future__ import annotations

import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# glTF target frame (D-003): glTF (x, y, z) = VCS (-Y, Z, -X) * 0.001  [VCS mm -> glTF m].
# Vehicle front faces glTF +Z, up is glTF +Y. Proper rotation (det = +1).
VCS_TO_GLTF = np.array([[0.0, -1.0, 0.0],
                        [0.0, 0.0, 1.0],
                        [-1.0, 0.0, 0.0]]) * 0.001


@dataclass
class MeshReport:
    triangles: int
    vertices: int
    bbox_min: np.ndarray
    bbox_max: np.ndarray
    volume: float              # signed; > 0 means outward-facing winding
    boundary_edges: int        # edges used by one triangle  -> holes
    nonmanifold_edges: int     # edges used by > 2 triangles
    flipped_edges: int         # directed edge used twice   -> inconsistent winding
    degenerate: int            # zero-area / collapsed triangles

    @property
    def size(self) -> np.ndarray:
        return self.bbox_max - self.bbox_min

    @property
    def watertight(self) -> bool:
        return self.boundary_edges == 0 and self.nonmanifold_edges == 0

    @property
    def consistent_winding(self) -> bool:
        return self.flipped_edges == 0


def analyse_triangles(tri: np.ndarray, weld_tol: float) -> MeshReport:
    """Topology and volume of a triangle soup (n, 3, 3), welding vertices within weld_tol."""
    tri = np.asarray(tri, dtype=np.float64).reshape(-1, 3, 3)
    pts = tri.reshape(-1, 3)
    q = np.round(pts / weld_tol).astype(np.int64)
    uniq, inv = np.unique(q, axis=0, return_inverse=True)
    f = np.asarray(inv).reshape(-1, 3)
    bad = (f[:, 0] == f[:, 1]) | (f[:, 1] == f[:, 2]) | (f[:, 0] == f[:, 2])
    g = f[~bad]
    directed = np.concatenate([g[:, [0, 1]], g[:, [1, 2]], g[:, [2, 0]]])
    _, ucount = np.unique(np.sort(directed, axis=1), axis=0, return_counts=True)
    _, dcount = np.unique(directed, axis=0, return_counts=True)
    vol = float(np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6.0)
    return MeshReport(len(tri), len(uniq), pts.min(0), pts.max(0), vol,
                      int((ucount == 1).sum()), int((ucount > 2).sum()),
                      int((dcount > 1).sum()), int(bad.sum()))


def read_stl(path) -> tuple[np.ndarray, np.ndarray]:
    """Return (triangles (n,3,3), stored facet normals (n,3)) from binary or ASCII STL."""
    data = Path(path).read_bytes()
    if len(data) >= 84:
        n = struct.unpack_from("<I", data, 80)[0]
        if 84 + 50 * n == len(data):
            rec = np.frombuffer(data, offset=84, count=n, dtype=np.dtype(
                [("n", "<f4", (3,)), ("v", "<f4", (3, 3)), ("attr", "<u2")]))
            return rec["v"].astype(np.float64), rec["n"].astype(np.float64)
    text = data.decode("ascii")
    if not text.lstrip().startswith("solid"):
        raise ValueError(f"{path}: not an STL file")
    num = r"([-+0-9.eE]+)"
    v = np.array(re.findall(rf"vertex\s+{num}\s+{num}\s+{num}", text), float).reshape(-1, 3, 3)
    n = np.array(re.findall(rf"facet\s+normal\s+{num}\s+{num}\s+{num}", text), float)
    return v, n


def stl_normal_flips(tri: np.ndarray, normals: np.ndarray) -> int:
    """Count facets whose stored normal points against the winding-derived normal."""
    c = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ok = (np.linalg.norm(c, axis=1) > 0) & (np.linalg.norm(normals, axis=1) > 0)
    return int((np.einsum("ij,ij->i", c[ok], normals[ok]) < 0).sum())


_COMPONENT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16,
              5125: np.uint32, 5126: np.float32}
_NCOMP = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def _node_matrix(node: dict) -> np.ndarray:
    if "matrix" in node:
        return np.array(node["matrix"], float).reshape(4, 4).T     # glTF is column-major
    x, y, z, w = node.get("rotation", [0, 0, 0, 1])
    r = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    m = np.eye(4)
    m[:3, :3] = r * np.array(node.get("scale", [1, 1, 1]), float)
    m[:3, 3] = node.get("translation", [0, 0, 0])
    return m


def read_glb(path) -> tuple[dict, np.ndarray, list[str]]:
    """Parse a GLB; return (json, world-space triangles (n,3,3), structural issues)."""
    data = Path(path).read_bytes()
    issues: list[str] = []
    magic, version, length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF":
        raise ValueError(f"{path}: not a GLB file")
    if version != 2:
        issues.append(f"glTF version {version} != 2")
    if length != len(data):
        issues.append(f"header length {length} != file size {len(data)}")
    off, js, binary = 12, None, b""
    while off + 8 <= len(data):
        clen, ctype = struct.unpack_from("<II", data, off)
        chunk = data[off + 8: off + 8 + clen]
        off += 8 + clen
        if ctype == 0x4E4F534A:
            js = json.loads(chunk)
        elif ctype == 0x004E4942:
            binary = chunk
    if js is None:
        raise ValueError(f"{path}: no JSON chunk")

    def accessor(i: int) -> np.ndarray:
        a = js["accessors"][i]
        bv = js["bufferViews"][a["bufferView"]]
        dt, k = np.dtype(_COMPONENT[a["componentType"]]), _NCOMP[a["type"]]
        if bv.get("byteStride", 0) not in (0, dt.itemsize * k):
            raise NotImplementedError("interleaved vertex buffers")
        start = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        return np.frombuffer(binary, dtype=dt, count=a["count"] * k, offset=start).reshape(a["count"], k)

    tris: list[np.ndarray] = []

    def walk(ni: int, parent: np.ndarray):
        node = js["nodes"][ni]
        m = parent @ _node_matrix(node)
        if "mesh" in node:
            for prim in js["meshes"][node["mesh"]]["primitives"]:
                if prim.get("mode", 4) != 4:
                    issues.append(f"mesh {node['mesh']}: primitive mode {prim.get('mode')} is not triangles")
                    continue
                ai = prim["attributes"]["POSITION"]
                pos = accessor(ai).astype(np.float64)
                acc = js["accessors"][ai]
                if "min" not in acc or "max" not in acc:
                    issues.append(f"accessor {ai}: POSITION without min/max")
                elif not (np.allclose(pos.min(0), acc["min"], atol=1e-6) and
                          np.allclose(pos.max(0), acc["max"], atol=1e-6)):
                    issues.append(f"accessor {ai}: POSITION min/max do not match data")
                idx = accessor(prim["indices"]).reshape(-1) if "indices" in prim else np.arange(len(pos))
                if len(idx) % 3 or (len(idx) and idx.max() >= len(pos)):
                    issues.append(f"accessor {ai}: bad triangle indices")
                    continue
                world = (np.c_[pos, np.ones(len(pos))] @ m.T)[:, :3]
                tris.append(world[idx.reshape(-1, 3)])
        for child in node.get("children", []):
            walk(child, m)

    for root in js["scenes"][js.get("scene", 0)]["nodes"]:
        walk(root, np.eye(4))
    return js, (np.concatenate(tris) if tris else np.zeros((0, 3, 3))), issues
