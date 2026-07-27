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
├── .devin/                              Devin Desktop runtime layout
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
   mv .claude/mcp.template.json .mcp.json                                 # Claude Code reads .mcp.json at repo root
   mv .claude/hooks/hooks.template.json .claude/hooks/hooks.json          # annotated hook source; see below
   chmod +x .claude/hooks/scripts/*.sh
   ```

   **Hooks live in `settings.json`, not in `hooks/hooks.json`.** Claude Code reads project hooks from `.claude/settings.json`, `.claude/settings.local.json`, `~/.claude/settings.json`, managed policy, plugin `hooks/hooks.json`, and skill/agent frontmatter - a *project-level* `.claude/hooks/hooks.json` is not a hook source and loading it is a plugins-only behaviour. `settings.template.json` therefore ships a working `hooks` key inline, so the `mv` above is enough to get firing hooks. `hooks/hooks.json` is kept as the annotated original you edit by hand; after editing it, merge it back:

   ```bash
   tools/sync-hooks-to-settings.sh .claude/hooks/hooks.json .claude/settings.json
   ```

   Confirm the wiring landed (`jq` exits 0 and prints the commands):

   ```bash
   jq -e '.hooks | to_entries[] | .value[].hooks[].command' .claude/settings.json
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
| Devin Desktop | [`.devin/README.md`](.devin/README.md) |
| MCP single-source | [`mcp/README.md`](mcp/README.md) |

## Cross-vendor parity

As of mid-2026 all six vendors support the same capability set (skills, agents, commands, hooks, MCP) - they differ in **file format**, not capability class:

- **Skills** (folder-per-skill `SKILL.md`) - the Agent Skills open standard; identical across every vendor.
- **Agents** - format diverges: flat Markdown for Claude/Gemini/Kiro/Cursor, standalone TOML for Codex (`<name>.toml`), per-profile `AGENT.md` dirs for Devin.
- **Commands** - Markdown for Claude/Cursor, TOML for Gemini, and skills for Codex/Kiro/Devin.
- **Hooks** - every vendor has them, but the config file each one reads differs. For Claude Code that file is `.claude/settings.json`; the `hooks/hooks.json` in this layout is an authoring convenience, not a runtime source. See [`.claude/README.md`](.claude/README.md#where-hooks-actually-live).

The matrix is documented in the root [`README.md`](../README.md). Adding a new vendor means a new column in the matrix and a new runtime directory here.

To check that Claude / Codex **skills** stay in sync: run [`tools/sync-skills.py --dry-run`](../tools/sync-skills.py) or the `/parity` command. Agents are not synced - the formats diverge.

To check that each `hooks.json` still matches the `hooks` key in its `settings.json`: run [`tools/sync-hooks-to-settings.sh --check`](../tools/sync-hooks-to-settings.sh). It exits 2 on drift and writes nothing.

## Authoring agent

Building, maintaining, and adding new vendors to runtime layouts is owned by the `runtime-architect` agent. See `.claude/agents/runtime-architect.md` for its operating principles.
