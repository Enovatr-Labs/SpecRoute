# Kiro hooks

Event-triggered automation for Kiro. Hooks live at `.kiro/hooks/<name>.json` in the consuming repo.

> ## ⚠️ Breaking change - Kiro IDE 1.0 (2026-06-25)
>
> Kiro IDE 1.0 **replaced the `*.kiro.hook` format**. If you installed a SpecRoute Kiro runtime
> before 2026-06-25, or wrote your own hooks against the 0.x format, migrate it to v1.
>
> Kiro 1.0 shows an upgrade badge next to legacy `*.kiro.hook` files, but does not execute them.
> If you relied on one as a guardrail, treat that guardrail as off until the migrated hook has
> been exercised.
>
> ### Migration checklist
>
> 1. `ls .kiro/hooks/*.kiro.hook` - anything listed is dead.
> 2. For each one, create `.kiro/hooks/<name>.json` using the v1 shape below.
> 3. Rewrite `when.type` to the new trigger vocabulary (table below).
> 4. Fold `when.patterns` (array) into a single `matcher` string - `|`-separated globs.
> 5. Rewrite `then.type`: `askAgent` → `"action": { "type": "agent", "prompt": ... }`,
>    `runCommand` → `"action": { "type": "command", "command": ... }`.
> 6. Add `timeout` (seconds) and `enabled` to each hook entry.
> 7. Move the `.kiro.hook` file out of the runtime once the `.json` replacement fires.
> 8. Restart Kiro and confirm the hook appears in the hooks panel as enabled.

## Layout

```
hooks/kiro/
├── README.md                          (this file)
└── examples/
    ├── auto-test-runner.json          scoped tests on source save (disabled by default)
    └── doc-sync-checker.json          doc cross-reference validation on doc save
```

Copy an example to `.kiro/hooks/<name>.json` in your own repo and edit the `matcher` and `prompt`.

## File shape (v1)

```json
{
  "version": "v1",
  "hooks": [
    {
      "name": "<Hook Name>",
      "trigger": "PostFileSave",
      "matcher": "src/**/*.ts|tests/**/*.ts",
      "action": {
        "type": "agent",
        "prompt": "<what the agent should do when this hook fires>"
      },
      "timeout": 30,
      "enabled": true
    }
  ]
}
```

- `version` - the string `"v1"`.
- `hooks` - array. One file may declare several hooks; SpecRoute's examples ship one each so they
  can be copied selectively.
- `trigger` - one of the ten values below.
- `matcher` - glob for file triggers or tool name / category for tool triggers. Multiple values
  are `|`-separated in a single string.
- `action.type` - `"command"` (shell) or `"agent"` (prompt handed to the Kiro agent).
- `timeout` - seconds. Keep it tight; a hook that blocks the editor is worse than no hook.
- `enabled` - boolean. Ship expensive hooks disabled and let the consumer opt in.

## Trigger vocabulary

| Trigger | Fires when | Blockable |
|---|---|---|
| `SessionStart` | Session begins or resumes | No |
| `Stop` | Agent completes its turn | (advisory) |
| `PreToolUse` | Agent about to invoke a tool | Yes |
| `PostToolUse` | After the agent invokes a tool | (advisory) |
| `PreTaskExec` | Before a spec task begins | Yes |
| `PostTaskExec` | After a spec task completes | (advisory) |
| `UserPromptSubmit` | User submits a prompt | (advisory) |
| `PostFileCreate` | New file matching `matcher` is created | (advisory) |
| `PostFileSave` | File matching `matcher` is saved | (advisory) |
| `PostFileDelete` | File matching `matcher` is deleted | (advisory) |

## 0.x → 1.0 mapping

| 0.x | 1.0 | Notes |
|---|---|---|
| `<name>.kiro.hook` | `.kiro/hooks/<name>.json` | Same directory, new extension |
| `"version": "1"` (string) | `"version": "v1"` (string) | Now at the file root, alongside `hooks` |
| single hook per file | `hooks: [ … ]` array | One file may hold several |
| `when.type: "fileEdited"` | `trigger: "PostFileSave"` | Or `PostToolUse` if you meant agent edits, not user saves |
| `when.type: "fileSaved"` | `trigger: "PostFileSave"` | Direct rename |
| `when.type: "manual"` | manual steering file | v1 retired the `Manual` trigger |
| `when.patterns: [ … ]` | `matcher: "a\|b"` | Array collapses to a `\|`-separated string |
| `then.type: "askAgent"` | `action.type: "agent"` | `prompt` unchanged |
| `then.type: "runCommand"` | `action.type: "command"` | Shell command in `command` |
| (none) | `timeout` | Now explicit per hook |
| root `enabled` | per-hook `enabled` | Moves inside the array entry |

`fileEdited` is the one genuinely ambiguous case. 0.x conflated "the user edited this file" with
"the agent edited this file". If your intent was a user-facing save, use `PostFileSave`. If your
intent was to react to the agent's own write tools, use `PostToolUse` with a tool-name `matcher`.
SpecRoute's `auto-test-runner` example took the first reading.

For a manual pre-commit checklist, use a steering file with `inclusion: manual`; the shipped
runtime includes `runtimes/.kiro/steering/pre-commit-coverage-check.md` as the replacement pattern.

## See also

- [`../README.md`](../README.md) - the cross-vendor hook taxonomy and per-vendor event matrices.
- [`../../runtimes/.kiro/hooks/`](../../runtimes/.kiro/hooks/) - the shipped runtime hook.
- [`../../rules/kiro-rules.md`](../../rules/kiro-rules.md) - Kiro rule and steering conventions.
