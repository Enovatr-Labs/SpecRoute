# Assets

Static assets referenced by SpecForge documentation — diagrams, screenshots, logos, sample data files. Not for runtime artifacts (those live with their owning directory).

```
assets/
├── README.md                       (this file)
└── (TODO: assets as the project requires them)
```

## What goes here

- **Diagrams** referenced by docs (architecture sketches, flowcharts). Prefer SVG; commit the source if generated.
- **Screenshots** of UI surfaces shown in PRDs or workflows. PNG, named after the surface they show.
- **Logos / brand artifacts**, if SpecForge or a consumer project develops them.
- **Sample data files** that worked examples reference. Generic only — no real customer data.

## What does NOT go here

- Code (lives with its module).
- Markdown content (lives in the appropriate top-level dir).
- Vendor-specific runtime files (live in `runtimes/.<vendor>/`).
- Anything domain-specific that compromises sanitization.

## File-naming conventions

- Lowercase, hyphen-separated: `architecture-overview.svg`, not `ArchitectureOverview.SVG`.
- Descriptive: `vendor-matrix-flowchart.svg`, not `image1.svg`.
- Optionally namespaced by topic: `prds/<topic>.svg`, `workflows/<topic>.svg`.

## Sizing

Keep assets reasonably small — under 500KB per file when possible. SpecForge is text-first; an asset directory dominated by megabyte screenshots becomes a clone-time tax for everyone.

## Empty by default

This directory ships empty (just this README) on a fresh SpecForge skeleton. Consumers populate it with their project's diagrams and screenshots as docs require them.
