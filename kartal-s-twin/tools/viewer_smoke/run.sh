#!/usr/bin/env bash
# Headless-Chromium functional test of the packaged viewer (build/viewer/kartal_viewer.html).
# The cloud network blocks the jsDelivr CDN, so three.js@0.147.0 is fetched from npm and the
# CDN URLs are rewritten to it. Checks: model loads, assemblies listed, tap-to-inspect,
# view / explode / status colouring controls, zero console errors. Writes screenshots.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
W="${TMPDIR:-/tmp}/kartal_viewer_smoke"; mkdir -p "$W/site"; cd "$W"
[[ -d node_modules/three ]] || npm install --silent three@0.147.0 >/dev/null
sed -e 's#https://cdn.jsdelivr.net/npm/three@0.147.0/#/node_modules/three/#g' -e '/fonts.googleapis/d' \
  "$ROOT/build/viewer/kartal_viewer.html" | { echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">'; cat; } > site/index.html
ln -sfn ../node_modules site/node_modules
cp "$ROOT/tools/viewer_smoke/smoke.js" .
PORT=$(( 20000 + RANDOM % 20000 ))
# python3's built-in server: nothing to download (npx http-server needed a download on fresh
# CI runners and was not listening yet after a fixed 2 s sleep -> ERR_CONNECTION_REFUSED).
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory site >/dev/null 2>&1 & srv=$!
trap 'kill $srv 2>/dev/null || true' EXIT
for _ in $(seq 1 60); do        # wait until the port really answers (max 30 s)
  curl -sf -o /dev/null "http://127.0.0.1:$PORT/index.html" && break
  sleep 0.5
done
curl -sf -o /dev/null "http://127.0.0.1:$PORT/index.html" || { echo "viewer test server did not start" >&2; exit 1; }
EXPECTED_PARTS=$(python3 -c "import json,sys; print(sum(1 for x in json.load(open(sys.argv[1]))['parts'] if x['representation'] == 'visual'))" "$ROOT/build/manifest.json") \
  PORT=$PORT NODE_PATH="${NODE_PATH:-/opt/node22/lib/node_modules}" node smoke.js
echo "screenshots: $W/iso.png $W/exploded.png"
