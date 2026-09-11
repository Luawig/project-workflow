# Authority

Read this when closeout or design hits a conflict, or when a document uses an undefined "current". Each class of fact has one authority. Other locations keep short pointers. Authority for one class does not cancel closeout sync of the others.

## Fact classes

Do not merge these into one "current" claim.

| Class | Question | Authority | Not authority |
|---|---|---|---|
| Version commitment | What this version plans to deliver, and where the bounds are | `docs/product/scope.md` | Implementation evidence, stable specs, README summaries |
| Implementation | What the system actually does now | Code, tests, machine contracts in `contracts/` | README examples, stale comments, chat, unarchived deltas |
| Stable behavior | What delivered, verifiable positive behavior exists, and which prohibitions are in force now | Stable specs, default `openspec/specs/<capability>/spec.md` | Active change dirs, unimplemented plans, later candidates, verbal acceptance |
| Deferred / non-goals / N/A | What is later, explicitly out of scope, or not applicable | Later-candidate and non-goal lists in `scope.md`; completion status `out-of-scope` / `not-applicable` | Defect lists, implementation-gap reports, stable positive specs |
| Decisions and constraints | Why, trade-offs, and long-lived bans | Still-binding clauses in ADRs (when the project uses them), `docs/rules.md`, `AGENTS.md` | Intake source text, historical appendices, superseded records, roadmap items, third-party analyses |

Version commitment may include unfinished work. Unfinished items must carry an explicit status such as `not yet implemented` or `in progress`. They are not proof of delivery.

Implemented capability requires implementation evidence: code, tests, machine contracts, or runnable behavior when a runtime exists. Stable positive specs must match that evidence.

Currently effective prohibitions apply immediately as negative constraints and regression bounds, even when no matching feature implementation exists.

Undelivered version-commitment items belong in `scope.md`, the roadmap, architecture "not yet", or an active change. They must not be written as ordinary stable `SHALL` statements.

Later candidates, explicit non-goals, and not-applicable items are not implementation gaps. They must not enter stable positive specs or the stable acceptance baseline.

Decisions and constraints explain bounds. They do not replace implementation evidence or field-level machine contracts.

Field-level machine contracts belong to `contracts/` with implementation. `docs/protocols.md` lists entries and does not copy schemas.

If the project uses incremental migrations, the current schema is the owner's ordered migration set as applied. A single initial migration is not, by itself, the complete current schema. Ignore this paragraph when the project does not use migrations.

## Entry docs

Entry docs point at the single source for each class. They do not copy those facts in full.

| File | Keep only |
|---|---|
| Repo `README.md` | How to run, a short status pointer, pointer to `docs/` |
| `docs/README.md` | Doc map; pointers to version commitment, implementation status, and stable specs |
| `docs/product/scope.md` | Version commitment, explicit non-goals, later candidates |
| `AGENTS.md` | Bounds, commands, and required workflow the agent will get wrong without |
| `docs/overview.md` | Goals, non-goals, principles, terms |
| `docs/architecture.md` | Component bounds, implemented / not yet, runtime and deploy |
| git / changelog | History; not a spec, not version commitment, not implementation evidence |

Do not copy the full architecture, scope list, or stable spec into README, `AGENTS.md`, or overview.

## Conflicts

1. Name the fact class before resolving. Do not use "current" to stand for version commitment, implementation, and stable behavior at once.
2. Check implementation from code, tests, contracts, and runtime when needed.
3. Stable positive behavior must match implementation. Change the spec or the code. Do not leave both standing.
4. Currently effective prohibitions stay in force even without a matching feature implementation. Keep them in stable specs and the regression baseline.
5. Delivered items in `scope.md` must match implementation and the implemented list in `architecture.md`. Unfinished version-commitment items must appear as not-yet in architecture, not as stable delivered behavior.
6. Sync only still-binding hard constraints into `AGENTS.md`. Mechanism belongs in docs.
7. Decision records, reference analyses, and historical materials are not construction instructions merely because the files exist. Only still-binding clauses apply.
8. Resolved intake items must already exist as Facts, ADRs, or RULES, then leave Open Questions.

Do not skip closeout by declaring one class the only authority. Implementation with a stale stable spec, a spec archived without evidence, or a spec archived while unfinished work is written as delivered, is unfinished.

## Subtract before add

- Rewrite stale sections in place. Do not add `v2`, `new`, or `updated` parallel docs.
- When a capability is replaced, converge the stable spec, default reading order, and entry docs onto one surviving definition. Mark replaced docs `superseded`, point to the replacement at the top, and remove them from the default reading path. Do not leave two current definitions of the same behavior.
- Keep one explanation of each fact. Other locations use a path pointer.
- Leave history in git, changelog, or a clearly marked historical appendix, not in executable decision or spec bodies.
