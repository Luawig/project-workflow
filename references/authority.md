# Authority

Read this when closeout or design hits a conflict. Each class of fact has one current authority. Other locations keep short pointers.

## Three layers

| Layer | Question | Authority | Not authority |
|---|---|---|---|
| Implementation | What does it actually do now? | Code, tests, OpenAPI/AsyncAPI in `contracts/` | README examples, stale comments, chat |
| Behavior | What observable behavior should it have? | Stable specs, default `openspec/specs/<capability>/spec.md` | Active change dirs, unarchived deltas, verbal acceptance |
| Decisions and context | Why, how much in this version, long-lived constraints | `docs/product/scope.md`, ADRs, `docs/rules.md`, `AGENTS.md` | Intake source text, future roadmap items |

Field-level HTTP/WS contracts belong to `contracts/` in the implementation layer. `docs/protocols.md` lists entries and does not copy schemas.

## Entry docs

| File | Keep only |
|---|---|
| Repo `README.md` | How to run, current-status summary, pointer to `docs/` |
| `docs/README.md` | Doc map and delivered / not-yet-built lists |
| `docs/product/scope.md` | Current scope, explicit non-goals, later candidates |
| `AGENTS.md` | Bounds, commands, and required workflow the agent will get wrong without |
| `docs/overview.md` | Goals, non-goals, principles, terms |
| `docs/architecture.md` | Component bounds, implemented / not yet, runtime and deploy |
| git / changelog | History; not a current spec |

Do not copy the full architecture into README, `AGENTS.md`, or overview.

## Conflicts

1. Check implementation first: code, tests, contracts, and runtime when needed.
2. Behavior must match implementation. Change the spec or the code. Do not leave both standing.
3. `scope.md` must match implementation and the implemented list in `architecture.md`. Change scope docs first, then entry summaries.
4. Sync only still-valid hard constraints into `AGENTS.md`. Mechanism belongs in docs.
5. Resolved intake items must already exist as Facts, ADRs, or RULES, then leave Open Questions.

Do not skip closeout by declaring one layer the only authority. Implementation done with an stale spec, or a spec archived while scope still says "not in this version", is unfinished.

## Subtract before add

- Rewrite stale current sections in place. Do not add `v2`, `new`, or `updated` parallel docs.
- Mark replaced docs `superseded`, point to the replacement at the top, and remove them from the default reading path when needed.
- Keep one explanation of each fact. Other locations use a path pointer.
- Leave history in git or changelog, not in current doc bodies.
