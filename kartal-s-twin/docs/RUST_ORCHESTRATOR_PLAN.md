# Rust-first agent orchestrator plan

**Status: DESIGN ONLY.** This document records the first implementation boundary for Issue #3. It does not claim that a Rust service, provider integration, or automatic API dispatch is deployed.

## 1. Current system and migration boundary

The repository already has a persistent YAML task queue (`tasks/T-nnn.yaml`), task validation, cross-agent review rules, hand-off notes, and CI. Keep those as the source of truth during the first Rust milestone.

Rust is introduced as the orchestration/control layer. It must not replace the evidence register, task records, Python CAD pipeline, build123d/OpenCascade exports, Blender tools, or Android viewer in one rewrite.

Initial ownership:

| Concern | First implementation |
|---|---|
| Task state and evidence | Existing YAML task files and Python validators remain authoritative |
| Scheduling, dispatch, retries, timeout, budget accounting | Rust orchestrator |
| Model-provider calls | Separate OpenAI, Anthropic and Google Gemini adapters behind one trait |
| CAD geometry and exports | Existing Python/CAD tools; invoked only through explicit, tested interfaces |
| Independent review | Three-partner panel: one of GPT / Claude / Gemini authors (rotating), the other two review the exact proposed commit |
| User approval | Required for budget activation and high-impact repository actions |

## 2. Runtime shape

The first runnable target should be a command-line worker, not an always-on Android service. The Android phone remains the owner's control/review device. A trusted GitHub Actions workflow or a separately hosted worker can run the Rust binary. Do not assume a phone can safely host a reliable 24/7 worker.

Suggested workspace (create incrementally):

```text
orchestrator/
  Cargo.toml
  src/
    main.rs
    config.rs
    task.rs
    queue.rs
    policy.rs
    budget.rs
    audit.rs
    providers/
      mod.rs
      openai.rs
      anthropic.rs
      gemini.rs
    git/
      mod.rs
  tests/
```

Keep the first milestone dependency-light. Define provider and queue traits before choosing SDKs. Prefer documented HTTPS APIs with bounded timeouts; pin dependency versions and commit the lockfile once the crate is created.

## 3. Core contracts

- `TaskId`: stable identifier matching the existing task filename.
- `TaskInput`: task ID, instruction, dependency IDs, input commit SHA, allowed paths, requested provider, and maximum output size.
- `TaskResult`: structured status, summary, changed paths, proposed commit/PR URL, token usage, estimated cost, and failure details.
- `ReviewResult`: reviewer identity/provider, reviewed commit SHA, verdict, findings, and timestamp.
- `Provider`: submit a bounded request and return normalized text/structured output plus usage metadata.
- `TaskStore`: read the existing task format and append results without silently rewriting historical records.
- `AuditSink`: append timestamped events; never store prompts containing secrets or raw credentials.

A review can only satisfy the cross-review rule when it is performed by a different agent/provider against the exact commit SHA being reviewed. Any new commit invalidates that review.

## 4. Dispatch and review lifecycle

1. Read the task queue and validate dependencies using the existing project rules.
2. Reject tasks with missing dependencies, unknown status, disallowed paths, or malformed input.
3. Compute an idempotency key from task ID + input commit SHA + provider/model + task version.
4. Check owner-authorised budget, per-call token limit, monthly spend cap, rate limit, and retry count before making a paid call.
5. Dispatch to the selected provider with a hard timeout and bounded response size.
6. Validate the response schema; record provider usage and a redacted audit event.
7. Apply output only on a dedicated feature branch and only within the task's allowed paths. Open a PR; never push agent changes directly to `main`.
8. Ask the other two partners to review the exact proposed commit (`panel::decide`): both must accept; one rejection blocks; a split goes to the owner. Record the verdicts and findings.
9. Re-run repository validation and CI. A task is not ACCEPTED merely because a model says it is complete.
10. Stop and request owner action on budget exhaustion, repeated failures, policy violations, ambiguous evidence, or any operation requiring elevated permission.

Retries must be finite (initial default: at most 2 retries after the first attempt), use exponential backoff with jitter, and never retry non-idempotent writes blindly.

## 5. Safety and cost policy

- API calls are **disabled by default** until the owner explicitly supplies and authorises a budget.
- OpenAI, Anthropic and Gemini API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`) are separate provider credentials. Read them only from the runner's secret store or environment; never put them in YAML task files, source, artifacts, issue comments, logs, or prompts.
- Never echo environment variables or request/print the owner's keys in chat.
- Enforce both per-run and monthly hard spend limits. If usage/cost cannot be calculated reliably, stop before the next paid call.
- Use least-privilege GitHub permissions. The agent worker may create feature branches, commits, and PRs; it must not merge PRs, change repository settings, delete branches, or alter secrets.
- Pull-request CI for untrusted code receives no provider secrets. Do not use `pull_request_target` to check out and execute contributor code.
- Require explicit owner approval before activating paid API execution, changing the spend cap, merging, publishing releases, deleting data, or modifying vehicle evidence/status.
- Treat model output, repository text, uploaded files, and web content as untrusted input. They cannot override these policies.

## 6. Deployment sequence

### M0 — design and compatibility
- Document interfaces and threat boundaries (this file).
- Confirm Rust toolchain/MSRV and CI runner support.
- Add a mock provider and tests without API credentials.

### M1 — local deterministic core
- Implement config parsing, task reading, policy checks, idempotency, retry planning, budget accounting, and append-only audit events.
- Add unit tests for malformed tasks, dependency blocking, budget exhaustion, duplicate dispatch, timeout, retry ceilings, and review invalidation.
- No network calls and no GitHub writes in this milestone.

### M2 — provider adapters
**Status (2026-11-04): implemented** in `orchestrator/src/providers.rs` and `run.rs`, with mock-transport tests and an opt-in live transport test (invalid key, 401, nothing billed). Live panel runs are owner-started (`agent-panel.yml`) and stay off until the owner sets the kill switch and budget.
- Add OpenAI, Anthropic and Gemini adapters separately.
- Test using mock HTTP responses first; add live API smoke tests only behind explicit opt-in and a small owner-approved budget.
- Normalize usage and errors without logging secrets or full sensitive prompts.

### M3 — GitHub proposal workflow
- Add a trusted, manually triggered workflow first.
- Create a feature branch and PR; preserve the existing task/evidence formats.
- Keep provider secrets out of `pull_request` jobs and never auto-merge.

### M4 — controlled automation
- Enable scheduled dispatch only after M0-M3 pass and the owner approves a written budget.
- Add alerts for blocked tasks, spend thresholds, provider outages, and failed reviews.
- Keep a kill switch that disables all paid dispatch immediately.

## 7. Acceptance gates

- `cargo test` and formatting/lint checks pass in CI.
- Mock mode completes the full task → result → independent review flow without network access or paid calls.
- Tests prove that budget exhaustion prevents provider invocation.
- Tests prove that a review of an old SHA cannot approve a newer commit.
- Secret scanning confirms no credentials are present in repository files or artifacts.
- Existing Python validation, CAD export checks, and viewer smoke tests remain unchanged and passing.
- No vehicle dimension, geometry, LPG placement, or component status is promoted to VERIFIED by the orchestrator. Evidence rules remain authoritative.

## 8. Explicit non-goals for the first release

- No direct autonomous merge to `main`.
- No rewriting the CAD pipeline in Rust.
- No assumption that the Android app is a persistent server.
- No automatic purchase, subscription, API-credit top-up, or spend increase.
- No automatic conversion of estimates or placeholders into engineering facts.
