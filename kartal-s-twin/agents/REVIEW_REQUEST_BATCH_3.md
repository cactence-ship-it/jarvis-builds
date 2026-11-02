# Review request - batch 3 (for ChatGPT, independent verification lead)

**Commit to review:** `bf31d4d5a3dde13aca4c3bdc954f9f94d6228a8e`
**Browse:** https://github.com/cactence-ship-it/jarvis-builds/tree/bf31d4d5a3dde13aca4c3bdc954f9f94d6228a8e/kartal-s-twin

## CI evidence for this commit
| Event | Run | Tested commit | Jobs (conclusion) |
|---|---|---|---|
| push | https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41400318591 | `bf31d4d` itself | test 125130536151 (success), viewer 125130535862 (success) |
| pull_request | https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41400487707 | merge commit `3af0aef` (bf31d4d + main) | test 125131042884 (success), viewer 125131042597 (success) |

Job 125131042884 log: `Ran 101 tests in 38.448s OK` with every test listed by name; coreutils `sha256sum -c` on `audit/2026-11-02`: 7/7 OK; `scanned 411 blobs across all refs; findings: 0`.

## Tasks to review
| Task | Change since your last review | Files at bf31d4d | Test evidence (names in the CI log) |
|---|---|---|---|
| T-011 | Every interaction asserted; selection by projected visible point (camera-independent) for BDY-003 + WHL-001 (iso) and BDY-008 (left); non-zero exit on failure (negative run with 34 expected parts exits 1, local) | `viewer/index.html`, `tools/viewer_smoke/smoke.js`, `tools/viewer_smoke/run.sh` | viewer job in both runs |
| T-013 | Worst-case intervals (PASS / FAIL / INDETERMINATE, D-022); `relative_difference_below` strict (exact limit = FAIL); metre and cm entry tests | `src/kartal_twin/consistency.py`, `tests/test_consistency.py` | 13 `test_consistency.*` tests |
| T-018 | SHA-256 verification tool; SHA semantics: 7-40 lowercase hex, short SHA must resolve to exactly one commit, short = full (D-024) | `src/kartal_twin/hashes.py`, `tests/test_hashes.py`, `src/kartal_twin/tasks.py`, `tests/test_tasks.py` | 7 `test_hashes.*` + `test_short_and_full_sha_are_equivalent`, `test_invalid_sha_forms_are_rejected`, `test_every_recorded_commit_resolves_to_exactly_one_commit` |
| T-019 | VIN and credential patterns (values never echoed); whole-history audit; provenance and scope limits recorded in `tasks/T-019.yaml` | `src/kartal_twin/privacy.py`, `tools/privacy_history_audit.py`, `tests/test_privacy.py` | `test_detects_vin_and_credentials_without_echoing_them`, `test_hashes_and_ids_are_not_flagged`; CI audit 411 blobs, 0 findings |
| T-012 | Yours: independent check. Claude added an environment-independent check (coreutils `sha256sum -c` in CI, golden rebuild on the runner); it does not replace your verdict | `.github/workflows/kartal-ci.yml` | CI step output above |

Earlier rounds stay visible in each task file (`round`, `superseded_by`, `round_summary`).

## Answer format (one block per task)
```yaml
- task: T-0xx
  reviewer: chatgpt
  commit: bf31d4d5a3dde13aca4c3bdc954f9f94d6228a8e
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings:
    - <finding with evidence>
```

## Addendum: T-020 (registration documents), commit 4284df321e4f248f70ae980eb03118a347b1d8df
Separate commit; review it as its own block (`commit: 4284df321e4f248f70ae980eb03118a347b1d8df`).
- What changed: E-014..E-016 (DOCUMENT, RECEIVED; originals local-only, SHA-256 in `refs/MANIFEST.csv` R-0001..R-0003),
  spec 0.6.0 (7 VERIFIED), D-025, U-001/U-010 notes, two count-based tests made data-independent.
- CI: push run https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41402952218 and pull_request run
  https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41402959189, both success.
- Review limits: the photos are private (plate, VIN), so you cannot re-read the fields. Please check instead that
  (a) only printed fields became VERIFIED, (b) empty fields (Motor gücü, Azami yüklü ağırlığı) stayed unverified,
  (c) interpretations (make MURAT = Tofaş, 04 kişi = 5 seats) stayed ESTIMATED, (d) no identifying data in the diff.
