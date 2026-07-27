# SpecRoute Implementation Agents

This directory contains the **12 Claude Code agents** that implement the SpecRoute skeleton. They are project-internal - they build SpecRoute itself, not consumer-facing templates that ship as artifacts.

Consumer-facing agent templates live separately in `agents/` (the SpecRoute artifact directory), with reference layouts in `runtimes/.claude/agents/`.

## Roster

**Verified against disk on 2026-07-27.** `Model` and `Color` below are copied from each file's frontmatter; `Owns` summarizes each file's `## Owns` section. `Department` is a README-only grouping - agent files carry no department field.

| Agent | Department | Model | Color | Memory | Owns |
|---|---|---|---|---|---|
| `prd-author` | Specification | opus | blue | - | `prds/` - PRD templates, lifecycle, examples |
| `spec-author` | Specification | opus | cyan | - | `specs/` - spec triplet (requirements/design/tasks), feature/technical specs, ADRs |
| `agent-roster-architect` | Specification | opus | purple | - | `agents/` - agent template, archetypes, examples, cross-vendor roster |
| `skill-author` | Implementation | opus | green | - | `skills/` - folder-per-skill `SKILL.md` template + examples |
| `prompt-engineer` | Implementation | opus | yellow | - | `prompts/` - global/phase/task master-prompt templates + per-vendor prompts |
| `command-author` | Implementation | sonnet | orange | - | `commands/` - Claude Markdown + Gemini **TOML** command templates |
| `hooks-author` | Implementation | sonnet | red | - | `hooks/` - Claude `hooks.template.json` + Kiro examples at `hooks/kiro/examples/*.json` |
| `runtime-architect` | Integration | opus | pink | project | `runtimes/`, `tools/sync-skills.py` - per-vendor runtime layouts + MCP single-source + cross-vendor sync |
| `framework-docs-author` | Documentation | opus | blue | project | `agentic-docs/`, `workflows/`, root context files (README, CLAUDE.md, GEMINI.md, AGENTS.md) |
| `sanitization-auditor` | Quality | opus | red | project | Pre-commit / pre-PR audits - blocks any private-project leak |
| `template-quality-reviewer` | Quality | sonnet | yellow | - | Template quality bar - production-grade, immediately usable, has worked examples |
| `docs-currency-auditor` | Quality | opus | orange | project | Vendor facts, version anchors, transition dates, counts that must match disk, cross-mirror consistency |

Current split: **9 opus, 3 sonnet**; four agents declare `memory: project`. Regenerate the model and color columns rather than editing them by hand:

```bash
# Model counts
grep -h '^model:' .claude/agents/*.md | sort | uniq -c

# Per-agent model + color, in table order
awk 'FNR==1 { n = split(FILENAME, p, "/"); f = p[n] }
     /^(model|color):/ { printf "%s\t%s\n", f, $0 }' .claude/agents/*.md
```

If either command disagrees with the table, the table is wrong - fix the table and bump the verification date above.

## When to invoke which

- **Adding a new artifact type** (e.g. a new template under `prds/templates/` or a new skill in `skills/examples/`): the corresponding author agent.
- **Adding a new vendor** (e.g. a new runtime layout under `runtimes/`): `runtime-architect` - coordinate with `framework-docs-author` for the matrix update and the per-vendor rule file.
- **Cross-cutting changes** (e.g. updating the supported vendor matrix in multiple files): `framework-docs-author` for the README/docs, then individual authors for each vendor's content.
- **Before any commit or PR**: `sanitization-auditor` (always) and `template-quality-reviewer` (when templates change).

## Coordination patterns

| Scenario | Lead | Supporting |
|---|---|---|
| Build the worked example in `examples/sample-project/` | `prd-author` (PRD) → `spec-author` (triplet) → `agent-roster-architect` (roster) → `prompt-engineer` (prompts) | `template-quality-reviewer` (final) |
| Add a new vendor to the matrix | `runtime-architect` | `framework-docs-author`, `command-author`, `hooks-author`, `skill-author` (vendor-specific shapes) |
| Set up the MCP single-source-of-truth | `runtime-architect` | `framework-docs-author` (`agentic-docs/cross-vendor-sync.md`) |
| Pre-publish review | `sanitization-auditor` | `template-quality-reviewer` |

## Notes

- Agents follow Claude Code's flat-file frontmatter convention. **Only `name` and `description` are required**; `model` and `color` are optional (an absent `model` inherits the parent session's). Every agent here sets all four for legibility. The `description` field includes trigger phrases that drive auto-selection.
- `model` takes a real Claude Code value - `opus`, `sonnet`, `haiku`, `fable`, a full model id, or `inherit`. SpecRoute's `flagship` / `balanced` / `fast` tier words belong in roster tables and vendor-neutral prose only; see [`wiki/Agents.md`](../../wiki/Agents.md#semantic-model-tiers) for the canonical mapping.
- There is no `internet:` field in any runtime. Web access is expressed through `tools` (`WebFetch` / `WebSearch`).
- Other optional fields worth reaching for: `tools`, `disallowedTools`, `skills`, `memory`, `effort`, `isolation`, `permissionMode`. See [`wiki/Frontmatter-Contracts.md`](../../wiki/Frontmatter-Contracts.md).
- `description` fields use hyphens instead of colons inside the YAML scalar to avoid YAML parsing issues with the `Triggers - "..."` enumeration.
- Sample agent definitions in this repo's `agents/examples/` (consumer templates) follow the same shape - these `.claude/agents/` files double as reference implementations.
- Generic domains only. No financial, healthcare, or other proprietary domain logic in any agent's content.
