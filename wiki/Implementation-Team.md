# Implementation Team

<!-- sources: CLAUDE.md, .claude/agents/README.md -->

This repo's own `.claude/` directory is **the SpecRoute implementation team** — the agents, skills, commands, and hooks that build SpecRoute itself. It is **not** the consumer template (those live in `runtimes/.claude/`).

For per-agent definitions, see [`.claude/agents/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agents/README.md).

## What lives in `.claude/`

| Path | What's there |
|---|---|
| `.claude/agents/` | 11 implementation agents |
| `.claude/skills/` | 4 contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`) |
| `.claude/commands/` | 4 slash commands (`/audit`, `/parity`, `/sanitize`, `/status`) |
| `.claude/hooks/` | SessionStart status banner, PreToolUse sanitization gate, PostToolUse frontmatter check |
| `.claude/agent-memory/` | Per-agent persistent context |
| `.claude/settings.json` | Tracked, project-wide settings |
| `.claude/settings.local.json` | **Gitignored** — per-user permissions, MCP enables |
| `.claude/.forbidden-strings.txt` | **Gitignored** — per-installation sanitization wordlist |

## The 11 implementation agents

| Agent | Owns | Model |
|---|---|---|
| `prd-author` | PRDs (full + lightweight + SRS templates and examples) | opus |
| `spec-author` | Spec triplet, lightweight feature spec, technical spec, ADRs | opus |
| `agent-roster-architect` | Agent roster template, archetypes, examples | opus |
| `skill-author` | Skill template, folder-per-skill convention | opus |
| `command-author` | Per-vendor command templates and examples | sonnet |
| `hooks-author` | Per-vendor hook templates, scripts, event matrix | sonnet |
| `prompt-engineer` | Global / phase / task prompt templates and per-vendor sets | opus |
| `framework-docs-author` | `agentic-docs/`, workflows, rules | opus |
| `runtime-architect` | `runtimes/.<vendor>/`, MCP single source, sync tools | opus |
| `sanitization-auditor` | `/sanitize`, `/audit`'s sanitization layer, wordlist guidance | sonnet |
| `template-quality-reviewer` | Production-grade-and-immediately-usable bar | opus |

Each agent has a `.md` definition with:
- Frontmatter (`name`, `description` with trigger phrases, `model`, `color`).
- Operating principles.
- Owns (what files the agent governs).
- Don't use for (boundaries; hands off to neighboring agents).
- Optional `memory: project` to read/write `.claude/agent-memory/<name>/`.

See [[Agents]] for the frontmatter contract and [[Frontmatter Contracts]] for the full reference.

## The 4 contributor skills

Interactive workflows for SpecRoute contributors:

- **`scaffold-artifact`** — bootstrap a new artifact (PRD / spec / agent / skill / command / hook / prompt / runtime) with the right frontmatter and target path.
- **`add-vendor`** — interactive walkthrough for adding a new agent CLI to the matrix.
- **`example-walkthrough`** — guided end-to-end build of `examples/sample-project/`.
- **`frontmatter-lint`** — interactive frontmatter validation across agents / skills / commands with offered fixes.

See [[Skills]] for the folder-per-skill convention.

## The 4 slash commands

Deterministic pre-commit checks:

- **`/audit`** — comprehensive sweep (sanitization + frontmatter + vendor-matrix consistency + broken links + TODO health).
- **`/parity`** — cross-vendor runtime parity check (`runtimes/.claude/` vs `runtimes/.codex/` skill / agent drift; MCP source-of-truth alignment).
- **`/sanitize`** — quick string-level wordlist scan.
- **`/status`** — SpecRoute skeleton state report (which top-level dirs exist, which artifacts have been drafted, what's outstanding).

See [[Commands]] and [[Sanitization]].

## The 3 hooks

Always-on automation:

- **`session-start-status.sh`** (SessionStart) — prints the SpecRoute skeleton status banner so Claude orients without re-grepping.
- **`pre-bash-sanitize.sh`** (PreToolUse) — blocks `git commit` / `git push` / `gh pr create` / `gh release create` if `git grep` finds forbidden terms.
- **`post-edit-frontmatter.sh`** (PostToolUse on Write/Edit) — validates frontmatter on agent / skill / command file writes; warns on stderr.

See [[Hooks]] and [[Sanitization]].

## Why `.claude/` and `runtimes/.claude/` exist separately

| Path | Who reads it | Contents |
|---|---|---|
| `.claude/` | This repo's contributors (Claude Code) | The implementation team that *builds* SpecRoute |
| `runtimes/.claude/` | Consumers who drop it into their own repo | The template that *uses* SpecRoute |

Don't confuse them. The consumer drops `runtimes/.claude/` into their repo; they do **not** copy `.claude/`. The implementation-team agents draft PRDs, specs, and agent definitions for the *consumer* template — they aren't themselves the template.

## Per-agent persistent context

Agents with `memory: project` in their frontmatter read/write `.claude/agent-memory/<agent-name>/<topic>.md`. Reference implementations:

- [`sanitization-auditor/checklist.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agent-memory/sanitization-auditor/checklist.md) — canonical wordlist pointer + audit protocol.
- [`runtime-architect/vendor-matrix-progress.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agent-memory/runtime-architect/vendor-matrix-progress.md) — vendor-by-vendor build-out state.
- [`framework-docs-author/docs-status.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agent-memory/framework-docs-author/docs-status.md) — drafting progress for `agentic-docs/`.

See [[Agent Memory]].

## Per-user vs tracked settings

- `.claude/settings.json` — tracked, project-wide.
- `.claude/settings.local.json` — **gitignored**, per-user overrides (permissions, MCP enables).
- `.claude/.forbidden-strings.txt` — **gitignored**, per-installation sanitization wordlist.

See [[Sanitization]] for how the wordlist is populated and refreshed.

## See also

- [[Agents]] · [[Skills]] · [[Commands]] · [[Hooks]] — the four primitives
- [[Automation Decision Framework]] — when to reach for which
- [[Agent Memory]] — per-agent persistent context
- [[Sanitization]] — the three-layer sanitization mechanism
- [[Frontmatter Contracts]] — required-field reference
