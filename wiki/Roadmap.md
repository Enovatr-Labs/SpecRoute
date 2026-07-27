# Roadmap

<!-- sources: ROADMAP.md, CHANGELOG.md -->

Where SpecRoute is, what's next, and what's deliberately out of scope.

Canonical source: [ROADMAP.md](https://github.com/Enovatr-Labs/SpecRoute/blob/main/ROADMAP.md). Release log: [CHANGELOG.md](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CHANGELOG.md).

**Current version**: v0.4.0 (released 2026-07-27).

Status legend: ✓ done · ◐ in progress · ☐ not started

## Phase 1 — Skeleton & implementation team ✓ Complete

Establish the repository structure, the implementation agent roster, and the sanitization infrastructure.

- ✓ Repository skeleton + root files + `LICENSE`
- ✓ Multi-vendor strategy documented (`README.md` vendor matrix)
- ✓ [[Implementation Team]] — 12 agents in `.claude/agents/`
- ✓ Contributor skills (`scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`, `all-hands`, `doc-currency-check`)
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
- ✓ Command templates (Claude markdown + Gemini TOML)
- ✓ Hook templates covering all six vendors
- ✓ Prompt templates: global-master, phase-master, task (production-grade)
- ✓ [[Worked Example]] — `examples/sample-project/` drop-in runnable with full PRD + spec triplet + 5 ADRs + 29 prompts + 9 implementation agents

## Phase 3 — Runtime layouts & cross-vendor tooling ✓ Complete

Ship copy-pasteable per-vendor runtime layouts and the tooling that keeps them in parity.

- ✓ `runtimes/.claude/` — full layout (settings, agents, skills, commands, hooks, agent-memory, MCP)
- ✓ `runtimes/.codex/` — config.toml template, TOML agents, skills, hooks, scripts
- ✓ `runtimes/.gemini/` — settings.json, skills, agents, commands, hooks
- ✓ `runtimes/.kiro/` — steering, specs, hooks, skills, agents, MCP
- ✓ `runtimes/.cursor/` — rules, agents, skills, commands, hooks, MCP
- ✓ `runtimes/.devin/` — Devin Desktop / Devin Local layout with `AGENTS.md` context, rules, skills, experimental agents, hooks, and MCP
- ✓ `runtimes/mcp/servers.yaml` + six renderers (claude, codex, gemini, kiro, cursor, devin)
- ✓ `tools/sync-skills.py` — body-aware sync across all six runtime layouts
- ✓ Workflow docs (5 playbooks: PRD-to-prod, spec-to-impl, agent-review, testing, release-readiness)
- ✓ Decision-framework doc
- ✓ Per-vendor rule files (codex, claude, gemini, kiro, cursor, devin)
- ✓ Hook templates across all supported runtime layouts; Kiro v1 uses 10 triggers and manual steering

## Phase 4 — Maturity ◐ In progress

Real-world adoption signals, additional vendors, and community-contributed examples.

- ◐ Versioned releases — v0.1.0 cut 2026-05-09 (private milestone); v0.2.0 / v0.2.1 cut 2026-05-11 / 2026-05-14 then retracted during pre-public sanitization (see [CHANGELOG](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CHANGELOG.md)); v0.2.3 cut 2026-05-19 (first publicly available release with wiki + GitHub-side hygiene); v0.2.4 cut 2026-05-19 (version-string synchronization in `CITATION.cff`, `ROADMAP.md`, and wiki); v0.3.0 cut 2026-06-29 (vendor capability convergence + vendor-doc currency cycle); v0.4.0 cut 2026-07-27 (multi-agent orchestration + second currency cycle and contract correction); v1.0 target after DOI registration and real-world adoption signals
- ✓ Vendor-doc currency cycle — all six vendors re-verified against their mid-2026 releases; runtime layouts built out to the converged capability set; matrix, tooling, and wiki reconciled (v0.3.0)
- ✓ Multi-agent orchestration — the `all-hands` pattern (coordinator skill + roster-as-registry + department routing), shipped in all six runtime layouts, with [[Multi-Agent Orchestration]] (v0.4.0)
- ✓ Second currency cycle + contract correction — hook wiring fixed (hooks execute from `settings.json`, not a project `hooks/hooks.json`), Kiro migrated off the retired `*.kiro.hook` format, agent/skill frontmatter contracts corrected against vendor docs, `docs-currency-auditor` agent and `doc-currency-check` skill added to make the next cycle repeatable (v0.4.0)
- ✓ Vendor-neutral runtime root — `.agents/skills/` added so Codex and other non-Claude CLIs find this repository's own skills; previously only `.claude/` was wired up (v0.4.0)
- ✓ Public-doc information architecture — vendor implementation notes and source evidence moved out of the root README into the integration reference and [[Vendor Matrix]], while `/audit` continues to enforce byte-identical matrix tables (v0.4.0)
- ◐ Guarded release automation — manual GitHub Actions `publish`, `resume`, and `realign-develop` operations plus deterministic preflight, fail-closed release-manager authorization, and SHA-bound local provenance attestation are implemented; the protected release environment, immutable-release setting, and narrowly scoped Release App installation remain prerequisites before the first dispatch, with its develop-ruleset bypass required only for optional automated realignment (see [[Maintainers]])
- ☐ Additional worked examples beyond `sample-project/`:
  - Lightweight feature (single-team, `lightweight-prd-template.md` + `feature-spec-template.md`)
  - Refactor (`technical-spec-template.md`)
  - ADR-only project
  - Codex variant of `sample-project/`
- ☐ Additional vendor support based on community demand
- ☐ Persistent DOI via Zenodo (at v1.0)
- ☐ Adoption case studies (anonymous welcome) under `examples/`
- ☐ A `specroute` CLI or extension (**TBD** — not committed; depends on whether a tool would meaningfully exceed `tools/sync-skills.py`)

## Non-goals

To stay focused, SpecRoute intentionally does **not** plan to:

- Ship a runtime, package manager, or build system. SpecRoute is markdown content.
- Become an opinionated framework on top of any single vendor. The [[Vendor Matrix]] is the contract.
- Provide hosted services, paid features, or infrastructure. Apache 2.0 content, full stop.
- Embed domain-specific business logic (financial, medical, legal). Examples stay generic.

## Versioning

Semantic Versioning. For a content-only framework:

- **MAJOR** — breaking change to artifact contracts (frontmatter, spec triplet shape, vendor matrix structure, the spec-driven flow itself).
- **MINOR** — new vendor support, new artifact type, new skill/command/hook category, substantive new templates.
- **PATCH** — doc fixes, sanitization, link corrections, typography, content refinements.

Current version lives in [`CITATION.cff`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CITATION.cff). Tagged releases are published as [GitHub releases](https://github.com/Enovatr-Labs/SpecRoute/releases).

## How to influence the roadmap

- Open an [issue](https://github.com/Enovatr-Labs/SpecRoute/issues) describing a use case that's currently awkward or impossible.
- Propose a new vendor or artifact shape with a worked sketch.
- Contribute a real-world worked example for `examples/`.
- Take ownership of a `☐` item and open a PR.

See [[Contributing]] for the workflow.

## See also

- [[Home]] — project overview
- [[Maintainers]] — who's driving this and how decisions get made
- [CHANGELOG](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CHANGELOG.md) — release log
