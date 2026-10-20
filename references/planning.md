# Planning

Finish the requested planning outcome without silently starting delivery.

| Checkpoint | Completion evidence |
|---|---|
| Clarify | Goal, users, bounds and important unknowns are understandable |
| Design | Requested design, rationale and risk disposition are reviewable |
| Spec | Acceptance and implementation boundaries are executable; consequential unknowns have a disposition |

Infer the smallest requested checkpoint. Investigate before asking. Write only
requested artifacts and essential context. Use [design](design.md) for technical
decisions and [spec](spec.md) for an implementation-ready contract.

Experiments must fit authorization. When coding is prohibited, describe the
falsifiable validation plan and leave untested assumptions visible. A complete
document does not prove a design validated.

At the checkpoint, check consistency and sources, record remaining assumptions,
and set the planning record to `completed` at that stage. Recovery fields become
`none`; Closeout uses `verification: not-applicable`. Describe document review
under Decisions or Closeout; leave Evidence as `none` unless recording structured
observations in the record format. Keep it outside the delivery archive. Do not
run delivery acceptance, publish delivered behavior claims or automatically
accept proposed designs.

Report checkpoint, artifacts, consequential unknowns and next stage. When delivery
is later authorized, recheck mandate and evidence, set the same record to
`delivery` / `active` with `verification: pending`, regrade and continue from the
first unsatisfied checkpoint.
Preserve the earlier outcome in a brief decision note, not a duplicate track.
