# `.devin/workflows/`

Workflows are SpecRoute's slash commands for Devin. Each workflow is a markdown file invoked as `/<name>` (the filename without extension).

## Layout

```
.devin/workflows/
└── <name>.md                         one file per workflow, invoked /<name>
```

## Frontmatter contract

```yaml
---
description: <one line shown in the /workflow picker>
---
```

The body is a title, a short purpose statement, and a numbered series of steps for Devin to follow. A step may delegate to a subagent under `.devin/agents/`. Files are limited to 12,000 characters.

## Suggested workflows

Mirror [`../../.claude/commands/`](../../.claude/commands/). The canonical example here is [`review-spec.md`](review-spec.md), invoked `/review-spec <path>`.
