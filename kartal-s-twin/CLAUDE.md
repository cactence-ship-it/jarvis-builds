# Working rules for this project (binding; condensed from the owner's master directive)

Read PROJECT_STATUS.md first; it holds the exact next action. Do not re-audit the
environment unless something indicates it changed.

1. **Integrity.** Classify every finding as VERIFIED / ESTIMATED / UNKNOWN (D-005). Never
   invent dimensions, engine data, internal geometry, wiring pinouts, materials, suspension
   coordinates, reinforcements or tolerances. Never promote an estimate silently. Never
   report an untested file as tested, or a push as successful without
   `scripts/checkpoint.sh` printing VERIFIED.
2. **Sources.** Originals are written only by `tools/ingest_refs.py`. Never overwrite or
   delete the only copy of anything.
3. **Privacy.** The repository is PUBLIC: no photos, archives, scans, plate, VIN or personal
   data in git (D-012). Use the alias VEH-01.
4. **Single sources of truth.** Values live in `specs/kartal_s_1997.yaml`; structure lives in
   `assembly/vehicle_master.yaml`. Regenerate `COMPONENT_INVENTORY.md` after edits. Append
   to component history; never rewrite it.
5. **Dependencies.** Keep them minimal (D-007). Add a package only for a specific task, note
   why in `requirements.in`, and re-lock.
6. **Exports.** Validate every export by re-opening it (D-011). Keep visual, CAD and
   mechanical representations separate (D-006).
7. **Phases** run in order 0-12. Work one deliverable at a time. If a subsystem lacks
   evidence, record it in UNCERTAINTY_REGISTER.md and continue with independent work.
8. **Quota.** Do not reread unchanged files or repeat analysis. Checkpoint before the
   session ends; if usage is near its limit, the verified checkpoint comes first.
9. **End-of-session report:** completed work, files changed, tests run, commit ID,
   persistence status, remaining work and the exact next action. Update PROJECT_STATUS.md
   and CHANGELOG.md.
10. Ask the owner only when a decision materially affects the real vehicle configuration
    or engineering correctness, or is reserved to them (for example privacy or publishing).

## Autonomous work protocol (owner instruction, 2026-11-02)
The owner has authorised autonomous work: do not wait for approval on routine engineering
decisions. Still ask only for decisions reserved to the owner (privacy/publishing, real
vehicle configuration that evidence cannot settle).

- **Start of session:** `git checkout ccr-b5d82c24-huyj0b` (until PR #1 is merged), then
  `bash scripts/setup_env.sh`, then read HANDOFF.md ("Sıradaki görevler" + the AUTO-CHECKPOINT
  block). Check `/mnt/user-data/uploads` for new owner files first: evidence beats everything.
- **Every significant stage:** `bash scripts/checkpoint.sh "type(kartal-s-twin): ..."`. It runs
  the privacy scan, validation and all tests, writes the AUTO-CHECKPOINT block in HANDOFF.md
  (parent commit, test result, changed files), commits, pushes and verifies the remote SHA.
- **Before usage runs out, or when work is half done:** `bash scripts/checkpoint.sh --wip "..."`
  saves even with failing tests (still privacy-gated) and marks the record WIP. Then update the
  hand-written sections of HANDOFF.md (stage table, next tasks) in the next normal checkpoint.
- **Never:** commit owner photos, archives, scans, the plate, VIN or personal data; model
  internals without evidence; mark anything VERIFIED without a primary evidence item.
- **Hand-off guarantee:** a new assistant needs only this file, HANDOFF.md and the repository.
