#!/usr/bin/env bash
# Fit generated GLB parts with tools/meshfit and check viewer/tripo.html in headless Chromium.
#   bash tools/viewer_smoke/tripo.sh [GLB_DIR] [PARTS_JSON]
# Defaults: refs/derived/tripo and assembly/tripo_parts.json. With --self-test, the twin's own
# build/vehicle.glb stands in for a whole-car Tripo mesh (it must fit with ~0 % deviation).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
W="${TMPDIR:-/tmp}/kartal_tripo_smoke"; rm -rf "$W/site"; mkdir -p "$W/site/parts"
DIR="${1:-refs/derived/tripo}"
if [[ -n "${2:-}" ]]; then PARTS="$2"
elif [[ -f "$DIR/body.glb" && ! -f "$DIR/car.glb" ]]; then PARTS=assembly/tripo_parts_split.json
else PARTS=assembly/tripo_parts.json; fi
if [[ "${1:-}" == "--self-test" ]]; then
  [[ -f build/vehicle.glb ]] || { echo "build/vehicle.glb missing: run tools/twin.py build" >&2; exit 1; }
  DIR="$W/self"; mkdir -p "$DIR"; cp build/vehicle.glb "$DIR/car.glb"
  printf '{"parts":[{"id":"VIS-TRIPO-CAR","file":"car.glb","kind":"car","front":"+z"}]}\n' > "$W/self_parts.json"
  PARTS="$W/self_parts.json"
fi
.venv/bin/python tools/blender/export_params.py >/dev/null
cargo build -q --release --manifest-path tools/meshfit/Cargo.toml
set +e
tools/meshfit/target/release/meshfit fit --params build/blender/params.json --parts "$PARTS" --dir "$DIR" --out "$W/site/placements.json"
fit=$?
set -e
# 0 consistent, 1 warn, 3 a part missing: still viewable. 2 inconsistent: shown, then fail.
[[ $fit -eq 0 || $fit -eq 1 || $fit -eq 2 || $fit -eq 3 ]] || exit "$fit"
for g in "$DIR"/*.glb; do [[ -e "$g" ]] && cp "$g" "$W/site/parts/"; done
cd "$W"
[[ -d node_modules/three ]] || npm install --silent three@0.147.0 >/dev/null
sed -e 's#https://cdn.jsdelivr.net/npm/three@0.147.0/#/node_modules/three/#g' "$ROOT/viewer/tripo.html" > site/index.html
ln -sfn ../node_modules site/node_modules
cp "$ROOT/tools/viewer_smoke/tripo.js" .
PORT=$(( 20000 + RANDOM % 20000 ))
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory site >/dev/null 2>&1 & srv=$!
trap 'kill $srv 2>/dev/null || true' EXIT
for _ in $(seq 1 60); do curl -sf -o /dev/null "http://127.0.0.1:$PORT/index.html" && break; sleep 0.5; done
EXPECTED_INSTANCES=$(python3 -c "import json,sys; print(sum(len(p.get('instances',[])) for p in json.load(open(sys.argv[1]))['parts']))" site/placements.json)
OUT="$W" PORT=$PORT EXPECTED_INSTANCES=$EXPECTED_INSTANCES NODE_PATH="${NODE_PATH:-/opt/node22/lib/node_modules}" node tripo.js
echo "screenshots: $W/tripo_front.png $W/tripo_side.png $W/tripo_top.png"
[[ $fit -ne 2 ]] || { echo "an INCONSISTENT part was placed: regenerate it" >&2; exit 2; }
