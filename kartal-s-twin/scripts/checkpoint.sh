#!/usr/bin/env bash
# Save project progress to GitHub and PROVE it arrived.
#
#   bash scripts/checkpoint.sh "commit message"   validate -> commit -> push -> verify
#   bash scripts/checkpoint.sh --wip "message"    emergency save: commits even if tests fail
#                                                 (privacy scan still mandatory), marked WIP
#   bash scripts/checkpoint.sh --verify           verify only: local HEAD == origin/<branch>
#
# Normal mode refuses to commit if validation, the privacy scan or any test fails.
# Every commit rewrites the AUTO-CHECKPOINT block in HANDOFF.md (parent commit, tests,
# changed files), so the hand-off record can never fall behind. Refuses to run on main.
# "VERIFIED" is printed only when GitHub reports the same commit SHA as local HEAD.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" == "main" || "$BRANCH" == "HEAD" ]]; then
  echo "[checkpoint] refusing to run on '$BRANCH' - work on a feature branch" >&2
  exit 1
fi

WIP=0
if [[ "${1:-}" == "--wip" ]]; then WIP=1; shift; fi
if [[ "${1:-}" != "--verify" ]]; then
  MSG="${1:?usage: scripts/checkpoint.sh [--wip] \"commit message\" | --verify}"
  PY="$ROOT/.venv/bin/python"; [[ -x "$PY" ]] || PY=python3
  "$PY" tools/twin.py privacy || { echo "[checkpoint] privacy scan FAILED - nothing committed" >&2; exit 1; }
  TESTS="not run (.venv missing)"
  if [[ -x "$ROOT/.venv/bin/python" ]]; then
    if bash scripts/run_tests.sh >/dev/null; then TESTS="PASS"; else TESTS="FAIL"; fi
    TESTS="$TESTS - $(grep -E '^Ran [0-9]+ tests' test-results/latest.txt | tail -1); $(tail -1 test-results/latest.txt)"
  fi
  if [[ $WIP -eq 0 ]]; then
    "$PY" tools/twin.py validate >/dev/null || { echo "[checkpoint] validation FAILED - nothing committed (use --wip to force a save)" >&2; exit 1; }
    [[ "$TESTS" == PASS* ]] || { echo "[checkpoint] tests FAILED - nothing committed (use --wip to force a save)" >&2; exit 1; }
  else
    MSG="WIP: $MSG"
  fi
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
  PARENT="$(git rev-parse --short HEAD)"
  CHANGED="$(git diff --cached --name-status -- . | sed 's/^/    /')"
  N="$(python3 -c 'import json;print(json.load(open("persistence/checkpoint.json"))["checkpoint"])')"
  python3 - "$N" "$PARENT" "$TESTS" "${MSG%%$'\n'*}" "$WIP" "$CHANGED" <<'PYEOF'
import datetime, re, sys
n, parent, tests, title, wip, changed = sys.argv[1:7]
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
block = f"""<!-- AUTO-CHECKPOINT:BEGIN (scripts/checkpoint.sh yazar; elle düzenlemeyin) -->
## Son checkpoint (otomatik)
- **Checkpoint #{n}** - {now}{' - **WIP: testler geçmemiş olabilir**' if wip == '1' else ''}
- **Commit:** bu kaydı içeren commit = `{parent}` commit'inin hemen ardından gelen commit
  (güncel SHA: `git log -1 --format=%h` veya `bash scripts/checkpoint.sh --verify`)
- **Başlık:** {title}
- **Testler:** {tests}
- **Değişen dosyalar:**
```
{changed or '    (yok)'}
```
<!-- AUTO-CHECKPOINT:END -->"""
p = "HANDOFF.md"
s = open(p, encoding="utf-8").read()
if "<!-- AUTO-CHECKPOINT:BEGIN" in s:
    s = re.sub(r"<!-- AUTO-CHECKPOINT:BEGIN.*?<!-- AUTO-CHECKPOINT:END -->", lambda m: block, s, flags=re.S)
else:
    s = s.replace("\n## Yeni oturumda devam etmek için", "\n" + block + "\n\n## Yeni oturumda devam etmek için", 1)
open(p, "w", encoding="utf-8").write(s)
PYEOF
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
