---
name: add-vendor
description: Interactive workflow for adding a new agent CLI vendor to the SpecRoute supported matrix. Walks through scaffolding the runtime layout, adding the vendor's row to the matrix table, creating the per-vendor rule file, wiring MCP rendering (if applicable), and updating cross-vendor sync. Use when proposing or implementing support for a new agent CLI.
argument-hint: "[vendor-name]"
user-invocable: true
allowed-tools: Read Write Edit Glob Grep Bash
---

# Add Vendor

Adds a new agent CLI vendor to SpecRoute end-to-end. The supported vendor matrix in the README is the contract - adding a vendor means a new column, not a fork.

## When to use

- A new agent CLI tool (e.g. Aider, Continue, Open Interpreter, etc.) needs SpecRoute support
- Updating SpecRoute to track a vendor's new feature (e.g. a vendor adds slash-command support)

## Step 1: Gather vendor information

Ask the user (or parse from the argument):

1. **Vendor name** (slug, lowercase): used as `runtimes/.<vendor>/`
2. **Runtime directory convention**: where does this vendor expect its config? (`.<vendor>/`, `.config/<vendor>/`, etc.)
3. **Root context file convention**: does this vendor read a top-level `<VENDOR>.md`? Does it delegate to AGENTS.md?
4. **Skills support**: does the vendor support skills? In what shape (folder-per-skill `SKILL.md`? Single config file?)?
5. **Agents support**: same question for agents.
6. **Commands support**: slash commands? In what shape?
7. **Hooks support**: event-triggered automation? Trigger types?
8. **MCP support**: which file? What format?
9. **Rules support**: where does the vendor read engineering rules?

## Step 2: Scaffold the runtime layout

Create `runtimes/.<vendor>/` with:

- `README.md` - what each subdir contains, the frontmatter contracts, drop-in instructions
- One subdir per supported feature (skills/, agents/, commands/, hooks/, rules/)
- Config template files with `.template.<ext>` suffix (e.g. `settings.template.json`)
- For features the vendor doesn't support, do NOT create empty dirs - document the gap in the README

## Step 3: Update the supported vendor matrix

Edit the matrix table in all four mirror locations (keep them lock-step):

- `README.md`
- `AGENTS.md`
- `wiki/Vendor-Matrix.md`
- `agentic-docs/agent-cli-integrations.md`

Add the new vendor row, naming the vendor's native shape for each capability (skills, agents, commands, hooks, MCP). Also update the context-file table in `agentic-docs/multi-vendor-context-files.md` if the vendor reads a root context file.

## Step 4: Create the per-vendor rule file

`rules/<vendor>-rules.md`:

- Vendor-specific rule file conventions (e.g. Cursor `.mdc` with `alwaysApply: true`, Windsurf `*.md` with custom frontmatter)
- Defer to `rules/engineering-rules.md`, `rules/code-review-rules.md` etc. for shared content
- Document the inclusion semantics (always-on vs file-pattern-matched) per the vendor's loader

## Step 5: Wire MCP rendering (if applicable)

If the vendor has an MCP config:

- Update `runtimes/mcp/render/` with a renderer that emits the vendor's MCP config from `runtimes/mcp/servers.yaml`
- Add the new format to `runtimes/mcp/README.md`

## Step 6: Update cross-vendor sync

If the vendor carries folder-per-skill `SKILL.md` skills:

- Add the vendor slug to `SKILL_VENDORS` in `tools/sync-skills.py`. The tool is **body-aware**: it syncs the SKILL.md body and preserves each vendor's own frontmatter, so differing skill frontmatter contracts are fine.
- Do **not** wire agent syncing - agent formats diverge across vendors (Claude flat Markdown, Codex TOML, Devin `AGENT.md` dirs), so agents are maintained per vendor.
- Update `agentic-docs/cross-vendor-sync.md` to describe the new sync target.

## Step 7: Update the worked example

If the vendor supports any of the artifacts in `examples/sample-project/`, mirror the example into `runtimes/.<vendor>/` so consumers can see the vendor-specific shape.

## Step 8: Report

Final checklist for the user:

- [ ] Runtime layout scaffolded
- [ ] Vendor matrix updated in README, agent-cli-integrations, multi-vendor-context-files
- [ ] Per-vendor rule file created
- [ ] MCP rendering wired (if applicable)
- [ ] Cross-vendor sync updated (if applicable)
- [ ] Worked example mirrored (if applicable)
- [ ] `sanitization-auditor` run on the new content
- [ ] `template-quality-reviewer` run on any new templates

## Don't use for

- Updating an existing vendor's runtime - use direct edits or invoke `runtime-architect`.
- One-off vendor experiments that aren't being committed to the matrix - use a sandbox branch.
