# Project Status - Tofaş Kartal S (1997) digital twin (VEH-01)

**Updated:** 2026-11-02 · **Phase:** 1 complete; Phase 2 blocked on inputs · **Spec rev:** 0.1.0
**Branch:** `ccr-b5d82c24-huyj0b` · **PR:** cactence-ship-it/jarvis-builds#1 (draft, not merged)
The latest verified commit is the branch head on GitHub (`bash scripts/checkpoint.sh --verify`).

## Resume in a new session (paste into Claude Android)
> Continue the Kartal S digital twin. Repo cactence-ship-it/jarvis-builds; work is on branch
> ccr-b5d82c24-huyj0b (PR #1) unless it is merged into main. Read kartal-s-twin/CLAUDE.md and
> kartal-s-twin/PROJECT_STATUS.md, run `bash kartal-s-twin/scripts/setup_env.sh`, then do the
> "Next action".

**Important:** new cloud sessions start from `main`. Until PR #1 is merged, a new session
must check out the branch above, or the Phase 1 files will not be there.

## Phase tracker
| Phase | Scope | State |
|---|---|---|
| 0 | Environment and repository verification | DONE (E-004, E-005) |
| 1 | Persistent project infrastructure | DONE |
| 2 | Photo and source-data analysis | BLOCKED: photos and ZIP not received (U-003, U-004) |
| 3 | Architecture and dimensional database | NOT STARTED: needs measurements and documents (U-002) |
| 4-12 | Body ... delivery | NOT STARTED |

## Verified in Phase 0/1
- **Environment (E-004):** 4 vCPU, 15 GiB RAM, about 30 GB disk, no GPU, Ubuntu 24.04,
  Python 3.13.18, Node 22.23.4. PyPI, npm, conda-forge and GitHub are reachable; most other
  sites are blocked.
- **Persistence (E-005):** checkpoint 1 = `28d8a83`, nonce `77f91cc9…`.
  - The push succeeded and the remote SHA equals local.
  - The GitHub API returns identical content.
  - A fresh clone has the same SHA-256 (`98c67606…`).
  - A **separate fresh cloud container** (a different machine boot ID) read the same commit,
    hash and nonce.
  - Checkpoint 2 = `66ae929` was pushed and verified by `scripts/checkpoint.sh`.
- **Toolchain (E-006):** build123d 0.13.0, OCP 8.0.1.1, no VTK. STEP, STL and GLB exports
  pass independent re-open checks (watertight, outward normals, exact scale, measured glTF
  axes).
- **Validator:** 0 errors. 96 spec parameters (0 VERIFIED, 6 ESTIMATED, 90 UNKNOWN).
  143 components with no geometry. 32 of 32 tests pass.

## Blockers and owner decisions needed
1. **Upload the inputs:** attach `Kartal_S_Studyo.zip` and the 9 photographs to a message in
   this cloud session. The uploads folder was empty, so there is nothing to preserve yet.
2. **Private storage (U-009):** the repository is **public**, so originals are not committed
   and survive only on your phone. Options: make the repository private (GitHub, then
   Settings, then Change visibility), or create a separate private repository for
   references. Then authorise committing them.
3. **Merge PR #1** into `main` when you are satisfied, so that future sessions start with
   this infrastructure.

## Next action
When the files arrive, run `python3 tools/ingest_refs.py` on them. Then register E-0xx per
photo and start Phase 2: inspect the legacy `index.html` and `kartal.json` (object count,
real or procedural geometry, reuse candidates) and map each photo to components.
