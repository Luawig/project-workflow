# Verify

Verification answers whether the change actually met its contract, not whether a command exited 0. On failure, return to implementation or spec. Do not archive.

## Evidence levels

Use the highest layer you can. Mark missing layers `not-applicable` or `pending`:

| Level | Meaning | Not enough to claim |
|---|---|---|
| Implementation complete | This branch's code and tests match the tasks | Released |
| Gates passed | The project's existing lint / test / build / spec checks passed | Behavior matches product acceptance |
| Behavior verified | Hit acceptance scenarios, contracts, or stable specs | Matches production |
| Runtime | Real start path, page, or API matches docs | Knowledge closed |
| Knowledge closed | Docs, specs, and rules match implementation | See closeout |

A clean `git status` or a merged PR is not verification by itself.

## What to run

Use **commands the project already has**, sized to risk. Do not invent a toolchain, and do not lower thresholds to pass a gate.

1. Read the repo README, `AGENTS.md`, package scripts, or Makefile for real commands.
2. Run the acceptance commands yourself. If the environment is unreachable, record discovery as `pending`. Do not claim verification.
3. Check the test names or scenarios named in the spec, item by item.
4. Reverse-check critical gates: the failure case should fail. If nobody would notice a break, add a check or record the risk.

Grade S: related tests or a manual repro, with no fake pass.
Grade M: related tests + acceptance scenarios + contract/spec check.
Grade L: add migration/rollback or Red-Team items.

## Anti-cheat

These do not count as a pass:

- Deleting, skipping, or commenting out failing tests
- Weakening assertions, widening tolerances, or checking only "does not throw"
- Mocking the unit under test and claiming the behavior is correct
- `|| true`, ignoring gates, or lowering coverage floors
- Running an unrelated subset and reporting all green

If "tests must pass" conflicts with "do not change the implementation" and the code is actually buggy: lock current behavior and mark a known defect. Do not silently change the implementation or delete tests.

Baseline must not regress: do not reduce test count or hide existing failures without an explanation.

## Spec check

- OpenSpec-compatible spec: every requirement / scenario claimed done has evidence.
- Lightweight change record: completion conditions checked off one by one.
- Acceptance-criteria docs: GIVEN/WHEN/THEN points at a test or repro.
- All hard constraints still hold.

## Output

When verification ends, list:

- Commands run and results
- Skipped items and why (not applicable / missing environment)
- Failures
- Whether closeout is allowed

Enter [closeout.md](closeout.md) only when applicable items passed.
