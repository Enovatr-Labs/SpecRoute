# Task 008: Implement Cursor Encode/Decode

> Production task prompt. Phase 1 backend component.

---

## 1. Objective

Implement `search.encode_cursor(row, sort)` and `search.decode_cursor(token)` per the design chosen in Phase 0 task 002 (default expectation: HMAC-SHA256-signed base64 with timestamp replay protection). The cursor encodes the position needed to fetch the next or previous page.

After this task: round-trip property tests pass; tampered cursors are rejected with HTTP 400; cursors older than 24 hours are rejected.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 17 (Security Requirements)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) — R4.1, R4.2, NFR-2.3
**Architecture Reference**: [`../../design.md`](../../design.md) Section 6 (State Management)
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 8. Depends on Phase 0 task 002 (cursor encoding decision). Consumed by task 7 (query builder uses decoded cursor) and task 10 (compose endpoint emits encoded cursor).
**Current File(s)**: `src/services/users/search/cursor.py` (new).

## 3. Agent Assignment

**Primary Agent**: `backend-engineer`
**Supporting Agents**:

- `security-auditor` — reviews signature implementation, key handling, replay protection.
- `unit-test-writer` — embedded.

## 4. Prerequisites

- [ ] Phase 0 task 002 closed; `design.md` Section 6 records the chosen format.
- [ ] Signing key available via the project's secrets manager. Key rotation strategy documented (rotation can be deferred but the strategy must exist).

## 5. Task Details

### 5.1 Goal

```python
def encode_cursor(last_row: UserRow, sort: Sort) -> str
def decode_cursor(token: str) -> CursorPayload | InvalidCursor
```

`CursorPayload` carries `(last_id, last_sort_key, ts)`. `ts` is the encode timestamp (epoch seconds). `decode_cursor` returns `InvalidCursor` for any of: tampered signature, expired (`now - ts > 24h`), malformed payload.

### 5.2 Default format (HMAC variant)

```
cursor = base64url(payload) + "." + base64url(hmac_sha256(key, base64url(payload)))
payload = json.dumps({"id": ..., "key": ..., "ts": ...})
```

The `.` separator splits payload from signature. base64url avoids `+/=` characters that need URL escaping.

### 5.3 Test matrix

| Test | Expected |
|---|---|
| `decode(encode(row))` | matches input row's `(id, sort_key)` |
| `decode("garbage")` | `InvalidCursor` |
| `decode(encode(row).replace("a", "b"))` (tampered payload) | `InvalidCursor` (signature fails) |
| `decode(<cursor with ts=now-25h>)` | `InvalidCursor` (replay window exceeded) |
| `decode(<cursor signed with old key>)` after key rotation | `InvalidCursor` (unless old key is in the verify list) |

### 5.4 Key rotation

The verify path tries the current key first, then the previous key (if any). Encode always uses the current key. This allows seamless rotation: rotate the key, old cursors keep working until the next encode, then they fall out naturally as users page.

### 5.5 Files to Modify

| File | Change |
|---|---|
| `src/services/users/search/cursor.py` | Create — encode/decode + `CursorPayload` + `InvalidCursor` |
| `src/services/users/search/__init__.py` | Export |
| `tests/services/users/search/test_cursor.py` | Create — test matrix above + property test for round-trip |

## 6. Acceptance Criteria

- [ ] Encode and decode functions exist with the signatures above.
- [ ] Round-trip property test passes for 1000 random rows.
- [ ] Tampered cursors are rejected.
- [ ] Expired cursors (>24h) are rejected.
- [ ] Encode + decode latency < 100µs each (microbenchmark).
- [ ] Signing key read from secrets manager — never hardcoded.
- [ ] `security-auditor` signs off.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Cursor migration between versions — out of v1.
- UI display of cursor (frontend handles opaquely).
- Key rotation automation — operational concern; document the procedure.

## 8. Validation

Unit tests cover the matrix. Mutation check: introduce a one-byte change in the signature path; confirm the tampered-cursor test fails. Restore.

## 9. Rollback

`git revert`. Cursors in flight at the moment of revert become invalid; users get a 400 once and re-paginate. Acceptable.
