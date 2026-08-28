# Spec system

This skill owns an **OpenSpec-compatible** file layout. Compatibility means projects that already use `openspec/changes/` and `openspec/specs/` can keep those paths and artifact roles. It does not mean this skill depends on the OpenSpec CLI, its generated instructions, or separate apply / verify / archive skills.

This skill writes, reads, validates, and archives the files itself through [spec.md](spec.md), [implement.md](implement.md), [verify.md](verify.md), and [closeout.md](closeout.md).

## OpenSpec-compatible layout

Default for grade M/L delivery:

```text
openspec/changes/<name>/
  proposal.md
  design.md
  tasks.md
  specs/<capability>/spec.md
openspec/specs/<capability>/spec.md   # stable specs after archive only
```

If `openspec/` does not exist, create it.

Write artifacts in this order:

1. `proposal.md`
2. `design.md`
3. spec deltas
4. `tasks.md`

Each artifact must be readable without chat context. Spec deltas must not introduce facts absent from docs unless marked Assumption or Pending Decision.

At closeout:

1. Merge deltas into `openspec/specs/<capability>/spec.md`.
2. Create the capability directory when needed.
3. Ensure Purpose describes the current capability and contains no placeholder.
4. Move the change directory to `openspec/changes/archive/<YYYY-MM-DD>-<name>/`.

## Lightweight change record

Grade S creates no record by default. Use [templates/change-record.md](../templates/change-record.md) only when durable coordination or traceability is needed.

When `spec_system: change-record`, grade M/L also use `docs/changes/<name>.md` instead of the OpenSpec-compatible layout.

After closeout, move completed records to `docs/changes/archive/<YYYY-MM-DD>-<name>.md`. Do not leave completed records in the active directory.

## Project config

Optional file: `docs/change-workflow.md`. Template: [templates/workflow-config.md](../templates/workflow-config.md).

Defaults when absent:

- `spec_system`: `openspec-compatible`
- Docs language: the project's existing language, otherwise the user's language
- Runtime verification: only when a deploy or startable service exists

Config must not require private MCP servers or non-open skills.

## Install location

The user and the installing agent agree on the location. The path written into `AGENTS.md` must point at the actual `SKILL.md`. Common candidates are in the repository README. Do not treat one platform default as the only valid path.
