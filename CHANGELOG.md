# Changelog

All notable changes to SpecForge are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For a content-only framework, versions are interpreted as:

- **MAJOR** - breaking change to artifact contracts (frontmatter, spec triplet shape, vendor matrix structure, the spec-driven flow itself).
- **MINOR** - new vendor support, new artifact type, new skill/command/hook category, substantive new templates.
- **PATCH** - doc fixes, sanitization, link corrections, typography, content refinements.

---

## [Unreleased]

(Changes accumulating since v0.1.0 will be listed here.)

---

## [0.1.0] - 2026-05-09

Initial public release. Phases 1-3 of the roadmap complete; Phase 4 (maturity) in progress.

### Added

#### Framework foundation

- Repository skeleton, root files (`README.md`, `LICENSE`, `.gitignore`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`).
- Canonical vendor-neutral context: `AGENTS.md`. Per-vendor delegation shims: `CLAUDE.md`, `GEMINI.md`.
- Two-tier docs pattern: short root context + deep references in `agentic-docs/` (10 conceptual docs).
- Implementation team in `.claude/`: 11 author agents, 4 contributor skills, 4 slash commands, 3 hooks, agent-memory directories.
- Sanitization infrastructure: `.claude/.forbidden-strings.txt` (gitignored, per-installation); PreToolUse hook gates `git commit` / `git push` / `gh pr create` / `gh release create`.

#### Artifact templates

- PRDs: full 23-section enterprise template, lightweight alternative, platform SRS.
- Specs: triplet (`requirements-template.md` + `design-template.md` + `tasks-template.md`) with stable IDs and back-reference contract; lightweight feature-spec template; technical-spec template; ADR template.
- Agents: `agent-template.md` with frontmatter contract; 7 archetypes (product, architect, backend, frontend, security, qa, devops); `roster.md` for cross-vendor inventory.
- Skills: `skill-template/SKILL.md` (folder-per-skill convention).
- Commands: per-vendor templates (Claude markdown + Gemini JSON).
- Hooks: comprehensive coverage across all six vendors (Claude Code ~27 events with 5 hook types; Codex 6 events; Gemini 11 events; Kiro 10 events; Cursor ~19 events; Windsurf 12 events).
- Prompts: master/phase/task production-grade trio + per-vendor sets for Claude and Codex + shared utility prompts (prd-to-spec, spec-to-tasks, code-review).

#### Runtime layouts

- Per-vendor `runtimes/.claude/`, `runtimes/.codex/`, `runtimes/.gemini/`, `runtimes/.kiro/`, `runtimes/.cursor/`, `runtimes/.windsurf/` — copy-pasteable into consumer repos.
- MCP single-source-of-truth: `runtimes/mcp/servers.yaml` + working Python renderers for Claude, Codex, Gemini.
- `tools/sync-skills.py` — cross-runtime skill / agent diff and copy.

#### Workflows and rules

- 5 workflow playbooks: `prd-to-production.md`, `spec-to-implementation.md`, `agent-review-loop.md`, `testing-and-validation.md`, `release-readiness.md`.
- Vendor-neutral rules: engineering, code-review, security, documentation.
- Per-vendor rule surfacing: codex, claude, gemini, cursor, windsurf.
- Steering templates (always-on vs file-pattern-matched).

#### Worked example

- `examples/sample-project/` - drop-in runnable, Claude-Code-only.
  - PRD (full 23-section, `prds/active/user-search.md`).
  - Spec triplet (`specs/user-search/{requirements,design,tasks}.md`) with 11 stable-ID requirements + 11 NFRs + full coverage table.
  - 5 ADRs (`adrs/`): Postgres indexed scans, cursor pagination, Redis cache TTL, HMAC-signed cursors, filter-set hash logging.
  - 7 project-specific deep references (`agentic-docs/`).
  - 28 prompt files: 1 global master + 4 phase masters + 22 numbered task prompts + 2 runtime operational prompts.
  - 8 implementation-team agents in `.claude/agents/`.
  - 4 slash commands, 3 hooks, agent-memory directory.
  - Self-contained: copy folder, rename `.template` files, open Claude Code, run `prompts/runtime/pickup-next-task.md`.

#### Documentation and attribution

- 10-file `agentic-docs/` framework reference (philosophy, spec-driven-development, agentic-coding-model, automation-decision-framework, documentation-structure, two-tier-docs-pattern, multi-vendor-context-files, agent-cli-integrations, cross-vendor-sync, agent-memory).
- `MAINTAINERS.md` with current-maintainer table, how-to-reach-us decision matrix, sponsoring-org context, becoming-a-maintainer process, decision-making conventions.
- README sections for Maintainers and Citation.
- `CITATION.cff` (CFF v1.2.0) - GitHub renders a "Cite this repository" button.

### Conventions established

- Vendor-neutrality matrix as the contract: adding a new vendor is a new column, not a fork.
- Sanitization-by-design: gitignored wordlist + runtime hook gate + `/sanitize` command + `sanitization-auditor` agent.
- Two-tier docs pattern: `AGENTS.md` (~100 lines max) + per-vendor delegation shims (~30-50 lines) + `agentic-docs/` deep references.
- Frontmatter contracts as load-bearing: agents, skills, commands all have required-field contracts; the PostToolUse hook validates on save.
- Spec-driven flow: PRD → spec triplet (with stable IDs) → numbered tasks (with back-refs) → phased prompts (with current/target diff blocks) → implementation → validation → review.

[Unreleased]: https://github.com/Enovatr-Labs/SpecForge/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Enovatr-Labs/SpecForge/releases/tag/v0.1.0
