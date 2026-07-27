# SpecRoute Roadmap

This roadmap is intentionally honest about the current state. Updated alongside major releases.

Status legend: ✓ done · ◐ in progress · ☐ not started

**Current version:** v0.4.0 (released 2026-07-27). See [`CHANGELOG.md`](CHANGELOG.md) for the release log.

---

## Phase 1 - Skeleton & implementation team ✓ Complete

**Goal:** Establish the repository structure, the implementation agent roster, and the sanitization infrastructure that lets us build SpecRoute in public without leaking private upstream material.

- ✓ Repository skeleton (root files, `.gitignore`, `LICENSE`)
- ✓ Multi-vendor strategy documented (`README.md` vendor matrix)
- ✓ Implementation agent roster (12 agents in `.claude/agents/`)
- ✓ Contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`, `all-hands`, `doc-currency-check`)
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
- ✓ Command templates (`command-template.claude.md`, `command-template.gemini.toml`)
- ✓ Hook templates (Claude `hooks.template.json`; Kiro `.kiro/hooks/<name>.json` v1 examples)
- ✓ Prompt templates: global-master, phase-master, task (production-grade with current/target diff blocks)
- ✓ Worked example `examples/sample-project/` - drop-in runnable; full PRD + spec triplet + 5 ADRs + 29 prompts + 9 implementation-team agents in `.claude/`

## Phase 3 - Runtime layouts & cross-vendor tooling ✓ Complete

**Goal:** Ship copy-pasteable per-vendor runtime layouts and the tooling that keeps them in parity.

- ✓ `runtimes/.claude/` - full layout (settings template, agents, skills, commands, hooks, agent-memory, `.mcp.json` config)
- ✓ `runtimes/.codex/` - config.toml template, TOML agents, skills, hooks, scripts
- ✓ `runtimes/.gemini/` - settings.json template (MCP), skills, agents, `commands/*.toml`, `hooks/` (merge-in snippet - settings.json is generated)
- ✓ `runtimes/.kiro/` - steering, specs, hooks, skills, agents, `settings/mcp.json`
- ✓ `runtimes/.cursor/` - `.mdc` rules, agents, skills, commands, `hooks/`, `mcp.template.json`
- ✓ `runtimes/.devin/` - Devin Local agents, skills, hooks, and `config.template.json`, plus Cascade-facing rule examples
- ✓ `runtimes/mcp/servers.yaml` - single source of truth + six per-vendor renderers (claude, codex, gemini, kiro, cursor, devin)
- ✓ `tools/sync-skills.py` - body-aware cross-runtime skill sync (all six runtime layouts; agents excluded - formats diverge)
- ✓ Workflow docs (`workflows/prd-to-production.md`, `spec-to-implementation.md`, `agent-review-loop.md`, `testing-and-validation.md`, `release-readiness.md`)
- ✓ Decision-framework doc (`agentic-docs/automation-decision-framework.md`)
- ✓ Per-vendor rule files (`rules/<vendor>-rules.md` for codex/claude/gemini/cursor/kiro/devin)
- ✓ Hook templates per vendor (30 Claude / 11 Codex / 11 Gemini / 10 Kiro / 21 Cursor / 8 Devin Local events), mirrored into all six runtime layouts. Note the taxonomies are **not** interchangeable even where Claude, Codex, Kiro, and Devin Local share event names

## Phase 4 - Maturity ◐ In progress

**Goal:** Real-world adoption signals, additional vendors, and community-contributed examples that prove the framework's reusability.

- ◐ Versioned releases - v0.1.0 cut 2026-05-09 (private milestone); v0.2.0 / v0.2.1 cut 2026-05-11 / 2026-05-14 then retracted during pre-public sanitization (see [`CHANGELOG.md`](CHANGELOG.md)); v0.2.3 cut 2026-05-19 (first publicly available release with wiki + GitHub-side hygiene); v0.2.4 cut 2026-05-19 (version-string synchronization in `CITATION.cff`, `ROADMAP.md`, and wiki); v0.3.0 cut 2026-06-29 (vendor capability convergence + vendor-doc currency cycle); v0.4.0 cut 2026-07-27 (multi-agent orchestration + second currency cycle and contract correction); v1.0 target after DOI registration and real-world adoption signals
- ✓ Vendor-doc currency cycle - all six vendors re-verified against their mid-2026 releases; runtime layouts built out to the converged capability set; matrix, tooling, and wiki reconciled (v0.3.0)
- ✓ Multi-agent orchestration - the `all-hands` pattern (coordinator skill + roster-as-registry + department routing), shipped in all six runtime layouts, with `agentic-docs/multi-agent-orchestration.md` (v0.4.0)
- ✓ Second currency cycle + contract correction - hook wiring fixed (hooks execute from `settings.json`, not a project `hooks/hooks.json`), Kiro migrated off the retired `*.kiro.hook` format, agent/skill frontmatter contracts corrected against vendor docs, `docs-currency-auditor` agent and `doc-currency-check` skill added to make the next cycle repeatable (v0.4.0)
- ✓ Vendor-neutral runtime root - `.agents/skills/` added so Codex and other non-Claude CLIs find this repository's own skills; previously only `.claude/` was wired up (v0.4.0)
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
