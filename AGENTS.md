# AGENTS.md

**Canonical, vendor-neutral context file for SpecRoute.** This is the single source of truth for every agent CLI working in this repository.

Not every CLI loads it automatically. Codex and Cursor read `AGENTS.md` natively; **Claude Code does not** - its documentation states plainly that it reads `CLAUDE.md`, not `AGENTS.md` - and **Gemini CLI does not** either, since it reads `GEMINI.md` and only picks up `AGENTS.md` if you opt in through `context.fileName`. So `CLAUDE.md` and `GEMINI.md` are short delegation shims that pull this file in (an `@AGENTS.md` import, or a symlink). Blog posts claiming universal native `AGENTS.md` support are wrong; the shim is what makes it universal here.

### About the `AGENTS.md` convention

`AGENTS.md` began as an OpenAI convention and is now stewarded by the **Agentic AI Foundation** under the Linux Foundation, with 60,000+ repositories using it. The convention specifies **no required fields, no frontmatter, and no schema** - it is plain Markdown, and its content is entirely up to the project. Nested `AGENTS.md` files are spec'd behaviour: an agent reads the nearest one up the directory tree.

## What this repository is

SpecRoute is an open-source framework for **spec-driven agentic software engineering**, vendor-neutral across Claude Code, Codex, Gemini CLI, Kiro, Cursor, and Devin Desktop. It ships markdown content - templates, prompts, agent definitions, runtime layouts, and engineering rules - not application code.

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

When to reach for which: see [`agentic-docs/automation-decision-framework.md`](agentic-docs/automation-decision-framework.md) - the 4-row decision matrix for Skill / Agent / Command / Hook. For work that spans several specialists at once, those four compose into the **all-hands** orchestration pattern: [`agentic-docs/multi-agent-orchestration.md`](agentic-docs/multi-agent-orchestration.md).

## Supported vendor matrix

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| Claude Code | `.claude/` | `CLAUDE.md` [^rootfile] | folder-per-skill `SKILL.md` | flat `<name>.md` + frontmatter | `commands/<name>.md` (merged into skills) | `settings.json` `hooks` (30 events; 5 handler types) [^claudehooks] | `.mcp.json` / `~/.claude.json` |
| Codex | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` | `agents/<name>.toml` | skills (`/skills`, `$mention`) | `hooks.json` or `config.toml [hooks]` (11 events; Claude-compatible names) [^codexhooks] | `config.toml [mcp_servers]` |
| Gemini CLI / Antigravity [^antigravity] | `.gemini/` | `GEMINI.md` (delegation shim) [^rootfile] | `skills/<slug>/SKILL.md` | `agents/<name>.md` | TOML in `.gemini/commands/` | `settings.json` `hooks` (11 events; `Before*` / `After*` names) | `settings.json [mcpServers]` |
| Kiro | `.kiro/` | `steering/` files | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `/skill` + manual steering | `.kiro/hooks/<name>.json` v1 (10 triggers) [^kiro10] | `.kiro/settings/mcp.json` |
| Cursor | `.cursor/` | `.cursor/rules/*.mdc` / `AGENTS.md` [^cursorrules] | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `commands/*.md` | `.cursor/hooks.json` v1 (21 events, camelCase) | `.cursor/mcp.json` |
| Devin Desktop [^devin] | `.devin/` | `AGENTS.md` | `.agents/skills/` (recommended) / `.devin/skills/` | `.devin/agents/<name>/AGENT.md` (experimental) | skills (`/skill-name`); Cascade workflows [^devin] | `.devin/hooks.v1.json` (8 events); Cascade hooks [^devin] | `.devin/config.json [mcpServers]`; Cascade MCP [^devin] |

[^rootfile]: Claude Code reads `CLAUDE.md`, **not** `AGENTS.md` - the official documentation says so directly. Gemini CLI reads `GEMINI.md` and only picks up `AGENTS.md` when you opt in via `context.fileName`; the upstream issue asking for default support was closed as not planned. Bridge either with an `@AGENTS.md` import inside the vendor file, or a symlink. Codex, Cursor, and Devin Desktop read `AGENTS.md` natively.
[^claudehooks]: Claude Code loads hooks from `settings.json` (user / project / local), managed policy settings, a **plugin's** `hooks/hooks.json`, and skill or agent frontmatter. A bare project-level `.claude/hooks/hooks.json` is **not** a hook source - keep it as the authoring artifact and merge its `hooks` key into `.claude/settings.json`. The five handler types are `command`, `http`, `mcp_tool`, `prompt`, and `agent`.
[^codexhooks]: Verified against an installed `codex-cli` 0.145.0 binary: `SessionStart`, `SessionEnd`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`. Codex adopted Claude Code's event names and handler JSON (`hookSpecificOutput`, `permissionDecision`, `decision: "block"`) almost verbatim - but the match is close, not total: Claude's `PostToolUseFailure` has no Codex counterpart, and only `type: "command"` actually executes in Codex (`prompt` and `agent` handlers are parsed, then skipped). Hooks are **enabled by default**; the canonical `[features]` key is `hooks`, with `codex_hooks` retained as a deprecated alias. Disable with `[features] hooks = false`.
[^antigravity]: Google redirected consumer access to **Antigravity CLI** on 2026-06-18 for free and Google AI Pro / Ultra tiers. Paid Gemini Code Assist Standard / Enterprise and qualifying API-key users retain Gemini CLI access. The `.gemini/` integration layout remains valid across both.
[^kiro10]: Kiro IDE 1.0 (2026-06-25) replaced the `*.kiro.hook` format with `.kiro/hooks/<name>.json` (root `"version": "v1"`). Triggers (10): `SessionStart`, `Stop`, `PreToolUse`, `PostToolUse`, `PreTaskExec`, `PostTaskExec`, `UserPromptSubmit`, `PostFileCreate`, `PostFileSave`, `PostFileDelete`. The 0.x `Manual` trigger was **retired** - manual invocation is now a steering file. Actions are `action.type: "command"` or `"agent"`, replacing `runCommand` / `askAgent`. Legacy `*.kiro.hook` files show an upgrade badge and no longer execute.
[^cursorrules]: `.cursorrules` has been removed from Cursor's documentation entirely and is reported non-functional in current versions. Treat it as removed rather than legacy-but-supported; use `.cursor/rules/*.mdc`. Cursor also ships Skills, Subagents, Hooks, and a Plugins marketplace.
[^devin]: Devin Desktop is the new name for Windsurf. Devin Local uses the `.devin/` paths shown above and is intended to become the primary local agent. Cascade remains available and still uses `.windsurf/workflows/*.md`, `.windsurf/hooks.json`, and `~/.codeium/windsurf/mcp_config.json`; `.windsurf/rules/` and `.windsurf/skills/` remain accepted compatibility locations. These are Devin Desktop configuration namespaces, not a separate vendor or runtime. Do not infer `.devin/workflows/`, `.devin/hooks.json`, or `.devin/mcp.json`.

All six tools ship the same **capability classes** - skills, agents/subagents, commands, hooks, MCP - but "same classes" is not "converged". **Skills are the one near-total convergence**: the `SKILL.md` shape is portable across all six with little more than a path change. **Hooks are not converged.** Claude Code, Codex, Kiro, and Devin Local share core event names such as `PreToolUse`, `PostToolUse`, and `SessionStart`, while Cursor uses camelCase and Gemini CLI uses `BeforeTool` / `AfterModel` / `BeforeToolSelection`. Similar names do not make the schemas interchangeable. See [`agentic-docs/agent-cli-integrations.md`](agentic-docs/agent-cli-integrations.md).

Vendor neutrality is the contract. Adding a new tool = a new column, not a fork. The matrix is mirrored in [`README.md`](README.md), [`agentic-docs/agent-cli-integrations.md`](agentic-docs/agent-cli-integrations.md), and [`wiki/Vendor-Matrix.md`](wiki/Vendor-Matrix.md); when one changes, all change in lock-step.

### `.agents/` - the emerging neutral location

Alongside `AGENTS.md`, a vendor-neutral **`.agents/` directory** is emerging as the shared home for runtime artifacts. This was verified against an installed Codex 0.145.0 binary rather than taken from documentation, because public docs are inconsistent on it: the binary carries `.agents/skills` as a repo-level skills root (its error string is `failed to stat repo skills root`), plus `.agents/plugins/marketplace.json` and `.agents/plugins/api_marketplace.json`, and enumerates `.agents` beside `.claude` and `.cursor` when detecting external agent configuration (`hooks.json`, `settings.json`).

The same binary **still** carries `.codex/skills` and `$CODEX_HOME/skills`. Both work today. SpecRoute records `.agents/` as the convergence point to watch; it does **not** yet recommend migrating off `.codex/skills`.

## Hard constraints

These are the rules that aren't obvious from the code and must be respected.

1. **Vendor neutrality.** Don't fold one vendor into another. Don't treat any vendor as the default. Every artifact declares which vendors it targets and uses each vendor's native shape.

2. **Sanitization.** Patterns in this repo are generalized from internal codebases. Never commit proprietary business logic, domain models, customer data, private endpoints, credentials, or internal product names. Generalize before adding. Run `/sanitize` before every commit; the PreToolUse hook (`.claude/hooks/pre-bash-sanitize.sh`) checks working, untracked, staged, and outgoing content before `git commit` / `git push`. Release maintainers also run the gitignored private-source provenance audit documented in `tools/README.md`.

3. **Spec-driven order.** PRD → spec triplet → tasks → implementation → validation → review. New examples and workflows reflect that order; don't jump straight to code.

4. **Folder-per-skill, flat-file-agent.** Skills are directories containing `SKILL.md`; agents are flat `<name>.md` files. For both, only `name` and `description` are required - `model`, `color`, `argument-hint`, `user-invocable`, `allowed-tools` are SpecRoute convention. Two traps: `model` takes a real runtime value (`opus`/`sonnet`/`haiku`/`fable`/`inherit`/full id), never the tier words `flagship`/`balanced`/`fast`, which are roster-table abstractions; and `allowed-tools` **pre-approves** tools rather than restricting them (`disallowed-tools` restricts). See [`wiki/Frontmatter-Contracts.md`](wiki/Frontmatter-Contracts.md).

5. **Two-tier docs.** Root context files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) stay short. Deep references live in `agentic-docs/`. See [`agentic-docs/two-tier-docs-pattern.md`](agentic-docs/two-tier-docs-pattern.md).

6. **TODO markers are intentional.** They mark places where a real example or value should later be added. Don't fill them with invented content; flag clearly when an example is illustrative.

7. **Templates over theory.** Templates must be production-grade and immediately usable, not abstract checklists. The `template-quality-reviewer` agent enforces this bar.

## SpecRoute implementation runtime

This repo's own `.claude/` directory is wired up as the SpecRoute implementation team. It does **not** contain consumer-facing templates (those live in `agents/`, `skills/`, `commands/`, `hooks/`).

| Path | What's there |
|---|---|
| `.claude/agents/` | 12 implementation agents - see `.claude/agents/README.md` for the roster |
| `.claude/skills/` | Contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`, `all-hands`, `doc-currency-check`) |
| `.claude/commands/` | Slash commands (`/sanitize`, `/status`, `/audit`, `/parity`) |
| `.claude/hooks/` | SessionStart status banner, PreToolUse sanitization gate, PostToolUse frontmatter check |
| `.claude/agent-memory/` | Per-agent persistent context |
| `.agents/skills/` | The same six skills in vendor-neutral shape - the repo-level skills root Codex and others read. See [`.agents/README.md`](.agents/README.md) |

When adding a new top-level artifact, prefer invoking the corresponding agent (`prd-author`, `spec-author`, etc.) - they own the contracts. The agent files are the authoritative briefs.

## Working in this repo

- Edits are almost always to markdown files. Use `Edit`/`Write` directly; nothing to compile or run.
- Before adding a new artifact, check `initial.md` (gitignored, locally) for the intended location and check sibling files for the established shape.
- If a top-level directory in the intended structure doesn't exist yet, create it as part of the work - but include the `README.md` for that directory at the same time.
- Run `/audit` before any commit. The PreToolUse hook will block publish-style git operations if forbidden strings are present.

## Getting oriented

1. Read [`README.md`](README.md) for the public framing.
2. Read [`agentic-docs/philosophy.md`](agentic-docs/philosophy.md) and [`agentic-docs/spec-driven-development.md`](agentic-docs/spec-driven-development.md) for the why.
3. Read [`agentic-docs/automation-decision-framework.md`](agentic-docs/automation-decision-framework.md) for when to reach for which artifact.
4. Walk the worked example in [`examples/sample-project/`](examples/sample-project/) - it exercises every artifact shape end-to-end.
5. Pick a vendor and copy `runtimes/.<vendor>/` into your own repo to start using SpecRoute.
