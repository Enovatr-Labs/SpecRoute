# `.kiro/` - Kiro runtime layout

Drop this directory into the root of your project. Kiro reads from these paths.

## Layout

```
.kiro/
├── steering/                        always-on or file-pattern-matched rules
├── specs/<feature>/                 spec triplet (requirements/design/tasks)
└── hooks/<name>.kiro.hook           event-triggered automation (JSON)
```

## What Kiro consumes

- **Steering files** (`*.md` under `steering/`) - rules with `inclusion: always` (loaded into every conversation) or `inclusion: fileMatch` (loaded when matching a file pattern).
- **Specs** (`<feature>/{requirements,design,tasks}.md`) - the spec triplet pattern Kiro pioneered.
- **Hooks** (`<name>.kiro.hook` JSON files) - file-pattern triggers that fire on `fileEdited`, `fileSaved`, or `manual`.

Kiro does NOT consume:

- Folder-per-skill `SKILL.md` files (those are Claude / Codex).
- Flat-file agents with `name`/`model`/`color` frontmatter.
- Slash commands.

## Spec triplet alignment

The triplet format SpecForge uses (`requirements.md` + `design.md` + `tasks.md` with stable IDs and back-references) maps directly to Kiro's `.kiro/specs/` layout. The same files work in both places.

If your project mainly targets Kiro, the canonical spec location can be `.kiro/specs/<feature>/`. If you target multiple vendors, keep specs in the vendor-neutral `specs/examples/<feature>/` and symlink or mirror into `.kiro/specs/<feature>/`.

## Steering inclusion semantics

Each steering file's frontmatter declares its loading mode:

```yaml
---
inclusion: always
---
```

or

```yaml
---
inclusion: fileMatch
fileMatchPattern: "src/**/*.tsx"
---
```

See [`steering/README.md`](steering/README.md) for templates.

## Hook format

Each `.kiro.hook` is a JSON file:

```json
{
  "enabled": true,
  "name": "<Hook Name>",
  "description": "<purpose>",
  "version": "1",
  "when": {
    "type": "fileEdited" | "fileSaved" | "manual",
    "patterns": ["src/**/*.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "<what the agent should do>"
  }
}
```

See [`hooks/README.md`](hooks/README.md) for examples and the canonical samples in [`../../hooks/kiro/examples/`](../../hooks/kiro/examples/).
