# AGENTS.md

**Canonical, vendor-neutral context file for SpecForge.** This is the single source of truth that every agent CLI working in this repository should read first. Vendor-specific files (`CLAUDE.md`, `GEMINI.md`) are short delegation shims that point here.

## What this repository is

SpecForge is an open-source framework for **spec-driven agentic software engineering**, vendor-neutral across Claude Code, Codex, Gemini CLI, Kiro, Cursor, and Windsurf. It ships markdown content - templates, prompts, agent definitions, runtime layouts, and engineering rules - not application code.

There is no package manager, no build step, no test suite, no lint config. Do not look for `package.json` or run tests; treat this as a documentation/templates repository.

## What "spec-driven" means here

The canonical flow is:

```
PRD → Spec (requirements + design + tasks) → Implementation → Validation → Review
```

Each stage has a template, an agent assignment, and an acceptance criterion. The point is not to slow work down - it's to make agent output reviewable. Code generation without a written spec is the failure mode this framework exists to prevent.

## Core artifact taxonomy

| Artifact | What it is | Lives in |
|---|---|---|
| **PRD** | Business intent, goals, scope, success metrics | `prds/` |
| **Spec** | Requirements + design + tasks (or single feature spec) | `specs/` |
| **Agent** | Defined role + model + tools, invokable by a runtime | `agents/` |
| **Skill** | Interactive parameterized workflow (folder-per-skill `SKILL.md`) | `skills/` |
| **Command** | Simple slash-invoked operation, vendor-specific shape | `commands/` |
| **Hook** | Event-triggered automation (file edit, pre-commit, session start) | `hooks/` |
| **Prompt** | Reusable prompt - global master, phase master, or task | `prompts/` |
| **Workflow** | End-to-end execution model | `workflows/` |
| **Rule** | Engineering standard, vendor-specific or shared | `rules/` |
| **Runtime** | Copy-pasteable per-vendor layout consumers drop into their own repos | `runtimes/` |

When to reach for which: see [`docs/automation-decision-framework.md`](docs/automation-decision-framework.md) - the 4-row decision matrix for Skill / Agent / Command / Hook.

## Supported vendor matrix

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| Claude Code | `.claude/` | `CLAUDE.md` | folder-per-skill `SKILL.md` | flat `<name>.md` + frontmatter | `commands/<name>.md` | `settings.json hooks` (~27 events, 5 hook types) | `claude_desktop_config.json` |
| Codex | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` | flat `<name>.md` | via skills (`user-invocable: true`) | `hooks.json` or `config.toml [hooks]` (6 events; flag `codex_hooks=true`) | `config.toml [mcp_servers]` |
| Gemini CLI | `.gemini/` | `GEMINI.md` (delegation shim) | - | - | `gemini_cli_config.json` | `settings.json hooks` (11 events; v0.26.0+) | `settings.json [mcpServers]` |
| Kiro | `.kiro/` | `steering/` files | - | - | - | `*.kiro.hook` (10 events incl. file/agent/task triggers) | - |
| Cursor | `.cursor/rules/` | `.cursorrules` | - | - | - | `hooks.json` v1 (~19 events; permission/decision schema) | - |
| Windsurf | `.windsurf/rules/` | - | - | - | - | `hooks.json` (12 events; pre-hooks block, post-hooks observe) | - |

Vendor neutrality is the contract. Adding a new tool = a new column, not a fork. The matrix is mirrored in [`README.md`](README.md), [`docs/agent-cli-integrations.md`](docs/agent-cli-integrations.md), and [`docs/multi-vendor-context-files.md`](docs/multi-vendor-context-files.md); when one changes, all three change in lock-step.

## Hard constraints

These are the rules that aren't obvious from the code and must be respected.

1. **Vendor neutrality.** Don't fold one vendor into another. Don't treat any vendor as the default. Every artifact declares which vendors it targets and uses each vendor's native shape.

2. **Sanitization.** Patterns in this repo are generalized from internal codebases. Never commit proprietary business logic, domain models, customer data, private endpoints, credentials, or internal product names. Generalize before adding. Run `/sanitize` before every commit; the PreToolUse hook (`.claude/hooks/pre-bash-sanitize.sh`) will block `git commit` / `git push` if forbidden strings appear in tracked files.

3. **Spec-driven order.** PRD → spec triplet → tasks → implementation → validation → review. New examples and workflows reflect that order; don't jump straight to code.

4. **Folder-per-skill, flat-file-agent.** Skills are directories containing `SKILL.md` (with frontmatter `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools`). Agents are flat `<name>.md` files (with frontmatter `name`, `description`, `model`, `color`). These contracts are load-bearing - artifacts that violate them won't register in the runtime.

5. **Two-tier docs.** Root context files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) stay short. Deep references live in `docs/`. See [`docs/two-tier-docs-pattern.md`](docs/two-tier-docs-pattern.md).

6. **TODO markers are intentional.** They mark places where a real example or value should later be added. Don't fill them with invented content; flag clearly when an example is illustrative.

7. **Templates over theory.** Templates must be production-grade and immediately usable, not abstract checklists. The `template-quality-reviewer` agent enforces this bar.

## SpecForge implementation runtime

This repo's own `.claude/` directory is wired up as the SpecForge implementation team. It does **not** contain consumer-facing templates (those live in `agents/`, `skills/`, `commands/`, `hooks/`).

| Path | What's there |
|---|---|
| `.claude/agents/` | 11 implementation agents - see `.claude/agents/README.md` for the roster |
| `.claude/skills/` | Contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`) |
| `.claude/commands/` | Slash commands (`/sanitize`, `/status`, `/audit`, `/parity`) |
| `.claude/hooks/` | SessionStart status banner, PreToolUse sanitization gate, PostToolUse frontmatter check |
| `.claude/agent-memory/` | Per-agent persistent context |

When adding a new top-level artifact, prefer invoking the corresponding agent (`prd-author`, `spec-author`, etc.) - they own the contracts. The agent files are the authoritative briefs.

## Working in this repo

- Edits are almost always to markdown files. Use `Edit`/`Write` directly; nothing to compile or run.
- Before adding a new artifact, check `initial.md` (gitignored, locally) for the intended location and check sibling files for the established shape.
- If a top-level directory in the intended structure doesn't exist yet, create it as part of the work - but include the `README.md` for that directory at the same time.
- Run `/audit` before any commit. The PreToolUse hook will block publish-style git operations if forbidden strings are present.

## Getting oriented

1. Read [`README.md`](README.md) for the public framing.
2. Read [`docs/philosophy.md`](docs/philosophy.md) and [`docs/spec-driven-development.md`](docs/spec-driven-development.md) for the why.
3. Read [`docs/automation-decision-framework.md`](docs/automation-decision-framework.md) for when to reach for which artifact.
4. Walk the worked example in [`examples/sample-feature/`](examples/sample-feature/) - it exercises every artifact shape end-to-end.
5. Pick a vendor and copy `runtimes/.<vendor>/` into your own repo to start using SpecForge.
