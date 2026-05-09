# Tools

Cross-runtime utility scripts for SpecForge consumers. These are templates - fork them as your project grows.

```
tools/
├── README.md                            (this file)
└── sync-skills.py                       cross-runtime skill and agent sync
```

## `sync-skills.py`

Diff-and-copy `runtimes/.claude/` ↔ `runtimes/.codex/` for the artifact shapes they share: skills (folder-per-skill `SKILL.md`) and agents (flat `<name>.md`).

### Usage

```bash
# Dry run (default): report drift without writing.
python3 tools/sync-skills.py

# Apply: copy missing skills/agents and overwrite drift with the source version.
python3 tools/sync-skills.py --apply

# Reverse direction: sync from Codex to Claude.
python3 tools/sync-skills.py --source codex --apply
```

### Output

The script reports:

- **MISSING** - file or folder exists in the source but not the target.
- **EXTRA** - file or folder exists in the target but not the source. The script never auto-removes; you decide whether the extra is intentional (Claude-only or Codex-only) or stale.
- **DRIFT** - file exists in both but contents differ.

### When drift is intentional

Some skills genuinely belong to only one vendor (e.g. a Claude skill that uses the `Task` tool has no Codex equivalent). In that case:

1. Document the asymmetry in `runtimes/README.md` or the skill's own `SKILL.md` body.
2. Accept the EXTRA in `sync-skills.py --dry-run` output as expected.

If most skills should be in lock-step but a handful are intentional asymmetries, consider extending `sync-skills.py` with an ignore list.

### Extending

The script is intentionally simple (~150 lines). Common extensions:

- **Hooks sync** - copy hooks across vendors that support them (Claude Code, Kiro). The shapes differ; you'd render rather than copy. See `runtimes/mcp/render/` for the rendering pattern.
- **Selective sync** - only copy skills matching a name pattern.
- **Pre-flight validation** - run frontmatter linting before copying.
- **Git-aware sync** - only sync skills that have changed in the last commit.

Treat this script as a starting point, not a final tool.

## Adding a new tool

When you need a new utility:

1. Make it self-contained - no external dependencies beyond the Python standard library when possible.
2. Default to dry-run; gate destructive operations behind explicit flags.
3. Print findings as a punch list so reviewers can scan results.
4. Document in this README.

## Authoring agent

Cross-vendor sync utilities (and the runtime layouts they sync) are owned by the `runtime-architect` agent.
