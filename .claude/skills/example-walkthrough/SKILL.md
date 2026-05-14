---
name: example-walkthrough
description: Guided end-to-end build of the canonical worked example under examples/sample-project/. Walks through each artifact in spec-driven order (PRD → requirements → design → tasks → agent roster → phased prompts → implementation plan), invoking the right specialist agent for each. Use when bootstrapping the worked example or when reviewing whether the existing example is complete.
argument-hint: "[feature-name?]"
user-invocable: true
allowed-tools: Read Write Edit Glob
---

# Example Walkthrough

Builds (or audits) the worked example in `examples/sample-project/` artifact-by-artifact, using the spec-driven flow as the script.

## When to use

- The worked example is missing or incomplete
- A reviewer wants to confirm the example exercises every artifact shape
- Demonstrating SpecRoute to a new contributor

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
| 1 | PRD (full 23-section) | `examples/sample-project/prds/active/user-search.md` | `prd-author` |
| 2 | Requirements | `examples/sample-project/specs/user-search/requirements.md` | `spec-author` |
| 3 | Design | `examples/sample-project/specs/user-search/design.md` | `spec-author` |
| 4 | Tasks | `examples/sample-project/specs/user-search/tasks.md` | `spec-author` |
| 5 | Agent roster | `examples/sample-project/agent-roster.md` | `agent-roster-architect` |
| 6 | Global master prompt | `examples/sample-project/prompts/000_GLOBAL_MASTER.md` | `prompt-engineer` |
| 7 | Phase masters | `examples/sample-project/prompts/phase{N}_<name>/000_MASTER_<phase>.md` | `prompt-engineer` |
| 8 | Numbered task prompts | `examples/sample-project/prompts/phase{N}_<name>/<NNN>_<task>.md` | `prompt-engineer` |
| 9 | Runtime ops prompts | `examples/sample-project/prompts/runtime/{pickup-next-task,daily-checkpoint}.md` | `prompt-engineer` |
| 10 | Implementation plan | `examples/sample-project/implementation-plan.md` | `framework-docs-author` |
| 11 | Project root context | `examples/sample-project/CLAUDE.md` | `framework-docs-author` |
| 12 | Drop-in README | `examples/sample-project/README.md` | `framework-docs-author` |
| 13 | Runtime layout | `examples/sample-project/.claude/{settings,agents,commands,hooks,agent-memory}` | `runtime-architect` |

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

- Building real features (this skill produces an example for SpecRoute contributors, not a real implementation).
- Single-artifact updates (use the corresponding agent directly).
