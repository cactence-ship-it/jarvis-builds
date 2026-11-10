# Project Status - Tofaş Kartal S (1997) digital twin (VEH-01)

**Updated:** 2026-11-10 · **Branch:** `claude/new-session-9teun9` (draft PR to `main`)
Task queue: [TASKS.md](TASKS.md) · Roadmap: [ROADMAP.md](ROADMAP.md) · Session log: [HANDOFF.md](HANDOFF.md). Rules: [CLAUDE.md](CLAUDE.md).

## Phase tracker (state at the close of the 2026-11-07..10 session)
| Phase | Scope | State |
|---|---|---|
| 0-1 | Environment, persistence, infrastructure | DONE |
| 2 | Photos, documents, literature | DONE for available sources: 25 owner photos, registration, **factory owner's manual (E-058)**, parts listings, two owner research reports (E-056, E-059) |
| 3 | Dimensional database | 169 parameters: 63 VERIFIED / 78 ESTIMATED / 28 UNKNOWN. All 28 unknowns need a tape, a weighbridge or a photo on the car (docs/engineering/UNKNOWN_VALUES_REGISTER.md) |
| 4 | Exterior | Photo-based Tripo shell fitted to the manual's dimensions (overhangs 765 / 1141), symmetric, lamp glass; parametric body below it |
| 4b | Interactive body | DONE: doors, hood, tailgate open; X-ray; part selection under the shell |
| 5 | Interior and engine bay | Photo skins (wheel, seats, rear bench, air filter, battery, LPG tank); parametric engine bay rev 2; dashboard still placeholder |
| 6 | Chassis and drivetrain | Catalogue / manual sizes: brakes, radiator, front struts and arms, rack, two-piece propshaft, four-link rear axle with Panhard |
| 7 | Electrical and LPG | Fuse box, relays and earth at the manual's locations; LPG routing schematic (mixer position not photographed) |
| 8 | Exploded view | DONE: per system or whole car, sequential, play / pause / reverse |
| 9 | Inspection tools | DONE: section plane, ruler, envelopes, isolate, parts list, evidence heat map; smoke-tested |

**Not done and why:** engine internals (no evidence, not invented); factory-grade exterior surface (needs a 3D scan or a professional model); the 28 measurement-only values; open uncertainties U-016..U-019 (rear damper top mount, rack vs engine package, half-shaft length, cowl vs bulkhead).

## Current numbers
- Spec: 169 parameters, 63 VERIFIED / 78 ESTIMATED / 28 UNKNOWN (factory owner's manual E-058) (engineering documents: docs/engineering/) (2026-11-07: 18 values filled from public literature E-029..E-036, all ESTIMATED with source and tolerance). Data classes (D-026): 25 DOCUMENT_CONFIRMED (documents and photos), 4 USER_CONFIRMED, 9 SOURCE_SUPPORTED, 40 ESTIMATED, 56 UNKNOWN - see docs/VERI_SOZLUGU.md. Evidence items: E-001..E-036 (photos E-022..E-028, originals local-only) (E-014..E-016 registration documents, originals local-only; E-017 owner configuration; E-018/E-019 provisional assumptions).
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
