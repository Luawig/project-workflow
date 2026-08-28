# Design

Turn clarified facts into product scope and a technical baseline. Update only docs this change hits. Do not create empty files to complete a directory.

If `docs/` already exists, update it. Do not rewrite. Product docs do not name classes, functions, or tables unless the user already did.

## Choose artifacts

Templates are a menu, not a checklist. Produce the documents the user requested plus the minimum prerequisites needed to keep them coherent.

| Need | Start with | Add only when needed |
|---|---|---|
| Clarify a new idea | `docs/product/scope.md` or the existing product entry | PRD when goals, users, and scenarios need a durable explanation |
| Define product behavior | `scope.md`, requested PRD / stories / acceptance docs | `roadmap.md` after a delivered baseline exists |
| Design a system | Minimum product context + `docs/architecture.md` | rules, data model, protocols, service specs, ADRs for decisions this design actually touches |
| Define an external interface | `docs/protocols.md` as inventory | OpenAPI / AsyncAPI in `contracts/` for field-level contracts |
| Evaluate a reference project | `docs/references/third-party-analysis.md` | ADR only if the analysis leads to a decision |

For a brand-new, one-sentence idea, the first planning pass should normally create at most one coherent product artifact and an explicit Open Questions list. Expand the document set only as the user advances the planning checkpoint.

`scope.md` is required once product scope is being defined, not for every local change. Grade M updates only affected files, but scope changes must sync `scope.md`.

## Status

Docs: `draft` | `accepted` | `superseded`.

- `draft`: scope or design is still changing.
- `accepted`: implementation baseline. After end-to-end delivery, overview, architecture, rules, current product docs, and current service specs must move here.
- `superseded`: must not be implemented. The top of the file points at the replacement.

ADRs: `proposed` | `accepted` | `superseded`. Partial replacement stays `accepted` and lists still-valid vs retired clauses at the top.

## Writing rules

- System constraints are `RULE-*` and must be checkable.
- Design principles are `PRINCIPLE-*`.
- Every user story maps to one role and one core scenario.
- Acceptance criteria must be testable. Do not use "good experience" or "fast enough".
- Service specs state both responsibilities and non-responsibilities.
- ADRs record the decision, alternatives, impact, and reversal cost. Not generic background.
- Third-party references become this project's rules, interfaces, architecture choices, or ADRs.
- `architecture.md` must split "implemented" and "not yet". `scope.md` and the repo README cite those lists instead of writing a third copy.
- Do not say "X is out of scope" in product docs while technical docs or code already delivered X.
- REST/WS field examples live only in `contracts/`.

## Architecture/Data gate

When architecture, protocol, data, or an ADR is involved:

- The ADR records trade-offs, downsides, and reversal cost.
- Core writes define idempotency and duplicate-request semantics.
- External-dependency failure has a degradation path.
- Core entities have states and illegal-transition constraints.

## Legacy Boundary gate

When integrating a legacy system or migrating:

- New logic reaches old APIs or dirty data through an anti-corruption layer.
- Direct deps, indirect deps, cron, messaging, and fallback paths are listed.
- Untested legacy code gets characterization tests first.
- Migration has canary, verification, and rollback.

## Templates

Use these skeletons only for selected artifacts. Keep the structure of existing docs and fill missing sections only.

### `docs/product/scope.md`

```md
# Scope

## Status
draft

## Current version
- TODO

## Out of scope
- TODO

## Later candidates
- TODO

## Scope change rules
RULE-SCOPE-1: New core user scenarios must update the PRD and acceptance criteria.
RULE-SCOPE-2: Scope changes that affect architecture, protocol, or the data model must create or update an ADR.
```

### `docs/product/prd.md`

```md
# Product requirements

## Status
draft

## Background
TODO

## Goals
- GOAL-1: TODO

## Non-goals
- NON-GOAL-1: TODO

## User roles
### Role A
- Goal: TODO
- Pain: TODO
- Success: TODO

## Core scenarios
### Scenario A
- Trigger: TODO
- User action: TODO
- System response: TODO
- Success: TODO

## Scope
### In Scope
- TODO
### Out of Scope
- TODO

## Acceptance summary
- AC-1: TODO

## Open Questions
- TODO
```

### `docs/product/user-stories.md`

```md
# User stories

## Status
draft

## Stories

### STORY-1
As a [role], I want [capability] so that [value].

#### Acceptance
- GIVEN TODO
- WHEN TODO
- THEN TODO
```

### `docs/product/acceptance-criteria.md`

```md
# Acceptance criteria

## Status
draft

## Global
- AC-1: TODO

## Scenario acceptance
### Scenario A
- GIVEN TODO
- WHEN TODO
- THEN TODO

## Non-functional
- Performance: TODO
- Security: TODO
- Observability: TODO
- Compatibility: TODO

## Not accepted
- TODO
```

### `docs/README.md`

```md
# Docs

## Reading order
1. `docs/product/scope.md`
2. `docs/overview.md`
3. `docs/architecture.md`
4. As needed: rules, protocols, services, ADRs

## Delivered
- TODO

## Not yet built
- TODO

## Contracts
- HTTP: `contracts/http/openapi.yaml`
- WebSocket: `contracts/ws/asyncapi.yaml`
```

### `docs/overview.md`

```md
# Overview

## Status
draft

## Scope
TODO

## Goals
- TODO

## Non-goals
- TODO

## Principles
PRINCIPLE-1: TODO

## Concepts
- TODO

## Glossary
- TODO

## Open Questions
- TODO
```

### `docs/architecture.md`

```md
# Architecture

## Status
draft

## Chosen architecture
TODO

## Components
### ComponentA
- Responsibilities: TODO
- Non-responsibilities: TODO
- Upstream: TODO
- Downstream: TODO

## Implemented
- TODO

## Not yet built
- TODO

## Architecture rules
RULE-ARCH-1: TODO

## Runtime flow
1. TODO

## Deploy model
TODO
```

### `docs/rules.md`

```md
# Rules

## Status
draft

## Global
RULE-GLOBAL-1: TODO

## Module rules
### ComponentA
RULE-COMPONENT-A-1: TODO

## Invalid patterns
- TODO
```

### `docs/protocols.md`

```md
# Protocols

## Status
draft

## Scope
Interface inventory. Field-level contracts live in `contracts/`.

## Where to look

| Want | Go to |
|---|---|
| HTTP API | contracts/http/openapi.yaml |
| WebSocket | contracts/ws/asyncapi.yaml |
```

### `docs/data-model.md`

```md
# Data model

## Status
draft

## Entities
### EntityA
- id: TODO
- state: TODO

## Transitions
TODO_STATE_A -> TODO_STATE_B

## Constraints
RULE-DATA-1: TODO
```

### `docs/decisions/ADR-0001-title.md`

```md
# ADR-0001 Title

## Status
proposed

## Context
TODO

## Decision
TODO

## Alternatives
- Option A: TODO
- Option B: TODO

## Consequences
- Positive: TODO
- Negative: TODO
- Reversal cost: TODO

## Related
- `docs/architecture.md`
```

### `docs/references/third-party-analysis.md`

```md
# Third-party reference analysis

## Status
draft

## Subject
- Name: TODO
- Source: TODO
- Why: TODO

## Adopt
- TODO

## Do not adopt
- TODO, because: TODO

## Adapt
- TODO, adaptation: TODO

## Risks
- TODO
```
