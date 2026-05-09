# Security Rules

Cross-cutting security standards. Apply to all code in any project that adopts SpecForge.

See also [`SECURITY.md`](../SECURITY.md) for the framework's own security policy and threat model.

## 1. Default to fail-closed

When a control could fail open or fail closed, choose fail closed. Permission denied beats permission granted by default. Auth required beats auth implied. Access logged beats access untracked.

## 2. Never hardcode secrets

- API keys, tokens, passwords, OAuth client secrets, certificates: environment variables or a secret manager only.
- `.env` files are gitignored. Don't commit them.
- Don't paste secrets into Slack, GitHub issues, or chat with agents.
- If a secret leaks (was committed, even briefly), rotate it. Don't revert and hope.

## 3. Validate all external input

Every system boundary validates:

- HTTP request bodies (JSON schema, length limits, type checks).
- File uploads (size, type, content sniffing where applicable).
- URL parameters (whitelisting allowed values).
- Webhook payloads (signature verification before parsing).

Don't trust internal callers either when the data has crossed a network boundary.

## 4. Output encoding by default

- HTML output: HTML-escape unless explicitly outputting trusted markup.
- SQL: parameterized queries, never string-concatenated.
- Shell: never interpolate untrusted input into shell strings.
- HTTP redirects: validate the target against an allow-list.

## 5. Authentication and authorization are separate concerns

- **Authentication** verifies *who* the request is from.
- **Authorization** verifies *what* they can do.

Every endpoint declares both posture explicitly. "It's authenticated implicitly" is not a posture.

## 6. Audit logs for sensitive actions

Logged actions include:

- Authentication events (login, logout, failed login).
- Authorization changes (role grants, role revokes).
- Sensitive resource access (PII, financial data, admin operations).
- Data exports.

Logs include actor, target, action, timestamp, correlation ID. Logs do not include passwords, tokens, or PII bodies.

## 7. Threat model first

For any non-trivial feature:

- Who's the attacker?
- What are they after?
- What boundary do they cross?
- What's the blast radius if a control fails?

Document in the PRD's security section or a linked threat-model doc. Don't skip - design without a threat model is an attack surface.

## 8. Least privilege

- Service accounts with minimum permissions for their job.
- API tokens scoped to specific operations.
- Database users with column-level access where supported.
- Container processes running as non-root.
- File system permissions tight enough that misconfiguration is loud.

## 9. Dependencies are an attack surface

- Pin dependency versions in lockfiles.
- Scan for known CVEs in CI (Dependabot, Snyk, equivalent).
- Review new dependencies before merging - what license, what supply-chain posture, what blast radius.
- Avoid `@latest` in production configs.

## 10. Sanitization before commit

For any project using SpecForge:

- Maintain `.claude/.forbidden-strings.txt` (gitignored) with private project names, internal identifiers, etc.
- Run `/sanitize` before committing.
- The PreToolUse hook (`pre-bash-sanitize.sh`) blocks `git commit` / `git push` if forbidden strings appear in tracked files. Treat that as a hard stop.

## 11. Secrets handling for SpecForge artifacts

- `.gitignore` excludes per-user settings and the wordlist.
- Templates contain placeholders, not real values.
- Examples use generic, non-domain-specific data.

## 12. Hooks and scripts are reviewed as carefully as production code

Hook scripts under `runtimes/.<vendor>/hooks/` and `runtimes/.<vendor>/scripts/` ship to every consumer who copies the runtime. Malicious shell in a hook is a supply-chain compromise.

For hook scripts:

- Quote shell variables: `"$var"`, never `$var`.
- Avoid `eval` and unquoted command interpolation.
- Use `set -u` to catch unset variables.
- Use `python3` (not `eval`) for JSON parsing.

See [`SECURITY.md`](../SECURITY.md) Hardening practices.

## 13. MCP servers are dependencies too

- Pin MCP server package versions in `runtimes/mcp/servers.yaml` examples - `@latest` invites supply-chain surprises.
- Scope filesystem MCP servers to the project root, not `/`.
- Document `requires_env` for any server that needs credentials; never inline.

## 14. Compliance is engineering, not paperwork

If your domain has regulatory requirements (SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, SOX), the requirements live in code:

- Audit logs for required actions.
- Encryption at rest and in transit.
- Data retention and deletion mechanisms.
- Privacy controls (consent, export, deletion).

Don't treat compliance as a separate workstream that catches up at audit time.

## See also

- [`SECURITY.md`](../SECURITY.md) - framework-level security policy.
- [`engineering-rules.md`](engineering-rules.md) - broader engineering standards.
- [`code-review-rules.md`](code-review-rules.md) - review checklist that includes security.
