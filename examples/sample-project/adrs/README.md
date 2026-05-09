# Architecture Decision Records

ADRs for the user-search project. Each ADR captures a single architectural decision and the rationale behind it. ADRs are immutable once accepted - corrections happen through new ADRs that supersede prior ones.

```
adrs/
├── README.md                                   (this file)
├── adr-001-postgres-indexed-scans.md           Status: Accepted
├── adr-002-cursor-based-pagination.md          Status: Accepted
├── adr-003-redis-cache-60s-ttl.md              Status: Accepted
├── adr-004-hmac-signed-cursors.md              Status: Accepted
└── adr-005-filter-set-hash-logging.md          Status: Accepted
```

## Index

| ADR | Title | Status | Source |
|---|---|---|---|
| 001 | Use Postgres indexed scans (not Elasticsearch) | Accepted | [`design.md`](../specs/user-search/design.md) §12.1 |
| 002 | Cursor-based pagination (not offset/limit) | Accepted | [`design.md`](../specs/user-search/design.md) §12.2 |
| 003 | 60-second Redis cache layer | Accepted | Phase 0 spike (Q2) |
| 004 | HMAC-signed cursors with replay protection | Accepted | Phase 0 spike (Q3) |
| 005 | Filter-set hash logging (no plaintext queries) | Accepted | Phase 0 privacy review (Q1) |

## Adding an ADR

1. Pick the next number. ADR numbers are sticky - never reused.
2. Use the SpecForge framework's [`specs/templates/architecture-decision-record.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/specs/templates/architecture-decision-record.md) template.
3. Fill the Context, Decision, Alternatives Considered, Consequences sections.
4. Set `Status: Proposed` initially. Flip to `Accepted` after stakeholder sign-off.
5. Link from this README's index.

## Lifecycle

- `Proposed` -> the ADR is drafted and circulating.
- `Accepted` -> the decision is in force. ADR is now immutable.
- `Deprecated` -> no longer in force, but no replacement.
- `Superseded by ADR-NNN` -> a new ADR replaces this one. Both stay in the directory; the new one references this one in its Context section.

## See also

- [`../specs/user-search/design.md`](../specs/user-search/design.md) - the design doc; ADRs deep-dive specific decisions surfaced there
- [`../prds/active/user-search.md`](../prds/active/user-search.md) - the PRD that motivates the project
- The SpecForge framework's [`specs/templates/architecture-decision-record.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/specs/templates/architecture-decision-record.md) - the canonical template
