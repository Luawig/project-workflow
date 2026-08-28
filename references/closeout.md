# Closeout

After verification, make implementation, stable specs, project docs, and agent rules point at the same current facts. Archive is one step of closeout.

Destructive cleanup is not default. Preview and get user confirmation before deleting branches, worktrees, or temp artifacts.

## Completion surfaces

Assign a status from the project facts: `verified-current` | `changed-and-verified` | `pending` | `out-of-scope` | `not-applicable`.

| Surface | Question | Typical evidence |
|---|---|---|
| Code | What is actually implemented? | Branch, tests, schema, config |
| Runtime | What does the user get? | Startable service, real API/page; N/A if there is no runtime entry |
| Behavior spec | Do stable specs cover current behavior? | OpenSpec-compatible `openspec/specs/` or completion conditions in an archived change record |
| Docs | Do humans and later agents see the current answer? | scope, README, architecture, rules |
| Rules | Are agent constraints the same source and executable? | `AGENTS.md`, this skill's routing |
| Workspace | Is leftover change work still unintegrated? | Active changes, throwaway plan docs |

Do not invent runtime when there is no deploy. Without an OpenSpec-compatible spec, the behavior surface lands in long-lived acceptance criteria.

Grade S lite closeout checks only:

- the targeted verification result;
- current docs directly affected by the change;
- whether a change record was created and, if so, archived.

Do not manufacture a full completion matrix, sync unrelated docs, or create missing project documentation for grade S.

## Required actions

1. **Archive specs**
   - OpenSpec-compatible: merge deltas into `openspec/specs/`. Do not leave a fully completed change in the active directory. Purpose must not be a placeholder.
   - Lightweight record: move to `docs/changes/archive/`.
   - Current capabilities must exist on the stable layer, not only in the change directory.
2. **Sync scope**
   - Move delivered capabilities from later candidates and PRD Out of Scope into current scope.
   - Write remaining unfinished parts as a clear boundary. Do not mix them into one "not in this version" sentence with delivered work.
   - `roadmap.md` keeps only undelivered milestones.
3. **Promote doc status**
   - Landed docs: `draft` → `accepted`.
   - Replaced specs: `superseded`, pointing at the replacement.
4. **Compact intake**
   - Keep only unresolved items.
   - Define any cited FACT that is missing.
   - Do not paste the same source twice.
5. **Align entry docs**
   - `docs/README.md`, repo `README.md`, and `AGENTS.md` implemented / not-yet lists match `scope.md`.
   - Do not copy the full architecture into those three files.
6. **Subtract before add**
   - Delete or rewrite stale current claims, completed todos, and duplicate pointers.
   - Session leftover plans: merge still-valid content into official docs; give the user a deletion candidate list.

## Closeout gate

- No fully checked OpenSpec-compatible change remains active and unarchived.
- `openspec/specs/` (if used) covers current capabilities, not only the first archive.
- `scope.md`, architecture implemented lists, README current status, and `AGENTS.md` do not contradict each other.
- Every cited `FACT-N` is defined.
- Every completion surface has a status. Unverified work is not marked done.

## Scope sync after delivery

Once the capability is in code:

1. Move it from later candidates in `scope.md` to current scope.
2. Remove "this version does not implement X" from PRD Out of Scope. If part of X is still undone, say which part.
3. Keep delivered scenarios in user stories and acceptance criteria.
4. Align repo README current status with `scope.md`.

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
- Docs:
- Rules:
- Workspace:

**Changes**
- <file> — <why>

**Needs your confirmation**
- Delete candidates:
- Cannot decide:

**Left**
- pending / out-of-scope; write "none" if empty
```

Do not run destructive cleanup before the user confirms. "Clean up when done" in the original task does not replace confirmation after this report.
