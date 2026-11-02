# Project Status - Tofaş Kartal S (1997) digital twin (VEH-01)

**Updated:** 2026-11-02 · **Spec rev:** 0.3.0 · **Branch:** `ccr-b5d82c24-huyj0b` · **PR:** #1 (open)
Detailed session log and next tasks: [HANDOFF.md](HANDOFF.md). Rules: [CLAUDE.md](CLAUDE.md).

## Phase tracker
| Phase | Scope | State |
|---|---|---|
| 0-1 | Environment, persistence, infrastructure | DONE |
| 2 | Photo and source-data analysis | BLOCKED: photos and legacy ZIP not received |
| 3 | Dimensional database | IN PROGRESS: literature estimates (17 ESTIMATED) and measurement guide ready; waiting for owner measurements |
| 4 | Exterior body | PLACEHOLDER envelope: 35 components (body, closures, glazing, lamps, trim incl. handles and wipers, wheels) |
| 11 (partial) | Export and validation, Android viewer | DONE for current parts: STEP/STL/GLB re-open checks, viewer published |
| 5-10, 12 | Interior, powertrain, chassis, suspension, electrical, integration, documentation | NOT STARTED: no evidence |

## Current numbers
- Spec: 111 parameters, 0 VERIFIED / 17 ESTIMATED / 94 UNKNOWN. Evidence items: E-001..E-010.
- Built: 35 of 143 components, all visual PLACEHOLDER. CAD and mechanical representations: none.
- Tests: 48/48 (`test-results/latest.txt`). Viewer smoke test: `test-results/viewer_smoke.txt`.
- Viewer: https://claude.ai/artifact/7hGubrkeaHVUZSJ4AeGchk

## Owner actions that unblock the most
1. Send the tape measurements in `docs/OLCUM_REHBERI.md` (`M05 = 2488` format).
2. Attach the 9 photos and `Kartal_S_Studyo.zip` in a session.
3. Send the registration (ruhsat) technical fields (in writing is enough).
4. Decide private storage for originals (U-009); merge PR #1 when satisfied.
