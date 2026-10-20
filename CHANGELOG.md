# Changelog

## 2.0.0

- Use one recoverable change record for durable work; direct invocation needs no installation.
- Separate authorization, observed behavior, task progress and completion state.
- Complete verification and affected knowledge sync before archiving delivery.
- Add architecture decision probes, risk-triggered review and explicit degraded execution.
- Replace the Bash checker with a Python standard-library validator and evidence fingerprints.
- Remove the built-in OpenSpec layout and workflow config. No compatibility or migration tooling is provided.
- Add deterministic regression tests and reproducible agent evaluation fixtures.

## 1.0.0

- Planning may stop at a user-selected document checkpoint; delivery continues through spec, implementation, verification, and closeout.
- Grade S delivery creates no workflow artifact by default and uses targeted verification plus affected-surface closeout.
- The user gives the repository URL to an agent; both agree on the install location; routing is written into `AGENTS.md` at install time.
- An OpenSpec-compatible file layout is the default spec system. This skill writes those files itself and does not use the OpenSpec CLI.
- Layered authority: implementation, stable behavior specs, and decision/context docs.
