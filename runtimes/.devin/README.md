# `.devin/` — Devin Desktop runtime

This is SpecRoute's single runtime for **Devin Desktop**. It targets the
next-generation Devin Local agent harness shared with Devin CLI.

## Layout

```text
.devin/
├── agents/
│   └── <name>/AGENT.md              experimental custom subagents
├── skills/
│   └── <slug>/SKILL.md              reusable prompts and workflows
├── hooks.v1.json                    lifecycle hooks
├── hooks/scripts/*.sh               scripts invoked by the hook file
├── config.json                      MCP servers and project settings
└── rules/                           optional Cascade-facing rule files
```

Root and nested `AGENTS.md` files are the recommended rules mechanism for
Devin Local. `.devin/rules/` remains in this bundle for Devin Desktop's Cascade
rules engine; it is not the primary Local rules path.

## Setup

1. Copy the runtime:

   ```bash
   mkdir -p .devin
   cp -R runtimes/.devin/. .devin/
   cp .devin/hooks/hooks.v1.template.json .devin/hooks.v1.json
   cp .devin/config.template.json .devin/config.json
   chmod +x .devin/hooks/scripts/*.sh
   ```

2. Create the gitignored, per-installation sanitization wordlist:

   ```bash
   printf '# One whitespace-free term per line.\n' > .devin/.forbidden-strings.txt
   echo '.devin/.forbidden-strings.txt' >> .gitignore
   ```

3. Keep secrets in `.devin/config.local.json`, which Devin treats as a local
   override. Do not add credentials to the tracked template.

4. Verify:

   ```bash
   python3 -m json.tool .devin/hooks.v1.json >/dev/null
   python3 -m json.tool .devin/config.json >/dev/null
   bash -n .devin/hooks/scripts/*.sh
   ```

## Supported artifacts

- **Rules/context**: `AGENTS.md` is recommended. `AGENTS.local.md` is the
  personal, gitignored alternative.
- **Skills**: `.devin/skills/<slug>/SKILL.md`; `.agents/skills/` is also
  supported.
- **Subagents**: `.devin/agents/<name>/AGENT.md`; custom subagents are
  currently experimental.
- **Commands**: skills are invoked as `/skill-name`.
- **Hooks**: `.devin/hooks.v1.json` using the Devin CLI lifecycle format.
- **MCP**: `.devin/config.json` under `mcpServers`; personal values belong in
  `.devin/config.local.json`.

## Cascade compatibility

Devin Desktop still includes the legacy Cascade agent during the transition.
Cascade uses `.windsurf/workflows/`, `.windsurf/hooks.json`, and
`~/.codeium/windsurf/mcp_config.json`. Those are compatibility paths inside
Devin Desktop, not a separate SpecRoute vendor or runtime. Devin Local does not
support Cascade workflows; migrate repeatable workflows to skills.

The public product name in SpecRoute is always **Devin Desktop**. The old name
appears only in literal paths, migration notes, or historical release context.
