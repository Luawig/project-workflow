# Closeout

Complete affected knowledge sync before marking delivery complete. Keep the
record discoverable until these actions finish.

1. Confirm acceptance evidence still applies. Resolve deviations through
   [authority](authority.md), including unexpected implemented capabilities.
2. Apply authorized spec edits to their owner, preserve unrelated requirements,
   inspect the consolidated result and run affected regressions.
3. Update affected descriptive docs, requirement owners and current constraint
   pointers. Separate unimplemented plans. Do not create unrelated documentation.
4. Check evidence against final code and acceptance. Rerun affected checks after
   relevant code, contract or meaningful documentation changes.
5. Record verification and knowledge-sync disposition. Keep `stage: closeout` /
   `status: active` until checks pass; run project structural validation.
6. Set `status: completed`, clear recovery fields to `none`, then move delivery
   records to `docs/changes/archive/YYYY-MM-DD-<slug>.md`. Validate again. A crash
   between completion and move is recoverable.

Do not archive failed or missing acceptance. User-cancelled/replaced work can
become `cancelled`; describe remaining changes and their disposition before
archiving. Cancellation does not authorize deleting or reverting them.

Completed planning records stay outside the delivery archive at their checkpoint.
Archived evidence describes its recorded baseline, not today's system.

S without a record reports targeted evidence and affected knowledge sync; no
fabricated completion matrix or archive is needed.

## Report

Report outcome, evidence and limitations, affected artifacts and residual risks.
Distinguish branch verification from release. Report unfinished work as active or
blocked.

Publication, deployment, merge and destructive cleanup follow existing user
authorization and platform permissions. Preview destructive effects and ask only
for authorization still missing; do not ask again for an already authorized
concrete action.
