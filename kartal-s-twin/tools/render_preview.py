#!/usr/bin/env python3
"""Render PNG previews of the built vehicle (no GPU, no extra dependencies).

    python tools/render_preview.py            -> build/previews/{iso,side,front,rear,top}.png + sheet.png

Orthographic painter's-algorithm renderer on Pillow: good enough for visual QA and for
sending previews to Android. Not a photorealistic renderer.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kartal_twin.gltf_writer import tessellate  # noqa: E402
from kartal_twin.pipeline import BUILD_DIR, build_parts  # noqa: E402

VIEWS = {  # camera direction (from eye towards the car) in VCS, up vector
    "iso": (np.array([1.0, 1.3, -0.7]), np.array([0, 0, 1.0])),   # front-left, above
    "side": (np.array([0, 1.0, 0]), np.array([0, 0, 1.0])),       # from the left (LH = -Y)
    "front": (np.array([1.0, 0, 0]), np.array([0, 0, 1.0])),      # front is -X
    "rear": (np.array([-1.0, 0, 0]), np.array([0, 0, 1.0])),
    "top": (np.array([0, 0, -1.0]), np.array([-1.0, 0, 0])),
}


def collect():
    parts, _ = build_parts()
    tris, cols = [], []
    for p in parts:
        for shape, rgba in p.bodies:
            pos, _, idx = tessellate(shape, 1.0, 0.4)
            t = pos[idx]
            tris.append(t)
            cols.append(np.repeat([rgba], len(t), axis=0))
    return np.concatenate(tris), np.concatenate(cols)


def render(tris, cols, view, size=(1200, 760)):
    d, up = VIEWS[view]
    d = d / np.linalg.norm(d)
    right = np.cross(d, up); right /= np.linalg.norm(right)
    up2 = np.cross(right, d)
    c = tris.reshape(-1, 3).mean(0)
    p = tris - c
    sx, sy, depth = p @ right, p @ up2, p @ d
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    nl = np.linalg.norm(n, axis=1); n = n / np.where(nl > 0, nl, 1)[:, None]
    facing = (n @ d) < 0
    light = np.array([0.4, 0.7, 0.6]) * -1 + d * -0.3
    light /= np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(-(n @ light), 0, 1)
    span = max(np.ptp(sx), np.ptp(sy) * size[0] / size[1])
    k = 0.9 * size[0] / span
    X = size[0] / 2 + sx * k
    Y = size[1] / 2 - sy * k
    img = Image.new("RGB", size, (245, 246, 248))
    dr = ImageDraw.Draw(img, "RGBA")
    order = np.argsort(depth.mean(1))[::-1]           # far to near
    opaque = cols[:, 3] >= 1.0
    order = np.concatenate([order[opaque[order]], order[~opaque[order]]])  # glass last
    for i in order:
        if not facing[i]:
            continue
        r, g, b, a = cols[i]
        s = shade[i]
        fill = (int(255 * r * s), int(255 * g * s), int(255 * b * s), int(255 * a))
        dr.polygon(list(zip(X[i], Y[i])), fill=fill)
    dr.text((12, 10), f"VEH-01 PLACEHOLDER envelope - {view} - not the real car shape", fill=(60, 60, 60))
    return img


def main():
    out = BUILD_DIR / "previews"
    out.mkdir(parents=True, exist_ok=True)
    tris, cols = collect()
    imgs = {}
    for v in VIEWS:
        imgs[v] = render(tris, cols, v)
        imgs[v].save(out / f"{v}.png")
    w, h = imgs["iso"].size
    sheet = Image.new("RGB", (w, h * 2 + h // 2), (255, 255, 255))
    sheet.paste(imgs["iso"], (0, 0))
    sheet.paste(imgs["side"].resize((w // 2, h // 2)), (0, h))
    sheet.paste(imgs["front"].resize((w // 2, h // 2)), (w // 2, h))
    sheet.paste(imgs["rear"].resize((w // 2, h // 2)), (0, h + h // 2))
    sheet.paste(imgs["top"].resize((w // 2, h // 2)), (w // 2, h + h // 2))
    sheet.save(out / "sheet.png")
    print(f"wrote {len(imgs) + 1} previews to {out}")


if __name__ == "__main__":
    main()
