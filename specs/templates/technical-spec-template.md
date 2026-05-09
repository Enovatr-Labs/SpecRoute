# Technical Spec: <Subject>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name>
**Status**: Draft | Approved | Implemented | Superseded

> Technical specs cover non-product-facing work - refactors, migrations, infrastructure changes, library upgrades - where there is no user-facing PRD. For product features, use the spec triplet ([`requirements-template.md`](requirements-template.md) + [`design-template.md`](design-template.md) + [`tasks-template.md`](tasks-template.md)) or [`feature-spec-template.md`](feature-spec-template.md).

---

## 1. Context

<Why this work is needed. What problem in the system does it solve? What forced the timing?>

## 2. Goals

- <Goal 1>
- <Goal 2>

## 3. Non-Goals

- <Non-goal 1>
- <Non-goal 2>

## 4. Current State

<What exists today. Be concrete - file paths, line counts, latency numbers, error rates.>

## 5. Proposed Changes

### 5.1 Approach

<2–4 paragraphs describing the technical approach.>

### 5.2 Component-by-component changes

| Component / file | Change |
|---|---|
| `<path>` | <what changes> |
| `<path>` | <what changes> |

### 5.3 New components introduced

<If any.>

### 5.4 Components retired

<If any. Include backwards-compat plan if removal is breaking.>

## 6. Sequence / Plan

Phase 1: <name>

1. <Step>
2. <Step>

Phase 2: <name>

1. <Step>

## 7. Risk and Mitigations

| Risk | Mitigation |
|---|---|
| TODO | TODO |

## 8. Validation

How we'll know it worked:

- <Test or measurement 1>
- <Test or measurement 2>

## 9. Rollback

<Procedure if validation fails.>

## 10. Open Questions

- <Question 1>
- <Question 2>
