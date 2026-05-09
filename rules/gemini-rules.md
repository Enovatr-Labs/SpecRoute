# Gemini-specific Rules

How rules and standards are loaded into Gemini CLI. Rules content itself defers to the vendor-neutral rule files in this directory.

## Where Gemini looks

- **`GEMINI.md`** at the repo root - Gemini's canonical context file. Recommended: a slim delegation shim pointing to `AGENTS.md`.
- **`AGENTS.md`** - broader project context. Most rules content is referenced from here.
- **`.gemini/settings.json`** - MCP server configuration (no rule loader).
- **`.gemini/gemini_cli_config.json`** - slash-command shortcuts (not a rule loader).

## Recommended structure

In `GEMINI.md`:

```markdown
# GEMINI.md

For project context, conventions, and rules, read [`AGENTS.md`](AGENTS.md).

## Gemini-specific overrides

<vendor-specific bits only - keep this short>
```

In `AGENTS.md`, link to:

- [`rules/engineering-rules.md`](engineering-rules.md)
- [`rules/code-review-rules.md`](code-review-rules.md)
- [`rules/security-rules.md`](security-rules.md)
- [`rules/documentation-rules.md`](documentation-rules.md)

## What Gemini does NOT support

- Folder-per-skill `SKILL.md` files.
- Flat-file agents.
- Slash commands with markdown body (Gemini commands are JSON entries with shell commands).

For features SpecForge ships that Gemini can't natively run, the equivalent is to:

- Use `prompts/shared/` and `prompts/codex|claude/` as reference prompts that humans copy into a Gemini conversation.
- Use `gemini_cli_config.json` for shell-shortcut equivalents of one-shot commands.

## Vendor-specific behaviors

| Topic | Gemini behavior |
|---|---|
| MCP servers | Configured in `.gemini/settings.json` `mcpServers`. Same JSON shape as Claude Desktop. |
| Slash commands | JSON entries in `.gemini/gemini_cli_config.json` `commands`. Run shell commands, not prompts. |
| Hooks | `.gemini/settings.json` `hooks` block - 11 events (`Before/AfterTool`, `Before/AfterAgent`, `Before/AfterModel`, `BeforeToolSelection`, `SessionStart`, `SessionEnd`, `Notification`, `PreCompress`). v0.26.0+. See [`hooks/gemini/`](../hooks/gemini/). |
| Stdout discipline (hooks) | Gemini is **strict** - hook scripts must print **only the final JSON to stdout**. Send diagnostics to stderr. Plain-text-mixed-with-JSON breaks the parser. |
| Rule loading | None native. Rules surface via `GEMINI.md` and `AGENTS.md`. |

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.gemini/README.md`](../runtimes/.gemini/README.md) - Gemini runtime layout.
- [`agentic-docs/multi-vendor-context-files.md`](../agentic-docs/multi-vendor-context-files.md) - the delegation-shim pattern.
