# Workflow: Release Readiness

<!-- sources: workflows/release-readiness.md -->

Pre-release checklist + rollout playbook. Runs as **Stage 11** of [[Workflow PRD to Production]], after validation has passed.

For the canonical version, see [`workflows/release-readiness.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/workflows/release-readiness.md).

## Entry conditions

- Validation report has `Status: PASS` (see [[Workflow Testing and Validation]]).
- Staging environment runs the release candidate stably for the duration specified in the PRD.
- No active P0 / P1 incidents.

## Pre-release checklist

```
[ ] Validation report attached to the PRD
[ ] Staging environment stable for >= duration specified in PRD
[ ] Performance budgets met in staging load tests
[ ] Rollback procedure drilled and confirmed working
[ ] Feature flag wired and tested (on / off)
[ ] Observability dashboards updated
[ ] Alerts configured for the new feature's failure modes
[ ] Documentation merged (PRD Section 12)
[ ] Changelog / release notes drafted
[ ] On-call team briefed on the new surface
[ ] Customer comms drafted (if user-visible change)
[ ] Compliance / privacy sign-off (if required by feature scope)
[ ] No active P0/P1 incidents
[ ] Deployment owner identified
```

**Every box must be checked.** Skipping a box and adding "we'll handle it after deploy" is the failure mode this checklist exists to prevent.

## Rollout strategy

PRD Section 19 defines the strategy. Common shapes:

### Feature-flag gradual rollout (recommended default)

- **10%** of traffic for 24 hours; monitor.
- **50%** of traffic for 24 hours; monitor.
- **100%** of traffic; monitor for 7 days.

At each stage:
- Monitor: error rate, latency p95/p99, success metrics from PRD Section 3.3.
- Trigger rollback if any metric breaches the threshold in PRD Section 19.1.

### Canary deploy (when feature flag is impractical)
- Deploy to one region or one cluster first.
- Monitor.
- Promote to remaining regions.

### Big-bang (only for low-risk changes)
- Deploy everywhere at once.
- Only appropriate when blast radius is minimal and rollback is fast.

**For most features, gradual rollout is the default.** Big-bang requires explicit ADR.

## Per-stage gates

### Stage 11a: 10% rollout
- Traffic shift confirmed in load balancer / feature flag.
- Error rate within baseline + 0.1%.
- p95 latency within budget.
- Alerts not firing.
- Customer impact: zero P0/P1 reports related to the feature.

If all green for 24 hours, advance. Otherwise rollback.

### Stage 11b: 50% rollout
- Same metrics as 11a with higher floor.
- Cache hit rates stabilizing as expected.
- Database load within projected envelope.

If all green for 24 hours, advance. Otherwise rollback.

### Stage 11c: 100% rollout
- Full traffic.
- Monitor for 7 days.
- Compare success metrics (PRD Section 3.3) against targets.

If success metrics within target after 7 days, declare release complete. Otherwise: investigate gap, fix, re-validate.

## Rollback triggers (mechanical)

Per PRD Section 19.1:

- p95 latency > `<threshold>` sustained for 5 minutes.
- Error rate > `<threshold>` sustained for 5 minutes.
- Customer-reported correctness regression with reproduction.

**Triggers are mechanical.** The on-call engineer doesn't deliberate — if a trigger fires, rollback is the response.

## Rollback procedure

Per PRD Section 19.2:

1. Toggle feature flag to off (or revert deploy if no flag).
2. Verify error rates drop to baseline within 1 minute.
3. Open an incident ticket.
4. Investigate root cause.
5. Fix and re-validate before re-attempting rollout.

## Post-rollout (after 100% stable for 7 days)

- **Update PRD status** to `Shipped`. Move from `prds/active/` to `prds/archive/`.
- **Update spec triplet status** to `Complete`.
- **Capture lessons learned** in a brief retrospective. The `prd-author` agent can draft a starting outline.
- **Identify follow-ups**. Anything explicitly out of scope (PRD Section 4.2) that's now worth doing → new PRD.

## Communication

| Milestone | Notify |
|---|---|
| 10% rollout begins | Engineering team, product owner |
| 50% rollout begins | Engineering team |
| 100% rollout begins | Engineering team, product owner, support |
| 100% stable for 7 days | Engineering team, product owner, support, customers (if user-visible) |
| Rollback triggered | All of the above + on-call escalation |

Comms templates are project-specific. Drafting is part of release readiness; ad-hoc comms during incidents are noisy.

## Anti-patterns

- **Skipping the rollback drill.** Untested rollback is no rollback.
- **Big-bang for non-trivial changes.** Saves a day; costs a week if it goes wrong.
- **Skipping the 7-day soak at 100%.** Some failure modes only surface at steady-state full traffic.
- **Closing the PRD before metrics are validated.** Premature closure leaves the PRD claim ("time-to-find < 2s") unverified.
- **No on-call briefing.** On-call gets paged at 3am for a feature they've never seen.

## Owner

The deployment / SRE role (see [`agents/archetypes/devops-agent.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agents/archetypes/devops-agent.md)).

## See also

- [[Workflow PRD to Production]] — Stage 11 in context
- [[Workflow Testing and Validation]] — Stage 10 (the gate before)
