# ADR-004: HMAC-Signed Cursors with Replay Protection

**Status**: Accepted
**Date**: 2026-05-08
**Deciders**: Backend engineer, Security auditor
**Context links**: Phase 0 spike (Q3), [ADR-002](adr-002-cursor-based-pagination.md)

---

## Context

[ADR-002](adr-002-cursor-based-pagination.md) chose cursor-based pagination. The cursor encodes `(last_sort_key, last_id)` from the most recently returned row. Two questions remained for Phase 0 to resolve:

1. **Format**: opaque (HMAC-signed base64) vs structured-ID (plaintext composite ID)?
2. **Replay protection**: if cursors are reusable indefinitely, an attacker can hold a cursor from before an RBAC change to enumerate users they no longer have access to.

Phase 0 task 002 (cursor encoding spike) prototyped both variants and measured encode/decode latency, cursor size in URLs, and tampering resistance.

## Decision

We will use **HMAC-SHA256 signed base64 cursors with timestamp replay protection**. Each cursor contains `(last_id, last_sort_key, ts)` JSON-encoded, signed with a project secret, base64url-encoded. Cursors older than 24 hours are rejected.

## Alternatives Considered

### Alternative 1: Structured-ID plaintext cursor

- **What it is**: A cursor like `<sort_key>__<row_id>` with no signature.
- **Why rejected**: Forgeable. An attacker can craft a cursor pointing to any `(id, created_at)` pair. Even though the endpoint re-checks RBAC for every page (so they can't bypass authorization), an attacker who knows another user's `id` could probe to confirm existence (information disclosure).

### Alternative 2: Encrypted (not signed) cursor

- **What it is**: Encrypt the cursor body with a project secret instead of HMAC-signing.
- **Why rejected**: Encryption hides the cursor body but doesn't prevent tampering (a flipped bit is still decryption-valid in ECB or non-AEAD modes). HMAC + plaintext is simpler and gives us tamper-evidence; we don't need confidentiality of the cursor body.

### Alternative 3: Server-side cursor allowlist

- **What it is**: Server stores the cursors it has issued and only accepts known cursors back.
- **Why rejected**: Server-side state. See [ADR-002](adr-002-cursor-based-pagination.md) Alternative 3.

## Consequences

### Positive

- **Tamper-evident**: signature mismatch = HTTP 400. Attacker cannot forge cursors.
- **Replay-protected**: cursors over 24 hours old are rejected, bounding the staleness window for enumeration attacks via leaked cursors.
- **Stateless**: no server-side cursor allowlist to maintain.
- **Fast**: HMAC-SHA256 is ~5µs per encode/decode. Phase 0 measurement: 100µs latency budget per cursor op met easily.

### Negative

- Cursor size is ~150 bytes (vs ~50 bytes for plaintext). URLs are longer; not a problem for our admin context.
- Key rotation requires support for verifying with the previous key during a rotation window. Implementation handles this; documented in the operations runbook.

### Neutral

- The 24-hour replay window is configurable. We chose 24h as the trade-off between "user finishing a long admin session" and "stale cursor outliving relevance."

## Implementation Implications

- Signing key read from secrets manager (no hardcoding).
- Encode: `base64url(payload) + "." + base64url(hmac_sha256(key, base64url(payload)))`.
- Payload: `{"id": ..., "key": ..., "ts": <epoch_seconds>}`.
- Decode validates signature first, then `now - ts <= 24h`, then returns the structured payload.
- Verify path tries current key first, then previous key (during rotation windows).
- Test matrix in [ADR-002](adr-002-cursor-based-pagination.md) and `tasks.md` task 8 covers tampering, expiry, and round-trip.

## Compliance / Security / Performance Notes

- Auditor's concern (information disclosure via cursor probing) is mitigated by HMAC.
- Performance budget (Phase 0): encode + decode < 100µs each. Measured at 5-15µs in the spike.
- The cursor's `id` field could leak if the cursor is intercepted. Cursors should not be logged in plaintext (see [ADR-005](adr-005-filter-set-hash-logging.md)).

## References

- [ADR-002](adr-002-cursor-based-pagination.md) - the pagination shape
- [ADR-005](adr-005-filter-set-hash-logging.md) - related decision on what we log
- [`design.md`](../specs/user-search/design.md) §6 (State Management), §8 (Security Considerations)
- [`tasks.md`](../specs/user-search/tasks.md) Tasks 2 (encoding spike), 8 (cursor implementation)
