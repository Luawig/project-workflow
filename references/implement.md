# Implement

Change code only after the spec is stable. Tasks come from OpenSpec-compatible `tasks.md` or the lightweight change record, not from a chat summary.

## Before starting

1. Read the active change proposal / design / tasks, or the change record.
2. Read the docs, contracts, and tests listed in the spec.
3. Confirm the execution contract still holds: goal, hard constraints, acceptance, stop conditions.
4. If this spans sessions, continue from the first unchecked task. Do not redo completed work.

Follow `tasks.md` (or the change-record task list) in order.

## Rules

- Advance tasks in order. Check each item off as soon as it is done.
- Hard constraints cannot be broken. Suggestions may change; record why in the task note or change record.
- Reuse existing tests and contracts as the spec. Do not write a parallel assertion language.
- On a design error: stop expanding code, update the spec and affected docs, then continue. Order is **change artifact → long-lived docs → code**.
- Drive-by refactors that touch behavior or contracts upgrade the change grade and need spec work.
- Do not delete, skip, or weaken assertions, or disable gates, to make tests pass.

## Docs during implementation

Change long-lived docs only when:

- Implementation shows a current claim is wrong.
- Interfaces or state values disagree with `contracts/` or the data model.
- A new ADR is required to continue.

Do not write a construction diary. Progress is the checked-off task list.

## Done enough to verify

Before verification, the active spec must have:

- Planned tasks checked off, or an explicit follow-up change the user agreed to split out.
- No unrecorded behavior change.
- New external fields or events present in contracts or specs.

Then go to [verify.md](verify.md). Do not archive before verification.
