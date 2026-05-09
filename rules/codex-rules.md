# Codex-specific Rules

How rules and standards are loaded into Codex. Rules content itself defers to the vendor-neutral rule files in this directory.

## Where Codex looks

Codex doesn't have a dedicated `rules/` loader. Rules surface through:

- **`AGENTS.md`** at the repo root - Codex's canonical context file. Reference shared rules from here.
- **`.codex/agents/<name>.md`** - agent-level operating principles (per-agent guidance).
- **`.codex/skills/<slug>/SKILL.md`** - skill-level operating principles.

## Recommended structure

In `AGENTS.md`, link to:

- [`rules/engineering-rules.md`](engineering-rules.md)
- [`rules/code-review-rules.md`](code-review-rules.md)
- [`rules/security-rules.md`](security-rules.md)
- [`rules/documentation-rules.md`](documentation-rules.md)

Codex reads `AGENTS.md` automatically; the linked rule files become accessible context when the agent reads them.

## Vendor-specific behaviors

| Topic | Codex behavior |
|---|---|
| `approval_policy = "on-request"` | Tool invocations may require approval per the approval mode. Configured in `.codex/config.toml`. |
| `sandbox_mode = "workspace-write"` | Codex sandboxes writes to the workspace. Don't expect writes outside the workspace to succeed. |
| Per-tool approval (`approval_mode`) | MCP server tools can be marked `"approve"` to require user confirmation. See `.codex/config.toml`. |
| Skills with `user-invocable: true` | Replace Claude-style commands. Document the equivalent in `commands/README.md`. |
| Hooks via `.codex/hooks.json` | 6 events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `Stop`). JSON schema is intentionally Claude-compatible. Requires `[features] codex_hooks = true` in `.codex/config.toml`. See [`hooks/codex/`](../hooks/codex/) for the template. |
| Hook concurrency | Multiple matching hooks for the same event run **in parallel** - one cannot prevent another from starting. Design scripts to be idempotent and side-effect-isolated. |

## Rule frontmatter (Codex-irrelevant)

Codex doesn't consume rule-loading frontmatter (`alwaysApply`, `inclusion: fileMatch`, etc.). Those are Cursor / Kiro concepts. In Codex, rule docs are surfaced through `AGENTS.md` references and agent operating principles.

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.codex/README.md`](../runtimes/.codex/README.md) - Codex runtime layout.
