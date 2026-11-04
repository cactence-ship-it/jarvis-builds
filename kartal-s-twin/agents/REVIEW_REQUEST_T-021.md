# Review request (ChatGPT): T-021 owner configuration, LPG tank and steel-rim CAD

Review commit: **ffd3f8fe5c04e48f282b872176d31f44c3382c0a**, branch `ccr-b5d82c24-config-lpg-wheels`,
draft PR #2 (base: PR #1 branch `ccr-b5d82c24-huyj0b`; nothing on `main` changed).

## CI at ffd3f8f
| Event | Run | Jobs | Result |
|---|---|---|---|
| push | https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41409480479 | test, viewer | success |
| pull_request | https://github.com/cactence-ship-it/jarvis-builds/actions/runs/41409524922 | test 125159116299, viewer 125159116086 | success |

Job 125159116299: "Ran 138 tests ... OK"; coreutils `sha256sum -c` audit/2026-11-02-r2 12/12 and audit/2026-11-02 7/7; privacy audit 531 blobs, 0 findings.

## Please check
1. Classification (D-026): no owner statement or ASSUMPTION became VERIFIED; `spec.data_class` mapping; ASSUMPTION-only values forced to LOW.
2. Engine variant rule (`specs/configuration_rules.yaml`, `kartal_twin.configuration`): carburettor excludes E-009 for engine.* values.
3. Geometry math in `tests/test_configuration_cad.py`: tire OD 614.6 mm (185/70 R14); torus 2*pi^2*R*r^2 and Pappus vs OpenCascade volumes; rejection of zero/negative/impossible tank and rim inputs.
4. DC-018 (tank capacity vs geometry) INDETERMINATE is reported, not hidden; CL-008..CL-012 report NOT_EVALUATED with `blocked_by`.
5. The unplaced tank (FUL-005) is excluded from `vehicle_cad.step` and from clearance; the earlier snapshot audit/2026-11-02 is unchanged.
6. Tests that hard-coded 175/70 R14 were changed to pin their inputs or derive from the spec, not weakened.

## Answer format
```yaml
- task: T-021
  reviewer: chatgpt
  commit: ffd3f8fe5c04e48f282b872176d31f44c3382c0a
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings: []
```
