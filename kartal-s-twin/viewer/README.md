# Android 3D viewer

`index.html` is the source. `python tools/package_viewer.py` embeds `build/vehicle.glb`
(base64) into the single file `build/viewer/kartal_viewer.html`, which is what gets published
as the artifact (the artifact host does not serve `.glb` files).

Features: orbit / zoom / pan (touch), Iso / Front / Rear / Left / Right / Top views,
exploded-view slider, per-assembly visibility, material vs evidence-status colouring
(PLACEHOLDER / DRAFT / VALIDATED), and tap-to-inspect (component ID, name, assembly,
geometry status, and every parameter with its provenance).

Test: `bash tools/viewer_smoke/run.sh` (headless Chromium; result in `test-results/viewer_smoke.txt`).
Published: https://claude.ai/artifact/7hGubrkeaHVUZSJ4AeGchk (private to the owner).
