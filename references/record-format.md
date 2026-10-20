# Change record format

Use one Markdown record under `docs/changes/<slug>.md`, with lowercase kebab-case
slug. Root-level second-level headings below are fixed parser keys; prose can
use the project's language. Start from [the template](../templates/change-record.md).

Metadata and recovery fields are unindented `key: value` lines outside code
fences. Do not repeat keys or required headings. Fenced examples are ignored.

## Sections

| Required heading | Content |
|---|---|
| Metadata | `intent: planning|delivery`, `grade: S|M|L`, `stage: triage|clarify|design|spec|implement|verify|closeout`, `status: active|blocked|completed|cancelled` |
| Goal | Observable authorized outcome |
| Non-goals | Bounds, or `none` |
| Constraints | Constraints and sources, or `none` |
| Acceptance | Unique `- AC-1: ...` lines naming executable checks |
| Decisions | Reasons, mandate sources and consequential assumptions, or `none` |
| Tasks | Dependent tasks; checkboxes do not determine status |
| Recovery | `next_action: ...`, `blocked_reason: ...` |
| Evidence | Evidence entries below, or `none` before evidence exists |
| Closeout | `verification: pending|passed|not-applicable`, `knowledge_sync: pending|complete|not-applicable`, followed by disposition details |

Active/blocked records need a concrete next action. Blocked also needs a reason.
Other statuses use `blocked_reason: none`; terminal records use `next_action: none`.

Delivery completion requires Closeout, passing acceptance and complete or explicitly
not-applicable knowledge sync. Planning uses `verification: not-applicable`:
document review is separate from delivery acceptance. Planning completion requires
Clarify/Design/Spec, without delivery evidence or archive. Delivery never uses
not-applicable verification. Cancelled work needs disposition in Closeout.

## Evidence

Entries have third-level headings `### EV-1` and these fields:

```text
acceptance: AC-1, AC-2
result: pass
method: python3 -m unittest discover -s tests -v
environment: local Python 3; isolated database
baseline: working tree based on the recorded commit
contract_sha256: <digest>
files: {"src/example.py": "<digest>", "tests/test_example.py": "<digest>"}
```

Results: `pass`, `fail`, `pending`, `invalidated`. Entries are chronological; the
last entry mentioning an acceptance ID determines its current disposition. A
later failure cannot be masked by an earlier pass. Fully superseded entries are
historical observations; only entries still current for an acceptance item are
checked against current inputs.

A pass binds Goal, Non-goals, Constraints, Acceptance and Decisions through
`contract_sha256`: LF newlines, trailing line whitespace removed, outer blank lines
stripped. `contract_digest` in the validator defines the exact algorithm.
`files` maps project-relative paths to SHA-256 byte digests. Include relevant
implementation, tests and external contract/spec inputs.

Generate digests after running the actual check:

```bash
python3 <skill-path>/scripts/validate-workflow.py fingerprint . docs/changes/example.md src/example.py tests/test_example.py
```

This read-only helper does not run tests or generate a passing result. Select
sufficient dependencies; manually review unlisted code, environment and external
dependency changes. Do not hash the record itself: the contract digest avoids
self-reference. Invalidate stale evidence with a reason and rerun affected checks.

The digest covers the whole contract conservatively. If only an independent part
changed, review applicability of the unaffected evidence instead of rerunning an
expensive unrelated check. Add an entry naming the original evidence, its method
and environment, what changed and why the covered acceptance and inputs remain
equivalent; retain its original code baseline and use the new contract digest.
This is an applicability review, not a new test execution. Merely regenerating
digests does not establish equivalence. If equivalence is uncertain, rerun.

Archived historical evidence is not compared to today's source files. Its recorded
contract and evidence structure are still checked.

## Validation

Python 3.8 or newer, standard library only. Commands never modify the project.

| Command | Purpose |
|---|---|
| `python3 <skill-path>/scripts/validate-workflow.py skill <skill-root>` | Check package resources, metadata, local links and templates |
| `python3 <skill-path>/scripts/validate-workflow.py project <project-root>` | Check formal installation routing and records |
| `python3 <skill-path>/scripts/validate-workflow.py project <project-root> --standalone` | Check records without requiring installation; declared routes are still checked |
| `python3 <skill-path>/scripts/validate-workflow.py fingerprint <project-root> <record> <file> [<file> ...]` | Print contract and file digests; paths are project-relative |

Exit `0`: no structural violations; `1`: violations; `2`: invalid input, unreadable
resource or environment error. Formal routing uses the exact `Workflow skill:`
line in the [installation block](../templates/agents-block.md). Naming the skill
or finding it in a conventional directory is not valid installation.

Metadata validation accepts a plain description starting with a letter, a quoted
string, or a folded/literal block; it is not a general YAML parser. Quote descriptions
starting with punctuation or digits. Use the package's simple frontmatter shape.
Empty/non-string descriptions are invalid.

The checker rejects missing/duplicate sections or fields, invalid states,
completed delivery left active, and non-terminal records in archive. Archive
names use a valid date followed by the slug. Record storage directories cannot be
symlinks. It does not infer task completion
or compare prose with implementation.

Without Python/shell, inspect routes, fields, state combinations, latest evidence
and archive placement manually. Report automation as not run. Missing required
behavior evidence still blocks delivery; manual inspection does not establish
automated freshness verification.
