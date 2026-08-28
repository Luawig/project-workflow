Replace `<skill-path>` with the installed `SKILL.md` path, then write this block into the target project's `AGENTS.md`. Do not overwrite project-specific rules already in `AGENTS.md`.

## Project Workflow

Requirement clarification, design, spec, implementation, verification, archive, and documentation sync for this project MUST follow `<skill-path>`.

- When the user proposes a product, architecture, protocol, scope, or code change, grade it with that skill and enter the matching stage.
- Do not update `docs/`, `contracts/`, `openspec/`, or scope claims in this file from chat context alone.
- Keep unresolved items as Open Questions or Pending Decisions. Do not invent facts.
- After implementation, verify and close out: archive completed changes and sync `docs/product/scope.md` with the entry docs.
