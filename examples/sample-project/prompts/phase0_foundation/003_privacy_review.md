# Task 003: Privacy Review for Query Logging

> Phase 0 task. Output is a sign-off, not code.

---

## 1. Objective

Confirm with the privacy lead what's logged when `/api/users/search` is called. The PRD's open question Q1 frames the choice: log full query strings (richer analytics) vs log only filter-set hashes (privacy-preserving). The default proposal is the latter.

After this task: privacy sign-off recorded; PRD Section 17 updated; Q1 marked resolved.

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 17 (Security Requirements)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) Q1; NFR-3.3
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 9 (Observability)
**Phase Master**: [`000_MASTER_foundation.md`](000_MASTER_foundation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)

The proposal: every search emits a structured log entry with `request_id`, `actor_id`, `filter_set_hash`, `result_count`, `duration_ms`, `cache_hit`. The hash is deterministic so analytics can group by query pattern, but the original strings (which may contain partial emails) are not preserved.

The privacy lead may raise:

- Whether `actor_id` paired with `filter_set_hash` constitutes PII linkage.
- Whether log retention windows are tight enough.
- Whether structured log access is auditable.

## 3. Agent Assignment

**Primary Agent**: `security-auditor` (see [`../../agent-roster.md`](../../agent-roster.md))
**Supporting Agents**:

- Privacy lead (human reviewer, not an agent).

## 4. Prerequisites

- [ ] Privacy lead identified and engaged.
- [ ] Existing log retention and access controls documented.
- [ ] PRD Section 17 has the proposed logging design.

## 5. Task Details

### 5.1 Goal

Get the privacy review signed off. The output is a one-page review summary attached to the PRD.

### 5.2 Process

1. Schedule the privacy review with the privacy lead.
2. Brief them: read PRD Section 17, design Section 9.
3. Walk the proposed log shape, including a sample log line.
4. Discuss alternatives (no logging at all; full string logging with consent banner).
5. Capture the decision.
6. Update PRD Section 17 with the final logging shape, retention window, and any constraints.

### 5.3 Sample log line for review

```json
{
  "level": "info",
  "ts": "2026-05-08T14:32:18Z",
  "request_id": "req-abc123",
  "service": "users-search",
  "actor_id": "u-550e8400",
  "filter_set_hash": "a3f2e1b9",
  "result_count": 14,
  "duration_ms": 87,
  "cache_hit": false
}
```

Note what's *absent*: no `name=` value, no `email=` value, no organization name. The hash is derived from the canonical filter set including the actor's `organization_id`, so the same admin doing the same search produces the same hash.

### 5.4 Decision options

| Option | Logged | Privacy posture | Analytics value |
|---|---|---|---|
| A: nothing | only access (gateway level) | Strongest | None |
| B: hash only (proposed) | hash + counts + timing | Strong; no PII recovery | Medium - group by pattern |
| C: full strings | every filter value | Weak; PII recoverable | High - exact analytics |

Default proposal: **B**.

### 5.5 Files to Modify

| File | Change |
|---|---|
| [`../../prds/active/user-search.md`](../../prds/active/user-search.md) | Section 17: record logging decision and retention window |
| [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) | Section 7: Q1 marked resolved |
| [`../../specs/user-search/design.md`](../../specs/user-search/design.md) | Section 9: confirm log shape matches the privacy decision |

## 6. Acceptance Criteria

- [ ] Privacy review held; outcome documented.
- [ ] PRD Section 17 updated with the chosen option.
- [ ] Q1 marked resolved.
- [ ] Task 11 (observability) reads the approved log shape.

## 7. Out of Scope

- Implementing the logger - that's task 11.
- Log retention policy changes - that's a separate workstream.
- Log access audit - handled by the existing logging infrastructure.

## 8. Validation

Confirmed at task 11 (observability) by reviewing the actual log entries against the approved shape.

## 9. Rollback

If the privacy decision changes after launch, the log shape is config-driven (filter-set hashing happens in the application; turning logging off is a config flag). No data backfill issue.
