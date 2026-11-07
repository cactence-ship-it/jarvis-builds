#!/usr/bin/env python3
"""Package the Android viewer as ONE self-contained HTML file with the GLB embedded.

    python tools/package_viewer.py   -> build/viewer/kartal_viewer.html
    python tools/package_viewer.py --shell refs/derived/tripo/car_web.glb --place build/tripo/placements.json
        also embeds the photo-based Tripo exterior shell (visual estimate, D-030..D-032).
        The shell texture is made from owner photos: the output stays in build/ (git-ignored)
        and is published only privately, by owner decision.

The GLB is generated CAD geometry (no photos, no personal data), so the packaged page
is safe to publish. Re-run after every `twin.py build`.
"""
import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


CLOSURE_LABELS = {"BDY-008": ("door", "Sol ön kapı"), "BDY-009": ("door", "Sağ ön kapı"),
                  "BDY-010": ("door", "Sol arka kapı"), "BDY-011": ("door", "Sağ arka kapı"),
                  "BDY-003": ("hood", "Kaput"), "BDY-012": ("tailgate", "Bagaj kapağı")}


def closure_map() -> dict:
    """Which components move with each closure, from vehicle_master.yaml dependencies.
    A component moves only if ALL its dependencies move (a set shared by several doors stays)."""
    master = yaml.safe_load((ROOT / "assembly" / "vehicle_master.yaml").read_text(encoding="utf-8"))
    deps = {}
    def walk(o):
        if isinstance(o, dict):
            if "id" in o and "dependencies" in o:
                deps[o["id"]] = list(o.get("dependencies") or [])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(master)
    out = {}
    for cid, (kind, label) in CLOSURE_LABELS.items():
        moving = {cid}
        changed = True
        while changed:
            changed = False
            for pid, ds in deps.items():
                if ds and all(d in moving for d in ds) and pid not in moving:
                    moving.add(pid)
                    changed = True
        out[cid] = {"kind": kind, "label": label, "deps": sorted(moving - {cid})}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shell", type=Path, help="photo-based exterior GLB (visual estimate)")
    ap.add_argument("--place", type=Path, help="meshfit placements.json for the shell")
    ap.add_argument("--skins", type=Path, help="interior skin config (assembly/tripo_interior.json)")
    args = ap.parse_args()
    glb = ROOT / "build" / "vehicle.glb"
    if not glb.exists():
        sys.exit("build/vehicle.glb missing - run: python tools/twin.py build")
    data = glb.read_bytes()
    page = (ROOT / "viewer" / "index.html").read_text(encoding="utf-8")
    blob = base64.b64encode(data).decode()
    tag = f'<script type="application/octet-stream" id="glb-data">{blob}</script>\n'
    tag += f'<script type="application/json" id="closures-data">{json.dumps(closure_map())}</script>\n'
    if args.skins:
        cfg = json.loads(args.skins.read_text(encoding="utf-8"))
        skins = []
        for i, sk in enumerate(cfg["skins"]):
            f = ROOT / "refs" / "derived" / "tripo" / sk["file"]
            if not f.exists():
                print(f"skin {sk['file']} missing - skipped")
                continue
            tag += (f'<script type="application/octet-stream" id="skin-{i}">'
                    f'{base64.b64encode(f.read_bytes()).decode()}</script>\n')
            skins.append(dict(sk, tag=f"skin-{i}"))
        tag += f'<script type="application/json" id="skins-data">{json.dumps(skins)}</script>\n'
    if args.shell:
        place = json.loads(args.place.read_text(encoding="utf-8"))
        inst = next(p for p in place["parts"] if p["kind"] == "car")["instances"][0]
        shell = base64.b64encode(args.shell.read_bytes()).decode()
        tag += f'<script type="application/octet-stream" id="glb-shell">{shell}</script>\n'
        tag += f'<script type="application/json" id="shell-place">{json.dumps(inst)}</script>\n'
        lenses = json.loads((ROOT / "assembly" / "tripo_parts.json").read_text(encoding="utf-8")).get("lenses")
        if lenses:
            tag += f'<script type="application/json" id="lens-data">{json.dumps(lenses["items"])}</script>\n'
    marker = '<script src="https://cdn.jsdelivr.net/npm/three@'
    if marker not in page:
        sys.exit("viewer/index.html: three.js script tag not found")
    out = ROOT / "build" / "viewer" / "kartal_viewer.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page.replace(marker, tag + marker, 1), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes, glb sha256 "
          f"{hashlib.sha256(data).hexdigest()[:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
