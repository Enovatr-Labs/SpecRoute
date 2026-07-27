# `.kiro/` - Kiro runtime layout

Drop this directory into the root of your project. Kiro reads from these paths.

Targets **Kiro IDE 1.0** (released 2026-06-25). If you are upgrading an existing install, read
[Hook format](#hook-format) first - 1.0 replaced the hook format and legacy hooks stop firing.

## Layout

```
.kiro/
├── steering/                        always-on or file-pattern-matched rules
├── specs/<feature>/                 spec triplet (requirements/design/tasks)
├── skills/<slug>/SKILL.md           on-demand Agent Skills          (Kiro 0.9+)
├── agents/<name>.md                 custom subagents                (Kiro 0.9+)
├── settings/mcp.json                MCP server inventory            (Kiro 0.9+)
└── hooks/<name>.json                event-triggered automation      (Kiro 1.0+)
```

## What Kiro consumes

- **Steering files** (`*.md` under `steering/`) - rules with `inclusion: always` (loaded into every conversation) or `inclusion: fileMatch` (loaded when matching a file pattern).
- **Specs** (`<feature>/{requirements,design,tasks}.md`) - the spec triplet pattern Kiro pioneered.
- **Skills** (`skills/<slug>/SKILL.md`) - folder-per-skill Agent Skills loaded on demand. Arrived in **Kiro 0.9** (2026-02-05). See [`skills/README.md`](skills/README.md).
- **Subagents** (`agents/<name>.md`) - flat-file workspace subagents Kiro can delegate to. Arrived in **Kiro 0.9** (2026-02-05). See [`agents/README.md`](agents/README.md).
- **MCP servers** (`settings/mcp.json`) - workspace-level `mcpServers` object. Arrived in **Kiro 0.9** (2026-02-05). See [MCP section](#mcp-servers) below.
- **Hooks** (`hooks/<name>.json`) - `"version": "v1"` files declaring a `hooks` array with lifecycle, file, and task triggers. Reformatted in **Kiro 1.0** (2026-06-25). Manual invocation moved to steering. See [Hook format](#hook-format) below.

There is no separate commands directory. Invoke a skill with `/skill <slug>`, or pull one in automatically by referencing it from a manual-inclusion steering file (`inclusion: manual`).

## Spec triplet alignment

The triplet format SpecRoute uses (`requirements.md` + `design.md` + `tasks.md` with stable IDs and back-references) maps directly to Kiro's `.kiro/specs/` layout. The same files work in both places.

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

## Skills and subagents

Both arrived in Kiro 0.9 (2026-02-05), carried forward unchanged into Kiro IDE 1.0, and are the converged capability layer shared with the other vendor runtimes:

- Skills use the Agent Skills open standard (progressive disclosure). Required frontmatter is `name` + `description` only - Kiro does not use the Claude/Codex fields `argument-hint`, `user-invocable`, or `allowed-tools`. See [`skills/README.md`](skills/README.md).
- Subagents are single-file prompts with frontmatter `name` (required) plus optional `description`, `tools`, `model`, `includeMcpJson`, `includePowers`. Kiro does not use the Claude fields `color` or `memory`. See [`agents/README.md`](agents/README.md).

The samples [`skills/audit-artifact/SKILL.md`](skills/audit-artifact/SKILL.md) and [`agents/spec-reviewer.md`](agents/spec-reviewer.md) mirror their `.claude/` counterparts so cross-vendor sync stays straightforward.

## MCP servers

Kiro reads MCP servers from `.kiro/settings/mcp.json` (workspace) or `~/.kiro/settings/mcp.json` (user-global), using a top-level `mcpServers` object. Local server entries support `command`, `args`, `env`, `disabled`, and `autoApprove`.

This repo ships the inventory as [`settings/mcp.template.json`](settings/mcp.template.json) to match the project's `.template.json` suffix convention. **On install, copy it to `.kiro/settings/mcp.json`** (drop the `.template` suffix) so Kiro finds it at the documented path.

The file is rendered from the single source of truth: edit [`runtimes/mcp/servers.yaml`](../mcp/servers.yaml), then run `runtimes/mcp/render/render_kiro.py` to regenerate it. Do not hand-edit the rendered output.

## Hook format

> ### ⚠️ Upgrading from Kiro 0.x
>
> **Kiro IDE 1.0 (2026-06-25) replaced the `*.kiro.hook` format.** Hooks now live at
> `.kiro/hooks/<name>.json` with a `"version": "v1"` root and a `hooks` array.
>
> Legacy `*.kiro.hook` files get an upgrade badge in the IDE, but 1.0 will not execute them.
> Treat a guardrail as off until its migrated replacement has been exercised.
>
> If you copied an earlier version of this runtime layout, run `ls .kiro/hooks/*.kiro.hook`;
> anything it prints needs porting. The field-by-field mapping is in
> [`hooks/README.md`](hooks/README.md) and [`../../hooks/kiro/README.md`](../../hooks/kiro/README.md).

Each hook file is JSON:

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
        "prompt": "<what the agent should do>"
      },
      "timeout": 30,
      "enabled": true
    }
  ]
}
```

Triggers: `SessionStart`, `Stop`, `PreToolUse`, `PostToolUse`, `PreTaskExec`, `PostTaskExec`,
`UserPromptSubmit`, `PostFileCreate`, `PostFileSave`, `PostFileDelete`. Actions are
`{"type": "agent", "prompt": …}` or `{"type": "command", "command": …}`. `matcher` is one string -
`|`-separate multiple globs or tool names.

See [`hooks/README.md`](hooks/README.md) for the full trigger table and the canonical samples in [`../../hooks/kiro/examples/`](../../hooks/kiro/examples/).
