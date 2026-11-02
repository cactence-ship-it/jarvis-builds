#!/usr/bin/env bash
# Run validation + the full unit-test suite and RECORD the result in test-results/latest.txt.
# Exit code is non-zero if anything fails (used by scripts/checkpoint.sh as a commit gate).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
mkdir -p test-results
OUT=test-results/latest.txt
(
  echo "# Test run $(date -u +%Y-%m-%dT%H:%M:%SZ) on commit base $(git rev-parse --short HEAD)"
  echo "## validate"
  "$PY" tools/twin.py validate; v=$?
  echo "## unittest"
  "$PY" -m unittest discover -s tests -t . 2>&1; t=$?
  echo "## result: validate=$v unittest=$t"
  exit $(( v != 0 || t != 0 ))
) > "$OUT" 2>&1
rc=$?
tail -4 "$OUT"
exit $rc
