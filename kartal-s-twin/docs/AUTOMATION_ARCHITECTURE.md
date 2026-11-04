# Kartal Jarvis - automation architecture

Status of every element is stated explicitly. **DEPLOYED** = exists and was tested in this
repository; **DESIGN** = specified, not running; **BLOCKED** = cannot run until the named
blocker is removed. Nothing below spends money without an explicit owner budget.

## Components

| # | Element | Status | Evidence / blocker |
|---|---|---|---|
| 1 | GitHub repo as source of truth (feature branch + PR, main untouched, no auto-merge) | DEPLOYED | `scripts/checkpoint.sh` verifies remote SHA; PR #1 |
| 2 | Persistent, idempotent task queue: `tasks/T-nnn.yaml` (ID = file name, append-only results and reviews) | DEPLOYED | `kartal_twin.tasks`, `tests/test_tasks.py`, generated `TASKS.md` |
| 3 | Cross-review rule: ACCEPTED only after a review of the same commit by a different agent | DEPLOYED (enforced by validator) | `tasks.validate`; self-approval test |
| 4 | Automatic tests on every push / PR (GitHub Actions, free for public repos, no secrets) | DEPLOYED if the workflow push succeeds - see T-005 in TASKS.md | `.github/workflows/kartal-ci.yml` |
| 5 | Session hand-off (any agent can resume) | DEPLOYED | `HANDOFF.md` AUTO-CHECKPOINT block, `CLAUDE.md` protocol, `--wip` saves |
| 6 | Claude task execution via API | BLOCKED | Anthropic API account has no credit; no budget authorisation |
| 7 | ChatGPT/OpenAI task execution via API | BLOCKED | No OpenAI API key; a ChatGPT subscription does not include API access; no budget |
| 8 | n8n orchestration (queue polling, dispatch, timeouts, retries, notifications) | BLOCKED | No n8n host (n8n Cloud is paid; self-hosting needs a server); see design below |
| 9 | Budget / token tracking | DESIGN | Read `usage` from every API response into `tasks/*` results; hard monthly cap in the orchestrator |
| 10 | Notifications for blocked / failed tasks | DESIGN | GitHub notifications on failed CI already reach the owner's GitHub app |

## Free-first design (what can run with zero spend)

```
owner (Android: GitHub app + Claude app)
      |  reviews PR, uploads evidence, authorises budget
      v
GitHub (public repo) ---- tasks/T-nnn.yaml (queue) ---- TASKS.md (board)
      |  push / PR
      v
GitHub Actions CI (no secrets, contents:read) -> tests, validation, privacy scan, build
      |  check results visible on the PR
      v
Claude Code sessions (this environment) pick the next unblocked task from TASKS.md,
work on a feature branch, record results; reviews by a second agent are recorded as
review entries before a task can be ACCEPTED.
```

Manual step that remains while #6-#8 are blocked: the owner forwards
`agents/REVIEW_REQUEST_*.md` to ChatGPT and pastes the verdict back (or ChatGPT opens a PR
that edits the `reviews` list). This is the only routine copy-paste left.

## Paid design (activates only with a written budget)

n8n (or a scheduled GitHub Action) polls `tasks/` for `open` tasks whose dependencies are
`accepted`, dispatches to the Anthropic or OpenAI API, writes the result to a new branch and
opens a PR; a second job sends the PR diff to the *other* provider for review; results and
token usage are written back to the task file. Idempotency key = `task id + input commit SHA`;
timeouts and retries per call; a monthly token cap stops dispatch.

## Security rules (apply to every element)

- No secrets in the repository. API keys only as GitHub Actions secrets or n8n credentials.
- Workflows triggered by `pull_request` never receive secrets (forks cannot read them); never
  use `pull_request_target` with code checkout; `permissions: contents: read` by default.
- Third-party actions pinned by full commit SHA.
- Agent-generated code runs only in CI without secrets, or in an isolated session.
- Owner photos, archives and personal data never enter the public repository (D-012).
