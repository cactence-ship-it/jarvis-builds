# Evidence Register

Every value in `specs/kartal_s_1997.yaml` and every component in `assembly/vehicle_master.yaml`
cites evidence by ID from this table. `tools/twin.py validate` parses the rows below. Keep the
column order, and never put a `|` inside a cell.

**Types:** USER_STATEMENT, PHOTO, DOCUMENT, MEASUREMENT, LEGACY_MODEL, LITERATURE, ENVIRONMENT_TEST.
**States:** RECEIVED (file ingested and checksummed in `refs/MANIFEST.csv`), RECORDED (result
captured in this repository), REPORTED (statement only, no artifact), NOT_RECEIVED (expected
but not yet available), SUPERSEDED.

**Rule (D-005):** only a RECEIVED PHOTO, DOCUMENT or MEASUREMENT can make a value VERIFIED.
Owner statements give ESTIMATED at most.

| ID | Title | Type | State | Ref (MANIFEST) | Date | Notes |
|---|---|---|---|---|---|---|
| E-001 | Owner master directive: vehicle is a 1997 Tofaş Kartal S; nine photos and a legacy archive described | USER_STATEMENT | REPORTED | - | 2026-11-01 | The registration plate was supplied but is withheld from this public repository (D-012) |
| E-002 | Legacy archive Kartal_S_Studyo.zip (index.html + kartal.json); reportedly about 47 mesh/part objects | LEGACY_MODEL | NOT_RECEIVED | - | 2026-11-01 | Not present in the cloud session (uploads folder empty). The 47-object figure is preliminary and unverified |
| E-003 | Owner photo set: 9 images (front, rear, side profiles, front three-quarter, dashboard, driver controls, front seats, cargo compartment, tailgate and rear glass) | PHOTO | NOT_RECEIVED | - | 2026-11-01 | Not present in the session. Split into one evidence ID per photo on ingestion. No views of the engine bay, underbody or mechanical internals are described |
| E-004 | Cloud environment audit (CPU, RAM, disk, runtimes, network, formats) | ENVIRONMENT_TEST | RECORDED | - | 2026-11-01 | 4 vCPU, 15 GiB RAM, about 30 GB disk, no GPU, Python 3.13.18, Node 22.23.4, restricted network. Summary in PROJECT_STATUS.md |
| E-005 | GitHub persistence test: push, API read-back, fresh clone, fresh-container read; repository visibility | ENVIRONMENT_TEST | RECORDED | - | 2026-11-01 | Repository is PUBLIC. Checkpoint 1 = commit 28d8a83, nonce 77f91cc9cbc444fe99a25ad42d179a0e. Details in PROJECT_STATUS.md |
| E-006 | CAD toolchain test: build123d 0.13.0 / OCP 8.0.1.1 STEP, STL and GLB export plus independent re-open | ENVIRONMENT_TEST | RECORDED | - | 2026-11-01 | tests/test_cad_toolchain.py. Measured GLB convention: metres, glTF (x, y, z) = CAD (X, Z, -Y) |
