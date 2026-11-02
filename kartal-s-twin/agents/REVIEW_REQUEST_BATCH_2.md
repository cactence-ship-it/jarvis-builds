# Review request - batch 2 (for ChatGPT, independent verification lead)

**Commit to review:** `c665cfb8245cc2c896bf77008b4b0c350ef786b8`
**Browse:** https://github.com/cactence-ship-it/jarvis-builds/tree/c665cfb8245cc2c896bf77008b4b0c350ef786b8/kartal-s-twin
**CI at this commit:** see the PR #1 checks (jobs `test` and `viewer`).

Verify independently; reject what you cannot reproduce. Answer with one review block per task.

| Task | What to check | Files |
|---|---|---|
| T-001 (round 2) | Your CHANGES_REQUESTED: rear wheels now use their own side's wheelbase; unequal-wheelbase test; LOW confidence for aggregator values (D-020) | `src/kartal_twin/layout.py` (axle_positions), `tests/test_pipeline.py` (WheelbaseAsymmetry), `specs/kartal_s_1997.yaml` |
| T-010 | Actions pinned to Node 24 releases by SHA (checkout v5.1.0 fbc6f39, setup-python v6.3.0 ece7cb0) | `.github/workflows/kartal-ci.yml` (repo root) |
| T-011 | Viewer browser test in CI; server readiness fix | `tools/viewer_smoke/run.sh`, workflow job `viewer` |
| T-013 | Consistency rules contain only relations; tolerance stacking; NOT_EVALUATED for unknown inputs; tests catch cm-for-mm, a 100 mm typo, arch below tire radius | `specs/consistency_rules.yaml`, `src/kartal_twin/consistency.py`, `tests/test_consistency.py` |
| T-014 | Measurement examples now use the right codes (M06 = left wheelbase, M23 = beltline) | `docs/OLCUM_REHBERI.md`, `tools/record_measurement.py` |
| T-015 | Golden test: fresh CAD STEP must equal `audit/2026-11-02` byte for byte | `tests/test_golden_cad.py`, `audit/2026-11-02/SHA256SUMS` |
| T-017 | ruff 0.15.0 E/F/W lint in CI | `ruff.toml`, workflow step "Lint" |

Optional (T-012): recompute SHA-256 of the ASCII STEP files from the raw URLs, e.g.
https://raw.githubusercontent.com/cactence-ship-it/jarvis-builds/c665cfb8245cc2c896bf77008b4b0c350ef786b8/kartal-s-twin/audit/2026-11-02/cad/WHL-001.step

## Answer format (one block per task)
```yaml
- task: T-0xx
  reviewer: chatgpt
  commit: c665cfb8245cc2c896bf77008b4b0c350ef786b8
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings:
    - <finding with evidence>
```
