# `.kiro/hooks/`

Kiro hook configurations. Each hook file is JSON with a `.json` extension, declaring `"version": "v1"`
and a `hooks` array.

> **Migrating from Kiro 0.x?** The `*.kiro.hook` format was replaced in **Kiro IDE 1.0
> (2026-06-25)**. Legacy files get an upgrade badge in the IDE but do not execute until migrated.
> See [Migrating from `*.kiro.hook`](#migrating-from-kirohook)
> below, or the fuller checklist in [`../../../hooks/kiro/README.md`](../../../hooks/kiro/README.md).

## Layout

```
.kiro/hooks/
└── <name>.json                      one JSON file per hook (or several hooks per file)
```

## File shape

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

`action.type` is `"agent"` (prompt handed to the Kiro agent) or `"command"` (shell command in a
`command` field). `matcher` is a single string - `|`-separate multiple globs or tool names.

## Trigger types

| Trigger | Fires when |
|---|---|
| `SessionStart` | Session begins or resumes |
| `Stop` | Agent completes its turn |
| `PreToolUse` | Agent is about to invoke a tool (blockable) |
| `PostToolUse` | After the agent invokes a tool |
| `PreTaskExec` | Before a spec task begins (blockable) |
| `PostTaskExec` | After a spec task completes |
| `UserPromptSubmit` | User submits a prompt |
| `PostFileCreate` | A file matching `matcher` is created |
| `PostFileSave` | A file matching `matcher` is saved |
| `PostFileDelete` | A file matching `matcher` is deleted |
| ~~`Manual`~~ | **Retired in Kiro IDE 1.0** - manual invocation is now a steering file |

## Migrating from `*.kiro.hook`

| 0.x | 1.0 |
|---|---|
| `<name>.kiro.hook` | `<name>.json` |
| `"version": "1"` (string, per hook) | `"version": "v1"` (string, at the file root) |
| one hook per file | `hooks: [ … ]` array |
| `when.type: "fileSaved"` | `trigger: "PostFileSave"` |
| `when.type: "fileEdited"` | `trigger: "PostFileSave"` (user saves) or `"PostToolUse"` (agent writes) |
| `when.type: "manual"` | manual steering file (`inclusion: manual`) |
| `when.patterns: [ … ]` | `matcher: "a\|b"` |
| `then.type: "askAgent"` | `action: { "type": "agent", "prompt": … }` |
| `then.type: "runCommand"` | `action: { "type": "command", "command": … }` |
| root-level `enabled` | per-hook `enabled` |
| (none) | per-hook `timeout` in seconds |

Move the `.kiro.hook` file out of the runtime only after the replacement fires.

## Setup

Kiro was the last runtime to get the three defaults its siblings ship. Install them:

```bash
mkdir -p .kiro/hooks/scripts
cp runtimes/.kiro/hooks/hooks.template.json .kiro/hooks/specroute.json
cp runtimes/.kiro/hooks/scripts/*.sh        .kiro/hooks/scripts/
chmod +x .kiro/hooks/scripts/*.sh
```

That wires three hooks: a `SessionStart` orientation banner, a `PreToolUse` sanitization gate that
blocks publish-style commands while forbidden strings remain in tracked *or newly added* files, and a
`PostFileSave` frontmatter check. Create the gate's wordlist and gitignore it:

```bash
printf '# One whitespace-free term per line.\n' > .kiro/.forbidden-strings.txt
echo '.kiro/.forbidden-strings.txt' >> .gitignore
```

Verify. Checking the config alone is **not** enough - it confirms the hook is registered, not that
the script it points at exists. A registered hook whose script is missing exits 127, and for the
sanitization gate that means the guardrail did not run:

```bash
python3 -c "import json;print(len(json.load(open('.kiro/hooks/specroute.json'))['hooks']),'hooks')"
for s in .kiro/hooks/scripts/*.sh; do test -x "$s" || echo "MISSING/NOT EXECUTABLE: $s"; done
```

**Blocking semantics.** `PreToolUse` and `PreTaskExec` are the blockable triggers - exit `2` blocks
with stderr as the reason, exit `0` allows. `PostFileSave` and the other `Post*` triggers are
advisory: the action has already happened, so a non-zero exit reports but cannot undo.

## Shipped hooks

- [`doc-sync-checker.json`](doc-sync-checker.json) - `PostFileSave` on docs and examples; asks the
  agent to report broken links, vendor-matrix drift, and unresolved TODO markers.

## Reference implementations

See [`../../../hooks/kiro/examples/`](../../../hooks/kiro/examples/) for worked examples:

- `auto-test-runner.json` - runs scoped tests when source files are saved (disabled by default).
- `doc-sync-checker.json` - validates doc cross-references when docs are saved.

The retired manual pre-commit example is now
[`../steering/pre-commit-coverage-check.md`](../steering/pre-commit-coverage-check.md).

## Anti-patterns

- **Slow hooks**. Sub-second target, and always set `timeout`. Slow hooks degrade the editor.
- **Non-idempotent hooks**. Hooks fire on every event; corrupt state if not idempotent.
- **Hooks that ask the user questions**. Hooks can't be interactive - use a steering rule or a manual workflow instead.
- **Hooks for occasional work**. If the user does it once a week, a manual workflow is better than a hook.
- **Leaving `enabled: true` on expensive hooks you ship to others**. Ship them disabled; let the consumer opt in.
