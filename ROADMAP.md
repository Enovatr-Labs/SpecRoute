# SpecForge Roadmap

This roadmap is intentionally honest about the current state. SpecForge is a young project - the skeleton is being built in public.

Status legend: ✓ done · ◐ in progress · ☐ not started

---

## Phase 1 - Skeleton & implementation team

**Goal:** Establish the repository structure, the implementation agent roster, and the sanitization infrastructure that lets us build SpecForge in public without leaking private upstream material.

- ✓ Repository skeleton (root files, `.gitignore`, `LICENSE`)
- ✓ Multi-vendor strategy documented (`README.md` vendor matrix)
- ✓ Implementation agent roster (11 agents in `.claude/agents/`)
- ✓ Contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`)
- ✓ Slash commands (`/sanitize`, `/status`, `/audit`, `/parity`)
- ✓ Hooks (SessionStart status, PreToolUse sanitization gate, PostToolUse frontmatter check)
- ✓ Agent memory for stateful agents (sanitization, runtime, docs)
- ✓ `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`
- ☐ `CODE_OF_CONDUCT.md`
- ☐ `AGENTS.md` (canonical vendor-neutral root context)
- ☐ `GEMINI.md` (delegation shim)

## Phase 2 - Core templates & worked example

**Goal:** Make the framework immediately useful - production-grade templates and one canonical worked example that exercises every artifact shape.

- ☐ PRD templates: `prd-template.md` (full 23-section), `lightweight-prd-template.md`, `platform-srs-template.md`
- ☐ Spec triplet templates: `requirements-template.md`, `design-template.md`, `tasks-template.md`
- ☐ Lightweight spec + ADR templates
- ☐ Agent template + archetypes (product, architect, backend, frontend, security, qa, devops)
- ☐ Skill template (`SKILL.md` with full frontmatter contract)
- ☐ Command templates (`command-template.claude.md`, `command-template.gemini.json`)
- ☐ Hook templates (`hooks.template.json`, sample `.kiro.hook` files)
- ☐ Prompt templates: global-master, phase-master, task (production-grade)
- ☐ Worked example end-to-end in `examples/sample-project/` - generic feature (e.g. notification preferences), all artifact shapes present, cross-referenced

## Phase 3 - Runtime layouts & cross-vendor tooling

**Goal:** Ship copy-pasteable per-vendor runtime layouts and the tooling that keeps them in parity.

- ☐ `runtimes/.claude/` - full layout (settings template, agents, skills, commands, hooks, agent-memory, MCP config)
- ☐ `runtimes/.codex/` - config.toml template, agents, skills, scripts
- ☐ `runtimes/.gemini/` - settings.json template, gemini_cli_config.json template
- ☐ `runtimes/.kiro/` - steering, specs, hooks
- ☐ `runtimes/.cursor/rules/` - `.mdc` templates with `alwaysApply` semantics
- ☐ `runtimes/.windsurf/rules/`
- ☐ `runtimes/mcp/servers.yaml` - single source of truth + per-vendor renderers
- ☐ `tools/sync-skills.py` - cross-runtime skill diff/copy
- ☐ Workflow docs (`workflows/prd-to-production.md`, etc.)
- ☐ Decision-framework docs (`agentic-docs/automation-decision-framework.md` - highest leverage)
- ☐ Per-vendor rule files (`rules/<vendor>-rules.md`)

## Phase 4 - Maturity

**Goal:** Real-world adoption signals, additional vendors, and community-contributed examples that prove the framework's reusability.

- ☐ Additional worked examples beyond `sample-project/`
- ☐ Additional vendor support based on community demand
- ☐ Versioned releases (`v0.1.0`, etc.) with release notes
- ☐ Adoption case studies (anonymous welcome) under `examples/`
- ☐ A `specforge` CLI or extension (TBD - not committed; depends on whether a tool would meaningfully exceed `tools/sync-skills.py`)

---

## Non-goals

To stay focused, SpecForge intentionally does **not** plan to:

- Ship a runtime, package manager, or build system. SpecForge is markdown content.
- Become an opinionated framework on top of any single vendor. The supported vendor matrix is the contract.
- Provide hosted services, paid features, or infrastructure. Apache 2.0 content, full stop.
- Embed domain-specific business logic (financial, medical, legal). Examples stay generic so the framework remains broadly applicable.

---

## How to influence the roadmap

- Open an issue describing a use case that's currently awkward or impossible.
- Propose a new vendor or artifact shape with a worked sketch.
- Contribute a real-world worked example for `examples/`.
- Take ownership of a `☐` item and open a PR.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the contribution workflow.
