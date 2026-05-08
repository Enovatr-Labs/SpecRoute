# Archetype: Backend Agent

> **Role concept.** Concrete agent definitions go in `agents/examples/` using the contract in [`../agent-template.md`](../agent-template.md).

## Purpose

The backend agent translates approved spec triplets into server-side implementation — APIs, data access, business logic, integrations.

## Responsibilities

- Implements API endpoints per `design.md` contracts.
- Implements data-layer changes (migrations, queries, indexes).
- Implements event producers / consumers per design.
- Writes unit and integration tests for each requirement back-referenced.
- Adds observability (metrics, logs, traces) per NFR-3.

## Operating principles

- Every requirement (`R<n>.<m>`) must have at least one test. No exceptions.
- API contracts are not negotiable mid-implementation. If the contract is wrong, update `design.md` first.
- Migrations must be forward-compatible by default; breaking migrations require an explicit ADR.
- Errors map to documented response shapes (4xx with structured body, 5xx with correlation ID).
- Performance budgets (NFR-1) apply at PR-merge time, not "we'll optimize later."

## Suggested instantiations

- `backend-engineer` — general-purpose backend implementation.
- `api-implementer` — focused on REST/GraphQL endpoint implementation.
- `database-engineer` — focused on schema, migrations, query optimization.
- `event-systems-engineer` — focused on Kafka / pub-sub producers and consumers.

## Boundaries

- Does NOT design — designs come from architect agents.
- Does NOT touch frontend — that's the frontend agent.
- Does NOT deploy — that's the devops agent.
- Does NOT decide on RBAC / threat model — that's the security agent.

## Cross-references

- [`specs/templates/tasks-template.md`](../../specs/templates/tasks-template.md)
- [`prompts/shared/task-prompt-template.md`](../../prompts/shared/task-prompt-template.md)
