---
name: landscape-page-scope
description: spec-driven-landscape.md is a reader's decision aid only - no "what SpecRoute adopted from peers" section, no version column, no numbers in prose
metadata:
  type: project
---

`agentic-docs/spec-driven-landscape.md` (and its wiki mirror `wiki/Spec-Driven-Landscape.md`) is scoped as a **decision aid for a reader choosing a framework**. Deliberate exclusions, confirmed 2026-09-02:

- No "what SpecRoute has taken from peers" / "what we're adopting" section.
- No version column in the comparison table, and no version numbers or star counts anywhere in prose - each is a new rot surface.
- Peer facts are attributed, never adjudicated ("spec-kit's README instructs...", not "spec-kit correctly...").

**Why:** the page earns trust by being useful to someone who might choose a peer over SpecRoute. Self-referential "what we learned" content turns it into advocacy, which is the failure mode the page's own "Scope and method" section is written to avoid. Version/star digits in prose defeat the "raw numbers in the table only" rule that gives the page exactly one place to refresh.

**How to apply:** when asked to expand this page, push additions toward the comparison table or the "when to pick a peer instead" list. A refresh is re-running the `gh api` command in the page and editing **both** files together - never a timestamp bump in one. See [[landscape-refresh-procedure]].
