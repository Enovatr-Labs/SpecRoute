# `.claude/` - Claude Code runtime layout

Drop this directory into the root of your project (rename or merge with any existing `.claude/`). Claude Code reads from these paths automatically.

## Layout

```
.claude/
├── settings.json                       project-wide settings (tracked)
├── settings.local.json                 per-user overrides (gitignored)
├── (repo root) .mcp.json               MCP server config for the Claude Code CLI
├── agents/<name>.md                    flat-file agents
├── skills/<slug>/SKILL.md              folder-per-skill
├── commands/<name>.md                  slash commands
├── hooks/
│   ├── hooks.json                      hook configuration
│   └── scripts/                        supporting shell scripts
└── agent-memory/<agent-name>/          per-agent persistent context
```

## Setup

1. **Copy templates into place** (rename `.template` suffix off):

   ```bash
   cp runtimes/.claude/settings.template.json .claude/settings.json
   cp runtimes/.claude/settings.local.template.json .claude/settings.local.json
   cp runtimes/.claude/mcp.template.json .mcp.json    # Claude Code reads .mcp.json at the repo root
   cp runtimes/.claude/hooks/hooks.template.json .claude/hooks/hooks.json
   ```

2. **Add to `.gitignore`**:

   ```
   .claude/settings.local.json
   .claude/.forbidden-strings.txt
   ```

3. **Install hook scripts** (starter scripts are included under `hooks/scripts/`):

   ```bash
   mkdir -p .claude/hooks/scripts
   chmod +x .claude/hooks/scripts/*.sh
   ```

4. **Populate the wordlist** (gitignored):

   ```bash
   cat > .claude/.forbidden-strings.txt <<'EOF'
   # Forbidden strings - one per line. Lines starting with '#' are comments.
   # Add upstream private project names, internal identifiers, etc.
   EOF
   ```

5. **Add agents, skills, commands as your project requires.** See per-subdir READMEs.

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.claude/settings.json` | Yes |
| `.claude/settings.local.json` | **No** (per-user) |
| `.claude/.forbidden-strings.txt` | **No** (per-installation) |
| `.mcp.json` (repo root) | Project decision; usually yes (sans secrets) |
| `.claude/agents/*.md` | Yes |
| `.claude/skills/<slug>/SKILL.md` | Yes |
| `.claude/commands/*.md` | Yes |
| `.claude/hooks/hooks.json` | Yes |
| `.claude/hooks/scripts/*.sh` | Yes |
| `.claude/agent-memory/**/*.md` | Yes (treat content as published) |

## Cross-vendor notes

- **Codex** consumes the same agent and skill shapes. Mirror agents and skills into `.codex/` and use `tools/sync-skills.py` to keep them aligned.
- **Gemini, Kiro, Cursor, Windsurf** do not consume Claude's runtime layout. See their respective runtime dirs.

## Reference implementation

This repo's own `.claude/` directory at the repo root is a working example of every concept here. Read those files as worked examples.
