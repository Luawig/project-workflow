# project-workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Compatible-8B5CF6)](https://agentskills.io)

Take a project change from a requirement to a verified implementation, then close out so code, stable specs, project docs, and agent rules point at the same current facts.

This repository is an [Agent Skills](https://agentskills.io) skill. The agent entry is [`SKILL.md`](./SKILL.md).

## What it does

After the user proposes a change, the agent first decides whether the request is planning-only or delivery:

```text
Planning: Triage → Clarify → optional Design → requested checkpoint → stop
Delivery: Triage → Clarify → Design → Spec → Implement → Verify → Closeout
```

- Users may request only a PRD, scope, architecture, or another planning checkpoint. An idea alone does not authorize implementation.
- Small delivery changes create no workflow artifacts by default and still run targeted verification.
- Complex delivery changes use an OpenSpec-compatible file layout owned by this skill. The OpenSpec CLI is not used.
- Documentation is maintained throughout, not as a separate upfront phase.

## Install

In Cursor, Claude Code, Codex, or another Agent Skills client:

```text
Install this skill: https://github.com/Luawig/project-workflow
```

Or:

```bash
npx skills add Luawig/project-workflow
```

You and the agent choose the install location. Prefer a path inside the project when others must reproduce it. Personal skills directories are fine for local trials.

The installing agent should:

1. Place `SKILL.md`, `references/`, `templates/`, `scripts/`, and `LICENSE` at the agreed location.
2. Write [`templates/agents-block.md`](templates/agents-block.md) into the target project's `AGENTS.md`, replacing `<skill-path>` with the actual `SKILL.md` path.
3. Append or update only that block when `AGENTS.md` already exists. Do not overwrite project-specific rules. If `AGENTS.md` is missing, a minimal file containing only the routing block is enough.

Agents that do not support skills can read [`SKILL.md`](./SKILL.md) as a project rule.

## Usage

After routing is in place, propose the change directly, for example:

```text
Add CSV export
Switch login to SSO
Plan a new project, but do not implement it
Write only the PRD and scope
Close out after implementation
```

Optional config: [`templates/workflow-config.md`](templates/workflow-config.md) → `docs/change-workflow.md` in the project.

Planning checkpoints: [`references/planning.md`](references/planning.md).

Spec file conventions: [`references/spec-system.md`](references/spec-system.md). The layout is OpenSpec-compatible, but the OpenSpec CLI is not required and is not used.

## Layout

```text
SKILL.md       Agent entry
references/    Stage playbooks
templates/     AGENTS routing block and optional config
scripts/       Deterministic checks
```

## Contributing

- Change the workflow only in `SKILL.md` and the matching `references/` files.
- Templates and examples must not include personal paths, private project names, or internal service URLs.
- Skill text describes current behavior only.

## License

[MIT](./LICENSE)
