# `.windsurf/` — Windsurf runtime layout

Drop this directory into the root of your project. Windsurf reads from these paths.

## Layout

```
.windsurf/
└── rules/
    └── <name>.md                    rule files
```

## What Windsurf consumes

- **Rule files** under `.windsurf/rules/`.

Windsurf doesn't have first-class skills, agents, slash commands, or hooks within the SpecForge taxonomy. Its rule system is the integration surface.

## Setup

1. Create `.windsurf/rules/` in your repo.
2. Add `*.md` files for each rule. See [`rules/README.md`](rules/README.md).
3. Windsurf loads rules according to their trigger / glob configuration.

## Cross-referencing project rules

Mirror or copy from the project's `rules/` directory.
