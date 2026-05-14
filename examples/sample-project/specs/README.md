# Specs

Spec triplets for this project. One subdirectory per feature, each containing `requirements.md`, `design.md`, and `tasks.md`.

```
specs/
├── README.md          (this file)
└── <feature-slug>/
    ├── requirements.md    spec triplet pt 1 (stable IDs)
    ├── design.md          spec triplet pt 2 (architecture, data model, APIs)
    └── tasks.md           spec triplet pt 3 (numbered, back-references requirements)
```

## Currently active

- [`user-search/`](user-search/) - the spec triplet for the user-search PRD (`../prds/active/user-search.md`).

## Lifecycle

The spec triplet's `Status:` frontmatter drives its state:

- `Draft` - author drafting; not yet ready for review
- `Approved` - reviewed and signed off; the contract for implementation
- `In Implementation` - tasks being worked
- `Complete` - all tasks checked, all requirements have passing tests

When a feature ships and its PRD moves to `../prds/archive/`, the spec triplet typically stays here as the project's reference (or move to `archive/<feature>/` if your team prefers).

## Templates

This project's specs are based on the SpecRoute framework's templates:

- [`specs/templates/requirements-template.md`](../../../specs/templates/requirements-template.md)
- [`specs/templates/design-template.md`](../../../specs/templates/design-template.md)
- [`specs/templates/tasks-template.md`](../../../specs/templates/tasks-template.md)

## Adding a new spec triplet

1. The PRD must be `Status: Approved` in `../prds/active/`.
2. Create `specs/<slug>/` matching the PRD's filename slug.
3. Copy the three template files.
4. Fill in stable IDs (R1.1 ... NFR-1.1 ...).
5. Confirm every PRD acceptance criterion maps to >= 1 requirement; every requirement maps to >= 1 task; coverage table fully populated.
6. Set `Status: Approved` on each of the three files.

## See also

- [`../prds/`](../prds/) - the PRDs that approved specs are based on
- [`../prompts/`](../prompts/) - the phased execution plan that consumes the spec triplet
- The framework's [`agentic-docs/spec-driven-development.md`](../../../agentic-docs/spec-driven-development.md)
