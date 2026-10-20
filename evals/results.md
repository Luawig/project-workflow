# Evaluation results

The 2026-10-20 evaluation covered four local software tasks, two prescribed
cross-session handoffs and a restricted-environment scenario. Results apply to
the fixtures and acceptance criteria in the [evaluation guide](README.md).

## Automated checks

| Check | Observed result | Scope |
|---|---|---|
| `python3 -m unittest discover -s tests -v` | 49 passed | Routing, fences, state, archive, record structure, evidence freshness, links, metadata and path handling |
| Same suite with Python 3.9.6 | 49 passed | Second interpreter on the same host |
| `python3 scripts/validate-workflow.py skill .` | Zero violations | Package resources, metadata and internal links |
| `python3 evals/run-fixture.py check <case> <workspace>` | Results below | External behavior, state and installed-skill integrity checks |
| Untouched fixture negative controls | All four rejected | Unfinished starting fixtures do not satisfy acceptance |

The primary regression interpreter was Python 3.14.3. Fixture agents reported
Python 3.8.6 and Python 3.13.5. The architecture task's structural check passed
with Python 3.8.6. This coverage is not a complete Python-version support matrix.

## Task outcomes

| Case | External checks | Observed outcome |
|---|---|---|
| [S local refactor](cases/local-refactor.md) | 3 passed | One normalization per string; preserved ordering, duplicates, Unicode and empty-value behavior; no workflow artifacts |
| [M behavior change](cases/behavior-change.md) | 4 passed | Exact-True filtering, preserved order and input, retained REQ-2 and authorized removal of REQ-3; one archived record |
| [L SQLite migration](cases/migration.md) | 7 passed | Data preservation, status constraints, invalid-input rejection, idempotency, safe rollback and transactional failure recovery; one archived record |
| [Architecture planning](cases/architecture.md) | 3 passed | Completed planning at Design; no code or probes; one record outside the delivery archive |

The M task resumed from Verify and excluded an unauthorized bulk-delete
suggestion. The L task resumed from active Closeout and completed its terminal
disposition. Both handoffs used fresh agent contexts and persisted files without
an implementation chat summary. Unexpected process termination was not tested.

Evaluator review found that the architecture proposal compared synchronous
processing with a background executor within the existing service and SQLite
boundary. It retained unknown workload targets, specified falsifiable validation
plans and identified conditions for reconsidering the recommendation. Design
quality and document consistency were reviewed by agents, without blind human
scoring. Task-local counterexample reviews disclosed their shared context.

The [restricted-environment scenario](cases/restricted-environment.md) kept
verification blocked, identified the missing execution environment and excluded
deletion. It reported automated checks as not run. This supplied-snapshot exercise
did not test another platform's file or shell integration.

## Method and applicability

Agents received isolated Git fixtures with explicit installation routes. The
external checker remained outside their workspaces, and installed skill files
were unchanged. Task outcomes were inspected and durable records were checked
with the validator included in this repository.

Delivery fixtures used development snapshots of v2; the architecture fixture
used the planning-state and Python 3.8-compatible rules. These are bounded
acceptance observations, not identical-version comparative trials. Reproduction
uses the checked-out skill version; record its revision with new results.

The historical baseline and file hashes are in [baseline.json](baseline.json).
All 19 hashes matched the pinned Git revision. No repeated matched comparison
against that baseline was performed.

## Cost and limitations

| Metric | Observation |
|---|---|
| Cross-session recovery | Both prescribed handoffs completed |
| Workflow records | S: 0; M, L and architecture: 1 each |
| Record size in UTF-8 bytes | M: 6,806; L: 9,403; architecture: 23,615 |
| Human clarification or correction during fixture execution | None observed; prescribed handoff and scope-challenge prompts were supplied |
| Tokens, total tool calls, wall time and monetary cost | Unmeasured |

Runs included agent retries and evaluator corrections, so intervention counts do
not establish first-attempt success. The architecture record is lengthy for a
small fixture; its context cost needs measurement before setting format limits.
Evidence-maintenance cost has not been measured in repeated runs.

The validator checks recorded structure and fingerprints. Semantic requirement
coverage, evidence truthfulness and dependency completeness require review.
The external M checks assess retained requirements separately. Migration checks
cover the fixture's one-table schema, not arbitrary database evolution.

Production reliability, quantified efficiency gains and multi-platform behavior
remain untested. Further evaluation needs repeated matched tasks, usage telemetry,
real maintenance work, unplanned interruptions and blind design review.
