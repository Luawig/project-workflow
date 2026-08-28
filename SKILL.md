---
name: project-workflow
description: >-
  Orchestrates a project change from a requirement through clarification, design,
  spec, implementation, verification, archive, and documentation sync. Use
  when the user proposes a product, architecture, protocol, or code change;
  asks to update PRD, scope, architecture, rules, OpenSpec, AGENTS.md, or
  project docs; requests implementation of a change; or needs closeout after
  implementation. Required workflow when AGENTS.md names this skill.
---

# Project Workflow

Take a project change from a requirement to a verified implementation, then close out so code, stable specs, project docs, and agent rules point at the same current facts.

This skill is a change-lifecycle orchestrator. It supports planning-only work as well as delivery. It owns OpenSpec-compatible file conventions and does not use the OpenSpec CLI. Load only the reference files needed for the current stage.

Write natural-language prose in the project's existing language. If the project has no established language, match the user's language. Leave code identifiers, paths, field names, APIs, event names, state values, service names, and spec IDs unchanged.

Keep unresolved items as `Open Questions` or `Pending Decisions`. Do not invent facts.

## Quick Start

1. Confirm this skill is the project's required workflow. Root `AGENTS.md` must point at the installed `SKILL.md`.
2. Treat the user input as a **change**. Docs, code, architecture, and scope edits are types and risk grades of the same thing.
3. Determine intent before risk: `planning` or `delivery`. Read [references/planning.md](references/planning.md). A new idea without implementation authorization starts in planning.
4. Read [references/lifecycle.md](references/lifecycle.md), grade the change, and locate the current stage.
5. Investigate the repo, existing specs, tests, and docs before asking questions. Ask only what would change scope, risk, or acceptance, and cannot be confirmed from the repo.
6. For planning, stop at the smallest requested checkpoint and produce only requested documents plus minimum prerequisites.
7. For delivery, follow the risk path through verification and closeout.
8. Before implementation, have an execution contract: goal, bounds, hard constraints, acceptance, and stop conditions. Prefer existing tests, schemas, contracts, and specs. Do not copy a parallel spec in prose.
9. Close delivery with [references/closeout.md](references/closeout.md). Archive is not the finish line.

## Authority

Read [references/authority.md](references/authority.md). Conflicts must be resolved at closeout:

| Layer | What it represents | Typical location |
|---|---|---|
| Implementation | What the system actually does | Code, tests, `contracts/` |
| Behavior | Observable, testable behavior | Stable specs (default `openspec/specs/`) |
| Decisions and context | Scope, motivation, long-lived decisions, agent bounds | `docs/`, `AGENTS.md`, ADRs |

## Risk paths

Risk grade and intent are independent. Planning may stop after Clarify or Design at any grade. The paths below apply when the user authorizes delivery.

| Grade | When | Path |
|---|---|---|
| S | Local change that does not alter user-visible behavior, external contracts, the data model, or scope | Implement → Verify (targeted) → Closeout (affected surfaces only) |
| M | New capability or user-visible behavior change, or a scope / acceptance change | Clarify → Design (affected docs only) → Spec → Implement → Verify → Closeout |
| L | Architecture, protocol, data model, migration, security, multi-module, or external-contract change | Full path + extra gates |

Complex changes default to the OpenSpec-compatible file layout in [references/spec-system.md](references/spec-system.md). Grade S creates no change artifact by default. Do not skip required spec work.

## Lifecycle

```text
Triage → Clarify → Design → Spec → Implement → Verify → Closeout
```

Entry, outputs, exits, and rollback for each stage: [references/lifecycle.md](references/lifecycle.md). Load the playbook for the current stage:

| Stage | When | File |
|---|---|---|
| Plan | The user wants to clarify or design without implementation | [references/planning.md](references/planning.md) |
| Clarify | New requirements, follow-ups, conflicting statements, third-party references | [references/clarify.md](references/clarify.md) |
| Design | Scope, product, architecture, rules, protocols, data model, ADRs | [references/design.md](references/design.md) |
| Spec | Ready to implement, or behavior / contracts will change | [references/spec.md](references/spec.md) |
| Implement | Spec is stable; code changes start | [references/implement.md](references/implement.md) |
| Verify | Implementation is done or claimed complete | [references/verify.md](references/verify.md) |
| Closeout | Verification passed, or the user is reviewing docs / scope consistency | [references/closeout.md](references/closeout.md) |

If an OpenSpec-compatible change or change record is already in progress, continue from its current stage. Do not start a parallel track.

## Hard gates

Do not skip these with "code first":

- Do not implement while direction-changing `Open Questions` / `Pending Decisions` are unresolved.
- Grade M/L must have a spec before implementation: an OpenSpec-compatible change or a recorded lightweight change record.
- Grade L must have affected design docs or an ADR before spec work.
- Do not archive, and do not mark docs as delivered, if verification failed.
- Passing tests or a merged PR is not, by itself, change completion.
- Destructive cleanup (branches, worktrees, temp artifacts) needs a preview and explicit user confirmation.

## When to ask

Do not ask what you can look up. Ask at most five questions per round, each with 2–4 options and a recommendation.

Stop and ask when:

- Project type, primary user, or success criteria cannot be judged and would change the design.
- Mutually exclusive options would change architecture, protocol, data model, or an external contract.
- A third-party reference is unreachable and the user requires its concrete behavior.

Continue with `TODO` when field names, secondary config, or non-critical copy are missing. Ship a minimal usable artifact and mark the gaps.

Do not write assumptions as facts. Do not silently decide for the user. If a default is required to continue, record it as an Assumption or pending decision and list it in the reply.

## Documentation

Docs are maintained through the lifecycle, not as a separate upfront phase:

- During clarify, capture Facts and write them into long-lived product or technical docs.
- During design, record scope, rules, and ADRs. Edit current sections; do not add a parallel version.
- During spec, point requirements back at rules, interfaces, or decisions in docs.
- At closeout, promote delivered state into long-lived docs and rewrite or delete stale current claims.

Planning may produce only selected documents. Templates are a menu, not a requirement to create the entire tree.

`docs/product/scope.md` is the authority for current vs later. Intake is a source log, not the default reading entry.

## Quality Gates

- Every `TODO` must say what information is missing.
- Every `RULE-*` must be checkable. Do not use "try to", "usually", or "appropriately".
- Third-party references must include a reason not to adopt, or adaptation conditions.
- Field-level REST/WS authority lives in `contracts/`. `docs/protocols.md` is an interface inventory only.
- Every OpenSpec-compatible `tasks.md` item must trace to the proposal, design, or spec delta.
- Hard constraints need a fact or user decision as source. Suggestions may change with field evidence if the reason is recorded.
- Do not pass acceptance by deleting tests, skipping assertions, lowering thresholds, or `|| true`.
- `Open Questions` / `Pending Decisions` must not keep resolved items. A cited `FACT-N` must be defined.

## Project contract

The consuming project's `AGENTS.md` must name this skill as the required workflow for change requests and must point at the installed copy. The routing text is [templates/agents-block.md](templates/agents-block.md), written by the installing agent. Do not generate a full project `AGENTS.md`. Optional config: [templates/workflow-config.md](templates/workflow-config.md).

Install location is agreed between the user and the installing agent. Do not rely on README while executing a change.
