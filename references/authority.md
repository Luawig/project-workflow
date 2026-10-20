# Authority and deviations

Keep accepted requirements separate from observed behavior. A reproducible
implementation defect does not authorize changing required behavior.

| Information | Owner | Use |
|---|---|---|
| User requirements and commitments | User decisions and designated requirements/scope source | Determines what is authorized and required |
| Accepted engineering decisions | Existing architecture, rules or accepted ADRs | Constrains implementation within the mandate |
| Observed implementation | Code, runtime, tests and machine contracts | Establishes observed behavior, with evidence limitations |
| Future ideas and non-goals | Existing scope/backlog owner | Bounds work; not a delivery defect |
| Execution status and evidence | Active change record | Coordinates work; does not replace requirements or tests |

A schema does not prove runtime behavior; a passing test does not prove every
requirement. Preserve deviations until resolved, even if completion is blocked.

## Conflict procedure

Identify conflicting statements and their sources, then classify:

| Class | Action |
|---|---|
| Implementation defect | Preserve requirement; fix within scope or record defect and block completion |
| Authorized requirement change | Record authorizing source; update affected requirements, implementation and tests together |
| Unauthorized expansion | Stop expansion; report deviation and proposed correction. Do not commit scope merely because code exists |
| Stale descriptive documentation | Correct against evidence without changing normative requirements |
| Insufficient evidence | Investigate or keep pending; do not choose the convenient source |

Use existing authorization. Ask only when the missing decision changes the
outcome, commitment or irreversible boundary. Decide reversible engineering
choices within the mandate and record the reason.

If code outside scope must remain unchanged, report that deviation explicitly.
Do not silently accept it or delete its regression tests. Independent authorized
work can continue.

## Knowledge ownership

Use one current owner for each requirement or decision; other locations link to
it. A record may snapshot its execution contract; after archive this is history,
not a competing current specification.

Correct descriptions in place. Preserve accepted decision history: add a new
decision with a supersedes link and point current guidance at effective clauses.
Do not rewrite old rationale to fit new code.

Separate future plans from implemented behavior. Planning completion does not
automatically accept a baseline. Deployment is distinct from working-tree
verification.
