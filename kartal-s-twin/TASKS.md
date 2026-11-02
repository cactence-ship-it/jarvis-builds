# Task Board - Kartal Jarvis

<!-- GENERATED from tasks/*.yaml by `python tools/twin.py tasks`. Do not edit by hand. -->

Dependency order. A task is ACCEPTED only after a review of the same commit by a different agent.

| ID | Phase | Task | Owner | Status | Depends on | Blocker / last result |
|---|---|---|---|---|---|---|
| T-001 | 11 | Assembly interface and clearance check module (exact B-rep) | claude | **submitted** | - | result claude@784ceb9005f0f1f939a764bedad4efe2ed852aa5 (HIGH) |
| T-002 | 11 | Independent review of the tire-envelope CAD (D-016) and T-001 | chatgpt | **accepted** | T-001 | result chatgpt@fa2f8cdc6f16917d4a9d6c9e781d22f1a38c35cf (MEDIUM) |
| T-003 | 3 | Owner tape measurements M01-M16 and reference state | owner | **open** | - | - |
| T-004 | 2 | Ingest the 9 owner photos and Kartal_S_Studyo.zip (private, not in git) | owner | **blocked** | - | Files not uploaded to any session; private storage decision U-009 pending |
| T-005 | 11 | Continuous integration on GitHub Actions (tests on every push and PR, no secrets) | claude | **accepted** | T-001 | result claude@fa2f8cdc6f16917d4a9d6c9e781d22f1a38c35cf (HIGH) |
| T-006 | 4 | Body side profile as DRAFT CAD from measurements and side photo | claude | **blocked** | T-003, T-004 | Needs T-003 measurements and a side-profile photo |
| T-007 | 8 | Wheel rim and hub interface CAD (width, ET, PCD, centre bore) | claude | **blocked** | T-003 | Rim width, ET, PCD and centre bore are UNKNOWN (need rim stamping photo or measurement) |
| T-008 | 11 | Clearance rule CL-003 tire envelope to wheel arch (static and steering lock) | claude | **blocked** | T-001, T-006 | Wheel-arch geometry is still a placeholder; steering lock angle UNKNOWN |
| T-009 | 11 | Agent orchestration (task dispatch to Claude/OpenAI APIs, cross-review, reports) | claude | **blocked** | T-005 | No Anthropic API credit, no OpenAI API key, no n8n host, no budget authorisation; consumer subscriptions do not include API access |
| T-010 | 11 | Upgrade CI actions to Node 24 releases, pinned by SHA (from T-005 review) | claude | **submitted** | T-005 | result claude@c29f5fe (HIGH) |
| T-011 | 11 | Run the viewer browser smoke test in CI (from T-005 review) | claude | **open** | T-005 | - |
| T-012 | 11 | Independent SHA-256 / rebuild verification of the audit snapshot (open item from T-001 review) | chatgpt | **open** | T-001 | - |
