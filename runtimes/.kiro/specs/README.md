# `.kiro/specs/`

Kiro's spec triplet location — `<feature>/{requirements,design,tasks}.md`. Same triplet shape SpecForge uses elsewhere; Kiro reads it from this directory natively.

## Layout

```
.kiro/specs/
└── <feature>/
    ├── requirements.md              spec triplet pt 1
    ├── design.md                    spec triplet pt 2
    └── tasks.md                     spec triplet pt 3
```

## Cross-vendor strategy

If your project targets only Kiro, the spec triplet can live exclusively here.

If you target multiple vendors, keep the vendor-neutral copy in `specs/examples/<feature>/` (the SpecForge convention) and either:

- **Mirror** into `.kiro/specs/<feature>/` on each spec change.
- **Symlink** `.kiro/specs/<feature>` → `../../../specs/examples/<feature>` (works in some Kiro versions; check yours).

The mirror approach is the safer default.

## Templates

Use the same templates as the framework-wide spec triplet:

- [`specs/templates/requirements-template.md`](../../../specs/templates/requirements-template.md)
- [`specs/templates/design-template.md`](../../../specs/templates/design-template.md)
- [`specs/templates/tasks-template.md`](../../../specs/templates/tasks-template.md)

The conventions (stable IDs, back-references, coverage table) are unchanged.
