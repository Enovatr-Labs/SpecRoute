# SpecRoute Wiki

**An open-source framework for spec-driven agentic software engineering — vendor-neutral across Claude Code, Codex, Gemini CLI, Kiro, Cursor, and Windsurf.**

SpecRoute captures production-grade patterns for PRDs, specifications, prompts, agents, skills, slash commands, hooks, workflows, and engineering rules. It is **content, not an application**: drop the templates and runtime layouts into your own repo and adapt them to your stack.

---

## Start here

| If you want to … | Read |
|---|---|
| Get a working setup in 15 minutes | [[Quickstart]] |
| Understand the project layout | [[Repository Structure]] |
| Know *why* the framework exists | [[Philosophy]] |
| See the framework end-to-end on a real feature | [[Worked Example]] |

## The core idea

```
PRD → Spec (requirements + design + tasks) → Implementation → Validation → Review
```

Each stage produces a reviewable artifact. Each stage has a template, an agent assignment, and an acceptance criterion. Cross-references that survive across stages — stable requirement IDs, design `Satisfies:` annotations, task back-refs, test back-refs — are what make agent-generated work reviewable.

Read [[Spec-Driven Development]] for the full flow, [[Agentic Coding Model]] for the four-primitive composition (skills, agents, commands, hooks), and [[Automation Decision Framework]] for the decision matrix.

## Browse by topic

### Concepts
- [[Philosophy]] — what we believe and why
- [[Spec-Driven Development]] — PRD → spec → tasks → impl → validation
- [[Agentic Coding Model]] — how four primitives compose
- [[Automation Decision Framework]] — skill vs agent vs command vs hook
- [[Two-Tier Docs Pattern]] — short root context + deep references
- [[Multi-Vendor Context Files]] — canonical `AGENTS.md` + delegation shims
- [[Documentation Structure]] — where new docs go
- [[Agent Memory]] — per-agent persistent state

### Artifacts
- [[Artifact Taxonomy]] — the nine artifact types at a glance
- [[PRDs]] · [[Specs]] · [[Agents]] · [[Skills]] · [[Commands]] · [[Hooks]] · [[Prompts]] · [[Rules]]
- [[Frontmatter Contracts]] — the load-bearing required fields
- [[Sanitization]] — what stays out of tracked content

### Workflows
- [[Workflows]] — index of the five operational playbooks
- [[Workflow PRD to Production]] · [[Workflow Spec to Implementation]] · [[Workflow Agent Review Loop]] · [[Workflow Testing and Validation]] · [[Workflow Release Readiness]]

### Vendors & integration
- [[Vendor Matrix]] — the supported-CLI contract
- [[Agent CLI Integrations]] — per-vendor wiring
- [[Cross-Vendor Sync]] — keeping Claude / Codex / MCP in lock-step
- [[MCP Integration]] — single source of truth + per-vendor renderers
- [[Adding a Vendor]] — adding a new column to the matrix

### Reference & governance
- [[Worked Example]] — drop-in runnable `user-search` feature
- [[Implementation Team]] — the `.claude/` runtime that builds SpecRoute itself
- [[Contributing]] · [[Security]] · [[Maintainers]] · [[Code of Conduct]]
- [[Roadmap]] · [[FAQ]] · [[Glossary]]

## Project status

- **Current version**: v0.2.0 (released 2026-05-11).
- **Phases 1–3 complete** (skeleton, core templates, runtime layouts).
- **Phase 4 in progress** (real-world adoption, more vendors, DOI registration).

See [[Roadmap]] for the full picture and the project's [CHANGELOG](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CHANGELOG.md) for the release log.

## License & citation

[Apache 2.0](https://github.com/Enovatr-Labs/SpecRoute/blob/main/LICENSE) — Copyright (c) Enovatr Labs. Maintainer: [Chika Ihejimba](https://github.com/cihejimba). For academic citation, see [`CITATION.cff`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CITATION.cff).
