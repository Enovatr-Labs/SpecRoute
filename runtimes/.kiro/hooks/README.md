# `.kiro/hooks/`

Kiro hook configurations. Each hook is a JSON file with the `.kiro.hook` extension.

## Layout

```
.kiro/hooks/
└── <name>.kiro.hook                 one JSON file per hook
```

## File shape

```json
{
  "enabled": true,
  "name": "<Hook Name>",
  "description": "<purpose>",
  "version": "1",
  "when": {
    "type": "fileEdited" | "fileSaved" | "manual",
    "patterns": ["src/**/*.ts", "tests/**/*.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "<what the agent should do when this hook fires>"
  }
}
```

## Trigger types

| Type | Fires when |
|---|---|
| `fileEdited` | A file matching `patterns` is edited |
| `fileSaved` | A file matching `patterns` is saved |
| `manual` | User explicitly invokes the hook (e.g. via a `pre-commit` trigger) |

## Reference implementations

See [`../../../hooks/kiro/examples/`](../../../hooks/kiro/examples/) for worked examples:

- `auto-test-runner.kiro.hook` - runs scoped tests when source files change.
- `pre-commit-coverage-check.kiro.hook` - verifies test coverage before commit.
- `doc-sync-checker.kiro.hook` - validates doc cross-references when docs are saved.

## Anti-patterns

- **Slow hooks**. Sub-second target. Slow hooks degrade the editor.
- **Non-idempotent hooks**. Hooks fire on every event; corrupt state if not idempotent.
- **Hooks that ask the user questions**. Hooks can't be interactive - use a steering rule or a manual workflow instead.
- **Hooks for occasional work**. If the user does it once a week, a manual workflow is better than a hook.
