# Kartal Agent Orchestrator

Rust M0 skeleton for the Kartal S digital-twin repository.

## Current guarantees

- Provider adapters for OpenAI, Anthropic and Gemini (`src/providers.rs`) over the system
  `curl`, configured on stdin so keys never reach argv; std-only JSON (`src/json.rs`).
- `panel-run` (`src/run.rs`): author report, guard, two reviews, charge-before-call budget.
  Manual workflow `.github/workflows/agent-panel.yml`; owner setup in Turkish: `KURULUM.md`.
- Paid dispatch is blocked unless the owner sets `KARTAL_PAID_DISPATCH=on` and a run budget
  (`KARTAL_RUN_BUDGET_MICROS`); a provider without a configured price is never called.
- Per-run budget ceiling, bounded retry planning, idempotency ledger, and independent-review SHA check.
- Standard-library-only implementation; no third-party crates or dependency downloads.
- Existing YAML task queue and Python CAD pipeline remain authoritative and untouched.
- Output guard (`src/guard.rs`): model text and model diffs are untrusted. It rejects success
  claims without a CI run link / exit status and commit SHA, flags flattery, rejects weakened
  checks (`cargo fmt` without `--check`, `|| true`, `continue-on-error`, `--no-verify`,
  `pull_request_target`), skipped or deleted tests, and marks owner-only switches (paid dispatch,
  VERIFIED/VALIDATED promotion, force push) as NEEDS_OWNER. Runs on every PR diff in CI.

- Senior-engineer system prompt (`prompts/engineer_tr.txt`, exposed as
  `ENGINEER_SYSTEM_PROMPT` / `engineer_prompt()`): method (problem, root cause, options and
  trade-offs, failure modes, minimal change, evidence-backed verification), units and
  VERIFIED/ESTIMATED/UNKNOWN on every value, and a fixed report format that
  `check-report` enforces.

- Three-partner panel (`src/panel.rs`): GPT, Claude and Gemini rotate as author; the other
  two review the exact commit. Both must accept; one rejection blocks; a split goes to the
  owner; self-reviews and reviews of older commits do not count. Approval never merges.

## Guard CLI

```sh
B=orchestrator/target/debug/kartal-orchestrator
$B prompt "task text"                   # engineer system prompt + task, for any chat model
$B check-report report.txt              # engineering report: sections, evidence, units
$B check-response answer.txt            # chat/model answer
git diff origin/main...HEAD | $B check-diff -
git log --format=%s origin/main..HEAD | $B check-commits -
```

Exit codes: 0 ACCEPT, 1 NEEDS_OWNER, 2 REJECT. Prompt rules for ChatGPT (Turkish):
`kartal-s-twin/agents/GPT_DAVRANIS_KURALLARI.md`.

## Run locally

Requires Rust 1.75 or newer:

```sh
cargo test --manifest-path orchestrator/Cargo.toml
cargo run --manifest-path orchestrator/Cargo.toml
```

Expected CLI output includes `mode=offline-mock` and `paid_api_calls=0`.

## Scope limits

Not a persistent worker. The dispatch ledger is process-local; task persistence, GitHub
branch/PR operations (M3) and scheduling (M4) are not implemented. A panel run produces a
report and two reviews on the job page and changes nothing in the repository. Paid execution is off unless the owner enables it in repository variables. Do not add API keys to
this repository; they belong in repository secrets only.
