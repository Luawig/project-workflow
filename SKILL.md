---
name: project-workflow
description: >-
  Guide a software change through planning or delivery, with proportionate
  design, acceptance evidence, and recoverable closeout. Use for project
  planning, implementation, or delivery consistency work, and when project
  instructions require this workflow.
---

# Project workflow

Deliver the authorized outcome with evidence proportionate to its consequences.
Planning is a complete outcome when that is what the user requested.

## Start

1. Read project instructions and inspect relevant code, tests and docs. Direct
   invocation works without installing a project routing block.
2. Read [lifecycle](references/lifecycle.md) to choose intent, risk, checkpoint
   and current stage. Reuse a matching active record instead of opening another.
3. Load only the current stage's guidance below. Existing evidence can satisfy a
   stage without a new document or another user interaction.
4. Keep a one-session S task in context. For other work, use one
   [change record](templates/change-record.md), governed by the
   [record format](references/record-format.md).

## Invariants

- Implementation does not authorize changing requirements. Resolve conflicts
  using [authority](references/authority.md), without weakening acceptance.
- Decide reversible engineering choices within the mandate. Ask when a missing
  decision changes goals, commitments or an irreversible boundary.
- Missing evidence stays missing. A checked task, successful command or merged
  PR does not establish acceptance.
- Bind verification to relevant code and acceptance. Recheck affected evidence
  after either changes.
- Finish verification and affected knowledge sync before completion and archive.
- Publication, deployment, merge and destructive cleanup follow existing user
  authorization and platform permissions; completion adds no authority.

## Load by need

| Need | Resource |
|---|---|
| Grade, stage, interruption or resumption | [Lifecycle](references/lifecycle.md) |
| Planning without implementation | [Planning](references/planning.md) |
| Missing requirements or competing statements | [Clarify](references/clarify.md) |
| Architecture, costly decisions or uncertainty | [Design](references/design.md) |
| Acceptance and existing specification changes | [Spec](references/spec.md) |
| Code changes and dependency scheduling | [Implement](references/implement.md) |
| Acceptance evidence and failure handling | [Verify](references/verify.md) |
| Knowledge sync and terminal disposition | [Closeout](references/closeout.md) |
| Requirements, decisions and implementation disagree | [Authority](references/authority.md) |
| Create or validate a durable record | [Record format](references/record-format.md) |
| Requested design document or ADR | [Design templates](templates/design-artifacts.md) |
| Specification edits or review evidence | [Spec templates](templates/spec-artifacts.md) |
| Formal project installation | [Routing block](templates/agents-block.md) |

Use the project's document language, otherwise the user's language. Keep code
identifiers unchanged. Reuse existing document owners, contracts and tests;
templates are optional shapes, not a required document tree.

## Structural checks

With Python 3, run this skill's `scripts/validate-workflow.py` as described in
[record format](references/record-format.md#validation). `project` checks the
consuming project; `skill` checks this package. These read-only checks do not
prove requirement coverage or implementation correctness.

Without Python or shell access, perform the same field, routing, state and
archive checks manually. Report automated validation as not run. Keep delivery
blocked if a required behavior check cannot be performed.
