# ADR-005: Log Filter-Set Hash, Not Plaintext Query Strings

**Status**: Accepted
**Date**: 2026-05-08
**Deciders**: Security auditor, Privacy lead
**Context links**: Phase 0 privacy review (Q1), [`prd.md`](../prds/active/user-search.md) §17

---

## Context

The user-search endpoint emits a structured log entry on every request (NFR-3.3). The log helps with observability, debugging, and analytics ("which filter combinations are most popular?"). The question for Phase 0: what exactly do we log?

Three options were live during the privacy review (Phase 0 task 003):

- **A. Log nothing beyond access** (just the gateway-level access log).
- **B. Log a deterministic hash of the filter set** (no plaintext values).
- **C. Log full plaintext query strings**.

The privacy lead's concern: filter values can include partial emails (`email=j.smith@`) and partial names. If the log is later exfiltrated or accessed by an unauthorized operator, plaintext queries leak PII associations - an attacker can correlate `actor_id` with the searches that actor ran.

## Decision

We will use **option B: log a deterministic hash of the filter set**. The log entry shape:

```json
{
  "level": "info",
  "ts": "<iso8601>",
  "request_id": "<from middleware>",
  "service": "users-search",
  "actor_id": "<actor.id>",
  "filter_set_hash": "<sha256 of canonical filter set, hex truncated to 8 chars>",
  "result_count": <int>,
  "duration_ms": <int>,
  "cache_hit": <bool>
}
```

No `name=`, `email=`, `role=`, or other filter values appear in plaintext.

## Alternatives Considered

### Alternative A: No logging beyond access

- **What it is**: Only the gateway access log records the request.
- **Why rejected**: Lose the ability to analyze filter patterns (which combinations are popular? what's the cache hit rate per filter shape?). The hash-based approach gives us aggregate analytics without PII exposure.

### Alternative C: Full plaintext queries

- **What it is**: Log everything as the user submitted it.
- **Why rejected**: Privacy lead explicitly rejected this. Even with rotation and access controls, the residual risk of PII recovery from logs is too high relative to the analytics value.

## Consequences

### Positive

- **No PII recovery from logs**. The hash is one-way; an analyst can group by hash to see "this filter pattern was searched 47 times this week" but cannot recover the original values.
- **Analytics still useful**. Same filter-set hash for the same actor gives us repeat-search detection. Different scopes (organization_id + role) get different hashes by construction (the hash includes them).
- **Privacy-by-design** posture. Documented in PRD §17 as the intended behavior, not an after-the-fact mitigation.

### Negative

- **Debugging is harder**. When an admin reports "I searched for John and got the wrong results," we can't reproduce by reading the log - we know what filter pattern fired but not the values. Mitigation: ad-hoc debugging uses a separate, ephemeral, opt-in trace mode (not in v1).
- **Hash collisions** are theoretically possible but practically negligible for our filter-set space. No correctness implications even if two different filter sets hash to the same value (collision rate ~ 2^-32 with 8-char truncation; we accept).

### Neutral

- Retention windows for the log are governed by the project's existing log policy. Hash-only logs reduce the privacy risk of long retention.

## Implementation Implications

- Hash computed by `derive_cache_key()` (Phase 1 task 9 also uses this hash as the cache key, so the implementation is shared).
- Logger emits the hash instead of the filter values; instrumentation in Phase 1 task 11.
- A unit test asserts no `name=` or `email=` field appears in any log entry produced by the search module (regression guard).
- Log-storage retention policy is unchanged - the application no longer adds PII risk to whatever the platform's log retention is.

## Compliance / Security / Performance Notes

- GDPR: by removing PII from logs, the search-endpoint log entries are not "personal data" for retention/deletion purposes. (Actor_id is still personal data, but it was already in our access logs.)
- The privacy review's sign-off is recorded in `prd.md` §17.

## References

- [`prd.md`](../prds/active/user-search.md) §17 (Security Requirements)
- [`design.md`](../specs/user-search/design.md) §9 (Observability)
- [`tasks.md`](../specs/user-search/tasks.md) Tasks 3 (privacy review), 11 (observability)
- [ADR-003](adr-003-redis-cache-60s-ttl.md) - shares the filter-set hash for cache keys
