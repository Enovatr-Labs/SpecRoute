# SpecRoute Roadmap

This roadmap is intentionally honest about the current state. Updated alongside major releases.

Status legend: ✓ done · ◐ in progress · ☐ not started

**Current version:** v0.2.4 (released 2026-05-19). See [`CHANGELOG.md`](CHANGELOG.md) for the release log.

---

## Phase 1 - Skeleton & implementation team ✓ Complete

**Goal:** Establish the repository structure, the implementation agent roster, and the sanitization infrastructure that lets us build SpecRoute in public without leaking private upstream material.

- ✓ Repository skeleton (root files, `.gitignore`, `LICENSE`)
- ✓ Multi-vendor strategy documented (`README.md` vendor matrix)
- ✓ Implementation agent roster (11 agents in `.claude/agents/`)
- ✓ Contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`)
- ✓ Slash commands (`/sanitize`, `/status`, `/audit`, `/parity`)
- ✓ Hooks (SessionStart status, PreToolUse sanitization gate, PostToolUse frontmatter check)
- ✓ Agent memory for stateful agents (sanitization, runtime, docs)
- ✓ `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `CODE_OF_CONDUCT.md`
- ✓ `AGENTS.md` (canonical vendor-neutral root context)
- ✓ `GEMINI.md` (delegation shim)
- ✓ `MAINTAINERS.md`, `CITATION.cff`, `CHANGELOG.md`

## Phase 2 - Core templates & worked example ✓ Complete

**Goal:** Make the framework immediately useful - production-grade templates and one canonical worked example that exercises every artifact shape.

- ✓ PRD templates: `prd-template.md` (full 23-section), `lightweight-prd-template.md`, `platform-srs-template.md`
- ✓ Spec triplet templates: `requirements-template.md`, `design-template.md`, `tasks-template.md`
- ✓ Lightweight feature-spec template + ADR template
- ✓ Agent template + 7 archetypes (product, architect, backend, frontend, security, qa, devops)
- ✓ Skill template (`SKILL.md` with full frontmatter contract)
- ✓ Command templates (`command-template.claude.md`, `command-template.gemini.json`)
- ✓ Hook templates (Claude `hooks.template.json` covering ~27 events; Kiro `.kiro.hook` examples)
- ✓ Prompt templates: global-master, phase-master, task (production-grade with current/target diff blocks)
- ✓ Worked example `examples/sample-project/` - drop-in runnable; full PRD + spec triplet + 5 ADRs + 28 prompts + 8 implementation-team agents in `.claude/`

## Phase 3 - Runtime layouts & cross-vendor tooling ✓ Complete

**Goal:** Ship copy-pasteable per-vendor runtime layouts and the tooling that keeps them in parity.

- ✓ `runtimes/.claude/` - full layout (settings template, agents, skills, commands, hooks, agent-memory, MCP config)
- ✓ `runtimes/.codex/` - config.toml template, agents, skills, scripts
- ✓ `runtimes/.gemini/` - settings.json template, gemini_cli_config.json template
- ✓ `runtimes/.kiro/` - steering, specs, hooks
- ✓ `runtimes/.cursor/rules/` - `.mdc` templates with `alwaysApply` semantics
- ✓ `runtimes/.windsurf/rules/`
- ✓ `runtimes/mcp/servers.yaml` - single source of truth + per-vendor renderers (claude, codex, gemini)
- ✓ `tools/sync-skills.py` - cross-runtime skill diff/copy
- ✓ Workflow docs (`workflows/prd-to-production.md`, `spec-to-implementation.md`, `agent-review-loop.md`, `testing-and-validation.md`, `release-readiness.md`)
- ✓ Decision-framework doc (`agentic-docs/automation-decision-framework.md`)
- ✓ Per-vendor rule files (`rules/<vendor>-rules.md` for codex/claude/gemini/cursor/windsurf)
- ✓ Comprehensive hook coverage across all six vendors (~27 Claude / 6 Codex / 11 Gemini / 10 Kiro / ~19 Cursor / 12 Windsurf events)

## Phase 4 - Maturity ◐ In progress

**Goal:** Real-world adoption signals, additional vendors, and community-contributed examples that prove the framework's reusability.

- ◐ Versioned releases - v0.1.0 cut 2026-05-09 (private milestone); v0.2.0 / v0.2.1 cut 2026-05-11 / 2026-05-14 then retracted during pre-public sanitization (see [`CHANGELOG.md`](CHANGELOG.md)); v0.2.3 cut 2026-05-19 (first publicly available release with wiki + GitHub-side hygiene); v0.2.4 cut 2026-05-19 (version-string synchronization in `CITATION.cff`, `ROADMAP.md`, and wiki); v1.0 target after vendor-doc currency cycle and DOI registration
- ☐ Additional worked examples beyond `sample-project/` (suggested: lightweight feature, refactor, ADR-only project, Codex variant of sample-project)
- ☐ Additional vendor support based on community demand
- ☐ Persistent DOI via Zenodo (at v1.0)
- ☐ Adoption case studies (anonymous welcome) under `examples/`
- ☐ A `specroute` CLI or extension (TBD - not committed; depends on whether a tool would meaningfully exceed `tools/sync-skills.py`)

---

## Non-goals

To stay focused, SpecRoute intentionally does **not** plan to:

- Ship a runtime, package manager, or build system. SpecRoute is markdown content.
- Become an opinionated framework on top of any single vendor. The supported vendor matrix is the contract.
- Provide hosted services, paid features, or infrastructure. Apache 2.0 content, full stop.
- Embed domain-specific business logic (financial, medical, legal). Examples stay generic so the framework remains broadly applicable.

---

## Versioning

We follow Semantic Versioning. For a content-only framework, versions are interpreted as:

- **MAJOR** - breaking change to artifact contracts (frontmatter, spec triplet shape, vendor matrix structure, the spec-driven flow itself).
- **MINOR** - new vendor support, new artifact type, new skill/command/hook category, substantive new templates.
- **PATCH** - doc fixes, sanitization, link corrections, typography, content refinements.

The current version lives in [`CITATION.cff`](CITATION.cff). Tagged releases are published as GitHub releases; see [`CHANGELOG.md`](CHANGELOG.md) for the per-release log.

---

## How to influence the roadmap

- Open an issue describing a use case that's currently awkward or impossible.
- Propose a new vendor or artifact shape with a worked sketch.
- Contribute a real-world worked example for `examples/`.
- Take ownership of a `☐` item and open a PR.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the contribution workflow.
