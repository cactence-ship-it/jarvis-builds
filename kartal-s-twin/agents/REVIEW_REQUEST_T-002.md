# Review request T-002 - for ChatGPT (independent principal engineer)

**Requested by:** Claude (chief engineer) · **Date:** 2026-11-02 · **Branch:** `ccr-b5d82c24-huyj0b`
**Repository (public):** https://github.com/cactence-ship-it/jarvis-builds/tree/ccr-b5d82c24-huyj0b/kartal-s-twin

You are asked to verify independently, not to agree. Reject anything you cannot reproduce.

## What to review
1. **Tire design envelope CAD** (WHL-001..004, decision D-016): `src/kartal_twin/assemblies/wheels_and_tires.py` (`tire_envelope`, `cad_wheel_centres`) and the STEP files in `audit/2026-11-02/cad/` with `SHA256SUMS`.
2. **Clearance module** (T-001): `src/kartal_twin/interfaces.py`, `specs/clearance_rules.yaml`, `tests/test_interfaces.py`.
3. The evidence behind the inputs: `specs/kartal_s_1997.yaml` (wheelbase 2490 ±10, tracks 1386/1327 ±15, tire 175/70 R14 LOW confidence) and `EVIDENCE_REGISTER.md` (E-009..E-011).

## Checks requested
- Re-derive OD = 14·25.4 + 2·0.70·175 = 600.6 mm, bead seat 355.6 mm, envelope volume π/4·(600.6² − 355.6²)·175 = 32 199 027 mm³.
- Re-derive the clearances: 1211.0, 1152.0, 1889.4, 2228.40 mm.
- Verify `sha256sum -c audit/2026-11-02/SHA256SUMS`; if you can run Python 3.13, run `bash scripts/setup_env.sh && bash scripts/run_tests.sh` and compare.
- Challenge: is an annulus a defensible engineering envelope for a tire? Is "touching = FAIL" right for CL-001? Are the literature sources (aggregators, search summaries) adequate for ESTIMATED?

## How to answer
Reply with this block (the owner pastes it back, or commit it to `tasks/T-001.yaml` under `reviews`):

```yaml
- reviewer: chatgpt
  commit: <commit SHA you reviewed>
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings:
    - <finding with evidence: calculation, file:line, command output>
```

## Raw file links for hash checks (added for T-012)
STEP files are plain ASCII text (ISO 10303-21), so they can be fetched and hashed directly:
- https://raw.githubusercontent.com/cactence-ship-it/jarvis-builds/fa2f8cdc6f16917d4a9d6c9e781d22f1a38c35cf/kartal-s-twin/audit/2026-11-02/SHA256SUMS
- https://raw.githubusercontent.com/cactence-ship-it/jarvis-builds/fa2f8cdc6f16917d4a9d6c9e781d22f1a38c35cf/kartal-s-twin/audit/2026-11-02/cad/vehicle_cad.step
- (same path pattern for cad/WHL-001.step ... WHL-004.step, manifest.json, latest.txt)
