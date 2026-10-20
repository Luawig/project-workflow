# Implement

Implement within the execution contract. Read relevant source, tests and decisions
before editing. On resumption use [lifecycle](lifecycle.md).

Advance dependency-ready tasks. Independent investigation and checks may run
concurrently; shared-file mutations need an owner and integration order. Use
subagents only when authorized and independence justifies coordination cost.

Mark observed task progress, but leave the record active while verification or
closeout remains. Targeted checks during implementation inform the work; Verify
assesses the complete contract.

If implementation exposes a design error, stop expanding affected work. Reopen the
decision, update the contract and invalidate affected evidence before continuing.
Regrade new consequences. Do not silently broaden scope because extra code exists.

Preserve tests for required behavior. Deleting assertions, widening tolerances or
disabling gates to manufacture success does not satisfy acceptance. Intentional
removal needs authorization and corresponding test/spec changes.

After repeated attempts without new information, change hypothesis or investigation
method. If the next useful action needs unavailable input, record `blocked` with
reason and resumption action. Do not use an arbitrary failure count instead of
diagnosis, or roll back unrelated user changes.

Before Verify, authorized implementation must be ready, drift recorded and relevant
tests present. Verification and closeout tasks may remain unchecked.
