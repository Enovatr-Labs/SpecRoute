# GEMINI.md

This file provides Gemini-specific guidance for working in this repository.

## Source of truth

For repository overview, artifact taxonomy, vendor matrix, hard constraints, and the spec-driven flow: read [`AGENTS.md`](AGENTS.md). It is the canonical, vendor-neutral context file. This file is a delegation shim and holds only Gemini-specific notes.

## Gemini-specific notes

### Runtime layout

Gemini reads:

- `.gemini/settings.json` — MCP server map (`mcpServers`).
- `.gemini/gemini_cli_config.json` — JSON command map (`commands` → `{command, description, directory?}`).

Templates for both live in `runtimes/.gemini/`. Drop them into your repo and edit.

### What Gemini supports in the SpecForge matrix

Gemini's first-class concepts are commands and MCP. It does **not** consume `SKILL.md` folders, flat agent files, or hook configurations as Claude Code and Codex do. When SpecForge discusses skills or agents, those are not directly invokable in Gemini — but the underlying prompts under `prompts/` and the rules under `rules/gemini-rules.md` are.

### Commands are JSON, not markdown

Unlike Claude Code's `commands/<name>.md` shape, Gemini's commands are entries in `.gemini/gemini_cli_config.json`. Each entry runs a shell command, not a prompt. See `commands/command-template.gemini.json` for the template.

## Working in this repo

Read [`AGENTS.md`](AGENTS.md). Then read this file. That's it.
