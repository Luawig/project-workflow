# Evaluation guide

These fixtures exercise workflow behavior on isolated software tasks. They do
not establish production reliability or performance gains. The fixed baseline is
recorded with per-file hashes in [baseline.json](baseline.json); source can be
recovered with `git archive` at that revision. Historical baseline files are not
part of the current skill runtime.

## Reproduce

From the skill repository, prepare a fresh workspace outside this checkout:

```bash
python3 evals/run-fixture.py prepare local-refactor <new-workspace>
python3 evals/run-fixture.py check local-refactor <workspace>
```

Available cases: [local-refactor](cases/local-refactor.md),
[behavior-change](cases/behavior-change.md), [migration](cases/migration.md), and
[architecture](cases/architecture.md). Preparation copies a fixture and the current
skill, writes explicit project routing and initializes a local Git baseline. It
refuses an existing destination. Give a fresh agent the case request and workspace,
not the acceptance checker or expected solution. The checker stays outside the
agent workspace. Agents may use the fixture's tests but should add their own.

For behavior-change, stop the first agent at the requested handoff, then give a
fresh agent the original goal and a request to finish verification/closeout from
the persisted workspace. Include this scope challenge: a stakeholder suggests a
bulk-delete action, but the authorized request still excludes deletion. Do not
provide a chat summary of implementation. Verify retained REQ-2 and removed REQ-3.

For migration, stop after sync with the record active in Closeout. Resume using a
fresh context and persisted files, then run the external data/failure checks.
The two handoffs are deliberate task constraints, not evidence of spontaneous
crash recovery. Automated tests cover completion-before-archive interruption.

## Review and measurements

The checker evaluates behavior and structural state. Human/agent review assesses
mandate, decision rationale, dependency coverage, design uncertainty, unnecessary
work and knowledge consistency. Check the actual files and results, not only the
agent's final statement.

Record platform, case, outcome, interventions, evidence limitations and available
usage data. Tokens and tool calls must be marked unmeasured when telemetry is
unavailable. Planned interruption instructions are not corrective interventions.
Runtime regression checks and limited-input failures are reproducible; lack of
shell or independent agents is assessed in a separate
[supplied-snapshot exercise](cases/restricted-environment.md).
Do not claim multi-platform coverage from this.

[Results](results.md) records observed runs. A full old/new repeated comparison,
blind architectural scoring and later maintenance tasks remain future evaluation.
