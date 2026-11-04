#!/usr/bin/env bash
# Headless Chromium check + phone screenshots of build/viewer/kartal_studio.html.
#   python tools/blender/package_studio.py && bash tools/blender/smoke_studio.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
W="${TMPDIR:-/tmp}/kartal_viewer_smoke"; mkdir -p "$W/site2" "$ROOT/build/renders"; cd "$W"
[[ -d node_modules/three ]] || npm install --silent three@0.147.0 >/dev/null
sed -e 's#https://cdn.jsdelivr.net/npm/three@0.147.0/#/node_modules/three/#g' \
  "$ROOT/build/viewer/kartal_studio.html" > site2/index.html
ln -sfn ../node_modules site2/node_modules
cp "$ROOT/tools/viewer_smoke/studio_glb.js" .
PORT=$(( 20000 + RANDOM % 20000 ))
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory site2 >/dev/null 2>&1 & srv=$!
trap 'kill $srv 2>/dev/null || true' EXIT
for _ in $(seq 1 60); do curl -sf -o /dev/null "http://127.0.0.1:$PORT/index.html" && break; sleep 0.5; done
OUT="$ROOT/build/renders" PORT=$PORT NODE_PATH="${NODE_PATH:-/opt/node22/lib/node_modules}" node studio_glb.js
