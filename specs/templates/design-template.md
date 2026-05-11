# Design: <Feature Name>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name>
**Status**: Draft | Approved
**Source PRD**: <link>
**Source Requirements**: `requirements.md`

---

> **Spec triplet - part 2 of 3.** This document captures *how* the system meets the requirements. It references requirement IDs from `requirements.md`; it does not restate them. Companion: `tasks.md` for concrete work items.

---

## 1. Overview

<2–4 paragraphs describing the design approach at a level a code reviewer can hold in their head. What's the architecture? What patterns are we using? What's the key technical insight that makes this feasible?>

## 2. Architecture

### 2.1 Component Diagram

```
TODO: high-level component diagram (boxes and arrows)
```

### 2.2 Components

| Component | Responsibility | Owner |
|---|---|---|
| <Component 1> | <one-paragraph responsibility> | <team> |
| <Component 2> | <responsibility> | <team> |

### 2.3 Data Flow

For each user-facing operation, describe the request path:

#### Operation: <name>

```
TODO: sequence diagram or numbered request path
```

1. <Step 1>
2. <Step 2>
3. <Step 3>

**Satisfies:** R1.1, R1.2

## 3. Data Model

### 3.1 Entities

#### <Entity 1>

| Field | Type | Constraints | Purpose |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | … |
| `<field>` | … | … | … |

#### <Entity 2>

TODO

### 3.2 Relationships

<Cardinality, foreign keys, orphan handling.>

### 3.3 Indexes

| Index | Columns | Reason |
|---|---|---|
| TODO | TODO | TODO |

### 3.4 Migrations

<Migration approach: forward-compatible? Backfill required? Lock concerns?>

## 4. API Contracts

### 4.1 Endpoint: `<METHOD> /api/<path>`

**Purpose:** <one line>
**Auth:** <method>
**Satisfies:** R1.1

#### Request

```http
<METHOD> /api/<path>
Content-Type: application/json

{
  "field": "value"
}
```

#### Response (200)

```json
{
  "id": "...",
  "...": "..."
}
```

#### Errors

| Status | Reason | Response |
|---|---|---|
| 400 | Invalid input | `{"error": "...", "fields": {...}}` |
| 401 | Unauthenticated | `{"error": "..."}` |
| 403 | Unauthorized | `{"error": "..."}` |
| 404 | Not found | `{"error": "..."}` |
| 429 | Rate limited | `Retry-After: <s>` |
| 500 | Internal | `{"error": "..."}` |

### 4.2 Endpoint: `<METHOD> /api/<path>`

TODO

## 5. Event Contracts

If the design uses async messaging:

### Event: `<event-name>`

| Field | Type | Purpose |
|---|---|---|
| `version` | int | Schema version (incremented on breaking changes) |
| `…` | … | … |

**Topic:** `<topic-name>`
**Producer:** <component>
**Consumers:** <components>
**Ordering / delivery:** <at-least-once / at-most-once / exactly-once; partition key>
**Satisfies:** RX.Y

## 6. State Management

<Where state lives. How concurrent updates are handled. Idempotency strategy. Cache invalidation.>

## 7. Performance Considerations

| Concern | Approach | Budget |
|---|---|---|
| Query throughput | <indexing, caching, pagination strategy> | <NFR-1.1 reference> |
| Hot path latency | <…> | <NFR-1.2 reference> |
| Bundle size | <code-splitting, lazy loading> | <reference> |

Reference NFR IDs from `requirements.md`. The design must explicitly meet each NFR.

## 8. Security Considerations

| Concern | Approach |
|---|---|
| Authentication | <NFR-2.1 reference; mechanism> |
| Authorization | <NFR-2.2 reference; RBAC / ABAC model> |
| Input validation | <where, how> |
| Output encoding | <XSS prevention, etc.> |
| Secrets handling | <how secrets reach the runtime> |
| Audit logging | <what's logged, where> |
| Threat model | <link or summary> |

## 9. Observability

| Signal | What's emitted | Dashboard / alert |
|---|---|---|
| Metrics | <names and labels> | <dashboard link> |
| Logs | <fields, levels> | <log query> |
| Traces | <spans, attributes> | <trace search> |

**Satisfies:** NFR-3.1, NFR-3.2.

## 10. Failure Modes and Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <upstream dependency unavailable> | medium | <user impact> | <circuit breaker, retry, fallback> |
| <database overload> | low | <…> | <…> |

## 11. Rollout Considerations

- **Feature flag**: <yes / no, flag name>
- **Migration ordering**: <data → app → release, or reverse>
- **Backwards compatibility**: <breaking change? grace period? versioned APIs?>

## 12. Alternatives Considered

For each significant choice, briefly note alternatives that were rejected and why. This isn't a place for theory - it's the record future readers need to understand the decision.

### 12.1 <Choice 1>

- **Chosen**: <approach>
- **Alternatives considered**: <list>
- **Why chosen**: <rationale>

### 12.2 <Choice 2>

TODO

## 13. Open Questions

| ID | Question | Resolution required by |
|---|---|---|
| Q1 | TODO | TODO |

Open design questions block task generation. Resolve them before promoting to `Approved`.

---

## Appendix: Requirement → Component Map

| Requirement | Components Involved |
|---|---|
| R1.1 | <Component 1>, <Component 2> |
| R1.2 | <Component 1> |
| R2.1 | <Component 3> |

Used by `tasks.md` to confirm coverage and ownership.
