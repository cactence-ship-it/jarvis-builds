# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/). Versions follow the master spec revision.

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
