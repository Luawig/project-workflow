# Verify

Verify the execution contract, not just a command's exit status. Use project
commands sized to consequences.

## Evidence

1. Run named acceptance tests or reproducible observations yourself.
2. Match each `AC-*` to evidence with appropriate scope. Inspect output;
   distinguish source inspection from runtime observation.
3. Preserve relevant regressions. For critical checks, demonstrate that a broken
   case is detected, using an isolated fixture when needed.
4. Record method, result, environment and code baseline using
   [record format](record-format.md#evidence).
5. Invalidate affected evidence after relevant source, contract or acceptance
   changes and rerun. Unrelated expensive checks need not repeat: when the shared
   contract digest changes, document an applicability review under
   [record format](record-format.md#evidence), without claiming a new test run.

S uses targeted tests or manual repro. M adds acceptance and affected regression
checks. L adds triggered risk cases and counterexample review; migration requires
data verification and recovery evidence.

## Failures and missing environments

- Implementation failures return to Implement. Wrong acceptance returns to Spec
  through the authorization rules.
- Missing required environment or decision leaves the change `blocked`, with
  what could not run and the exact next action.
- Irrelevant checks can be not applicable with a reason. Missing required checks
  cannot. Known defects remain visible when fixing them is outside scope.
- Changing a test requirement needs authorization, not silent deletion.

Unrelated green tests, ignored failures, weakened assertions or a mocked unit
under test do not establish acceptance. Fingerprints validate freshness only for
listed inputs; reviewers still assess coverage and truthfulness.

## Exit

Applicable acceptance needs current passing evidence. Report methods, results,
omissions and unresolved findings. Runtime checks establish the tested environment,
not an unobserved deployment. Only then enter Closeout.
