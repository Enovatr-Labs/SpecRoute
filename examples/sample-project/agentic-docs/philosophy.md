# Philosophy: User Search Project

Operating beliefs for this project. These shape every artifact, agent assignment, and review.

## Why spec-driven for user-search

User-search is a deceptively simple feature - "add a search box" - that touches API design, data layer, RBAC, caching, observability, and frontend ergonomics. Without a written spec, the team would inevitably build five inconsistent versions of the contract (one per stakeholder's mental model) and then spend the rollout reconciling them.

Specs collapse the negotiation cost into one clear artifact. The PRD ([`prds/active/user-search.md`](../prds/active/user-search.md)) is the contract; the spec triplet ([`specs/user-search/`](../specs/user-search/)) is the implementation contract; the prompts ([`prompts/`](../prompts/)) are the execution contract.

## What we believe

### 1. The spec is the contract

If the implementation doesn't match the design, the design wins until renegotiated. A backend engineer who finds the design doesn't fit reality stops, opens an updated `design.md`, gets it re-approved, and resumes. They do not silently diverge.

### 2. Stable IDs survive everything

Requirements have IDs (`R1.1`, `NFR-3.1`). They never change once published. Tasks back-reference them. Tests cite them. Audit logs reference them. When someone three months from now asks "is this requirement still in force?" the answer is unambiguous because the ID never moved.

### 3. Performance budgets are merge gates

NFR-1.1 (p95 < 200ms) and NFR-1.2 (p99 < 500ms) apply at PR-merge time, not "we'll optimize later." A PR that regresses p95 doesn't merge. The load test ([Phase 3 task 18](../prompts/phase3_validation/018_load_test.md)) is the explicit gate.

### 4. Privacy and security are designed in, not bolted on

[ADR-005 (filter-set hash logging)](../adrs/adr-005-filter-set-hash-logging.md) and [ADR-004 (signed cursors)](../adrs/adr-004-hmac-signed-cursors.md) were Phase 0 outputs - decisions made before any production code. Adding privacy/security after the fact is exponentially more expensive than baking them into Phase 0.

### 5. Generic, not domain-specific

Sample data, fixtures, log examples, and changelog entries use generic content ("Jane Example", "jane@example.com"). This project ships content that survives open-source release. No real customer data anywhere.

### 6. TODO markers are intentional

When a section in a template says "TODO: insert your example here," that's a marker for a real value to be added - not a placeholder for missing thinking. Filling TODOs with invented content defeats the purpose.

## What we reject

- **Implementation without specs.** "I'll figure it out as I go" produces unreviewable change sets. We stop and write the spec first.
- **Optimization-as-feature.** Performance and observability ship with the feature, not as follow-up work.
- **Cross-vendor lock-in inside the project.** This project is Claude-only intentionally; if you find yourself adding `.codex/`-specific behavior into the agents' core operating principles, factor it out.

## Trade-offs we accepted

- **No "jump to page N"** because of cursor pagination ([ADR-002](../adrs/adr-002-cursor-based-pagination.md)). Fine for admin search; would not work for a public catalog.
- **60-second cache freshness gap** ([ADR-003](../adrs/adr-003-redis-cache-60s-ttl.md)). Admins running the same search across sessions see slightly-stale results in exchange for faster pages.
- **No full-text search** beyond name and email. Outside scope; documented in PRD §4.2.

## See also

- The framework's canonical [`agentic-docs/philosophy.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/philosophy.md) for SpecRoute's broader operating beliefs.
- [`prd.md`](../prds/active/user-search.md) §3 (Goals and Success Metrics) for the project's quantitative targets.
