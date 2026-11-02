# Project Status - Tofaş Kartal S (1997) digital twin (VEH-01)

**Updated:** 2026-11-02 · **Spec rev:** 0.5.0 · **Branch:** `ccr-b5d82c24-huyj0b` · **PR:** #1 (open)
Task queue: [TASKS.md](TASKS.md) · Roadmap: [ROADMAP.md](ROADMAP.md) · Session log: [HANDOFF.md](HANDOFF.md). Rules: [CLAUDE.md](CLAUDE.md).

## Phase tracker
| Phase | Scope | State |
|---|---|---|
| 0-1 | Environment, persistence, infrastructure | DONE |
| 2 | Photo and source-data analysis | BLOCKED: photos and legacy ZIP not received |
| 3 | Dimensional database | IN PROGRESS: literature estimates (27 ESTIMATED, incl. tracks and engine family) and measurement guide ready; waiting for owner measurements |
| 4 | Exterior body | PLACEHOLDER envelope: 35 components (body, closures, glazing, lamps, trim incl. handles and wipers, wheels) |
| 4 (CAD) | First engineering CAD | 4 tire design envelopes (DRAFT), STEP re-opened, byte-reproducible; review: COLLAB_REVIEW_CLAUDE.md |
| 11 (partial) | Export and validation, Android viewer | DONE for current parts: STEP/STL/GLB re-open checks, viewer published |
| 5-10, 12 | Interior, powertrain, chassis, suspension, electrical, integration, documentation | NOT STARTED: no evidence |

## Current numbers
- Spec: 111 parameters, 0 VERIFIED / 27 ESTIMATED / 84 UNKNOWN. Evidence items: E-001..E-013.
- Built: 35 of 143 components visual (all PLACEHOLDER); 4 engineering CAD (WHL-001..004 tire design envelopes, DRAFT, evidence only); mechanical: none.
- Tests: see test-results/latest.txt (all passing at last checkpoint) (`test-results/latest.txt`). Viewer smoke test: `test-results/viewer_smoke.txt`.
- Viewer: https://claude.ai/artifact/7hGubrkeaHVUZSJ4AeGchk

## Owner actions that unblock the most
1. Send the tape measurements in `docs/OLCUM_REHBERI.md` (`M06 = 2488` format; M06 = left wheelbase).
2. Attach the 9 photos and `Kartal_S_Studyo.zip` in a session.
3. Send the registration (ruhsat) technical fields (in writing is enough).
4. Decide private storage for originals (U-009); merge PR #1 when satisfied.
