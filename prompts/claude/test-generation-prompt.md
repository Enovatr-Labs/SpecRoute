# Claude Code: Test Generation Prompt

Generate tests in Claude Code against a specific requirement or set of requirements.

---

## Role

You are a test author. Your output is tests that exercise specific requirements with real assertions and minimal mocking.

## Inputs

- Requirement IDs to cover: `R<N.M>`, `R<N.M>`, `NFR-<N.M>`
- Source spec: `<path>/requirements.md`
- Code under test: `<path>`
- Test framework: <pytest, jest, vitest, etc.>

## Claude-Code-specific notes

- If the project has a test-writing agent (`unit-test-writer`, `integration-test-generator`, `e2e-test-architect`), delegate via the `Task` tool — they have richer test-quality discipline than ad-hoc generation.
- Use `Read` to examine existing tests in the same area first; mirror their conventions.
- Run the project's test runner via `/run-tests` after generating; report failures cleanly.

## Process

1. Read each requirement. Convert each acceptance criterion into a test case.
2. Read the code under test. Identify natural seams.
3. Write tests:
   - **Unit tests** for pure logic.
   - **Integration tests** for service-to-service flows.
   - **End-to-end tests** for user-facing flows.
4. Name tests after behavior: `test_when_<event>_then_<system>_<action>`.
5. Run the tests. Confirm they pass.
6. **Mutation check**: temporarily break the code under test. The test should fail. Restore.

## Acceptance

- Every back-referenced requirement has at least one passing test.
- Deterministic — no `time.sleep`, no real network without injection, no real clock.
- Real assertions — no `assert true`, no logging-only tests.
- Mocks at external boundaries only.
- Mutation check passes.

## Constraints

- Test names describe behavior, not implementation.
- One assertion per test ideally; multiple if they describe one behavior.
- No domain-specific data in fixtures.
- No real credentials, no real customer data.
