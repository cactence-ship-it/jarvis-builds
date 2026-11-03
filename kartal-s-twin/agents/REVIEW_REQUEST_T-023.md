# Review request (ChatGPT): T-023 complete-vehicle PLACEHOLDER package

Review commit: **8d9f16fc035440ec7b73f62072f45a2ad626e333** (docs count fix at 048d35271baaf8b1136ebe8d376c8311757be3b7),
branch `ccr-b5d82c24-config-lpg-wheels`, draft PR #2. CI at 8d9f16f: push run
https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41567984550 and pull_request run
https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41567989478, both success.

Please check:
1. No fabricated measurement: every new size comes from `specs/placeholder_assumptions.yaml` (`pkg_*`, with rationale)
   and every mechanical part is PLACEHOLDER (`tests/test_full_vehicle.py`).
2. Unknown component TYPES are neutral envelopes with notes (front brake, rear spring, steering gear, anti-roll bar).
3. The STEP occurrence-counter finding and the fix (CAD exported first, D-027); r4 geometry equals r3.
4. The viewer hook fix (`camera.updateMatrixWorld()` in `screenPoint`) - test-only behaviour.
5. Whether the NOT_BUILT list in `tests/test_full_vehicle.py` is acceptable.

## Answer format
```yaml
- task: T-023
  reviewer: chatgpt
  commit: 8d9f16fc035440ec7b73f62072f45a2ad626e333
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings: []
```
