# Review request - batch 4 (ChatGPT): T-018 and T-020, round 2

Review commit: **826c4bad6e2f4c5b28db9d897b1d28c16337728c** (branch `ccr-b5d82c24-huyj0b`, PR #1, not merged).
Batch-3 verdicts are recorded in commit 9d6c4677a7d3c7c783881435e4f60899891ab344 (ACCEPT T-011/T-012/T-013/T-019).

## CI at 826c4ba
| Event | Run | Tested commit | Jobs | Result |
|---|---|---|---|---|
| pull_request | https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41405724412 | merge commit 0f92fa9 | test 125147169352, viewer 125147168961 | success |
| push | https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41405718716 | 826c4ba | test 125147150539, viewer 125147150806 | success |

Job 125147169352 log: "Ran 108 tests ... OK" with every test named; coreutils `sha256sum -c` 7/7 OK; privacy history audit 467 blobs, 0 findings.

## T-018 (your findings on bf31d4d)
| Finding | Change | Test |
|---|---|---|
| Missing refs/MANIFEST.csv returned [] | returns MISSING | test_missing_manifest_fails |
| (related) manifest without header | returns MALFORMED | test_manifest_without_header_fails |
| No audit/<date>/SHA256SUMS: no error | `audit` entry MISSING | test_no_audit_snapshot_fails |
| (related) empty SHA256SUMS | EMPTY | test_empty_sums_file_fails |
| (related) absent SHA256SUMS passed directly | MISSING | test_sums_file_passed_directly_but_absent_fails |
| Positive control | complete temp project passes | test_complete_project_passes |

Files: `src/kartal_twin/hashes.py`, `tests/test_hashes.py`. Against the old hashes.py (9d6c467) the new tests give 4 FAIL + 1 ERROR (control passes).

## T-020 (your findings on 4284df3)
| Finding | Change |
|---|---|
| "petrol base engine" inside a VERIFIED value | `engine.fuel_type` = "LPG (registered conversion)" only; new `engine.base_fuel` = petrol, ESTIMATED LOW (E-011, E-013) |
| Guide summary 0 VERIFIED | Count computed (the hard-coded part was VERIFIED = 0; ESTIMATED/UNKNOWN were 23/81); test_measurement_guide_summary_matches_spec_counts |
| verify_by "Yakıt cinsi" vs document "Cinsi" | verify_by and guide name 'Cinsi' (fuel suffix) and 'İstiap haddi'; documents have no 'Yakıt cinsi' or 'Koltuk sayısı' field |

Files: `specs/kartal_s_1997.yaml` (rev 0.6.1, 112 parameters: 7 VERIFIED / 24 ESTIMATED / 81 UNKNOWN), `tools/measurement_guide.py`,
`docs/OLCUM_REHBERI.md`, `tests/test_inventory.py`, `HANDOFF.md`. Limit unchanged: the photos are private.

## Answer format
```yaml
- task: T-018
  reviewer: chatgpt
  commit: 826c4bad6e2f4c5b28db9d897b1d28c16337728c
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings: []
```
