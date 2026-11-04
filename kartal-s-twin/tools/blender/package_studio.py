#!/usr/bin/env python3
"""Embed build/blender/kartal_studio.glb into viewer/studio.html.

Writes two files:
  build/viewer/kartal_studio.html           standalone page (opens directly in a browser)
  build/viewer/kartal_studio_fragment.html  same page without doctype/html/head/body tags, for
                                            hosts that wrap the content in their own skeleton
"""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
glb = (ROOT / "build" / "blender" / "kartal_studio.glb").read_bytes()
html = (ROOT / "viewer" / "studio.html").read_text(encoding="utf-8")
tag = f'<script type="application/octet-stream" id="glb-data">{base64.b64encode(glb).decode()}</script>\n'
assert html.count("<script src=") >= 1, "studio.html has no library <script src=> to insert before"
page = html.replace("<script src=", tag + "<script src=", 1)

out = ROOT / "build" / "viewer" / "kartal_studio.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page, encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")

frag = re.sub(r"<!doctype html>\s*|</?html[^>]*>\s*|</?head>\s*|</?body>\s*|<meta (charset|name=\"viewport\")[^>]*>\s*",
              "", page, flags=re.I)
assert "<title>" in frag[:8192] and "<html" not in frag and "<body" not in frag
fout = out.with_name("kartal_studio_fragment.html")
fout.write_text(frag, encoding="utf-8")
print(f"wrote {fout.relative_to(ROOT)} ({fout.stat().st_size} bytes)")
