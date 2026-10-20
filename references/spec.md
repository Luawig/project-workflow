# Spec

Make acceptance executable using existing tests, contracts and requirement owners.
Use the record for missing change-specific details without retelling tests.

## Execution contract

Before implementation, identify:

- Observable goal and non-goals.
- Hard constraints with user or accepted-decision sources.
- Acceptance items with stable `AC-*` identifiers and named tests, commands or
  reproducible observations, including relevant boundaries and failures.
- Adjustable decisions and reconsideration triggers.
- Dependency-aware tasks including tests and affected knowledge sync.
- Stop conditions: mandate violation, invalidated architectural assumption,
  unavailable essential evidence or repeated attempts without new evidence.

S can keep this in context. Durable work uses [record format](record-format.md).
Optional shapes are in [spec templates](../templates/spec-artifacts.md).

## Existing specification changes

This skill does not install or own a spec system. Follow the project's existing
format and tools. For an existing requirement:

1. Identify its owner and baseline, with stable ID or unambiguous heading.
2. Record `add`, `modify` or `delete`, affected identity and authorizing source.
   Treat rename as an explicit old-to-new identity map.
3. Capture the before/after acceptance difference; preserve unrelated requirements.
4. Compare against the baseline before applying. Resolve concurrent edits instead
   of overwriting them.
5. Inspect the consolidated specification, references, retained requirements and
   affected regression behavior, not just the new text.

Keep edits in the existing record; do not create another schema or automatic
specification merge engine. Evidence supports implementation claims;
authorization supports changing what is required.

## Test design

Map acceptance to evidence appropriate to the claim. Schema validation establishes
structure, not runtime behavior. Preserve the existing baseline unless required
behavior is explicitly changed.

Prefer deterministic local checks and controlled dependency doubles. Never mock
the unit being evaluated. Use end-to-end checks for mission-critical paths,
including non-commercial projects. Add concurrency, timeout, abuse or migration
cases when their consequences apply.
