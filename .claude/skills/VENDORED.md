# Vendored skills

These skills are copied unchanged from Vercel's public skill collection.

- Source: https://github.com/vercel-labs/agent-skills (commit 1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62)
- License: MIT (Copyright Vercel, Inc.)

| Skill | Use in this repo |
| --- | --- |
| `web-design-guidelines` | Review `kartal-s-twin/viewer/*.html` for UI and accessibility issues. |
| `writing-guidelines` | Review Markdown docs (README, HANDOFF, specs notes) for clarity. |

Both skills fetch their current rules from GitHub at run time, so they need network access
to `raw.githubusercontent.com`.

Not vendored: the React / React Native / Next.js skills (no React code here) and
`deploy-to-vercel` / `vercel-cli-with-tokens` (publishing is reserved to the owner, D-012).

To update: re-copy the folders from a newer upstream commit and change the commit above.
