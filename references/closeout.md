# Closeout

After verification, align version commitment, implementation, stable specs, tests, project docs, and agent rules. Archive is one step of closeout, not a substitute for proving delivery.

Destructive cleanup is not default. Preview and get user confirmation before deleting branches, worktrees, or temp artifacts.

## Completion surfaces

Assign a status from the project facts: `verified-current` | `changed-and-verified` | `pending` | `out-of-scope` | `not-applicable`.

| Surface | Question | Typical evidence |
|---|---|---|
| Code | What is actually implemented? | Branch, tests, schema, config |
| Runtime | What does the user get? | Startable service, real API/page; N/A if there is no runtime entry |
| Behavior spec | Do stable specs cover delivered behavior and currently effective prohibitions? | OpenSpec-compatible `openspec/specs/` or completion conditions in an archived change record |
| Tests | Do stable tests protect only delivered behavior and currently effective prohibitions? | Stable suite vs spec and version commitment |
| Docs | Do humans and later agents see version commitment, implementation status, and stable specs without mixed "current" claims? | scope, README, architecture, rules |
| Rules | Are agent constraints the same source and executable? | `AGENTS.md`, this skill's routing, still-binding decision clauses |
| Workspace | Is leftover change work still unintegrated? | Active changes, throwaway plan docs |

Do not invent runtime when there is no deploy. Without an OpenSpec-compatible spec, the behavior surface lands in long-lived acceptance criteria.

`out-of-scope` and `not-applicable` are not implementation gaps. Do not report later candidates or explicit non-goals as missing delivery.

Grade S lite closeout checks only:

- the targeted verification result;
- the docs this change directly affected;
- whether a change record was created and, if so, archived.

Do not manufacture a full completion matrix, sync unrelated docs, or create missing project documentation for grade S.

## Required actions

1. **Archive specs**
   - OpenSpec-compatible: merge into `openspec/specs/` only positive requirements that are delivered and evidenced, plus currently effective prohibitions. Do not leave a fully completed change in the active directory. Purpose must not be a placeholder.
   - Do not archive unimplemented version-commitment items, later candidates, explicit non-goals, or placeholders such as "add fields, RPCs, or contracts during implementation" as ordinary stable `SHALL`.
   - Lightweight record: move to `docs/changes/archive/`. Write only delivered, evidenced behavior into long-lived docs.
   - When OpenSpec-compatible specs are used, delivered capabilities must exist there, not only in the change directory. Archive does not by itself prove they are delivered.
2. **Sync version commitment**
   - Move actually delivered capabilities from later candidates and PRD Out of Scope into version commitment, and mark them delivered.
   - Keep unfinished version-commitment items in `scope.md` with explicit status. Do not mix them into one delivered sentence, and do not write them as stable `SHALL`.
   - `roadmap.md` keeps only undelivered milestones.
3. **Promote doc status**
   - Docs that now record the agreed baseline: `draft` → `accepted`. Unfinished version-commitment items in those docs stay explicitly not yet or in progress.
   - Replaced specs or wholly replaced decisions: `superseded`, pointing at the replacement, and removed from the default reading path.
   - Partially replaced decisions: still-binding clauses remain in the executable Decision section; retired clauses are only in a historical appendix, or the whole record is `superseded`. A top-of-file "superseded" note is not enough if retired clauses still read as instructions.
4. **Compact intake**
   - Keep only unresolved items.
   - Define any cited FACT that is missing.
   - Do not paste the same source twice.
5. **Align entry docs**
   - `docs/README.md`, repo `README.md`, and `AGENTS.md` point at `scope.md` for version commitment and at architecture for implemented / not yet. They do not copy those lists in full, and they do not contradict them.
   - If a capability was replaced, the default reading order and entry docs point at the surviving definition only.
6. **Subtract before add**
   - Delete or rewrite stale delivered claims, completed todos, and duplicate pointers.
   - Third-party analyses that were rejected or replaced must not describe those options in the present tense as currently adoptable.
   - Machine contracts in `contracts/` must match implementation in paths and fields, and in `summary`, `description`, examples, and terms. Removed system models must not remain in that text.
   - Session leftover plans: merge still-valid content into official docs; give the user a deletion candidate list.

## Closeout gate

- No fully checked OpenSpec-compatible change remains active and unarchived.
- `openspec/specs/` (if used) covers delivered capabilities and currently effective prohibitions, not unimplemented plans.
- `scope.md` version commitment, architecture implemented / not-yet lists, README status pointers, stable specs, stable tests, and `AGENTS.md` do not contradict each other.
- Every cited `FACT-N` is defined.
- Every completion surface has a status. Unverified work is not marked done.
- Implementation and stable positive specs do not retain opposite facts. If they conflict, the closeout chooses to change the spec or the code.

## Scope sync after delivery

Once the capability is evidenced in code:

1. Record it as delivered in `scope.md` version commitment. If it was a later candidate or listed as out of scope, move it.
2. If part of the capability is still undone, name that part as unfinished version commitment or as later / out of scope. Do not write the unfinished part as delivered.
3. Keep delivered scenarios in user stories and acceptance criteria. Leave undelivered positive acceptance in the active change until this closeout.
4. Align architecture implemented / not yet with implementation evidence. Align repo README status pointers with `scope.md` and architecture; do not copy the full lists.

## Report

List only items with action value:

```text
## Change closeout

**Grade**: S | M | L
**Spec**: OpenSpec-compatible <name> archived | lightweight record archived | none

**Surfaces**
- Code:
- Runtime:
- Behavior spec:
- Tests:
- Docs:
- Rules:
- Workspace:

**Changes**
- <file> — <why>

**Needs your confirmation**
- Delete candidates:
- Cannot decide:

**Left**
- pending / out-of-scope / not-applicable / unfinished version commitment; write "none" if empty
```

Do not run destructive cleanup before the user confirms. "Clean up when done" in the original task does not replace confirmation after this report.
