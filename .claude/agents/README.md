# SpecForge Implementation Agents

This directory contains the **11 Claude Code agents** that implement the SpecForge skeleton. They are project-internal — they build SpecForge itself, not consumer-facing templates that ship as artifacts.

Consumer-facing agent templates live separately in `agents/` (the SpecForge artifact directory), with reference layouts in `runtimes/.claude/agents/`.

## Roster

| Agent | Department | Model | Color | Owns |
|---|---|---|---|---|
| `prd-author` | Specification | opus | blue | `prds/` — PRD templates, lifecycle, examples |
| `spec-author` | Specification | opus | cyan | `specs/` — spec triplet (requirements/design/tasks), feature/technical specs, ADRs |
| `agent-roster-architect` | Specification | opus | purple | `agents/` — agent template, archetypes, examples, cross-vendor roster |
| `skill-author` | Implementation | opus | green | `skills/` — folder-per-skill `SKILL.md` template + examples |
| `prompt-engineer` | Implementation | opus | yellow | `prompts/` — global/phase/task master-prompt templates + per-vendor prompts |
| `command-author` | Implementation | sonnet | orange | `commands/` — Claude markdown + Gemini JSON command templates |
| `hooks-author` | Implementation | sonnet | red | `hooks/` — Claude hooks.json + Kiro `.kiro.hook` examples |
| `runtime-architect` | Integration | opus | pink | `runtimes/`, `tools/sync-skills.py` — per-vendor runtime layouts + MCP single-source + cross-vendor sync |
| `framework-docs-author` | Documentation | opus | blue | `docs/`, `workflows/`, root context files (README, CLAUDE.md, GEMINI.md, AGENTS.md) |
| `sanitization-auditor` | Quality | opus | red | Pre-commit / pre-PR audits — blocks any private-project leak |
| `template-quality-reviewer` | Quality | sonnet | yellow | Template quality bar — production-grade, immediately usable, has worked examples |

## When to invoke which

- **Adding a new artifact type** (e.g. a new template under `prds/templates/` or a new skill in `skills/examples/`): the corresponding author agent.
- **Adding a new vendor** (e.g. a new runtime layout under `runtimes/`): `runtime-architect` — coordinate with `framework-docs-author` for the matrix update and the per-vendor rule file.
- **Cross-cutting changes** (e.g. updating the supported vendor matrix in multiple files): `framework-docs-author` for the README/docs, then individual authors for each vendor's content.
- **Before any commit or PR**: `sanitization-auditor` (always) and `template-quality-reviewer` (when templates change).

## Coordination patterns

| Scenario | Lead | Supporting |
|---|---|---|
| Build the worked example in `examples/sample-feature/` | `prd-author` (PRD) → `spec-author` (triplet) → `agent-roster-architect` (roster) → `prompt-engineer` (prompts) | `template-quality-reviewer` (final) |
| Add a new vendor to the matrix | `runtime-architect` | `framework-docs-author`, `command-author`, `hooks-author`, `skill-author` (vendor-specific shapes) |
| Set up the MCP single-source-of-truth | `runtime-architect` | `framework-docs-author` (`docs/cross-vendor-sync.md`) |
| Pre-publish review | `sanitization-auditor` | `template-quality-reviewer` |

## Notes

- Agents follow Claude Code's flat-file frontmatter convention: `name`, `description`, `model`, `color`. The `description` field includes trigger phrases that drive auto-selection.
- `description` fields use hyphens instead of colons inside the YAML scalar to avoid YAML parsing issues with the `Triggers - "..."` enumeration.
- Sample agent definitions in this repo's `agents/examples/` (consumer templates) follow the same shape — these `.claude/agents/` files double as reference implementations.
- Generic domains only. No financial, healthcare, or other proprietary domain logic in any agent's content.
