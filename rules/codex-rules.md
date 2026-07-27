# Codex-specific Rules

How rules and standards are loaded into Codex. Rules content itself defers to the vendor-neutral rule files in this directory.

> **Naming collision.** This file is a *SpecRoute* vendor-rules doc: how SpecRoute's Markdown standards reach Codex. Codex also ships a feature it calls **rules** - `.rules` files written in **Starlark** that decide whether a command needs approval. Those are a policy language, not instruction Markdown, and they are out of scope here. See "Codex's own `.rules` files" below so the two are never conflated.

## Where Codex looks

Codex has no loader for Markdown instruction files beyond its context files. SpecRoute rules surface through:

- **`AGENTS.md`** at the repo root - Codex's canonical context file. Reference shared rules from here.
- **`.codex/agents/<name>.toml`** - agent-level operating principles (per-agent guidance, TOML).
- **`.codex/skills/<slug>/SKILL.md`** - skill-level operating principles.
- **`.agents/skills/<slug>/SKILL.md`** - the emerging vendor-neutral skills root, also read by Codex. See [`agentic-docs/cross-vendor-sync.md`](../agentic-docs/cross-vendor-sync.md).

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
| `approval_policy` | Configured in `.codex/config.toml`. Valid values are `untrusted`, `on-request`, and `never`. **`on-failure` was removed** - a config still carrying it is invalid, not merely deprecated. |
| `sandbox_mode = "workspace-write"` | Codex sandboxes writes to the workspace. Don't expect writes outside the workspace to succeed. |
| Per-tool approval | MCP server tools can be marked to require user confirmation. See `.codex/config.toml`. |
| Profiles | The `[profiles.*]` tables in `config.toml` were **deprecated in 0.134.0**. A profile is now its own flat file: `~/.codex/<name>.config.toml`, one per profile. Migrate rather than nesting. |
| Skills invoked with `$name` or from `/skills` | Codex's slash-command equivalent. Document the mapping in [`commands/README.md`](../commands/README.md). |
| Custom prompts | **Deprecated in favour of skills.** Do not author new prompt files; write a skill with portable `name` / `description` frontmatter. |
| Hooks via `.codex/hooks.json` | JSON schema is intentionally Claude-compatible. Enabled by default. Canonical `[features]` key is `hooks` (`codex_hooks` is a deprecated alias); disable with `[features] hooks = false`. See [`hooks/codex/`](../hooks/codex/) for the template and the current event list. |
| Hook concurrency | Multiple matching hooks for the same event run **in parallel** - one cannot prevent another from starting. Design scripts to be idempotent and side-effect-isolated. |

## Codex's own `.rules` files (different thing)

Codex ships a command-approval policy layer whose files are also called rules. They are **Starlark**, not Markdown, and they answer one question: does this command need human approval? They cannot carry engineering standards, and nothing in SpecRoute's `rules/` directory compiles to them.

Treat them as adjacent to `approval_policy` and `sandbox_mode`, not as an instruction surface:

- Use `.rules` (or `approval_policy`) when you want a command class *blocked or gated*.
- Use `AGENTS.md` and skill bodies when you want the model to *know a standard*.

If a standard is important enough that violating it should be impossible rather than discouraged, that is the signal to add an approval rule or a hook on top of the Markdown - the same "rule vs hook vs review" split described in [`README.md`](README.md).

## Rule-loading frontmatter (Codex-irrelevant)

Codex doesn't consume rule-loading frontmatter (`alwaysApply`, `inclusion: fileMatch`, Claude's `paths:`). Those are Cursor / Kiro / Claude Code concepts. In Codex, rule docs are surfaced through `AGENTS.md` references and agent operating principles.

## See also

- [`README.md`](README.md) - what SpecRoute's `rules/` directory is and is not.
- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.codex/README.md`](../runtimes/.codex/README.md) - Codex runtime layout.
- Codex documentation: <https://learn.chatgpt.com/docs/> (the older `developers.openai.com/codex/*` paths 308-redirect here, with changed path segments).
