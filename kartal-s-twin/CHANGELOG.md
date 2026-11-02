# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/). Versions follow the master spec revision.

## [0.9.1] - 2026-11-02 - ChatGPT batch-3 review: T-018 and T-020 reworked

### Recorded
- ChatGPT batch-3 verdicts (relayed by the owner): ACCEPT T-011, T-012, T-013, T-019 on bf31d4d; CHANGES_REQUESTED T-018 (bf31d4d) and T-020 (4284df3).

### Fixed
- T-018: a missing `refs/MANIFEST.csv`, a manifest without its header, no `audit/<date>/SHA256SUMS` at all, an empty SHA256SUMS, or an absent SHA256SUMS passed in directly now FAIL (MISSING / MALFORMED / EMPTY) instead of reading as clean; 6 new tests, 5 of which fail on the old code (the sixth is a positive control).
- T-020: `engine.fuel_type` holds only what the document prints, "LPG (registered conversion)"; the petrol base engine is a new ESTIMATED LOW parameter `engine.base_fuel`. `verify_by` texts name the real document fields ('Cinsi', 'İstiap haddi').
- Measurement guide summary printed a hard-coded "0 VERIFIED"; it now counts, and a test compares it with the spec. Spec 0.6.1: 112 parameters, 7 VERIFIED / 24 ESTIMATED / 81 UNKNOWN.

## [0.9.0] - 2026-11-02 - Registration documents as primary evidence (T-020)

### Added
- E-014..E-016: owner photos of the registration documents and the emission form, ingested as R-0001..R-0003 (originals local-only, SHA-256 in `refs/MANIFEST.csv`; plate, VIN, engine number, serials and dates withheld).
- D-025: a registration document verifies the registered value, not the car's present physical state.

### Changed
- Spec 0.6.0: VERIFIED model, variant, model year, colour name, net weight 1125 kg (was ESTIMATED 1060 kg), displacement 1581 cm3, fuel type LPG (registered conversion); seating 5 ESTIMATED from 'İstiap haddi 04 kişi'. Totals 7 VERIFIED / 23 ESTIMATED / 81 UNKNOWN.
- U-001 and U-010 updated: LPG conversion registered; 'Motor gücü' and 'Azami yüklü ağırlığı' are empty on the documents.

### Fixed
- Two tests assumed a fixed number of VERIFIED values (0 and 2) and failed once real evidence arrived. `test_no_verified_values_without_received_evidence` now checks that every VERIFIED value cites RECEIVED primary evidence; the measurement test compares against the count before recording.

## [0.8.0] - 2026-11-02 - Record integrity, hash verification, wider privacy guard

### Added
- T-018 `kartal_twin.hashes`: SHA-256 verification of audit snapshots and the reference manifest, in `validate`; negative tests for every failure mode.
- T-019 privacy: VIN and credential patterns, `tools/privacy_history_audit.py` (0 findings in 364 blobs), CI step with full history.
- Validator rule and test: recorded commits must be real SHAs that exist in git (D-023).

### Changed
- T-013: `relative_difference_below` is strict; exact-limit and metre/cm entry tests.
- T-011: selection test taps the projected visible point of a part (camera-independent), for three parts in two views.

### Fixed
- Four task results carried placeholder text instead of a commit SHA (T-011, T-013, T-014, T-015); replaced with the real SHAs (bbeefcf, cf87630).

## [0.7.1] - 2026-11-02 - ChatGPT batch-2 review: T-011 and T-013 reworked

### Changed
- T-013: worst-case interval semantics (D-022) - PASS / FAIL / INDETERMINATE; boundary tests for clearance and sum_at_most.
- T-011: the viewer smoke test asserts every interaction (load, part count vs manifest, BDY-003 selection, explode and restore, GLAZING visibility, no console errors) and exits non-zero on failure; read-only test hook in the viewer.
- Recorded ChatGPT ACCEPT for T-001, T-010, T-014, T-015, T-017.

## [0.7.0] - 2026-11-02 - Phase 0 audit, consistency rules, CAD regression gate

### Added
- T-013 dimensional consistency rules DC-001..DC-015 (D-021), wired into `validate` and the measurement intake.
- T-015 golden CAD regression test against `audit/2026-11-02` (proven sensitive to a 1 mm wheelbase change).
- Task schema: description, priority, timestamps, error, evidence; owner-facing status mapping; `tasks/tasks.json` export for orchestrators (n8n). T-013..T-016.

### Fixed
- T-014: misleading measurement examples (`M05 = 2488` and `M20=955` pointed at the wrong quantities) in the guide, intake tool and status file.

## [0.6.0] - 2026-11-02 - Kartal Jarvis organisation: clearance checks, task registry

### Added
- T-001: exact B-rep clearance/interference module (`interfaces.py`, `specs/clearance_rules.yaml`, D-018). CL-001 and CL-002 PASS; values match analytic results.
- Task registry `tasks/T-001..T-009` with an enforced cross-review rule (no self-approval, D-019); generated `TASKS.md`; `ROADMAP.md`; `docs/AUTOMATION_ARCHITECTURE.md`; `agents/REVIEW_REQUEST_T-002.md`. 68 tests.

## [0.5.0] - 2026-11-02 - Independent review and first engineering CAD

### Added
- First engineering CAD: tire design envelopes WHL-001..004 (175/70 R14 designation, ESTIMATED inputs only, DRAFT), per-part and assembly STEP with re-open checks (D-016). Resolver forbids placeholders outside the visual representation.
- `COLLAB_REVIEW_CLAUDE.md`: evidence-backed review for a ChatGPT cross-check. `audit/2026-11-02/` snapshot with SHA256SUMS (D-017).
- Reproducibility tests (separate processes) and a stale-output test: 55 tests.

### Fixed
- `manifest.json` listed stale files from earlier runs and the delivery staging folder; outputs are now cleaned and only this run's files are listed.
- STEP header timestamp is fixed, so CAD STEP files are byte-reproducible (the coloured visual STEP is not, because of OCCT style ordering; it is checked geometrically).
- `tests/test_legacy.py` leaked temporary archives; spec and inventory revision fields updated (were 0.1.0).

## [0.4.0] - 2026-11-02 - Autonomous mode, more literature evidence

### Added
- `tools/photo_scale.py`: side-photo pixel points to VCS mm (wheelbase scale, camera-roll removal, tolerance with a perspective allowance); `--apply` writes ESTIMATED values and never replaces VERIFIED ones. Synthetic tests (50 tests in total).
- `checkpoint.sh` writes an AUTO-CHECKPOINT record into HANDOFF.md on every commit and supports `--wip` emergency saves; `twin.py privacy`; autonomous work protocol in CLAUDE.md.
- Literature evidence E-011..E-013: front/rear track 1386/1327 mm (replacing placeholders), gross mass 1550 kg, engine family (4-cylinder inline SOHC carburettor 1.6, 1581 cm3, ~61 kW, ~131 N·m). 27 ESTIMATED values, still 0 VERIFIED.

## [0.3.2] - 2026-11-02 - Exterior detail (PLACEHOLDER)

### Added
- Rounded roof edges, door handles EXT-006..009, front wipers EXT-015 and wheel hub caps. 35 components built; viewer version 3 published.

## [0.3.1] - 2026-11-02 - Delivery and legacy-archive analysis

### Added
- `scripts/package_delivery.sh`: build, render and package STEP/STL/GLB, per-assembly GLBs, previews, viewer, manifest and the measurement guide into one ZIP (sent to the owner).
- `tools/analyze_legacy.py`: read-only analysis of the legacy archive (three.js JSON, glTF or generic JSON; procedural vs mesh geometry; embedded-image privacy warning). Tested on synthetic archives, since the real ZIP has not been received.

## [0.3.0] - 2026-11-02 - Measurement intake

### Added
- `docs/OLCUM_REHBERI.md` (generated): 31 coded measurements, registration fields and the required photo list.
- `body_profile` spec group (15 UNKNOWN slots; placeholders now `replaces` them). 111 spec parameters in total.
- `tools/record_measurement.py`: owner measurement log, then a MEASUREMENT evidence row, then VERIFIED values (D-015).
- Resolver guard: a stand-in placeholder can only be read through its spec key. 46 tests.

## [0.2.1] - 2026-11-02 - Closures as separate components

### Added
- Hood BDY-003, doors BDY-008..011 and tailgate BDY-012 are cut from the envelope as separate PLACEHOLDER components with 3 mm panel gaps (30 components in total).

### Fixed
- Viewer smoke test: a stale http-server on a fixed port could serve old files to later runs. The test now uses a random port and its own server process.

## [0.2.0] - 2026-11-02 - CAD pipeline and first PLACEHOLDER envelope

### Added
- Literature evidence E-007..E-010 and 11 ESTIMATED spec values (length 4396, width 1642, height 1496, wheelbase 2490, tire 175/70 R14 and others). None are VERIFIED.
- `specs/placeholder_assumptions.yaml`, the provenance-tracking `Resolver`, `layout.py` (wheels, profile, greenhouse) and `cad/` helpers.
- Builders for BODY_ASSEMBLY (BDY-001 envelope), GLAZING (8), WHEELS_AND_TIRES (4), LIGHTING (6) and EXTERIOR_TRIM (5): 24 components, all visual PLACEHOLDER.
- `pipeline.py` and `twin.py build`: STEP, STL, full and per-assembly GLB, manifest.json, and an independent re-open of every export. `twin.py sync-inventory`.
- `gltf_writer.py` (metadata-rich GLB), `tools/render_preview.py` (PNG previews, no GPU) and `tools/spec_set.py`.
- `scripts/run_tests.sh`: records results in `test-results/latest.txt`. `checkpoint.sh` now refuses to commit when tests fail.

### Fixed
- Negative spec tests depended on current data and broke when wheelbase became ESTIMATED (commit 183c608 was pushed with 2 failing tests; fixed in 9b76991).

## [0.1.0] - 2026-11-01 - Phase 0/1: environment, persistence and infrastructure

### Added
- Persistence workflow: `scripts/checkpoint.sh` (validate, commit, push, then verify that the remote SHA equals local HEAD) and `persistence/checkpoint.json` nonce.
- Reproducible environment: `requirements.in` (2 direct dependencies), `requirements.lock` (59 hash-pinned packages), and the idempotent `scripts/setup_env.sh`.
- Master spec `specs/kartal_s_1997.yaml`: 96 parameters, VCS and units. Only 6 identity values are set (ESTIMATED, owner-declared); the rest are UNKNOWN.
- VEHICLE_MASTER inventory `assembly/vehicle_master.yaml`: 17 assemblies, 143 components, no geometry. Generated `COMPONENT_INVENTORY.md`.
- Registers: evidence, uncertainty and engineering decisions; project status.
- Tooling: `tools/twin.py` (validate / inventory / status), `tools/ingest_refs.py` (byte-identical, read-only, checksummed ingestion).
- Library: `kartal_twin.spec`, `.inventory`, `.export_check` (numpy STL/GLB re-open), `.privacy`; 17 assembly builder stubs.
- 32 unit tests, including negative tests proving that fabricated or unsourced data is rejected, and CAD STEP/STL/GLB round-trips.

### Verified
- Push to GitHub, read-back through the GitHub API, fresh clone, and a fresh separate cloud container all returned identical checkpoint content (E-005).
