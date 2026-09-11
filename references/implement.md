# Implement

Change code only after the spec is stable, or after grade S has an execution contract when no change artifact exists. Tasks come from OpenSpec-compatible `tasks.md`, the lightweight change record, or that grade S execution contract, not from a chat summary.

## Before starting

1. Read the active change proposal / design / tasks, the change record, or the grade S execution contract.
2. Read the docs, contracts, and tests listed in the spec or execution contract.
3. Confirm the execution contract still holds: goal, hard constraints, acceptance, stop conditions.
4. If this spans sessions, continue from the first unchecked task. Do not redo completed work.

Follow the active task list in order.

## Rules

- Advance tasks in order. Check each item off as soon as it is done.
- Hard constraints cannot be broken. Suggestions may change; record why in the task note or change record.
- Reuse existing tests and contracts as the spec. Do not write a parallel assertion language.
- On a design error: stop expanding code, update the spec and affected docs, then continue. Order is **change artifact → long-lived docs → code**. Do not write unimplemented work into stable specs as delivered.
- Drive-by refactors that touch behavior or contracts upgrade the change grade and need spec work.
- Do not delete, skip, or weaken assertions, or disable gates, to make tests pass.

## Docs during implementation

Change long-lived docs only when:

- Implementation shows a delivered claim is wrong.
- Interfaces or state values disagree with `contracts/` or the data model.
- A still-binding decision is required to continue; when the project uses ADRs, record it as an ADR.

When updating `contracts/`, paths and fields must match implementation, and so must `summary`, `description`, examples, and terms. Do not leave removed system models in that text.

Do not write a construction diary. Progress is the checked-off task list. Do not mark capabilities delivered or archive before verification.

## Done enough to verify

Before verification, the active spec or execution contract must have:

- Planned tasks checked off, or an explicit follow-up change the user agreed to split out.
- No unrecorded behavior change.
- New external fields or events present in the active change's contracts or spec deltas.

Then go to [verify.md](verify.md). Do not archive before verification. Do not treat checked-off tasks as a stable delivered spec.
