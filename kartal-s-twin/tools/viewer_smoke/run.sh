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
npx --yes http-server site -p 8765 -s >/dev/null 2>&1 & srv=$!
trap 'kill $srv 2>/dev/null || true' EXIT
sleep 2
NODE_PATH=/opt/node22/lib/node_modules node smoke.js
echo "screenshots: $W/iso.png $W/exploded.png"
