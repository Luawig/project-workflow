# Lifecycle and grading

Read this at the start of every change to set grade, current stage, and the next exit. Do not copy the checklists into project docs.

## Intent before grade

First classify the request as `planning` or `delivery` with [planning.md](planning.md).

- `planning` may stop at Clarify or Design after the requested documents are coherent. It does not imply permission to implement.
- `delivery` continues through Spec when required, Implement, Verify, and Closeout.
- An ambiguous new-project idea starts as planning.

Intent controls how far to go. Risk grade controls how much rigor is needed within that path.

## Identify the change

Treat requirements, follow-ups, scope edits, design requests, implementation requests, doc sync, and reviews as one change.

Look for in-progress work first to avoid a parallel track:

1. Non-archive directories under `openspec/changes/`.
2. Lightweight change records under `docs/changes/` that are not archived.
3. A change name named by the user.

If one exists, continue from its unfinished stage when it matches the request. Otherwise enter Triage.

## Grading

Grade by **consequence**, not by line count.

| Grade | Any one of these |
|---|---|
| L | Architecture boundary, external protocol, data model, migration, auth/security, multi-module coupling, destructive cleanup, cross-repo contract |
| M | User-visible behavior, new capability, acceptance criteria, scope, external field semantics, new long-lived rules |
| S | Everything else: local bugs, refactors, copy, comments, test hardening, doc fixes that do not change a contract |

When unsure, use the higher grade. If a grade S change reveals behavior or contract changes during implementation, upgrade to M/L and complete design and spec before continuing.

Projects may add extra grade L triggers in `docs/change-workflow.md`. Use the table above when that file is absent.

## Paths

```text
Planning: Triage → Clarify → optional Design → requested checkpoint → stop
S delivery: Triage → Implement → Verify(targeted) → Closeout(affected surfaces)
M: Triage → Clarify → Design(delta) → Spec → Implement → Verify → Closeout
L: Triage → Clarify → Design → Spec → Implement → Verify → Closeout
    + Legacy / Architecture-Data / Red-Team (when triggered)
```

### Grade S minimum

Grade S creates no intake, design doc, spec, or change record by default. A clear goal and acceptance may stay in the active task context for a one-session local change.

Create a lightweight change record only when one of these is true:

- the work spans sessions;
- several agents or owners need a shared task list;
- acceptance or assumptions need a durable audit trail;
- the user asks for one;
- project rules require one.

Grade S updates long-lived docs only when their current facts changed. Verification runs the smallest relevant test or repeatable check. Closeout checks only affected surfaces and does not fabricate a full completion matrix.

M/L default to the OpenSpec-compatible layout. If the project sets `spec_system: change-record`, an equivalent testable change record is required, and closeout must write behavior into long-lived docs.

## Stage contracts

Each stage does only its own work. Do not enter the next stage until the exit conditions hold.

### Triage

- **Entry**: The user proposed a change, or an in-progress change needs re-grading.
- **Read**: This file. If they exist, read `docs/product/scope.md`, `docs/README.md`, and `AGENTS.md` first. Do not start from intake.
- **Output**: Intent, grade, path, target planning checkpoint if applicable, current stage, whether an existing change is reused.
- **Exit**: Grade and stage are recorded; the next playbook is chosen.
- **Rollback**: If an existing change conflicts with this request, report first, then merge or open a new change.

### Clarify

- **Entry**: Facts, scope, or decisions are still unclear.
- **Read**: [clarify.md](clarify.md)
- **Output**: Facts / Assumptions / Open Questions / Pending Decisions / Reference Signals. Long-lived facts are already in product or technical docs, not only in intake.
- **Exit**: Direction can continue. Direction-changing questions are resolved or explicitly parked and not needed this stage.
- **Rollback**: If the user retracts a fact, update Facts and the docs already written. Do not append a "latest version".

### Design

- **Entry**: Grade M/L, or a grade S upgrade needs scope, architecture, rules, or contract docs.
- **Read**: [design.md](design.md), [authority.md](authority.md)
- **Output**: Updates to affected `docs/` and `contracts/`; ADRs when needed.
- **Exit**: For planning, the requested checkpoint in [planning.md](planning.md) is coherent and the agent stops. For delivery, scope, non-goals, affected components, and rules can support spec work. Grade L delivery must have an architecture or ADR landing.
- **Rollback**: If design contradicts product scope, change `scope.md` first, then technical docs.

### Spec

- **Entry**: Design is stable, or grade S needs a traceable implementation brief.
- **Read**: [spec.md](spec.md), [spec-system.md](spec-system.md)
- **Output**: An OpenSpec-compatible change, or `docs/changes/<name>.md`.
- **Exit**: Goal, non-goals, hard constraints, acceptance scenarios, and tasks are complete. M/L behavior changes trace to a spec requirement.
- **Rollback**: If requirements are still moving, stay in Design/Clarify. Do not create a spec.

### Implement

- **Entry**: Spec meets implementation conditions, or grade S has an execution contract.
- **Read**: [implement.md](implement.md)
- **Output**: Code and tests advanced by task; tasks checked off; design drift written back to spec and docs.
- **Exit**: Claimed tasks are checked off, with no unrecorded scope drift.
- **Rollback**: If implementation exposes a design error, stop coding and return to Spec/Design.

### Verify

- **Entry**: Implementation is claimed complete, or the user asks for acceptance.
- **Read**: [verify.md](verify.md)
- **Output**: Evidence run at the change's risk; anti-cheat checks; a list of failures.
- **Exit**: Applicable gates passed, or failures are reported and the change is not marked complete.
- **Rollback**: Failures return to Implement. If acceptance itself is wrong, return to Spec.

### Closeout

- **Entry**: Verification passed, or the user is reviewing docs / scope / rule consistency.
- **Read**: [closeout.md](closeout.md), [authority.md](authority.md)
- **Output**: Specs archived or promoted, scope and entry docs synced, stale current claims removed, completion-surface status.
- **Exit**: Every applicable surface has a terminal status; no fully completed change remains active; entry docs match scope.
- **Rollback**: If implementation conflicts with docs or specs and cannot be judged now, mark `pending`. Do not fake a finished closeout.

## Gate router

Run a gate only when it triggers. Write conclusions into the target docs or spec. Do not paste this table into the project.

| Trigger | Gate | Write back to |
|---|---|---|
| New requirement, scope change | Alignment: goals / non-goals / gray areas, terms, success and exception scenarios | intake, product docs, overview |
| Legacy system, migration | Legacy Boundary: anti-corruption layer, dependencies, characterization tests, rollback | architecture, service specs, ADRs, tasks |
| Architecture, protocol, data, ADR | Architecture/Data: trade-offs, idempotency, degradation, state machines | architecture, protocols, contracts, data-model, rules, ADRs |
| Concurrency, external deps, auth, untrusted input, high-risk migration | Red-Team: races, downstream failure, malicious input, misleading boundaries | risks, RULE, tests, tasks |
| Implementation done, scope drift, doc review | Closeout Evidence: code / runtime / spec / docs / rules / residue | scope, stable specs, doc status, AGENTS.md |

Grade S delivery defaults to targeted Verify plus affected-surface closeout. Grade M delivery adds Alignment, and Architecture/Data when interfaces or data are involved. Grade L delivery runs every matching row. Planning runs only gates needed for its requested checkpoint.

## Across sessions

When a change spans sessions, progress lives in OpenSpec-compatible `tasks.md` or the lightweight change record task list. Do not create `PROGRESS.md`, `TODO.md`, or `implementation-notes.md` by default.

A new session reads:

1. `AGENTS.md` and `docs/README.md` / `scope.md`
2. The active change or change record
3. Docs hit by this change

Then continue from the first unfinished task.
