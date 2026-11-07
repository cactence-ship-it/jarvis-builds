# Project Status - Tofaş Kartal S (1997) digital twin (VEH-01)

**Updated:** 2026-11-03 · **Spec rev:** 0.8.0 · **Branch:** `ccr-b5d82c24-config-lpg-wheels` (stacked on `ccr-b5d82c24-huyj0b`, PR #1 open)
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
- Spec: 149 parameters, 25 VERIFIED / 72 ESTIMATED / 52 UNKNOWN (2026-11-07: 18 values filled from public literature E-029..E-036, all ESTIMATED with source and tolerance). Data classes (D-026): 25 DOCUMENT_CONFIRMED (documents and photos), 4 USER_CONFIRMED, 9 SOURCE_SUPPORTED, 40 ESTIMATED, 56 UNKNOWN - see docs/VERI_SOZLUGU.md. Evidence items: E-001..E-036 (photos E-022..E-028, originals local-only) (E-014..E-016 registration documents, originals local-only; E-017 owner configuration; E-018/E-019 provisional assumptions).
- Built: 150 visual parts covering 150 of 157 inventory components (all PLACEHOLDER; every assembly built, 7 components excepted with a reason) + 9 engineering CAD (tire envelopes 185/65 R14, steel rims, LPG tank unplaced; DRAFT); mechanical: none. Previews: build/previews/{sheet,mechanical_sheet,interior_sheet}.png.
- Tests: see test-results/latest.txt (all passing at last checkpoint) (`test-results/latest.txt`). Viewer smoke test: `test-results/viewer_smoke.txt`.
- Viewer: https://claude.ai/artifact/7hGubrkeaHVUZSJ4AeGchk (engineering, part by part)
- Combined twin (real-look Tripo shell from owner photos + 150 engineering parts, X-ray, opening doors/hood/tailgate, cabin/engine cameras, photo-based steering wheel, seats, air filter, battery and LPG tank, D-033..D-036): https://claude.ai/artifact/N6Wiwb9pzGy2QmLDPF2Xq3 (private; shell texture shows the plate by owner decision)
- Studio 3D (realistic visual model, D-028, rotatable on the phone): https://claude.ai/artifact/9D8o5byLmjc6xJ6ba2BzVR

## Owner actions that unblock the most
0. Generate the car on tripo3d.ai from your photos and send `car.glb` here (phone guide: `docs/TRIPO_URETIM.md`). Claude fits it to the twin and publishes the phone viewer.
1. Send the tape measurements in `docs/OLCUM_REHBERI.md` (`M06 = 2488` format; M06 = left wheelbase).
2. Attach the 9 photos and `Kartal_S_Studyo.zip` in a session.
3. DONE: registration documents received 2026-11-02 (T-020). Still useful: engine-bay and cargo-area photos (LPG tank location, fuel system).
4. Decide private storage for originals (U-009); merge PR #1 when satisfied.
