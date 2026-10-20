# Lifecycle

Choose intent, consequence and evidence before choosing documents. Stages are
checkpoints; a satisfied checkpoint needs no duplicate work.

## Triage

Read project instructions, relevant document entries, code and tests. Use existing
locations; no particular product or architecture directory is required. Find
matching records under `docs/changes/`, including completed records awaiting
archive. Match by goal and scope rather than recency.

Record in context, or in a record when required: intent (`planning` or `delivery`),
authorized outcome, planning checkpoint, grade and reasons, current stage,
acceptance sources and next action. A new idea alone does not authorize coding.

## Grade by consequence

Use the highest matching grade. Uncertainty matters when it could invalidate the
main solution, not merely because implementation details are unknown.

| Grade | Consequences | Required rigor |
|---|---|---|
| S | Local change without changing user-visible behavior, external contracts, data model, security boundaries or product scope | Execution contract in context; targeted verification; affected-surface closeout |
| M | Bounded behavior change using established architecture, with no L trigger | Durable record; acceptance scenarios; relevant regression and contract checks |
| L | Architecture boundary, external contract, migration, security, irreversible operation, multi-module coupling, or uncertainty that could overturn the solution | Durable record; affected design decisions; risk validation and counterexample review |

Project instructions can add consequence-based gates. Regrade when evidence
changes consequences; complete missing checks before expanding the work.

## Record policy

One-session S work creates no workflow artifact. Cross-session S and all M/L use
one [record](record-format.md). Persist the contract and next action before a
foreseeable interruption. Planning M/L also uses a record, but only requested
planning artifacts are added.

Reference existing docs and tests. Create a separate PRD, architecture document
or ADR only for a requested artifact or a decision needing a long-lived owner.
No fixed documentation tree or spec system is installed as a side effect.

## Stage contracts

| Stage | Enter when | Exit evidence | On failure |
|---|---|---|---|
| Triage | New request or recovery | Intent, grade, mandate, checkpoint and next stage | Resolve conflicting request or missing mandate |
| Clarify | A consequential requirement or assumption is unclear | Goal, bounds and acceptance intent are usable; remaining unknowns do not block the next action | Investigate or ask the decision owner |
| Design | An affected decision or technical risk needs work | Quality scenarios, boundaries, decision reasons and risk disposition | Validate the assumption or return to Clarify |
| Spec | Acceptance or implementation boundaries need definition | Executable goal, non-goals, sourced constraints, acceptance and dependent tasks | Return to unresolved requirement or design |
| Implement | Execution contract holds | Authorized changes and tests are ready; drift is recorded | Fix locally or reopen affected decision |
| Verify | Behavior or requested acceptance needs checking | Current evidence for applicable acceptance; failures resolved | Return to Implement/Spec or block on missing environment |
| Closeout | Verification passed | Affected knowledge consistent; no unapproved deviation; disposition recorded | Keep active or blocked |

Planning ends at the requested Clarify, Design or Spec checkpoint using
[planning](planning.md). Delivery proceeds to Closeout. S can go directly from
Triage to Implement when its execution contract is clear.

## State and interruption

`stage` identifies the checkpoint; `status` is independent of task checkboxes:

- `active`: an actionable next step exists.
- `blocked`: progress requires a missing decision, permission, dependency or
  environment. Record the reason and resumption action. Independent authorized
  work may continue.
- `completed`: the requested outcome is satisfied. Planning completes at
  Clarify/Design/Spec; delivery completes only at Closeout.
- `cancelled`: the user cancelled or explicitly replaced the request. Record
  disposition of partial changes; cancellation grants no rollback permission.

Before interruption, update stage, status, next action, decisions and evidence
in the same record. Do not create a parallel progress log.

On resumption:

1. Read project instructions, the matching record and its recovery section, then
   only the affected sources.
2. Inspect actual files and workspace changes. Confirm the mandate and
   consequential assumptions still hold.
3. Recheck evidence applicability. Changed code, contracts or acceptance
   invalidate affected evidence.
4. Continue from stage and next action, not the first unchecked box. All code
   tasks may be checked while verification is blocked.
5. If delivery is completed but still active on disk, finish archive after
   confirming closeout remains valid. Do not repeat implementation.

Archived records are history, not proof of the current system.
