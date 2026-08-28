# Spec

Turn a stable design into an implementable, testable spec. If requirements are still moving, return to clarify or design.

## Choose the spec form

| When | Form |
|---|---|
| M/L delivery, with the default config | OpenSpec-compatible change |
| S needing durable coordination or traceability | Lightweight change record |
| Project sets `spec_system: change-record` | Lightweight change record; write behavior into long-lived docs at closeout |

Layout and write order: [spec-system.md](spec-system.md).

## OpenSpec-compatible mapping

| Source | Target | Content |
|---|---|---|
| PRD, scope | `proposal.md` | Motivation, scope, non-goals |
| Acceptance criteria | `tasks.md` / spec scenarios | Executable acceptance |
| overview, architecture, ADRs | `design.md` | Bounds, flows, decisions |
| rules | `design.md` / spec | `RULE-*` |
| contracts, protocols, data-model, services | specs / `design.md` | Interfaces and data; fields from contracts |
| Third-party analysis | `design.md` | Adopt, skip, adaptation risk |

Specs must not introduce facts that are not in docs unless marked Assumption or Pending Decision. Do not write product vision as a spec requirement.

## Execution contract

Before implementation, the spec must state:

1. **Goal**: observable change when done.
2. **Non-goals**: what will not be done.
3. **Hard constraints**: fail if violated; each from a Fact, RULE, ADR, or user decision.
4. **Suggestions**: may change during implementation if the reason is recorded.
5. **Acceptance**: commands, test names, or repeatable steps; prefer existing tests, schemas, and contracts.
6. **Stop conditions**: baseline must not regress; switch after repeated failure; roll back if worse than baseline.
7. **Forbidden shortcuts**: name deleting tests, skipping assertions, lowering thresholds, or mocking the unit under test to manufacture a pass.

Do not retell test files in prose. Write paths and test names.

## OpenSpec-compatible templates

### `proposal.md`

```md
# Proposal

## Summary
TODO

## Motivation
- TODO

## Scope
- TODO

## Non-goals
- TODO

## Affected Docs
- `docs/product/scope.md`

## Open Questions
- TODO
```

### `design.md`

```md
# Design

## Overview
TODO

## Source Documents
- `docs/architecture.md`

## Architecture Impact
- TODO

## Protocol Impact
- TODO

## Data Model Impact
- TODO

## Rules
- RULE-*: TODO

## Decisions
- ADR-XXXX: TODO

## Risks
- TODO

## Constraints
- Hard: TODO
- Suggestions: TODO
```

### `tasks.md`

```md
# Tasks

- [ ] 1. Update contracts or specs: TODO
- [ ] 2. Implement TODO
- [ ] 3. Add or update tests: TODO
- [ ] 4. Update affected docs: TODO
- [ ] 5. Verify acceptance criteria for TODO
```

Each item must be completable on its own and trace to the proposal, design, or spec delta. Do not write "implement everything". Include test tasks, not only implementation tasks.

### Spec delta

```md
# Capability: TODO

## ADDED Requirements

### Requirement: TODO
The system SHALL TODO.

#### Scenario: TODO
- GIVEN TODO
- WHEN TODO
- THEN TODO
```

Every requirement has at least one testable scenario and traces to a `RULE-*` or acceptance criterion.

## Lightweight change record

Grade S does not enter this stage by default. If it needs a durable record under the conditions in [lifecycle.md](lifecycle.md), use [templates/change-record.md](../templates/change-record.md) with a kebab-case name under `docs/changes/`.

## Harness gate

Before leaving this stage:

- Tasks include tests, not only implementation.
- Happy path, boundary, and exception are covered. Grade L adds concurrency, timeout, or malicious input.
- Tests default to not using real networks or real third parties.
- E2E covers only commercially critical paths.

For grade L, also open Red-Team from [lifecycle.md](lifecycle.md): races, downstream failure, malicious input, and boundaries that would mislead a successor in three months.
