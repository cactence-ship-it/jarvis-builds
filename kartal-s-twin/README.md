# Tofaş Kartal S (1997) - Complete Vehicle Digital Twin

An evidence-based, parametric digital twin of one specific car (public alias **VEH-01**),
built entirely in a temporary cloud environment and controlled from the Claude Android
app. **Current state: Phase 1 complete. No vehicle geometry exists yet.** See
[PROJECT_STATUS.md](PROJECT_STATUS.md).

## Principles
- **Evidence first.** Every value is VERIFIED, ESTIMATED or UNKNOWN, with traceable sources
  ([EVIDENCE_REGISTER.md](EVIDENCE_REGISTER.md)). Unknowns stay `null`; the validator
  rejects fabricated or unsourced numbers.
- **One source of truth.** Dimensions come from [specs/kartal_s_1997.yaml](specs/kartal_s_1997.yaml);
  structure comes from [assembly/vehicle_master.yaml](assembly/vehicle_master.yaml)
  ([COMPONENT_INVENTORY.md](COMPONENT_INVENTORY.md) is generated from it).
- **Three representations,** never confused: visual, engineering CAD and mechanical assembly.
- **GitHub is the memory.** The container is temporary; a checkpoint counts only when it is
  verified on GitHub.
- **Public repository.** No photos, archives, scans, plate, VIN or personal data in git (D-012).

## Layout
```
kartal-s-twin/
  specs/kartal_s_1997.yaml      master spec: units, coordinate system, 96 parameters
  assembly/vehicle_master.yaml  17 assemblies / 143 components (IDs, status, deps, history)
  src/kartal_twin/              integrity rules, inventory, export checks, privacy guard
    assemblies/                 one geometry-builder module per assembly (stubs for now)
  tools/twin.py                 validate | inventory [--check] | status
  tools/ingest_refs.py          preserve originals byte-identically (stdlib only)
  scripts/setup_env.sh          reproducible, hash-locked environment (idempotent)
  scripts/checkpoint.sh         validate, commit, push, VERIFY on GitHub
  tests/                        32 unit tests (integrity, privacy, CAD export round-trips)
  refs/                         MANIFEST.csv (committed); originals and derived (git-ignored)
  persistence/checkpoint.json   nonce proving each checkpoint reached GitHub
  viewer/  docs/                Android 3D viewer (Phase 11/13), documentation (Phase 12)
  build/                        generated exports (git-ignored)
```

## Commands (run in `kartal-s-twin/`)
```
bash scripts/setup_env.sh          # 15 s fresh, about 3 s when already up to date
.venv/bin/python tools/twin.py validate
.venv/bin/python -m unittest discover -s tests -t .
python3 tools/ingest_refs.py --note "front view" /mnt/user-data/uploads/<file>
bash scripts/checkpoint.sh "message"   # or: make checkpoint MSG="..."
```

## Coordinate system (D-003)
X longitudinal, positive rearward; Y lateral, positive to the right; Z up. The origin is at
the front wheel centre line, the vehicle centre plane and the ground. All lengths are in mm.
GLB exports are in metres with the vehicle front at glTF +Z and up at +Y.

## Registers
[PROJECT_STATUS](PROJECT_STATUS.md) · [ENGINEERING_DECISIONS](ENGINEERING_DECISIONS.md) ·
[EVIDENCE_REGISTER](EVIDENCE_REGISTER.md) · [UNCERTAINTY_REGISTER](UNCERTAINTY_REGISTER.md) ·
[COMPONENT_INVENTORY](COMPONENT_INVENTORY.md) · [CHANGELOG](CHANGELOG.md)
