# `.cursor/` — Cursor runtime layout

Drop this directory into the root of your project. Cursor reads from these paths.

## Layout

```
.cursor/
└── rules/
    └── <name>.mdc                   rule files with MDC frontmatter
```

## What Cursor consumes

- **Rule files** (`*.mdc`) under `.cursor/rules/`.

That's it. Cursor doesn't have first-class skills, agents, slash commands, or hooks (within the SpecForge taxonomy). Its rule system is the integration surface.

## Setup

1. Create `.cursor/rules/` in your repo.
2. Add `*.mdc` files for each rule. See [`rules/README.md`](rules/README.md) for the MDC frontmatter contract.
3. Cursor loads matching rules automatically when you work with files matching the rule's `globs`.

## Cross-referencing project rules

The project's `rules/` directory holds the canonical content. Mirror or copy into Cursor MDC files; the MDC format is the integration shape.
