# Quickstart

Get a working SpecRoute setup in your own repo in 15 minutes.

## Prerequisites

- A repository you control.
- One or more supported agent CLIs installed locally. All six (Claude Code,
  Codex, Gemini, Kiro, Cursor, and Devin Desktop) support the same capability
  set; they differ in file format, not capability class. See [[Vendor Matrix]].
- `git`, `python3` (only if you'll use `tools/sync-skills.py` or the MCP renderers).

## Three paths

### A. "Just show me how it works" (5 min)

Walk the [[Worked Example]] in spec-driven order:

1. [PRD](https://github.com/Enovatr-Labs/SpecRoute/blob/main/examples/sample-project/prds/active/user-search.md) — read as a product reviewer.
2. [`requirements.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/examples/sample-project/specs/user-search/requirements.md) — see how PRD goals translate to stable-ID requirements.
3. [`design.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/examples/sample-project/specs/user-search/design.md) — see how requirements drive the architecture.
4. [`tasks.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/examples/sample-project/specs/user-search/tasks.md) — see how design decomposes into numbered work items with back-refs.
5. [`prompts/000_GLOBAL_MASTER.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/examples/sample-project/prompts/000_GLOBAL_MASTER.md) — the agent CLI entry-point.
6. Open any phase master and any numbered task prompt.

### B. "Bootstrap a new feature from the templates" (10 min)

```bash
# In your repo:
# 1. Copy a PRD template
cp SpecRoute/prds/templates/lightweight-prd-template.md prds/active/<your-feature>.md

# 2. Fill it in (Status: Draft → Approved per the lifecycle).

# 3. Generate the spec triplet from the PRD using prompts/shared/prd-to-spec-prompt.md.

# 4. Generate tasks from requirements + design using prompts/shared/spec-to-tasks-prompt.md.

# 5. Implement task by task per the spec-to-implementation workflow.
```

See [[PRDs]], [[Specs]], [[Workflow Spec to Implementation]].

### C. "Drop the runtime in" (15 min)

Pick the vendors you target (see [[Vendor Matrix]]) and copy the corresponding runtime directories:

```bash
# Claude Code
cp -R SpecRoute/runtimes/.claude/ /path/to/your/repo/.claude/
cd /path/to/your/repo/.claude
mv settings.template.json            settings.json
mv settings.local.template.json      settings.local.json
mv mcp.template.json                 ../.mcp.json    # Claude Code CLI reads .mcp.json at repo root
mv hooks/hooks.template.json         hooks/hooks.json
chmod +x hooks/scripts/*.sh

# Hooks EXECUTE from settings.json's `hooks` key - a bare .claude/hooks/hooks.json is
# only read for plugins, never for a project. settings.template.json already ships a
# working `hooks` block, so the copy above is enough. If you keep editing hooks.json as
# your annotated source of truth, re-merge it after each change:
#   bash /path/to/SpecRoute/tools/sync-hooks-to-settings.sh
jq -e '.hooks' settings.json >/dev/null && echo "hooks wired"

# Set up the sanitization wordlist (gitignored)
touch .forbidden-strings.txt
echo ".claude/settings.local.json"       >> ../.gitignore
echo ".claude/.forbidden-strings.txt"    >> ../.gitignore
```

For other vendors (Codex, Gemini, Kiro, Cursor, and Devin Desktop), the
per-vendor README under `runtimes/.<vendor>/` walks the exact steps. See
[[Agent CLI Integrations]] for all six.

## Run the canonical example

```bash
# 1. Copy the worked example into a new repo.
cp -R SpecRoute/examples/sample-project/. /path/to/your-new-repo/
cd /path/to/your-new-repo/

# 2. Rename .template files (they become gitignored).
mv .claude/settings.local.template.json     .claude/settings.local.json
mv .claude/mcp.template.json                 .mcp.json    # Claude Code CLI reads .mcp.json at repo root
mv .claude/.forbidden-strings.template.txt  .claude/.forbidden-strings.txt

# 3. Add the renamed files to .gitignore.
cat >> .gitignore <<'EOF'
.claude/settings.local.json
.claude/.forbidden-strings.txt
EOF

# 4. Open in Claude Code and run:
#    "Read prompts/000_GLOBAL_MASTER.md, then run prompts/runtime/pickup-next-task.md."
```

The implementation team in `.claude/agents/` reads the spec triplet, picks the next unblocked task, and drives implementation phase-by-phase. See [[Worked Example]] for the full walkthrough.

## What to read next

- [[Philosophy]] — why spec-driven beats "I'll figure it out as I go."
- [[Automation Decision Framework]] — when to reach for skill vs agent vs command vs hook.
- [[Workflow PRD to Production]] — the outer engineering loop.
- [[Vendor Matrix]] — what each supported CLI does and doesn't support.
