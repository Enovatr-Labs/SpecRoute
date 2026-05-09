# Workflow: Testing and Validation

How a SpecForge-driven feature is validated against its spec. Runs as Stage 10 of [`prd-to-production.md`](prd-to-production.md), after all task PRs have merged.

## Prerequisites

- All tasks in `tasks.md` are checked off.
- All PRs merged to the integration branch.
- Staging environment matches production schema and approximate scale.

## Validation steps

### Step 1: Coverage audit

For every requirement (`R<N.M>`) and NFR (`NFR-<N.M>`) in `requirements.md`:

- [ ] At least one test asserts the behavior.
- [ ] The test passes in CI.
- [ ] The test is referenced in the coverage table in `tasks.md`.

If a requirement has no test, that's a coverage gap. Either:

- Add the test before promoting to validation pass, or
- Document why the requirement can't be tested (e.g. it's an attestation rather than executable behavior) and have a human reviewer sign off.

### Step 2: Functional tests

Run the full test suite:

```bash
# Unit + integration
<your project's unit test runner>
<your project's integration test runner>
```

Pass criteria: 100% green. Flaky tests block; fix them or quarantine with a follow-up task.

### Step 3: End-to-end tests

Run E2E flows against staging:

- Each user story in `requirements.md` has an E2E test that exercises it from the UI.
- Empty states, error states, loading states all exercised.
- Cross-browser / cross-device matrix per the project's standards.

### Step 4: Performance tests

For each performance NFR (`NFR-1.x`):

- Run a load test with the profile specified in the design doc.
- Capture p50, p95, p99 latencies.
- Compare against the budget in the PRD's Section 18.

If any budget is exceeded, that's a blocker. Performance regressions are not "fix it next sprint" - they block release.

### Step 5: Security validation

Per [`rules/security-rules.md`](../rules/security-rules.md):

- Authentication required on every new endpoint.
- Authorization (RBAC) enforced; cross-tenant attempts blocked.
- Input validation rejects malformed requests with structured 400s.
- Audit logs emit per the design.
- Rate limits enforced.
- No new secrets in tracked files (run `/sanitize`).

For features with regulatory requirements (SOC 2, GDPR, HIPAA, PCI-DSS, SOX): confirm the controls map to the framework's required attestations.

### Step 6: Observability validation

For each observability NFR (`NFR-3.x`):

- The metric appears in the project's monitoring system.
- The log entry has the required fields.
- The trace span links to the parent span.

A feature without observability ships blind. Block release until observability is wired.

### Step 7: Rollback drill

Per the PRD's Section 19:

- Trigger the rollback procedure in staging.
- Verify the system returns to the pre-feature state.
- Verify error rates drop.
- Re-enable; verify recovery.

A rollback that's never been tested is not a rollback.

### Step 8: Documentation audit

Per the PRD's Section 12:

- API reference updated for any new or changed endpoints.
- User-facing docs updated for any user-visible changes.
- Internal docs (architecture, data-model) updated for any structural changes.
- Changelog or release notes drafted.

## Validation report

Output of validation is a report attached to the PRD's spec triplet:

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
- Unit: <pass count>/<total>
- Integration: <pass count>/<total>
- E2E: <pass count>/<total>

## Performance
- p95 latency: <observed> vs <budget>
- p99 latency: <observed> vs <budget>
- Other metrics: <list>

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

## Validation outcomes

- **PASS**: every step green; ready for rollout (Stage 11).
- **FAIL**: one or more steps red; back to implementation. The failing step's owner has the action.
- **CONDITIONAL**: green except for non-blocking items; rollout proceeds with the conditions logged.

## Common validation failures

### "Tests pass locally but fail in CI"

CI environment differs from local - usually a missing fixture, a real-time-dependent test, or an order-dependency. Fix the test, not the CI.

### "Performance regresses unexpectedly"

The load test reveals a contention point that single-user testing missed. Profile, identify, fix. The PR that introduced the regression should not have merged; tighten review for performance-impacting changes.

### "Coverage gap at validation time"

A requirement was missed during implementation. Add the test (and the implementation if needed), re-run validation. This is the failure mode the coverage table in `tasks.md` is designed to prevent - keep it populated.

### "Rollback drill fails"

The rollback procedure has a step that doesn't work. Fix the procedure, re-drill. Don't release until the rollback works.

## Authoring agent

Validation is owned by the QA / test engineer role (see [`agents/archetypes/qa-agent.md`](../agents/archetypes/qa-agent.md)). The cross-cutting `template-quality-reviewer` agent can run the documentation audit step.

## See also

- [`prd-to-production.md`](prd-to-production.md) - Stage 10 in context.
- [`release-readiness.md`](release-readiness.md) - what happens after PASS.
- [`rules/security-rules.md`](../rules/security-rules.md), [`rules/engineering-rules.md`](../rules/engineering-rules.md) - the standards the validation enforces.
