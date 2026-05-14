# Workflow: Testing and Validation

<!-- sources: workflows/testing-and-validation.md -->

How a SpecRoute-driven feature is validated against its spec. Runs as **Stage 10** of [[Workflow PRD to Production]], after all task PRs have merged.

For the canonical version, see [`workflows/testing-and-validation.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/workflows/testing-and-validation.md).

## Prerequisites

- All tasks in `tasks.md` checked off.
- All PRs merged to the integration branch.
- Staging environment matches production schema and approximate scale.

## Validation steps

### 1. Coverage audit

For every requirement (`R<N.M>`) and NFR (`NFR-<N.M>`) in `requirements.md`:

- [ ] At least one test asserts the behavior.
- [ ] The test passes in CI.
- [ ] The test is referenced in the coverage table in `tasks.md`.

If a requirement has no test: either add one before passing, or document why it can't be tested (attestation rather than executable behavior) and have a human reviewer sign off.

### 2. Functional tests

Run the full unit + integration test suite. **100% green** required. Flaky tests block — fix them or quarantine with a follow-up task.

### 3. End-to-end tests

Run E2E flows against staging. Every user story in `requirements.md` has an E2E test. Empty / error / loading states exercised. Cross-browser / cross-device matrix per project standards.

### 4. Performance tests

For each performance NFR:

- Run a load test with the profile specified in the design.
- Capture p50, p95, p99 latencies.
- Compare against the budget in the PRD's Section 18.

**Any budget exceeded is a blocker.** Performance regressions are not "fix it next sprint."

### 5. Security validation

Per [`rules/security-rules.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/rules/security-rules.md):

- Authentication required on every new endpoint.
- Authorization (RBAC) enforced; cross-tenant attempts blocked.
- Input validation rejects malformed requests with structured 400s.
- Audit logs emit per the design.
- Rate limits enforced.
- No new secrets in tracked files (run `/sanitize`).

For features with regulatory requirements (SOC 2, GDPR, HIPAA, PCI-DSS, SOX): confirm controls map to the required attestations.

### 6. Observability validation

For each observability NFR:

- The metric appears in the project's monitoring system.
- The log entry has the required fields.
- The trace span links to the parent span.

**A feature without observability ships blind.** Block release until observability is wired.

### 7. Rollback drill

Per the PRD's Section 19:

- Trigger the rollback procedure in staging.
- Verify the system returns to the pre-feature state.
- Verify error rates drop.
- Re-enable; verify recovery.

**A rollback that's never been tested is not a rollback.**

### 8. Documentation audit

Per PRD Section 12:

- API reference updated for any new / changed endpoints.
- User-facing docs updated for user-visible changes.
- Internal docs (architecture, data-model) updated for structural changes.
- Changelog / release notes drafted.

## Validation report

Output is a report attached to the PRD's spec triplet:

```markdown
# Validation Report: <Feature Name>

**Date**: <YYYY-MM-DD>
**Validator**: <name / role>
**Status**: PASS | FAIL | CONDITIONAL

## Coverage
- Requirements covered: <N>/<total>
- NFRs covered: <N>/<total>
- Coverage gaps: <list>

## Tests
- Unit: <pass>/<total>
- Integration: <pass>/<total>
- E2E: <pass>/<total>

## Performance
- p95 latency: <observed> vs <budget>
- p99 latency: <observed> vs <budget>

## Security
- (per security-rules.md checklist)

## Observability
- Metrics emitted: <list>
- Logs structured: <yes/no>
- Traces linked: <yes/no>

## Rollback
- Drill executed: <date>
- Result: <pass/fail>

## Documentation
- API reference: <updated/needed>
- User docs: <updated/needed>
- Internal docs: <updated/needed>

## Recommendation
<PASS / FAIL / CONDITIONAL>

## Outstanding
- <items that don't block release but should follow up>
```

## Outcomes

- **PASS** — every step green; ready for rollout ([[Workflow Release Readiness]]).
- **FAIL** — one or more steps red; back to implementation.
- **CONDITIONAL** — green except for non-blocking items; rollout proceeds with conditions logged.

## Common failures

### "Tests pass locally but fail in CI"
CI environment differs from local — usually a missing fixture, a real-time-dependent test, or an order-dependency. Fix the test, not CI.

### "Performance regresses unexpectedly"
Load test reveals a contention point single-user testing missed. Profile, identify, fix. Tighten review for performance-impacting changes.

### "Coverage gap at validation time"
A requirement was missed during implementation. Add the test (and the implementation if needed); re-run. The coverage table in `tasks.md` is designed to prevent this — keep it populated.

### "Rollback drill fails"
The rollback procedure has a broken step. Fix the procedure; re-drill. Don't release until rollback works.

## Owner

The QA / test engineer role (see [`agents/archetypes/qa-agent.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agents/archetypes/qa-agent.md)). The cross-cutting `template-quality-reviewer` agent can run the documentation audit step.

## See also

- [[Workflow PRD to Production]] — Stage 10 in context
- [[Workflow Release Readiness]] — what happens after PASS
- [[Rules]] — security-rules.md and engineering-rules.md
