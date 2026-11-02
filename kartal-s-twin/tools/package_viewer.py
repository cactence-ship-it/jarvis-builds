#!/usr/bin/env python3
"""Package the Android viewer as ONE self-contained HTML file with the GLB embedded.

    python tools/package_viewer.py   -> build/viewer/kartal_viewer.html

The GLB is generated CAD geometry (no photos, no personal data), so the packaged page
is safe to publish. Re-run after every `twin.py build`.
"""
import base64
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    glb = ROOT / "build" / "vehicle.glb"
    if not glb.exists():
        sys.exit("build/vehicle.glb missing - run: python tools/twin.py build")
    data = glb.read_bytes()
    page = (ROOT / "viewer" / "index.html").read_text(encoding="utf-8")
    blob = base64.b64encode(data).decode()
    tag = f'<script type="application/octet-stream" id="glb-data">{blob}</script>\n'
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
