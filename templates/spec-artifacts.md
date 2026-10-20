# Specification and review shapes

Use inside the record or an existing document, not separate files merely for tables.

## Acceptance mapping

| Acceptance ID | Required outcome and source | Check | Relevant failure case |
|---|---|---|---|
| AC-1 | Observable requirement | Named test or repeatable steps | Boundary or failure to detect |

The record's Acceptance section uses `- AC-1: ...`; optional tables can expand
those entries elsewhere by reference.

## Existing requirement edit

| Operation | Owner and identity | Baseline | Authorized difference | Regression |
|---|---|---|---|---|
| add / modify / delete | Existing path and ID/heading | Commit or snapshot | Source and before/after behavior | Changed and retained checks |

Record old/new identities for rename. Reconcile concurrent changes before applying
edits, then inspect the consolidated specification.

## Counterexample review

| Concern | Counterexample or probe | Evidence | Disposition |
|---|---|---|---|
| Critical assumption | What would disprove it | Observed result or pending check | Decision, test, task or accepted residual risk |

State whether review used an independent agent or shared context. Resolve findings
that invalidate acceptance before completion.
