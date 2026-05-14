# GEMINI.md

Gemini CLI shim for this repository. Read [`AGENTS.md`](AGENTS.md) first; it is the canonical vendor-neutral source of truth for SpecRoute.

## Gemini-Specific Context

- Gemini reads `.gemini/settings.json` for MCP servers (same JSON shape as Claude Desktop's `claude_desktop_config.json`).
- Gemini reads `.gemini/gemini_cli_config.json` for command shortcuts (JSON command map; commands run shell strings, not prompts).
- Templates for both live in [`runtimes/.gemini/`](runtimes/.gemini/).

## Command Shape

Gemini commands are JSON entries, not markdown prompts:

```json
{
  "commands": {
    "<slug>": {
      "command": "<shell command to run>",
      "description": "<one-line description>",
      "directory": "<optional working dir>"
    }
  }
}
```

See [`commands/command-template.gemini.json`](commands/command-template.gemini.json) for the full template and [`commands/examples/`](commands/examples/) for worked entries.

## Matrix Notes

Gemini supports **commands and MCP** in the SpecRoute matrix. It does not consume `SKILL.md` folders, flat-file agents, or hook configurations directly. The SpecRoute concepts that don't map natively to Gemini still apply through:

- [`prompts/`](prompts/) - reusable prompts (paste into a Gemini conversation).
- [`prompts/shared/`](prompts/shared/) - the master/phase/task prompt trio works in any agent CLI.
- [`rules/gemini-rules.md`](rules/gemini-rules.md) - Gemini-specific rule guidance and how shared rules surface here.

## MCP Single Source of Truth

`.gemini/settings.json`'s `mcpServers` map is regenerated from [`runtimes/mcp/servers.yaml`](runtimes/mcp/servers.yaml) via `python3 runtimes/mcp/render/render_gemini.py`. Do not hand-edit the generated file - edit `servers.yaml` and re-render.

## Before Publishing

This repo's sanitization tooling is in `.claude/` (Claude-Code-specific) but the wordlist at `.claude/.forbidden-strings.txt` applies to all tracked content regardless of which vendor authored it. Confirm new Gemini config or content passes the same check before committing.
