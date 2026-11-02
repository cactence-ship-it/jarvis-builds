# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/). Versions follow the master spec revision.

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
