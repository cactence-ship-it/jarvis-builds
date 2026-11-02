#!/usr/bin/env bash
# Reproducible environment setup for the Kartal S digital twin.
#
#   bash scripts/setup_env.sh            # create/refresh .venv from requirements.lock
#   bash scripts/setup_env.sh --force    # rebuild even if the lock is unchanged
#   bash scripts/setup_env.sh --check    # verify only, install nothing (exit 1 if not ready)
#
# Idempotent: when .venv already matches the SHA-256 of requirements.lock it installs
# nothing, so it is safe (and cheap) to run at the start of every cloud session.
# Every install is hash-checked against requirements.lock (--require-hashes).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${KARTAL_VENV:-$ROOT/.venv}"
LOCK="$ROOT/requirements.lock"
STAMP="$VENV/.lock.sha256"
PY_REQUIRED="3.13"
MODE="${1:-}"

want="$(sha256sum "$LOCK" | cut -d' ' -f1)"
have="$(cat "$STAMP" 2>/dev/null || true)"

if [[ -x "$VENV/bin/python" && "$have" == "$want" && "$MODE" != "--force" ]]; then
  echo "[setup] environment already matches requirements.lock (${want:0:12}) - nothing installed"
elif [[ "$MODE" == "--check" ]]; then
  echo "[setup] NOT READY: .venv missing or out of date - run: bash scripts/setup_env.sh" >&2
  exit 1
else
  PY="${PYTHON:-python3}"
  ver="$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
  if [[ "$ver" != "$PY_REQUIRED" ]]; then
    echo "[setup] ERROR: requirements.lock is compiled for Python $PY_REQUIRED, but $PY is $ver" >&2
    exit 1
  fi
  t0=$SECONDS
  if command -v uv >/dev/null 2>&1; then
    echo "[setup] installing with uv into $VENV"
    [[ -x "$VENV/bin/python" ]] || uv venv --quiet --python "$PY" "$VENV"
    uv pip sync --quiet --require-hashes --python "$VENV/bin/python" "$LOCK"
  else
    echo "[setup] uv not found - installing with pip into $VENV"
    [[ -x "$VENV/bin/python" ]] || "$PY" -m venv "$VENV"
    "$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --require-hashes -r "$LOCK"
  fi
  echo "$want" > "$STAMP"
  echo "[setup] installed in $((SECONDS - t0)) s"
fi

# Import check: proves the CAD kernel loads (not just that files were copied).
"$VENV/bin/python" - <<'EOF'
import importlib.metadata as md, sys
import build123d, OCP, yaml, numpy
print(f"[setup] OK  python {sys.version.split()[0]} | build123d {md.version('build123d')} | "
      f"OCP/OpenCascade binding {OCP.__version__} | "
      f"numpy {numpy.__version__} | pyyaml {yaml.__version__}")
EOF
