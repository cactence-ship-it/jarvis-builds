#!/usr/bin/env bash
# Save project progress to GitHub and PROVE it arrived.
#
#   bash scripts/checkpoint.sh "commit message"   validate -> commit -> push -> verify
#   bash scripts/checkpoint.sh --verify           verify only: local HEAD == origin/<branch>
#
# Refuses to commit if validation or the privacy scan fails, and refuses to run on main.
# "VERIFIED" is printed only when GitHub reports the same commit SHA as local HEAD.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" == "main" || "$BRANCH" == "HEAD" ]]; then
  echo "[checkpoint] refusing to run on '$BRANCH' - work on a feature branch" >&2
  exit 1
fi

if [[ "${1:-}" != "--verify" ]]; then
  MSG="${1:?usage: scripts/checkpoint.sh \"commit message\" | --verify}"
  PY="$ROOT/.venv/bin/python"; [[ -x "$PY" ]] || PY=python3
  "$PY" tools/twin.py validate
  "$PY" - <<'EOF'
import datetime, json, pathlib, secrets
p = pathlib.Path("persistence/checkpoint.json")
d = json.loads(p.read_text())
d.update(checkpoint=d.get("checkpoint", 0) + 1, nonce=secrets.token_hex(16),
         created_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
p.write_text(json.dumps(d, indent=2) + "\n")
print(f"[checkpoint] checkpoint #{d['checkpoint']} nonce {d['nonce']}")
EOF
  git add -A -- .
  git commit -q -m "$MSG"
  for delay in 0 2 4 8 16; do
    sleep "$delay"
    if git push -q -u origin "$BRANCH"; then break; fi
    echo "[checkpoint] push failed, retrying" >&2
  done
fi

local_sha="$(git rev-parse HEAD)"
remote_sha="$(git ls-remote origin "refs/heads/$BRANCH" | cut -f1)"
if [[ "$local_sha" == "$remote_sha" ]]; then
  echo "[checkpoint] VERIFIED: origin/$BRANCH == $local_sha"
else
  echo "[checkpoint] NOT VERIFIED: local $local_sha, origin/$BRANCH '${remote_sha:-missing}'" >&2
  exit 2
fi
