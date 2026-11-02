"""Build the VEHICLE_MASTER visual representation, export it and validate every export.

    python tools/twin.py build        -> build/{vehicle.step, vehicle.stl, vehicle.glb,
                                          assemblies/<ASSEMBLY>.glb, manifest.json}

No export is reported as good unless it was re-opened and checked (D-011).
"""
from __future__ import annotations

import hashlib
import importlib
import json
import time
from pathlib import Path

import build123d as bd
import numpy as np

from . import PROJECT_ROOT
from . import export_check as xc
from .assemblies import MODULES
from .cad.part import BuildContext, Part
from .gltf_writer import GlbBuilder
from .inventory import iter_components, load_assembly

BUILD_DIR = PROJECT_ROOT / "build"
# Fixed STEP header timestamp so identical geometry gives identical files (auditable SHA-256).
STEP_TIMESTAMP = "2000-01-01T00:00:00"
GENERATED = ("vehicle.step", "vehicle.stl", "vehicle.glb", "manifest.json")


def build_parts(representation: str = "visual") -> tuple[list[Part], list[str]]:
    ctx = BuildContext(representation=representation)
    skipped = []
    for name, modname in MODULES.items():
        mod = importlib.import_module(modname)
        fn = mod.build if representation == "visual" else getattr(mod, f"build_{representation}", None)
        if fn is None:
            skipped.append(name)
            continue
        try:
            fn(ctx)
        except NotImplementedError:
            skipped.append(name)
    return ctx.parts, skipped


def export_cad(parts: list[Part], out: Path) -> dict:
    """Engineering CAD: one STEP per component + one assembly STEP, each re-opened."""
    d = out / "cad"
    d.mkdir(parents=True, exist_ok=True)
    rep = {}
    children = []
    for p in parts:
        shape = p.bodies[0][0]
        shape.label = p.component_id
        children.append(shape)
        f = d / f"{p.component_id}.step"
        bd.export_step(shape, f, timestamp=STEP_TIMESTAMP)
        back = bd.import_step(f)
        rep[p.component_id] = {"file": str(f.relative_to(out)), "bytes": f.stat().st_size, "sha256": _sha(f),
                               "valid": back.is_valid, "volume_mm3": back.volume,
                               "volume_rel_error": abs(back.volume - shape.volume) / shape.volume,
                               "bbox_mm": [[round(v, 3) for v in (back.bounding_box().min.X, back.bounding_box().min.Y, back.bounding_box().min.Z)],
                                           [round(v, 3) for v in (back.bounding_box().max.X, back.bounding_box().max.Y, back.bounding_box().max.Z)]]}
    asm = d / "vehicle_cad.step"
    bd.export_step(bd.Compound(children=children, label="VEHICLE_MASTER_CAD"), asm, timestamp=STEP_TIMESTAMP)
    back = bd.import_step(asm)
    rep["_assembly"] = {"file": str(asm.relative_to(out)), "bytes": asm.stat().st_size, "sha256": _sha(asm),
                        "solids_written": len(children), "solids_read": len(back.solids()), "valid": back.is_valid}
    return rep


def check_parts(parts: list[Part]) -> list[str]:
    """Kernel-level checks before export."""
    inv = {c["id"]: (a, c) for a, _, c in iter_components(load_assembly())}
    errs, seen = [], set()
    for p in parts:
        if p.component_id in seen:
            errs.append(f"{p.component_id}: built twice")
        seen.add(p.component_id)
        if p.component_id not in inv:
            errs.append(f"{p.component_id}: not in inventory")
        elif inv[p.component_id][0] != p.assembly:
            errs.append(f"{p.component_id}: built by {p.assembly}, inventory says {inv[p.component_id][0]}")
        for i, (shape, _) in enumerate(p.bodies):
            if not shape.is_valid:
                errs.append(f"{p.component_id}[{i}]: invalid solid")
            if not shape.volume > 0:
                errs.append(f"{p.component_id}[{i}]: zero volume")
        if p.geometry_status != "PLACEHOLDER" and "PLACEHOLDER" in p.used.values():
            errs.append(f"{p.component_id}: uses placeholders but status is {p.geometry_status}")
    return errs


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export_all(parts: list[Part], out: Path = BUILD_DIR) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    (out / "assemblies").mkdir(exist_ok=True)
    names = {c["id"]: c["name"] for _, _, c in iter_components(load_assembly())}
    report: dict = {"files": {}, "checks": {}}

    # STEP - engineering exchange, one labelled solid per body
    children = []
    for p in parts:
        for i, (shape, rgba) in enumerate(p.bodies):
            s = shape if isinstance(shape, bd.Shape) else shape.solid()
            s.label = f"{p.component_id}" + (f"_{i}" if len(p.bodies) > 1 else "")
            s.color = bd.Color(*rgba)
            children.append(s)
    vehicle = bd.Compound(children=children, label="VEHICLE_MASTER")
    step = out / "vehicle.step"
    bd.export_step(vehicle, step, timestamp=STEP_TIMESTAMP)
    back = bd.import_step(step)
    vol_cad = sum(c.volume for c in children)
    report["checks"]["step"] = {
        "solids_written": len(children), "solids_read": len(back.solids()),
        "volume_rel_error": abs(back.volume - vol_cad) / vol_cad, "valid": back.is_valid}

    # STL - whole vehicle mesh
    stl = out / "vehicle.stl"
    bd.export_stl(vehicle, stl, tolerance=0.5, angular_tolerance=0.3)
    tri, normals = xc.read_stl(stl)
    rs = xc.analyse_triangles(tri, 1e-3)
    report["checks"]["stl"] = {"triangles": rs.triangles, "normal_flips": xc.stl_normal_flips(tri, normals),
                               "bbox_mm": [rs.bbox_min.round(1).tolist(), rs.bbox_max.round(1).tolist()]}

    # GLB - Android viewer, full vehicle + one per assembly
    def glb(path: Path, subset: list[Part]):
        g = GlbBuilder()
        for p in subset:
            g.add_part(p.component_id, p.assembly, p.bodies, {
                "id": p.component_id, "name": names.get(p.component_id, ""), "assembly": p.assembly,
                "representation": p.representation, "geometry_status": p.geometry_status,
                "parameters": p.used, "note": p.note})
        g.write(path)
        js, tris, issues = xc.read_glb(path)
        r = xc.analyse_triangles(tris, 1e-6)
        return {"triangles": r.triangles, "issues": issues, "bytes": path.stat().st_size,
                "bbox_m": [r.bbox_min.round(4).tolist(), r.bbox_max.round(4).tolist()]}

    report["checks"]["glb"] = glb(out / "vehicle.glb", parts)
    for asm in sorted({p.assembly for p in parts}):
        f = out / "assemblies" / f"{asm}.glb"
        report["checks"][f"glb:{asm}"] = glb(f, [p for p in parts if p.assembly == asm])

    # Per-body closed-mesh check on the GLB content (each body tessellated independently)
    open_bodies = []
    from .gltf_writer import tessellate
    for p in parts:
        for i, (shape, _) in enumerate(p.bodies):
            pos, _, idx = tessellate(shape)
            r = xc.analyse_triangles(pos[idx], 1e-3)
            if not (r.watertight and r.volume > 0):
                open_bodies.append(f"{p.component_id}[{i}]")
    report["checks"]["mesh_closed_outward"] = {"failed_bodies": open_bodies}

    return report


def _clean(out: Path) -> None:
    """Remove outputs of earlier runs so the manifest can only describe this run."""
    import shutil
    for name in GENERATED:
        (out / name).unlink(missing_ok=True)
    for sub in ("assemblies", "cad"):
        shutil.rmtree(out / sub, ignore_errors=True)


def _list_outputs(out: Path) -> dict:
    files = [out / n for n in GENERATED[:3]] + sorted((out / "assemblies").glob("*.glb")) \
        + sorted((out / "cad").glob("*.step"))
    return {str(f.relative_to(out)): {"bytes": f.stat().st_size, "sha256": _sha(f)} for f in files if f.exists()}


def run(out: Path = BUILD_DIR) -> dict:
    t0 = time.time()
    out.mkdir(parents=True, exist_ok=True)
    _clean(out)
    parts, skipped = build_parts()
    errors = check_parts(parts)
    report = export_all(parts, out) if not errors else {"files": {}, "checks": {}}
    cad_parts, _ = build_parts("cad")
    cad_errors = check_parts(cad_parts)
    errors += [f"cad: {e}" for e in cad_errors]
    if cad_parts and not cad_errors:
        report["checks"]["cad"] = export_cad(cad_parts, out)
    parts = parts + cad_parts
    report["files"] = _list_outputs(out)
    report.update({
        "errors": errors, "skipped_assemblies": skipped, "seconds": round(time.time() - t0, 1),
        "parts": [{"id": p.component_id, "assembly": p.assembly, "representation": p.representation,
                   "geometry_status": p.geometry_status, "parameters": p.used, "note": p.note}
                  for p in parts]})
    (out).mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps(report, indent=2, default=float))
    return report
