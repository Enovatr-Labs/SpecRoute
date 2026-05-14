# PRDs

Product Requirements Documents for this project. Lifecycle directories follow the SpecRoute convention.

```
prds/
├── README.md              (this file)
├── active/                in-flight PRDs - Draft, Under Review, Approved, In Implementation
├── deprecated/            superseded PRDs (kept for context)
└── archive/               shipped or abandoned PRDs (historical record)
```

## Currently active

- [`active/user-search.md`](active/user-search.md) - paginated, filterable, indexed user-directory search. Status: `Approved`.

## Lifecycle

A PRD's `Status:` frontmatter drives its directory:

- `Draft`, `Under Review`, `Approved`, `In Implementation` -> `active/`
- `Deprecated`, `Superseded` -> `deprecated/` (with `Superseded-By:` pointer)
- `Shipped` -> `archive/` (filename year-prefixed for sorting, e.g. `2026-05-user-search.md`)

## Templates

This project's PRDs are based on the SpecRoute framework's [`prds/templates/prd-template.md`](../../../prds/templates/prd-template.md) (full 23-section enterprise) and [`prds/templates/lightweight-prd-template.md`](../../../prds/templates/lightweight-prd-template.md) (single-page alternative). Copy and fill in.

## Adding a new PRD

1. Pick the template (full or lightweight).
2. Create `active/<slug>.md` with the slug matching the feature name across `specs/<slug>/` and any prompts.
3. Set frontmatter: Version, Date, Author, Status, Architecture Reference, Scope.
4. Run `/audit` (or the equivalent) before promoting to `Status: Approved`.

## See also

- [`../specs/`](../specs/) - the spec triplet for each approved PRD
- [`../prompts/`](../prompts/) - the phased execution plan
- The framework's [`agentic-docs/spec-driven-development.md`](../../../agentic-docs/spec-driven-development.md) for the canonical flow
