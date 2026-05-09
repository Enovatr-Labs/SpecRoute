# Workflow: Release Readiness

Pre-release checklist. Runs as Stage 11 of [`prd-to-production.md`](prd-to-production.md), after validation has passed.

## Entry conditions

- Validation report has `Status: PASS` (see [`testing-and-validation.md`](testing-and-validation.md)).
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

Every box must be checked before rollout. Skipping a box and adding "we'll handle it after deploy" is the failure mode this checklist exists to prevent.

## Rollout strategy

The PRD's Section 19 defines the strategy. Common shapes:

### Feature-flag gradual rollout (recommended default)

- 10% of traffic for 24 hours; monitor.
- 50% of traffic for 24 hours; monitor.
- 100% of traffic; monitor for 7 days.

At each stage:

- Monitor: error rate, latency p95/p99, success metrics from PRD Section 3.3.
- Trigger rollback if any metric breaches the threshold in PRD Section 19.1.

### Canary deploy (when feature flag is impractical)

- Deploy to one region or one cluster first.
- Monitor.
- Promote to remaining regions.

### Big-bang (only for low-risk changes)

- Deploy everywhere at once.
- Only appropriate when the feature has minimal blast radius and a fast rollback.

For most features in SpecForge-driven projects, **gradual rollout is the default**. Big-bang requires explicit ADR.

## Per-stage gates

### Stage 11a: 10% rollout

- Traffic shift confirmed in load balancer / feature flag.
- Error rate within baseline + 0.1%.
- p95 latency within budget.
- Alerts not firing.
- Customer impact: zero P0/P1 reports related to the feature.

If all green for 24 hours, advance. Otherwise rollback.

### Stage 11b: 50% rollout

- Same metrics as 11a, with a higher traffic floor.
- Cache hit rates stabilizing as expected.
- Database load increase within projected envelope.

If all green for 24 hours, advance. Otherwise rollback.

### Stage 11c: 100% rollout

- Full traffic.
- Monitor for 7 days.
- Compare success metrics (PRD Section 3.3) against targets.

If success metrics within target after 7 days, declare release complete. Otherwise: investigate gap, fix, re-validate.

## Rollback triggers

Per the PRD's Section 19.1:

- p95 latency > <threshold> sustained for 5 minutes.
- Error rate > <threshold> sustained for 5 minutes.
- Customer-reported correctness regression with reproduction.

Triggers are mechanical. The on-call engineer doesn't deliberate - if a trigger fires, rollback is the response.

## Rollback procedure

Per the PRD's Section 19.2:

1. Toggle feature flag to off (or revert deploy if no flag).
2. Verify error rates drop to baseline within 1 minute.
3. Open an incident ticket.
4. Investigate root cause.
5. Fix and re-validate before re-attempting rollout.

## Post-rollout

After 100% rollout is stable for 7 days:

- **Update PRD status** to `Shipped`. Move from `prds/active/` to `prds/archive/`.
- **Update spec triplet status** to `Complete`.
- **Capture lessons learned** in a brief retrospective. The `prd-author` agent can draft a starting outline based on the PRD, the spec triplet's open questions, and the validation report.
- **Identify follow-ups**. Anything explicitly out of scope (PRD Section 4.2) that's now worth doing → new PRD.
- **Archive the worked example** if the feature was used as a SpecForge demo.

## Communication

Stakeholders to notify at each milestone:

| Milestone | Notify |
|---|---|
| 10% rollout begins | Engineering team, product owner |
| 50% rollout begins | Engineering team |
| 100% rollout begins | Engineering team, product owner, support |
| 100% stable for 7 days | Engineering team, product owner, support, customers (if user-visible) |
| Rollback triggered | All of the above + on-call escalation |

Comms templates are project-specific. Drafting is part of release readiness; ad-hoc comms during incidents are noisy.

## Anti-patterns

- **Skipping the rollback drill.** Untested rollback is no rollback. The first time you exercise it should not be during an incident.
- **Big-bang for non-trivial changes.** Saves a day; costs a week if it goes wrong.
- **Skipping the 7-day soak at 100%.** Some failure modes only surface under steady-state full traffic.
- **Closing the PRD before metrics are validated.** Premature closure leaves the PRD claim ("time-to-find < 2s") unverified.
- **No on-call briefing.** On-call gets paged at 3am for a feature they've never seen. Brief before launch.

## Authoring agent

Release readiness is owned by the deployment / SRE role (see [`agents/archetypes/devops-agent.md`](../agents/archetypes/devops-agent.md)).

## See also

- [`prd-to-production.md`](prd-to-production.md) - Stage 11 in context.
- [`testing-and-validation.md`](testing-and-validation.md) - Stage 10 (the gate before this stage).
