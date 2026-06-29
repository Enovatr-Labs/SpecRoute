# GEMINI.md

Gemini CLI shim for this repository. Read [`AGENTS.md`](AGENTS.md) first; it is the canonical vendor-neutral source of truth for SpecRoute.

## Gemini-Specific Context

- Gemini reads `.gemini/settings.json` for MCP servers (`mcpServers` map).
- Gemini reads TOML command files under `.gemini/commands/<name>.toml` for slash commands (each file is a prompt, not a shell string).
- Gemini also supports skills under `.gemini/skills/` and subagents under `.gemini/agents/`.
- Templates for all of these live in [`runtimes/.gemini/`](runtimes/.gemini/).

## Command Shape

Gemini commands are TOML files, one per command, under `.gemini/commands/`:

```toml
# .gemini/commands/<slug>.toml  ->  /<slug>
description = "<one-line description>"
prompt = """
<the prompt the command expands to; use {{args}} for arguments>
"""
```

`prompt` is required; `description` is optional. Subdirectories namespace the command (`.gemini/commands/git/commit.toml` -> `/git:commit`).

See [`commands/command-template.gemini.toml`](commands/command-template.gemini.toml) for the full template and [`commands/examples/`](commands/examples/) for worked entries.

## Matrix Notes

Gemini supports **commands, skills, subagents, and MCP** in the SpecRoute matrix. The SpecRoute concepts surface through:

- [`prompts/`](prompts/) - reusable prompts (paste into a Gemini conversation).
- [`prompts/shared/`](prompts/shared/) - the master/phase/task prompt trio works in any agent CLI.
- [`rules/gemini-rules.md`](rules/gemini-rules.md) - Gemini-specific rule guidance and how shared rules surface here.

## MCP Single Source of Truth

`.gemini/settings.json`'s `mcpServers` map is regenerated from [`runtimes/mcp/servers.yaml`](runtimes/mcp/servers.yaml) via `python3 runtimes/mcp/render/render_gemini.py`. Do not hand-edit the generated file - edit `servers.yaml` and re-render.

## Before Publishing

This repo's sanitization tooling is in `.claude/` (Claude-Code-specific) but the wordlist at `.claude/.forbidden-strings.txt` applies to all tracked content regardless of which vendor authored it. Confirm new Gemini config or content passes the same check before committing.
