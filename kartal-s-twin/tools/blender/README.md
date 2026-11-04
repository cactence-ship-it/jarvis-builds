# Realistic visual model (Blender) - D-028

Visual only. Not engineering geometry, not measured shape. Every size is read through the
Resolver (`export_params.py`), so owner measurements flow in automatically; the shape between
those values is a visual estimate from the owner's photos (E-026).

## Setup (once per container; not part of `requirements.lock`, not in CI)
bpy wheels need Python 3.11, so it lives in its own venv, outside the repository:

    uv venv -p 3.11 /tmp/bpyenv
    uv pip install -p /tmp/bpyenv/bin/python "bpy==4.2.*"

## Build (about 1.5 min on CPU)
    .venv/bin/python tools/blender/export_params.py            # -> build/blender/params.json
    /tmp/bpyenv/bin/python tools/blender/kartal_body.py \
        build/blender/params.json build/blender/kartal_studio.glb build/blender/preview.png
    .venv/bin/python tools/blender/package_studio.py           # -> build/viewer/kartal_studio{,_fragment}.html
    bash tools/blender/smoke_studio.sh                         # headless Chromium, phone viewport

`smoke_studio.sh` fails on any console error or fewer than 50 meshes and writes
`build/renders/studio_{front,side,rear}.png`. Published page: https://claude.ai/artifact/9D8o5byLmjc6xJ6ba2BzVR
