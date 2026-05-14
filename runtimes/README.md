# Runtimes

Copy-pasteable per-vendor runtime layouts. Drop the relevant `runtimes/.<vendor>/` directory into your project's repo and the agent CLI of that vendor will pick it up automatically.

```
runtimes/
├── README.md                            (this file)
├── .claude/                             Claude Code runtime layout
├── .codex/                              Codex runtime layout
├── .gemini/                             Gemini CLI runtime layout
├── .kiro/                               Kiro runtime layout
├── .cursor/                             Cursor runtime layout
├── .windsurf/                           Windsurf runtime layout
└── mcp/                                 MCP single source of truth + renderers
```

## How to use

1. **Pick the vendors your project targets.** See the [supported vendor matrix](../README.md#supported-vendor-matrix) in the root README.

2. **Copy the relevant runtime layouts into your project's root**:

   ```bash
   # Example: copy Claude Code and Codex layouts into the consumer's repo.
   cp -R runtimes/.claude/  /path/to/your/repo/.claude/
   cp -R runtimes/.codex/   /path/to/your/repo/.codex/
   ```

3. **Rename `.template`-suffixed files**:

   ```bash
   cd /path/to/your/repo
   mv .claude/settings.template.json .claude/settings.json
   mv .claude/settings.local.template.json .claude/settings.local.json    # then customize
   mv .claude/claude_desktop_config.template.json .claude/claude_desktop_config.json
   mv .claude/hooks/hooks.template.json .claude/hooks/hooks.json
   ```

4. **Add to `.gitignore`** (per the per-runtime README):

   ```
   .claude/settings.local.json
   .claude/.forbidden-strings.txt
   .codex/local-overrides.toml
   ```

5. **Wire MCP** if your team uses it:

   - Edit `runtimes/mcp/servers.yaml` for your server inventory.
   - Run the renderers: `python3 runtimes/mcp/render/render_<vendor>.py > <output path>`.
   - Or, if your project ships its own `runtimes/mcp/`, maintain it there and point each vendor's MCP config at the rendered output.

6. **Populate agents, skills, commands, hooks** as your project requires. See per-runtime READMEs for the file shapes each vendor consumes.

## Per-runtime READMEs

| Runtime | README |
|---|---|
| Claude Code | [`.claude/README.md`](.claude/README.md) |
| Codex | [`.codex/README.md`](.codex/README.md) |
| Gemini CLI | [`.gemini/README.md`](.gemini/README.md) |
| Kiro | [`.kiro/README.md`](.kiro/README.md) |
| Cursor | [`.cursor/README.md`](.cursor/README.md) |
| Windsurf | [`.windsurf/README.md`](.windsurf/README.md) |
| MCP single-source | [`mcp/README.md`](mcp/README.md) |

## Cross-vendor parity

Two vendors share most artifact shapes (Claude Code and Codex):

- Agents (flat `<name>.md` with frontmatter) - identical.
- Skills (folder-per-skill `SKILL.md`) - identical.

The other vendors have different concepts. The matrix is documented in the root [`README.md`](../README.md). Adding a new vendor means a new column in the matrix and a new runtime directory here.

To check that Claude / Codex stay in sync: run [`tools/sync-skills.py --dry-run`](../tools/sync-skills.py) or the `/parity` command (in the SpecRoute runtime itself).

## Authoring agent

Building, maintaining, and adding new vendors to runtime layouts is owned by the `runtime-architect` agent. See `.claude/agents/runtime-architect.md` for its operating principles.
