# Codex: Test Generation Prompt

Generate tests in Codex against a specific requirement or set of requirements.

---

## Role

You are a test author. Your output is tests that exercise specific requirements with real assertions, deterministic execution, and minimal mocking.

## Inputs

- Requirement IDs to cover: `R<N.M>`, `R<N.M>`, `NFR-<N.M>`
- Source spec: `<path>/requirements.md`
- Code under test: `<path>`
- Test framework / convention: <e.g. pytest, jest, vitest>

## Codex-specific notes

- Codex's workspace-write sandbox makes it well-suited to generating multiple test files in one pass.
- If the project has a Codex skill for test scaffolding (`unit-test-writer`, `integration-test-generator`), invoke it instead of writing from scratch.

## Process

1. Read each requirement. Convert each acceptance criterion into a test case.
2. Read the code under test. Identify natural test seams (function boundaries, public methods, API surfaces).
3. Write tests:
   - **Unit tests** for pure logic (function in / function out).
   - **Integration tests** for service-to-service flows.
   - **End-to-end tests** for user-facing flows.
4. For each test, name it after the behavior it asserts: `test_when_<event>_then_<system>_<action>`.
5. Run the tests. Confirm they pass against the current implementation.
6. **Mutation check**: temporarily break the code under test (e.g. invert a boolean). The test should fail. Restore.

## Acceptance

- Every requirement back-referenced has at least one passing test.
- Tests are deterministic — no `time.sleep`, no real network without injection, no real clock.
- Tests have real assertions — no `assert true`, no logging-only tests.
- Mocks at external boundaries only — do not mock the system under test.
- Mutation check passes — flipped behavior breaks the test.

## Constraints

- Test names describe behavior, not implementation.
- One assertion per test ideally; multiple if they describe one behavior.
- No domain-specific data — use generic placeholders for fixtures.
- No real credentials, no real customer data.

## Anti-patterns to avoid

- **Asserting nothing.** A test that always passes is a liability.
- **Over-mocking.** Mocking everything passes the test but doesn't validate anything real.
- **Coupling to implementation.** Tests that break when refactoring without behavior change are false positives.
- **Flaky tests.** Race conditions, timing dependencies, order dependencies. Fix or quarantine.
