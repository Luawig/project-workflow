# Clarify

Turn scattered input into facts later stages can cite. Intake is a source log, not the default reading entry. Current scope is `docs/product/scope.md` and `docs/overview.md`.

## Inputs

- Goals, constraints, refusals, and priorities stated by the user.
- Later additions and corrections.
- Third-party projects, competitors, open-source implementations.
- Existing README, PRD, design docs, contracts, OpenSpec.
- Information that would change direction but is not yet known.

## Normalize

Split into five kinds. Do not mix them:

| Kind | Definition | Goes to |
|---|---|---|
| Facts | The user stated it, or current docs/code already prove it | PRD, overview, architecture, RULE |
| Assumptions | Adopted to continue, not yet proven | Assumptions in related docs; never a RULE |
| Open Questions | Unresolved items that affect scope, architecture, protocol, data, or plan | End of affected docs; do not delete while open |
| Pending Decisions | Known options waiting on the user | ADR or RULE after confirmation |
| Reference Signals | Third-party adopt / skip / adapt | `docs/references/third-party-analysis.md` |

Rules:

- Split "would be nice" into goals, non-goals, acceptance, or an open question.
- Split "like project X" into concrete capabilities, interaction, technical constraints, and skip points.
- Put "later" into Pending Decisions. Do not assume approval.
- Keep conflicting statements side by side, prefer the latest user follow-up, and replace superseded Facts.
- Unverified third-party claims are not Facts.

Grade S does not need `docs/intake.md` when facts are already enough. For M/L, create or update `docs/intake.md` with the template below if the project has no intake log.

## Template

```md
# Intake

## Status
draft

## Sources
- Source 1: TODO

## Facts
- FACT-1: TODO

## Assumptions
- ASSUMPTION-1: TODO, because: TODO

## Open Questions
- QUESTION-1: TODO, affects: scope | architecture | protocol | data model | implementation plan

## Pending Decisions
- DECISION-1: TODO, options: TODO

## Reference Signals

### Adopt
- REF-1: TODO

### Do not adopt
- REF-2: TODO, because: TODO

### Adapt
- REF-3: TODO, adaptation: TODO
```

## Maintenance

- Open Questions / Pending Decisions keep only unresolved items. After resolution, delete the item; the content must already be a `FACT-*`, ADR, or `RULE-*`.
- Each `FACT-N` has exactly one current definition. Do not cite skipped numbers.
- Superseded FACT: keep one pointer line in the current list. Old body may move to `docs/intake-history.md`.
- Do not paste the same source twice.
- Facts must not stay only in intake. After capture, write them into long-lived product or technical docs.
- Do not recopy implementation-time config into overview. Overview keeps only still-needed points and links back.

## Alignment gate

Before leaving this stage on M/L:

- Goals, non-goals, and gray areas are split.
- Terms and key states are consistent.
- Each core capability has success, boundary, and exception acceptance intent.
- Missing information is in Open Questions or Pending Decisions.
