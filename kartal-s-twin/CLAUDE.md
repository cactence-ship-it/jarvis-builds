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
