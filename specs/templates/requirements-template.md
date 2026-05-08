# Requirements: <Feature Name>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name>
**Status**: Draft | Approved
**Source PRD**: <link to PRD>

---

> **Spec triplet — part 1 of 3.** This document captures *what* must be true for the feature to be considered complete. Companion documents:
> - [`design.md`](design.md) — *how* the system meets these requirements
> - [`tasks.md`](tasks.md) — concrete, ordered work items, each back-referencing requirement IDs

---

## 1. Introduction

<2–3 sentences placing this feature in context. Who is this for? What problem does it solve? Reference the source PRD for the full motivation.>

## 2. Glossary

| Term | Definition |
|---|---|
| <Term 1> | <Definition> |
| <Term 2> | <Definition> |

Define every domain term used in the requirements below. Stable definitions reduce ambiguity in acceptance criteria.

## 3. User Stories

User stories drive the requirements. Each story leads to one or more requirements with stable IDs.

### Story 1: <Title>

**As a** <role>, **I want** <capability>, **so that** <outcome>.

Linked requirements: R1.1, R1.2, …

### Story 2: <Title>

**As a** <role>, **I want** <capability>, **so that** <outcome>.

Linked requirements: R2.1, R2.2, …

## 4. Requirements

Each requirement has a stable ID (`R<group>.<index>`) and an acceptance criterion in the form `WHEN <event>, THE <system> SHALL <action>`. **IDs are immutable** — when a requirement is removed, mark it deprecated and reuse the next available number for new ones.

### Requirement Group 1: <Group Name>

#### R1.1 — <Short title>

**User Story:** Story 1.

**Acceptance Criteria:**

1. WHEN <event>, THE <system> SHALL <action>.
2. WHEN <event with condition>, THE <system> SHALL <action>.
3. IF <precondition>, THEN <expected behavior>.

**Notes:** <Optional clarifications, edge cases, or non-obvious constraints.>

#### R1.2 — <Short title>

**User Story:** Story 1.

**Acceptance Criteria:**

1. WHEN <event>, THE <system> SHALL <action>.

### Requirement Group 2: <Group Name>

#### R2.1 — <Short title>

**Acceptance Criteria:**

1. WHEN <event>, THE <system> SHALL <action>.

## 5. Non-Functional Requirements

Treated separately because they cross-cut multiple user stories.

### NFR-1: Performance

- **NFR-1.1** — All API endpoints SHALL respond within p95 of <N>ms under <load profile>.
- **NFR-1.2** — Initial page load SHALL complete within <N> seconds on <reference network>.

### NFR-2: Security

- **NFR-2.1** — All endpoints SHALL require authentication via <method>.
- **NFR-2.2** — All write operations SHALL be authorized against <RBAC model>.

### NFR-3: Observability

- **NFR-3.1** — All requests SHALL emit structured logs including <fields>.
- **NFR-3.2** — All operations SHALL emit a metric named <pattern>.

### NFR-4: Reliability

- **NFR-4.1** — The feature SHALL maintain <availability target> as measured by <SLO>.

## 6. Out of Scope

Explicit non-requirements to prevent scope creep:

- <Item 1: what is NOT a requirement and why>
- <Item 2>

## 7. Open Questions

| ID | Question | Owner | Resolution target |
|---|---|---|---|
| Q1 | TODO | TODO | TODO |

Open questions block requirement approval. They do not block design exploration.

---

## Appendix: Requirement → User Story Map

| Requirement | User Story |
|---|---|
| R1.1 | Story 1 |
| R1.2 | Story 1 |
| R2.1 | Story 2 |

This map is also rebuilt in `tasks.md` to confirm task → requirement coverage.
