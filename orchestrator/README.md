# Kartal Agent Orchestrator

Rust M0 skeleton for the Kartal S digital-twin repository.

## Current guarantees

- Offline mock provider only; no HTTP client and no API integrations.
- OpenAI/Anthropic dispatch is blocked by default in policy.
- Per-run budget ceiling, bounded retry planning, idempotency ledger, and independent-review SHA check.
- Standard-library-only implementation; no third-party crates or dependency downloads.
- Existing YAML task queue and Python CAD pipeline remain authoritative and untouched.

## Run locally

Requires Rust 1.75 or newer:

```sh
cargo test --manifest-path orchestrator/Cargo.toml
cargo run --manifest-path orchestrator/Cargo.toml
```

Expected CLI output includes `mode=offline-mock` and `paid_api_calls=0`.

## Scope limits

This is an initial in-memory core, not a persistent worker. The dispatch ledger is process-local; task persistence, provider HTTP adapters, GitHub branch/PR operations, and scheduling are not implemented. Paid provider execution remains disabled. Do not add API keys to this repository.
