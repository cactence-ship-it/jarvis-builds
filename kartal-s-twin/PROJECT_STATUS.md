# Project Status - Tofaş Kartal S (1997) digital twin (VEH-01)

**Updated:** 2026-11-02 · **Spec rev:** 0.8.0 · **Branch:** `ccr-b5d82c24-config-lpg-wheels` (stacked on `ccr-b5d82c24-huyj0b`, PR #1 open)
Task queue: [TASKS.md](TASKS.md) · Roadmap: [ROADMAP.md](ROADMAP.md) · Session log: [HANDOFF.md](HANDOFF.md). Rules: [CLAUDE.md](CLAUDE.md).

## Phase tracker
| Phase | Scope | State |
|---|---|---|
| 0-1 | Environment, persistence, infrastructure | DONE |
| 2 | Photo and source-data analysis | IN PROGRESS: 28 owner photos and registration documents analysed (E-014..E-028); legacy ZIP not received |
| 3 | Dimensional database | IN PROGRESS: registration documents received (7 VERIFIED, E-014..E-016); literature estimates and measurement guide ready; waiting for owner measurements |
| 4 | Exterior body | PLACEHOLDER envelope: 35 components (body, closures, glazing, lamps, trim incl. handles and wipers, wheels) |
| 4 (CAD) | First engineering CAD | 4 tire design envelopes (DRAFT), STEP re-opened, byte-reproducible; review: COLLAB_REVIEW_CLAUDE.md |
| 11 (partial) | Export and validation, Android viewer | DONE for current parts: STEP/STL/GLB re-open checks, viewer published |
| 5-10 | Interior, powertrain, chassis, suspension, electrical | PLACEHOLDER package built (D-027): arrangement from photos, every size a labelled guess; engineering CAD needs measurements |
| 12 | Documentation | IN PROGRESS |

## Current numbers
- Spec: 134 parameters, 25 VERIFIED / 35 ESTIMATED / 74 UNKNOWN. Data classes (D-026): 25 DOCUMENT_CONFIRMED (documents and photos), 4 USER_CONFIRMED, 2 SOURCE_SUPPORTED, 29 ESTIMATED, 74 UNKNOWN - see docs/VERI_SOZLUGU.md. Evidence items: E-001..E-028 (photos E-022..E-028, originals local-only) (E-014..E-016 registration documents, originals local-only; E-017 owner configuration; E-018/E-019 provisional assumptions).
- Built: 150 visual parts covering 150 of 157 inventory components (all PLACEHOLDER; every assembly built, 7 components excepted with a reason) + 9 engineering CAD (tire envelopes 185/65 R14, steel rims, LPG tank unplaced; DRAFT); mechanical: none. Previews: build/previews/{sheet,mechanical_sheet,interior_sheet}.png.
- Tests: see test-results/latest.txt (all passing at last checkpoint) (`test-results/latest.txt`). Viewer smoke test: `test-results/viewer_smoke.txt`.
- Viewer: https://claude.ai/artifact/7hGubrkeaHVUZSJ4AeGchk

## Owner actions that unblock the most
1. Send the tape measurements in `docs/OLCUM_REHBERI.md` (`M06 = 2488` format; M06 = left wheelbase).
2. Attach the 9 photos and `Kartal_S_Studyo.zip` in a session.
3. DONE: registration documents received 2026-11-02 (T-020). Still useful: engine-bay and cargo-area photos (LPG tank location, fuel system).
4. Decide private storage for originals (U-009); merge PR #1 when satisfied.
