#!/usr/bin/env bash
# Studio renders (build/renders/*.png) from the packaged viewer in headless Chromium.
#   python tools/package_viewer.py && bash tools/render_studio.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
W="${TMPDIR:-/tmp}/kartal_viewer_smoke"; mkdir -p "$W/site" "$ROOT/build/renders"; cd "$W"
[[ -d node_modules/three ]] || npm install --silent three@0.147.0 >/dev/null
sed -e 's#https://cdn.jsdelivr.net/npm/three@0.147.0/#/node_modules/three/#g' -e '/fonts.googleapis/d' \
  "$ROOT/build/viewer/kartal_viewer.html" | { echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">'; cat; } > site/index.html
ln -sfn ../node_modules site/node_modules
cp "$ROOT/tools/viewer_smoke/studio.js" .
PORT=$(( 20000 + RANDOM % 20000 ))
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory site >/dev/null 2>&1 & srv=$!
trap 'kill $srv 2>/dev/null || true' EXIT
for _ in $(seq 1 60); do curl -sf -o /dev/null "http://127.0.0.1:$PORT/index.html" && break; sleep 0.5; done
OUT="$ROOT/build/renders" PORT=$PORT NODE_PATH="${NODE_PATH:-/opt/node22/lib/node_modules}" node studio.js
