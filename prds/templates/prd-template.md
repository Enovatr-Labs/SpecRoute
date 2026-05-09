# PRD: <Feature or Initiative Name>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name / role>
**Status**: Draft | Under Review | Approved | In Implementation | Shipped | Deprecated
**Architecture Reference**: <link to ADR or architecture doc, or "TODO">
**Scope**: <one-line scope statement: what's covered, what's not>

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Background and Motivation](#2-background-and-motivation)
3. [Goals and Success Metrics](#3-goals-and-success-metrics)
4. [Scope and Boundaries](#4-scope-and-boundaries)
5. [Target Architecture](#5-target-architecture)
6. [Domain / Module Specifications](#6-domain--module-specifications)
7. [Data Strategy](#7-data-strategy)
8. [Infrastructure](#8-infrastructure)
9. [Frontend Impact](#9-frontend-impact)
10. [Backend / Integration Contracts](#10-backend--integration-contracts)
11. [Deployment and Operations Tooling](#11-deployment-and-operations-tooling)
12. [Documentation Plan](#12-documentation-plan)
13. [Script and Tooling Changes](#13-script-and-tooling-changes)
14. [Testing Strategy](#14-testing-strategy)
15. [Migration / Rollout Phases](#15-migration--rollout-phases)
16. [Multi-Cloud / Multi-Env Deployment](#16-multi-cloud--multi-env-deployment)
17. [Security Requirements](#17-security-requirements)
18. [Performance Requirements](#18-performance-requirements)
19. [Rollback Strategy](#19-rollback-strategy)
20. [Non-Functional Requirements](#20-non-functional-requirements)
21. [Risks and Mitigations](#21-risks-and-mitigations)
22. [Dependencies](#22-dependencies)
23. [Acceptance Criteria](#23-acceptance-criteria)

---

## 1. Executive Summary

<2–4 paragraphs summarizing the change at the level a busy executive needs.
What is being built or changed? Why now? What's the expected outcome? Who is affected?
End with a one-line "by the numbers" if applicable: "Reduces X from N to M; estimated effort N person-weeks across N phases."

TODO: replace with the real summary>

---

## 2. Background and Motivation

### 2.1 Current State

<What exists today. Be concrete: numbers of services, data stores, users, requests/sec, lines of code, named pain points. Quote benchmarks or measurements where possible.>

### 2.2 Why Now

<The forcing function. Compliance deadline? User-visible bug? Cost ceiling? Competitive pressure? Failed prior attempt with new context?>

### 2.3 Industry / Internal Precedent

<Optional. References to prior art or analogous decisions made elsewhere. Cite sources.>

### 2.4 Alignment

<How this PRD connects to higher-level strategy, OKRs, or other in-flight initiatives. Reference them by ID.>

---

## 3. Goals and Success Metrics

### 3.1 Goals

In priority order:

1. **<Goal 1>** - <one-line description>
2. **<Goal 2>** - <one-line description>
3. **<Goal 3>** - <one-line description>

### 3.2 Non-Goals

Explicit non-goals to prevent scope creep:

- <Non-goal 1: what we're NOT doing and why>
- <Non-goal 2>
- <Non-goal 3>

### 3.3 Success Metrics

| Metric | Baseline | Target | Measurement method |
|---|---|---|---|
| <metric 1> | <current value> | <target value> | <how measured> |
| <metric 2> | TODO | TODO | TODO |

Include leading indicators (early signals) and lagging indicators (the actual outcome).

---

## 4. Scope and Boundaries

### 4.1 In Scope

- <Item 1>
- <Item 2>

### 4.2 Out of Scope

- <Item 1 - and why it's out>
- <Item 2>

### 4.3 Open Questions

Questions that must be resolved before implementation. Track with owners and target dates.

| Question | Owner | Resolution target |
|---|---|---|
| TODO | TODO | TODO |

---

## 5. Target Architecture

<High-level architecture diagram or description. Components, boundaries, communication patterns.

If superseding an existing architecture, show before/after side-by-side.

Reference the canonical architecture doc; do not duplicate it inline.>

```
TODO: architecture diagram or component list
```

---

## 6. Domain / Module Specifications

For each domain or module affected:

### 6.1 <Module 1>

- **Responsibility**: <one paragraph>
- **Inputs**: <data, events, requests>
- **Outputs**: <data, events, responses>
- **Owner**: <team or individual>

### 6.2 <Module 2>

TODO

---

## 7. Data Strategy

### 7.1 Data Stores

| Store | Purpose | Schema owner | Migration plan |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

### 7.2 Schema Changes

<List schema changes with migration approach. Forward-compatible vs breaking. Backfill strategy.>

### 7.3 Data Retention and Privacy

<Retention windows, PII handling, GDPR / regional considerations.>

---

## 8. Infrastructure

### 8.1 Compute and Networking

<Kubernetes namespaces, services, ingresses, load balancers. Capacity assumptions.>

### 8.2 Observability

<Metrics, logs, traces. Dashboards to create or update. Alert rules.>

### 8.3 Secrets Management

<How secrets are provisioned, rotated, scoped. Reference the secrets-management doc.>

---

## 9. Frontend Impact

### 9.1 New UI Surfaces

- <Surface 1: routes, components, navigation>

### 9.2 Modified Surfaces

- <Surface 1: what changes>

### 9.3 UX Considerations

<Accessibility, i18n, responsive behavior, error states, empty states, loading states.>

---

## 10. Backend / Integration Contracts

### 10.1 New APIs

| Endpoint | Method | Purpose | Auth |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

### 10.2 Modified APIs

<Breaking vs non-breaking. Versioning strategy.>

### 10.3 Event Contracts

<Topic names, message schemas, ordering / delivery guarantees.>

---

## 11. Deployment and Operations Tooling

<New or modified deploy scripts, CI/CD pipelines, GitOps configs, runbooks.>

---

## 12. Documentation Plan

| Document | Action | Owner |
|---|---|---|
| README.md | update | TODO |
| AGENTS.md | <update if cross-cutting> | TODO |
| `docs/<topic>.md` | create | TODO |

---

## 13. Script and Tooling Changes

<New scripts to add, deprecated scripts to remove. Backwards-compat windows.>

---

## 14. Testing Strategy

### 14.1 Unit Tests

<Coverage targets, frameworks, scope.>

### 14.2 Integration Tests

<What service-to-service interactions are tested. Test environments.>

### 14.3 End-to-End Tests

<User-facing flows covered by E2E tests. Browser / device matrix.>

### 14.4 Performance and Load Tests

<Load profile, performance budgets, regression detection.>

### 14.5 Security Tests

<SAST, DAST, dependency scanning, pen-test scope.>

---

## 15. Migration / Rollout Phases

| Phase | Duration | Goals | Acceptance |
|---|---|---|---|
| Phase 0 | <weeks> | <foundation> | <criterion> |
| Phase 1 | <weeks> | <scaffold> | <criterion> |
| Phase 2 | <weeks> | <core domains> | <criterion> |

Each phase ends in a reviewable checkpoint. Phase N+1 is blocked on phase N's acceptance.

---

## 16. Multi-Cloud / Multi-Env Deployment

| Environment | Branch | Cloud / Region | Notes |
|---|---|---|---|
| local-dev | <branch> | <local> | TODO |
| develop | <branch> | <cloud-region> | TODO |
| staging | <branch> | <cloud-region> | TODO |
| production | <branch> | <cloud-region> | TODO |

---

## 17. Security Requirements

- **Authentication / Authorization**: <approach>
- **Data encryption**: <at rest, in transit>
- **Audit logging**: <what's logged, retention>
- **Compliance**: <SOC 2, GDPR, HIPAA, PCI-DSS, SOX, etc.>
- **Threat model**: <link to threat-model doc, or section here>

---

## 18. Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Page load | < 1s | TODO |
| API p95 latency | < 200ms | TODO |
| Throughput | <N> req/s | TODO |
| Bundle size | < 200KB initial JS | TODO |

Performance regressions are blockers, not follow-ups.

---

## 19. Rollback Strategy

### 19.1 Triggers

<Conditions that trigger rollback: error rate, latency, business metric.>

### 19.2 Procedure

1. <Step 1>
2. <Step 2>
3. <Step 3>

### 19.3 Recovery

<How to recover state, replay events, reconcile data after rollback.>

---

## 20. Non-Functional Requirements

- **Availability**: <SLO, e.g. 99.9%>
- **Reliability**: <RPO, RTO>
- **Maintainability**: <code health, doc currency>
- **Observability**: <metrics, logs, traces requirements>
- **Cost ceiling**: <if applicable>

---

## 21. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| TODO | low / med / high | low / med / high | TODO |

---

## 22. Dependencies

### 22.1 Internal

| Dependency | Owner | Status |
|---|---|---|
| TODO | TODO | <ready / blocked / in flight> |

### 22.2 External

| Vendor / service | Purpose | Contract / SLA |
|---|---|---|
| TODO | TODO | TODO |

---

## 23. Acceptance Criteria

The PRD is satisfied when **all** of the following are true:

- [ ] All in-scope items shipped to production
- [ ] Success metrics measured and meeting targets
- [ ] Documentation updated per Section 12
- [ ] Tests passing per Section 14
- [ ] Performance budgets met per Section 18
- [ ] Security requirements met per Section 17
- [ ] Rollback procedure tested at least once in staging
- [ ] Open questions (Section 4.3) all resolved
- [ ] <feature-specific acceptance criterion>
- [ ] <feature-specific acceptance criterion>

---

## Appendix

### A. Glossary

<Domain terms used in this document, defined>

### B. References

- <Link 1>
- <Link 2>
