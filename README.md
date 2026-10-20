# project-workflow

An Agent Skills workflow for authorized software planning and delivery. The entry
is [SKILL.md](SKILL.md). Start with the requested outcome, apply checks according
to consequences, and finish with acceptance evidence and recoverable closeout.

## Use

Invoke the skill directly for a change, architecture proposal or delivery review.
Direct invocation does not modify project instructions. Planning stops at the
requested checkpoint. Delivery continues through verification and affected
knowledge sync.

One-session local changes need no workflow artifact. Cross-session work and
behavioral or high-risk changes use one [change record](templates/change-record.md).
Existing specs, architecture docs, contracts and tests retain their owners.
See [record format](references/record-format.md) for persistent state and evidence.

The skill supports file-based agents without private connectors. Python 3.8+ is
needed only for the bundled structural checker. Without command execution, follow
the documented manual checks and report required evidence that remains unavailable.
Independent agents are optional; shared-context review must be identified as such.

## Install as the project workflow

Copy SKILL.md, references/, templates/, scripts/ and LICENSE to an agreed location,
then append the [routing block](templates/agents-block.md) to the project's
AGENTS.md. Replace its path with the actual installed SKILL.md. Preserve all
project-specific instructions. No separate workflow configuration is required.

The skill does not install a specification framework or migrate existing records.
Current format and command contracts are documented in
[record format](references/record-format.md#validation).

## Validate and develop

Run from this skill repository:

```bash
python3 scripts/validate-workflow.py skill .
python3 -m unittest discover -s tests -v
```

For an installed consuming project:

```bash
python3 <skill-path>/scripts/validate-workflow.py project <project-root>
```

Use `--standalone` for direct invocation without an installation route. The checker
validates structure, explicit state and fingerprints of listed inputs. It cannot
prove authorization, test truthfulness, dependency coverage or design quality.

[Evaluation guide](evals/README.md) contains reproducible tasks and baseline
provenance. [Evaluation results](evals/results.md) distinguish automated checks,
agent observations and unmeasured performance.

Maintain rules in the main entry and matching references, and keep templates and
validator behavior synchronized. Do not add personal paths, private project names
or internal service URLs. History belongs in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE).
