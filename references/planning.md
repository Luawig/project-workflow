# Planning intent and checkpoints

Use this playbook when the user has an idea but has not authorized implementation, or explicitly asks to clarify, plan, design, or write only part of the documentation.

Planning is a valid terminal state for the current request. Do not treat it as an incomplete delivery run.

## Infer the intent

Choose intent before risk grade:

| Intent | Signals | Allowed work |
|---|---|---|
| `planning` | "help me think this through", "plan first", "write the PRD/design", "do not code yet", a new idea with no implementation request | Investigate, clarify, make decisions, and write only the requested or prerequisite planning docs |
| `delivery` | "implement", "build", "fix", "ship", or explicit approval to continue after planning | Follow the full risk-graded lifecycle through verification and closeout |

If a new-project idea is ambiguous, start with `planning`. Do not interpret an idea as authorization to write code.

## Choose a checkpoint

Infer the smallest checkpoint that satisfies the request. Ask only when different checkpoints would materially change the work.

| Checkpoint | Typical output | Stop when |
|---|---|---|
| `clarified` | Goals, users, non-goals, assumptions, open questions | The product direction is understandable |
| `product-defined` | `scope.md` plus the requested PRD, stories, or acceptance docs | Product scope and success are reviewable |
| `technically-designed` | Requested architecture, rules, data, protocol docs, and ADRs | Major technical decisions and risks are reviewable |
| `spec-ready` | Product and technical baseline sufficient to create an implementation spec | No direction-changing question blocks spec work |

The user may request one artifact, several artifacts, or an entire checkpoint. Produce only those artifacts and the minimum prerequisites needed to keep them coherent. Do not create a full documentation tree just because templates exist.

Examples:

- A one-sentence product idea normally starts at `clarified`.
- "Write a PRD and scope, no code" stops at `product-defined`.
- "Design the architecture only" creates the minimum product context plus the affected architecture / ADR docs, then stops at `technically-designed`.
- "Plan this until it is ready for implementation" stops at `spec-ready`; it does not create implementation tasks unless the user asked for a spec.

## Planning exit

Before stopping:

1. Update the requested docs in the project's existing structure.
2. Resolve contradictions among the docs touched in this run.
3. Keep unresolved items as Open Questions or Pending Decisions.
4. Report:
   - checkpoint reached;
   - artifacts created or updated;
   - assumptions and open decisions;
   - whether the plan is ready for the next checkpoint;
   - the next stage, without starting it.

Do not run implementation verification or delivery closeout. Do not archive the planning work. Leave document status `draft` unless the user explicitly accepts it as an implementation baseline.

## Resume as delivery

When the user later authorizes implementation:

1. Read the planning docs and current project rules.
2. Re-check unresolved direction-changing decisions.
3. Grade the implementation consequence.
4. Continue at Spec, or return to Clarify / Design if the planning baseline is not ready.

Do not repeat planning that is still current.
