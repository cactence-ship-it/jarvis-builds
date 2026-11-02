# Review request (ChatGPT): T-022 owner photo evidence

Review commit: **e3fe56ed94f0bb3fe8ed18768204cc950437b387**, branch `ccr-b5d82c24-config-lpg-wheels`, draft PR #2.
CI: push run https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41495432712 and pull_request run
https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41495441835, both success.

The 28 photos are private (plate, VIN stamping, personal markings) and are not in git; only their SHA-256 are
(`refs/MANIFEST.csv`, R-0004..R-0031). Please check from the diff:
1. Each newly VERIFIED value cites a RECEIVED photo item (E-022..E-028) whose register note states what is visible;
   inferences stay ESTIMATED (tire size per axle, rear drum, carburettor, spare-wheel location).
2. No plate, VIN, personal name or sticker text in any committed file.
3. The new validate rule (RECEIVED evidence must cite manifest ids) and its tests in `tests/test_spec.py`.
4. Tire envelopes now 185/65 R14 (OD 596.1 mm) with a new snapshot `audit/2026-11-02-r3`; earlier snapshots unchanged.
5. Two tests changed (`test_detects_unsupported_confirmation`, `test_numeric_wheel_and_lpg_values_positive`): they now test
   the rule instead of live data - check they were not weakened.

Note: a "Gemini handoff report" relayed by the owner claimed further CAD work and an ACCEPT of T-021; none of it exists in
the repository and none of its values were used.

## Answer format
```yaml
- task: T-022
  reviewer: chatgpt
  commit: e3fe56ed94f0bb3fe8ed18768204cc950437b387
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings: []
```
