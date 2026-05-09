# Lightweight PRD: <Feature Name>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name>
**Status**: Draft | Approved | In Implementation | Shipped
**Owner**: <single team or individual>
**Effort estimate**: <e.g. 2 weeks>

> Use this template only when the feature has a single owner, a single acceptance criterion, and fits comfortably on one page. Anything larger uses the full [`prd-template.md`](prd-template.md).

---

## Problem

<2–4 sentences: who is affected, what the problem is, why it matters now.>

## Proposed solution

<2–4 sentences: what we're going to build. Reference the design doc if one exists; otherwise sketch the approach.>

## User stories

- As a <role>, I want <capability>, so that <outcome>.
- As a <role>, I want <capability>, so that <outcome>.

## Goals

- <Goal 1>
- <Goal 2>

## Non-goals

- <Non-goal 1>
- <Non-goal 2>

## Acceptance criteria

- [ ] <criterion 1, testable>
- [ ] <criterion 2, testable>
- [ ] <criterion 3, testable>

## Implementation notes

<Bullet points covering anything non-obvious: data changes, API impact, migration steps, performance considerations, rollback approach. Keep terse - if this section grows past ~10 bullets, escalate to the full PRD template.>

## Risks

| Risk | Mitigation |
|---|---|
| TODO | TODO |

## Dependencies

- <Dependency 1>
- <Dependency 2>

## Open questions

- <Question 1>
- <Question 2>

---

> When this PRD is approved: move from `prds/active/` to a tracked location, create the matching spec triplet under `specs/examples/<feature>/`, and link them from this document.
