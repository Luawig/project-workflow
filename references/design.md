# Design

Make affected decisions defensible before expensive implementation. Reuse
established architecture for bounded changes; the stage alone does not require
a design document.

## Decision loop

1. Identify drivers from core scenarios, operating constraints, the existing
   system and stakeholder priorities. Select quality scenarios that could change
   the solution: context, stimulus, expected response and acceptance method.
   Unknown thresholds stay unknown; investigate or ask their owner.
2. Establish affected responsibilities, exclusions, data ownership, trust
   boundaries, dependencies and runtime paths. Add diagrams only when they
   resolve a boundary or interaction question.
3. Compare viable alternatives for costly, hard-to-reverse or disputed choices,
   including retaining the current approach or a smaller change. Compare against
   actual drivers, not generic lists of advantages.
4. Identify the assumption most likely to invalidate the preferred approach.
   Define a bounded probe, failure criterion, cost boundary and resulting decision.
   Run only within authorization. Failure reopens the decision.
5. Record choice, evidence, costs, applicability and reconsideration trigger.
   Connect quality scenarios to acceptance and implementation tasks.
6. State residual risks, detection and containment. A future investigation is
   not evidence that a risk is resolved.

Keep bounded decisions in the record. Use an existing architecture owner or ADR
only when the decision needs an enduring owner. Select shapes from
[design templates](../templates/design-artifacts.md) only when needed.

## Triggered checks

| Consequence | Questions and evidence |
|---|---|
| Core writes, retries, concurrency | Duplicate identity, atomicity, race and partial-failure behavior |
| External dependencies | Timeout, malformed response, outage and recovery checks |
| Security, untrusted input | Trust boundary, authorization, isolation and relevant abusive inputs |
| Legacy integration | Affected direct/indirect callers and characterization tests; add an adapter only for a real incompatibility |
| Migration | Data invariants, partial failure, transition compatibility, repeat execution, rollback or forward repair rehearsal |
| Operations | Failure signals, stop conditions, rollout boundary and recovery; do not assume reversibility |
| Maintainability | A likely follow-up change and the boundaries it would cross |

## Counterexample review

For L changes, review design before implementation and results before closeout.
Focus on high-risk assumptions and adversarial scenarios.

When independent agents are available and delegation is authorized, supply the
requirements, raw artifacts and bounded review question without the preferred
conclusion. Otherwise perform a separate pass and state that it shares the
implementer's context. A role label does not establish independence.

Resolve findings into a decision, test, task or explicitly accepted residual risk.
A review receipt alone is not a quality gate. Unresolved findings that invalidate
acceptance or violate constraints block completion.

## Exit

Affected boundaries, decision basis, risk disposition and verification plan must
support implementation. Planning may finish with a reviewable proposal; it must
not claim an unrun probe passed.
