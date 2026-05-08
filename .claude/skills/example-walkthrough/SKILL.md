---
name: example-walkthrough
description: Guided end-to-end build of the canonical worked example under examples/sample-feature/. Walks through each artifact in spec-driven order (PRD → requirements → design → tasks → agent roster → phased prompts → implementation plan), invoking the right specialist agent for each. Use when bootstrapping the worked example or when reviewing whether the existing example is complete.
argument-hint: "[feature-name?]"
user-invocable: true
allowed-tools: Read Write Edit Glob
---

# Example Walkthrough

Builds (or audits) the worked example in `examples/sample-feature/` artifact-by-artifact, using the spec-driven flow as the script.

## When to use

- The worked example is missing or incomplete
- A reviewer wants to confirm the example exercises every artifact shape
- Demonstrating SpecForge to a new contributor

## Step 1: Pick a feature

Ask the user (or use the argument) for a generic feature name. Suggestions:

- `notification-preferences`
- `file-upload-service`
- `user-search`
- `audit-log-export`

Domain-neutral only. No financial, healthcare, or proprietary domains.

## Step 2: Walk the spec-driven flow

For each step, verify the artifact exists and is complete; if not, invoke the named agent to draft it.

| Step | Artifact | Path | Agent |
|---|---|---|---|
| 1 | PRD (full 23-section) | `examples/sample-feature/prd.md` | `prd-author` |
| 2 | Requirements | `examples/sample-feature/requirements.md` | `spec-author` |
| 3 | Design | `examples/sample-feature/design.md` | `spec-author` |
| 4 | Tasks | `examples/sample-feature/tasks.md` | `spec-author` |
| 5 | Agent roster | `examples/sample-feature/agent-roster.md` | `agent-roster-architect` |
| 6 | Global master prompt | `examples/sample-feature/prompts/000_master.md` | `prompt-engineer` |
| 7 | Numbered task prompts | `examples/sample-feature/prompts/001_*.md`, `002_*.md`, … | `prompt-engineer` |
| 8 | Implementation plan | `examples/sample-feature/implementation-plan.md` | `framework-docs-author` |

## Step 3: Cross-artifact validation

After each step, check:

- The new artifact references the previous artifact (PRD ← requirements ← design ← tasks ← prompts).
- Requirement IDs in `requirements.md` are referenced by `tasks.md`.
- Tasks in `tasks.md` are referenced by the numbered prompts.
- Agents named in `agent-roster.md` are the same agents referenced in the prompts.
- No private-project leaks (run `/sanitize` after each step).

## Step 4: Final review

Once all 8 artifacts exist:

- Run `/audit` for a comprehensive sweep
- Invoke `template-quality-reviewer` on each artifact to confirm "production-grade and immediately usable"
- Confirm cross-references render (no broken markdown links)

## Step 5: Mirror into runtime examples

If consumers should see the vendor-specific shape of the example, ask `runtime-architect` to mirror appropriate parts into `runtimes/.claude/`, `runtimes/.codex/`, etc.

## Don't use for

- Building real features (this skill produces an example for SpecForge contributors, not a real implementation).
- Single-artifact updates (use the corresponding agent directly).
