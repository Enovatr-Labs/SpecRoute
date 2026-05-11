# Roadmap

<!-- sources: ROADMAP.md, CHANGELOG.md -->

Where SpecForge is, what's next, and what's deliberately out of scope.

Canonical source: [ROADMAP.md](https://github.com/Enovatr-Labs/SpecForge/blob/main/ROADMAP.md). Release log: [CHANGELOG.md](https://github.com/Enovatr-Labs/SpecForge/blob/main/CHANGELOG.md).

**Current version**: v0.1.0 (released 2026-05-09).

Status legend: ✓ done · ◐ in progress · ☐ not started

## Phase 1 — Skeleton & implementation team ✓ Complete

Establish the repository structure, the implementation agent roster, and the sanitization infrastructure.

- ✓ Repository skeleton + root files + `LICENSE`
- ✓ Multi-vendor strategy documented (`README.md` vendor matrix)
- ✓ [[Implementation Team]] — 11 agents in `.claude/agents/`
- ✓ Contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`)
- ✓ Slash commands (`/sanitize`, `/status`, `/audit`, `/parity`)
- ✓ Hooks (SessionStart status, PreToolUse sanitization gate, PostToolUse frontmatter check)
- ✓ Agent memory for stateful agents
- ✓ `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `CODE_OF_CONDUCT.md`
- ✓ `AGENTS.md` (canonical) + `GEMINI.md` (delegation shim)
- ✓ `MAINTAINERS.md`, `CITATION.cff`, `CHANGELOG.md`

## Phase 2 — Core templates & worked example ✓ Complete

Make the framework immediately useful — production-grade templates and one canonical worked example.

- ✓ PRD templates: full 23-section, lightweight, platform SRS
- ✓ Spec triplet templates: requirements, design, tasks
- ✓ Lightweight feature-spec + technical spec + ADR templates
- ✓ Agent template + 7 archetypes
- ✓ Skill template (`SKILL.md` with full frontmatter contract)
- ✓ Command templates (Claude markdown + Gemini JSON)
- ✓ Hook templates covering all six vendors
- ✓ Prompt templates: global-master, phase-master, task (production-grade)
- ✓ [[Worked Example]] — `examples/sample-project/` drop-in runnable with full PRD + spec triplet + 5 ADRs + 28 prompts + 8 implementation agents

## Phase 3 — Runtime layouts & cross-vendor tooling ✓ Complete

Ship copy-pasteable per-vendor runtime layouts and the tooling that keeps them in parity.

- ✓ `runtimes/.claude/` — full layout (settings, agents, skills, commands, hooks, agent-memory, MCP)
- ✓ `runtimes/.codex/` — config.toml template, agents, skills, scripts
- ✓ `runtimes/.gemini/` — settings.json + gemini_cli_config.json templates
- ✓ `runtimes/.kiro/` — steering, specs, hooks
- ✓ `runtimes/.cursor/rules/` — `.mdc` templates
- ✓ `runtimes/.windsurf/rules/`
- ✓ `runtimes/mcp/servers.yaml` + per-vendor renderers (claude, codex, gemini)
- ✓ `tools/sync-skills.py` — cross-runtime skill diff/copy
- ✓ Workflow docs (5 playbooks: PRD-to-prod, spec-to-impl, agent-review, testing, release-readiness)
- ✓ Decision-framework doc
- ✓ Per-vendor rule files (codex, claude, gemini, cursor, windsurf)
- ✓ Comprehensive hook coverage across all six vendors

## Phase 4 — Maturity ◐ In progress

Real-world adoption signals, additional vendors, and community-contributed examples.

- ◐ Versioned releases — v0.1.0 cut 2026-05-09; v1.0 target after vendor-doc currency cycle and DOI registration
- ☐ Additional worked examples beyond `sample-project/`:
  - Lightweight feature (single-team, `lightweight-prd-template.md` + `feature-spec-template.md`)
  - Refactor (`technical-spec-template.md`)
  - ADR-only project
  - Codex variant of `sample-project/`
- ☐ Additional vendor support based on community demand
- ☐ Persistent DOI via Zenodo (at v1.0)
- ☐ Adoption case studies (anonymous welcome) under `examples/`
- ☐ A `specforge` CLI or extension (**TBD** — not committed; depends on whether a tool would meaningfully exceed `tools/sync-skills.py`)

## Non-goals

To stay focused, SpecForge intentionally does **not** plan to:

- Ship a runtime, package manager, or build system. SpecForge is markdown content.
- Become an opinionated framework on top of any single vendor. The [[Vendor Matrix]] is the contract.
- Provide hosted services, paid features, or infrastructure. Apache 2.0 content, full stop.
- Embed domain-specific business logic (financial, medical, legal). Examples stay generic.

## Versioning

Semantic Versioning. For a content-only framework:

- **MAJOR** — breaking change to artifact contracts (frontmatter, spec triplet shape, vendor matrix structure, the spec-driven flow itself).
- **MINOR** — new vendor support, new artifact type, new skill/command/hook category, substantive new templates.
- **PATCH** — doc fixes, sanitization, link corrections, typography, content refinements.

Current version lives in [`CITATION.cff`](https://github.com/Enovatr-Labs/SpecForge/blob/main/CITATION.cff). Tagged releases are published as [GitHub releases](https://github.com/Enovatr-Labs/SpecForge/releases).

## How to influence the roadmap

- Open an [issue](https://github.com/Enovatr-Labs/SpecForge/issues) describing a use case that's currently awkward or impossible.
- Propose a new vendor or artifact shape with a worked sketch.
- Contribute a real-world worked example for `examples/`.
- Take ownership of a `☐` item and open a PR.

See [[Contributing]] for the workflow.

## See also

- [[Home]] — project overview
- [[Maintainers]] — who's driving this and how decisions get made
- [CHANGELOG](https://github.com/Enovatr-Labs/SpecForge/blob/main/CHANGELOG.md) — release log
