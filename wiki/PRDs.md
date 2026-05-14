# PRDs

<!-- sources: prds/README.md -->

Product Requirements Documents — the **business intent** layer of the spec-driven flow.

For the canonical reference, see [`prds/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prds/README.md).

## Directory layout

```
prds/
├── templates/
│   ├── prd-template.md                  full 23-section enterprise PRD
│   ├── lightweight-prd-template.md      single-page alternative
│   └── platform-srs-template.md         system-wide SRS
├── active/                              in-flight PRDs
├── deprecated/                          superseded PRDs
├── archive/                             shipped or abandoned PRDs
└── examples/                            illustrative worked PRDs
```

## When to use which template

| Template | Use when |
|---|---|
| `prd-template.md` (full) | Multi-team feature, multi-week effort, cross-service impact, or significant architectural change. Default for non-trivial work. |
| `lightweight-prd-template.md` | Single owner, single team, single acceptance criterion, fits on one page. |
| `platform-srs-template.md` | Specifying the platform as a whole. One per platform; revise rather than duplicate. |

**Rule of thumb:** if you're unsure, start with the lightweight template. If filling it in produces an awkward doc that wants to be longer, escalate to the full template.

## Lifecycle

1. **Draft** in `prds/active/` with `Status: Draft`.
2. **Review** — promote to `Status: Under Review` once the author considers it ready.
3. **Approve** — flip to `Status: Approved` when stakeholders sign off. **This is the gate before spec-triplet work begins.**
4. **Implement** — status `In Implementation` while the matching `specs/<feature>/` is being built and work is in flight.
5. **Ship** — `Status: Shipped`; move to `prds/archive/`.
6. **Deprecate** — when superseded, move to `prds/deprecated/` with a pointer to the replacement PRD.

Filenames:
- `active/` → `<slug>.md` (e.g. `notification-preferences.md`).
- `archive/` → prefix the year for sorting (e.g. `2026-04-notification-preferences.md`).

## Frontmatter contract

```yaml
---
Version: 0.1
Date: YYYY-MM-DD
Author: <name>
Status: Draft | Under Review | Approved | In Implementation | Shipped | Deprecated
Architecture Reference: <link or "TODO">
Scope: <one-line scope statement>
---
```

- A PRD without `Status` is not actionable.
- A PRD without `Architecture Reference` is missing context downstream stages need.

## What's in the full template (overview)

The 23-section template covers:

1. Header & metadata
2. Problem statement
3. Goals & success metrics
4. Scope (in / out)
5. User stories
6. Functional requirements (high-level — the spec triplet refines)
7. Non-functional requirements (NFRs)
8. UX considerations
9. Open questions
10. Dependencies
11. Risks & mitigations
12. Documentation requirements
13. Analytics / observability needs
14. Privacy / data handling
15. Security requirements
16. Compliance considerations
17. Internationalization
18. Performance budgets
19. Rollout strategy + rollback triggers + rollback procedure
20. Communication plan
21. Timeline / phases
22. Alternatives considered
23. Acceptance criteria

For trivial features, the **lightweight PRD** collapses sections 2–23 into a single page with the essentials.

## Owner agent

Drafting and reviewing PRDs is owned by the `prd-author` agent (in `.claude/agents/prd-author.md`). It uses the templates above and produces PRDs that match the frontmatter contract.

## From PRD to spec triplet

Once a PRD is `Approved`, the next step is the spec triplet. Use [`prompts/shared/prd-to-spec-prompt.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/prd-to-spec-prompt.md) as the conversion prompt. See [[Specs]] for what comes next.

## See also

- [[Specs]] — the technical layer after PRD approval
- [[Workflow PRD to Production]] — the 13-stage outer workflow PRDs anchor
- [[Spec-Driven Development]] — why PRD → spec → tasks → impl
- [[Worked Example]] — a real 23-section PRD for the `user-search` feature
