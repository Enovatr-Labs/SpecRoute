---
inclusion: always
---

# Spec-Driven Workflow

Use this steering file in every Kiro conversation for a SpecRoute-enabled repo.

Work moves in this order:

```text
PRD -> requirements/design/tasks -> implementation -> validation -> review
```

## Artifact Routing

- Product intent and success metrics live in `prds/`.
- Kiro-native specs live in `.kiro/specs/<feature>/requirements.md`, `design.md`, and `tasks.md`.
- Shared engineering rules live in `rules/`.
- Event automation lives in `.kiro/hooks/*.json` (Kiro IDE 1.0 format; the 0.x `*.kiro.hook` files no longer execute).

## Readiness Bar

Implementation starts only after requirements have stable IDs, design explains interfaces and failure modes, and tasks reference the requirements they satisfy.
