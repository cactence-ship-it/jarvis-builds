#!/usr/bin/env python3
"""Analyse the owner's legacy 3D project archive (Kartal_S_Studyo.zip) - Phase 2.

    python3 tools/analyze_legacy.py refs/original/R-0001_Kartal_S_Studyo.zip

Reads the archive WITHOUT extracting or modifying it and writes
refs/derived/<name>_legacy_analysis.{json,md} (git-ignored: may describe private content).
For every object it reports: name, type, geometry kind and size, so we can decide what
is real geometry (reusable), what is procedural (rebuild parametrically) and what is
incomplete. Formats understood: three.js JSON (Object/Scene format 4), glTF JSON, and a
generic fallback that finds named object lists in any JSON. Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

PROCEDURAL = {"BoxGeometry", "BoxBufferGeometry", "CylinderGeometry", "CylinderBufferGeometry",
              "SphereGeometry", "SphereBufferGeometry", "ConeGeometry", "TorusGeometry",
              "PlaneGeometry", "PlaneBufferGeometry", "CircleGeometry", "RingGeometry",
              "CapsuleGeometry", "ExtrudeGeometry", "LatheGeometry", "ShapeGeometry",
              "TubeGeometry", "TorusKnotGeometry", "DodecahedronGeometry", "IcosahedronGeometry",
              "OctahedronGeometry", "TetrahedronGeometry", "EdgesGeometry", "WireframeGeometry"}


def _bbox(flat):
    xs, ys, zs = flat[0::3], flat[1::3], flat[2::3]
    if not xs:
        return None
    return [[min(xs), min(ys), min(zs)], [max(xs), max(ys), max(zs)]]


def analyse_threejs(doc: dict) -> dict:
    geos = {}
    for g in doc.get("geometries", []):
        t = g.get("type", "?")
        info = {"type": t}
        if t in PROCEDURAL:
            info["kind"] = "PROCEDURAL"
            info["params"] = {k: v for k, v in g.items() if k not in ("uuid", "type", "shapes", "options")}
        else:
            pos = (((g.get("data") or {}).get("attributes") or {}).get("position") or {}).get("array")
            if pos:
                info.update(kind="MESH", vertices=len(pos) // 3, bbox=_bbox(pos),
                            indexed=bool((g.get("data") or {}).get("index")))
            else:
                info["kind"] = "EMPTY_OR_UNKNOWN"
        geos[g.get("uuid")] = info
    objects = []

    def walk(o, path):
        name = o.get("name") or o.get("type", "?")
        p = f"{path}/{name}"
        g = geos.get(o.get("geometry"))
        objects.append({"path": p, "name": o.get("name", ""), "type": o.get("type"),
                        "geometry": g, "has_matrix": "matrix" in o})
        for c in o.get("children", []):
            walk(c, p)

    if "object" in doc:
        walk(doc["object"], "")
    return {"format": "three.js JSON", "geometries": len(geos), "objects": objects}


def analyse_gltf(doc: dict) -> dict:
    objects = []
    for i, n in enumerate(doc.get("nodes", [])):
        m = doc["meshes"][n["mesh"]] if "mesh" in n else None
        objects.append({"path": f"/node{i}", "name": n.get("name", ""), "type": "Mesh" if m else "Node",
                        "geometry": {"kind": "MESH", "primitives": len(m["primitives"])} if m else None})
    return {"format": "glTF JSON", "geometries": len(doc.get("meshes", [])), "objects": objects}


def analyse_generic(doc) -> dict:
    found = []

    def walk(x, path):
        if isinstance(x, list) and x and all(isinstance(i, dict) for i in x) and any("name" in i for i in x):
            found.append({"path": path, "count": len(x), "keys": sorted({k for i in x for k in i})[:20],
                          "names": [i.get("name") for i in x][:200]})
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{path}/{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x[:50]):
                walk(v, f"{path}[{i}]")

    walk(doc, "")
    return {"format": "generic JSON", "named_lists": found,
            "top_level_keys": list(doc)[:50] if isinstance(doc, dict) else type(doc).__name__}


def analyse_json(text: str) -> dict:
    doc = json.loads(text)
    if isinstance(doc, dict) and (doc.get("metadata") or {}).get("type") in ("Object", "Scene") \
            or (isinstance(doc, dict) and "object" in doc and "geometries" in doc):
        return analyse_threejs(doc)
    if isinstance(doc, dict) and "asset" in doc and "nodes" in doc:
        return analyse_gltf(doc)
    return analyse_generic(doc)


def analyse_html(text: str) -> dict:
    return {
        "bytes": len(text.encode()),
        "script_sources": re.findall(r"<script[^>]+src=[\"']([^\"']+)", text)[:30],
        "threejs_procedural_calls": dict(sorted(
            {g: len(re.findall(rf"new\s+THREE\.{g}\s*\(", text)) for g in PROCEDURAL}.items())),
        "embedded_images": len(re.findall(r"data:image/", text)),
        "embedded_json_blocks": len(re.findall(r"<script[^>]+type=[\"']application/json", text)),
        "mentions_kartal_json": "kartal.json" in text,
    }


def analyse_zip(path: Path) -> dict:
    rep = {"archive": path.name, "members": [], "json": {}, "html": {}, "warnings": []}
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            rep["warnings"].append(f"corrupt member: {bad}")
        for i in z.infolist():
            rep["members"].append({"name": i.filename, "bytes": i.file_size})
            low = i.filename.lower()
            if low.endswith(".json"):
                try:
                    rep["json"][i.filename] = analyse_json(z.read(i).decode("utf-8"))
                except (ValueError, UnicodeDecodeError) as e:
                    rep["json"][i.filename] = {"error": str(e)[:200]}
            elif low.endswith((".html", ".htm")):
                rep["html"][i.filename] = analyse_html(z.read(i).decode("utf-8", errors="replace"))
    for name, h in rep["html"].items():
        if h["embedded_images"]:
            rep["warnings"].append(f"{name}: {h['embedded_images']} embedded image(s) - may be private photos; "
                                   "never publish this file")
    return rep


def summary(rep: dict) -> dict:
    kinds: dict[str, int] = {}
    n = 0
    for j in rep["json"].values():
        for o in j.get("objects", []):
            n += 1
            k = (o.get("geometry") or {}).get("kind", "NO_GEOMETRY")
            kinds[k] = kinds.get(k, 0) + 1
    return {"objects": n, "by_geometry_kind": kinds,
            "procedural_calls_in_html": sum(sum(h["threejs_procedural_calls"].values()) for h in rep["html"].values())}


def to_markdown(rep: dict) -> str:
    s = summary(rep)
    lines = [f"# Legacy archive analysis: {rep['archive']}", "",
             f"Objects: **{s['objects']}** - by geometry kind: {s['by_geometry_kind']}. "
             f"Procedural constructor calls in HTML: {s['procedural_calls_in_html']}.", ""]
    lines += [f"- WARNING: {w}" for w in rep["warnings"]]
    lines += ["", "| Path | Type | Geometry | Detail |", "|---|---|---|---|"]
    for j in rep["json"].values():
        for o in j.get("objects", []):
            g = o.get("geometry") or {}
            detail = g.get("vertices") or g.get("params") or g.get("primitives") or ""
            lines.append(f"| {o['path']} | {o.get('type')} | {g.get('kind', '-')} {g.get('type', '')} | {str(detail)[:80]} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    rep = analyse_zip(src)
    rep["summary"] = summary(rep)
    out = Path(__file__).resolve().parents[1] / "refs" / "derived"
    out.mkdir(parents=True, exist_ok=True)
    stem = src.stem
    (out / f"{stem}_legacy_analysis.json").write_text(json.dumps(rep, indent=2))
    (out / f"{stem}_legacy_analysis.md").write_text(to_markdown(rep))
    print(json.dumps(rep["summary"]), "| warnings:", rep["warnings"] or "none")
    print(f"report: refs/derived/{stem}_legacy_analysis.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
