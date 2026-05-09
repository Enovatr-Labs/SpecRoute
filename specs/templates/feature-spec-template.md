# Feature Spec: <Feature Name>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name>
**Status**: Draft | Approved | In Implementation | Complete
**Source PRD**: <link>

> **Lightweight single-file alternative to the spec triplet.** Use this template for features that genuinely fit on one page - single team, single owner, single acceptance criterion. Anything larger uses [`requirements-template.md`](requirements-template.md), [`design-template.md`](design-template.md), [`tasks-template.md`](tasks-template.md).

---

## 1. Overview

<2–4 sentences: what we're building and why.>

## 2. Requirements

Each requirement has a stable ID. `WHEN <event>, THE <system> SHALL <action>` form for testability.

- **R1** - TODO
- **R2** - TODO
- **R3** - TODO

## 3. Design

### 3.1 Approach

<2–3 paragraphs of the implementation approach.>

### 3.2 Data model changes (if any)

```
TODO
```

### 3.3 API changes (if any)

| Endpoint | Method | Purpose |
|---|---|---|
| TODO | TODO | TODO |

### 3.4 Sequence

<Numbered request path or short sequence diagram for the critical flow.>

## 4. Tasks

Numbered for execution order. Each task back-references requirements.

1. <Task> _(Requirements: R1)_
2. <Task> _(Requirements: R1, R2)_
3. <Task> _(Requirements: R3)_

## 5. Performance and security

| Concern | Approach |
|---|---|
| Performance | <budget and approach> |
| Security | <auth, validation, secrets> |
| Observability | <metrics, logs, traces> |

## 6. Risks and rollout

- **Risks**: <bullet list>
- **Feature flag**: <yes / no, name>
- **Rollback**: <one-line procedure>

## 7. Done checklist

- [ ] All tasks checked off
- [ ] Each requirement has a passing test
- [ ] Performance budget met
- [ ] Documentation updated
- [ ] PR merged
