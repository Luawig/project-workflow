# Change Workflow Config

Place this file at `docs/change-workflow.md` in the consuming project. If it is absent, the skill defaults apply.

```md
# Change Workflow

## spec_system
openspec-compatible

Allowed values:

- `openspec-compatible`: grade M/L delivery uses the OpenSpec-compatible layout; grade S creates no record unless durable traceability is needed
- `change-record`: every grade that needs a durable spec uses a change record under `docs/changes/`

## docs_locale
auto

`auto`: use the project's existing language; if none, match the user.
Set an explicit locale (for example `en` or `zh-CN`) to pin it.

## closeout

- runtime: auto
- memory: not-applicable
- workspace_audit: current-project

`runtime: auto` verifies runtime only when a startable service or deploy entry exists.
`memory` does not maintain agent memory by default.
`workspace_audit` covers the current project only and does not scan sibling repos.

## extra_large_triggers
- TODO: project-specific grade L conditions; delete this section if none
```
