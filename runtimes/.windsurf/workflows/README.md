# `.windsurf/workflows/`

> **Legacy.** Windsurf is now Devin Desktop. Devin reads `.devin/workflows/` in preference to this directory; `.windsurf/workflows/` is a read-only fallback retained for Cascade installs until EOL (2026-07-01). New workflows belong under [`../../.devin/workflows/`](../../.devin/workflows/).

Workflows are SpecRoute's slash commands for Windsurf/Cascade. Each workflow is a markdown file invoked as `/<name>` (the filename without extension).

## Layout

```
.windsurf/workflows/
└── <name>.md                         one file per workflow, invoked /<name>
```

## Frontmatter contract

```yaml
---
description: <one line shown in the /workflow picker>
---
```

The body is a title, a short purpose statement, and a numbered series of steps for Cascade to follow. Files are limited to 12,000 characters.

## Suggested workflows

Mirror [`../../.claude/commands/`](../../.claude/commands/). The canonical example here is [`review-spec.md`](review-spec.md), invoked `/review-spec <path>`.
