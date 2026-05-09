# Task 002: Spike - Cursor Encoding Choice

> Phase 0 spike. Output is a decision, not production code.

---

## 1. Objective

Decide between opaque base64-HMAC cursors and structured-ID cursors for `/api/users/search` pagination. The PRD's open question Q3 (`requirements.md` Section 7) frames the choice. We need a side-by-side prototype to evaluate.

After this spike: a decision is recorded in [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 6 (State Management).

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 17 (Security Requirements)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) Q3; R4.1, R4.2; NFR-2.3
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 6
**Phase Master**: [`000_MASTER_foundation.md`](000_MASTER_foundation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)

Cursor pagination needs a token that encodes the position in the result set (typically `(last_id, last_sort_key)`). Two designs:

- **Opaque base64-HMAC**: encode the position dict, sign with HMAC-SHA256, base64. Looks like `eyJpZCI6Ii4uLiJ9.<sig>`. Tamper-evident; consumers can't introspect.
- **Structured ID**: a composite ID like `<sort_key>__<row_id>` with no signature. Compact; introspectable; trivial to forge.

The signing variant prevents forge-and-bypass attacks (e.g. crafting a cursor that returns a different RBAC scope). The structured variant is smaller and simpler.

## 3. Agent Assignment

**Primary Agent**: `backend-engineer` (see [`../../agent-roster.md`](../../agent-roster.md))
**Supporting Agents**:

- `security-auditor` - advises on signature requirements and replay protection.

## 4. Prerequisites

- [ ] Phase 0 task 003 (privacy review) is in flight or scheduled. (Independent.)
- [ ] Test scaffolding exists for round-trip property tests.

## 5. Task Details

### 5.1 Goal

Prototype both cursor encodings. Compare:

- Encode/decode latency.
- Cursor size in URL (typical and worst case).
- Cross-version stability (does an old cursor decode correctly after a deploy?).
- Tamper resistance (is forging a malicious cursor possible?).

### 5.2 Approach

1. Implement both encoders/decoders behind a feature toggle (no production wiring).
2. Round-trip test 100k random positions.
3. Measure encode + decode latency: target < 100µs each.
4. Measure cursor sizes; log p50, p95, p99.
5. Run a tampering test against the structured variant: craft a cursor for a different organization and confirm it deserializes (it should - that's the security gap).
6. Run the same test against the HMAC variant: confirm tampering produces a signature failure.

### 5.3 Decision criteria

The HMAC variant wins unless:

- Encode/decode adds > 5ms p95 latency on the request path (unlikely with HMAC-SHA256 - it's fast).
- Cursor size becomes a problem for URL length (HMAC adds ~32 bytes signature; opaque base64 adds 33% overhead).

If those conditions hold, structured wins **only if RBAC scoping is enforced server-side every request** (which it is - see task 6). In that case the cursor doesn't carry security; it carries position. But replay protection (timestamp) is still useful.

The default expectation is HMAC + replay timestamp.

### 5.4 Files to Modify

| File | Change |
|---|---|
| [`../../specs/user-search/design.md`](../../specs/user-search/design.md) | Section 6: cursor encoding decision and signing key strategy |
| [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) | Section 7: Q3 marked resolved |

## 6. Acceptance Criteria

- [ ] Both prototypes implemented and round-trip tested.
- [ ] Latency, size, tampering measurements captured.
- [ ] Decision recorded in `design.md` Section 6 with measurements.
- [ ] Q3 marked resolved in `requirements.md` Section 7.
- [ ] Task 8 (cursor encode/decode implementation) reads the chosen design.

## 7. Out of Scope

- Implementing the chosen variant in production code - that's task 8.
- Migrating from one cursor format to another - out of scope for v1.

## 8. Validation

`security-auditor` reviews the decision with particular attention to:

- Tamper resistance.
- Replay protection (timestamp inside the signed payload, validated server-side).
- Key rotation strategy (the signing key needs a rotation plan even if not exercised at launch).

## 9. Rollback

Spike is non-production; no rollback. The chosen format is stable across the v1 lifetime; format migration would be a v2 ADR.
