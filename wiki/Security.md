# Security

<!-- sources: SECURITY.md -->

SpecForge is markdown content — templates, prompts, agent definitions, runtime layouts — not a runtime application. The threat model is narrow but real.

Full policy: [SECURITY.md](https://github.com/Enovatr-Labs/SpecForge/blob/main/SECURITY.md).

## In scope

We treat the following as security issues:

- **Malicious shell in hook templates or runtime examples.** Hook scripts (`hooks/claude/*.sh`, `runtimes/.claude/hooks/*.sh`) and any executable shipped here run on contributor and consumer machines. A backdoor or command injection affects every consumer who copies them.
- **Supply-chain risk in tooling.** Scripts under `tools/` (`sync-skills.py`, MCP renderers in `runtimes/mcp/render/`) execute on consumer machines. Vulnerabilities here — arbitrary file write, code execution from untrusted YAML — qualify.
- **Prompt-injection vectors in templates.** A template that, when filled in with adversarial input, causes the consumer's agent CLI to leak credentials or execute unintended commands.
- **Sanitization bypass.** A change that lets private upstream terms or secrets evade `.claude/hooks/pre-bash-sanitize.sh`, `/sanitize`, or `/audit`. See [[Sanitization]].
- **Insecure default configurations** in `runtimes/.<vendor>/` templates that consumers are likely to copy verbatim (e.g. an MCP server config exposing `filesystem` to `/` instead of the project root).

## Out of scope

- Vulnerabilities in the agent CLIs themselves (Claude Code, Codex, Gemini CLI, Kiro, Cursor, Windsurf). Report upstream.
- Vulnerabilities in MCP servers SpecForge references but doesn't ship. Report upstream.
- Generic prompt-injection in third-party content a consumer feeds into their agent CLI.
- Security of consumer-extracted artifacts after they fork/copy templates — the responsibility shifts at extraction time.

## Reporting

Report suspected vulnerabilities **privately** before opening a public issue:

- **Email**: `security@enovatr.com` (primary), `chika@enovatr.com` (fallback).
- **GitHub**: open a [private security advisory](https://github.com/Enovatr-Labs/SpecForge/security/advisories/new).
- **Subject line**: `[SpecForge SECURITY] <short description>`.

Include:
- Affected file(s) and version (commit SHA or tag).
- Reproduction steps or PoC.
- Impact assessment.
- Suggested fix, if you have one.

**Do not** open a public GitHub issue describing the vulnerability before we've responded, or disclose details on social media during the embargo.

## Response commitment

| Step | Target time |
|---|---|
| Acknowledge receipt | within 3 business days |
| Initial assessment | within 7 business days |
| Fix or mitigation released (for confirmed issues) | typically within 30 days |
| Public disclosure | after fix is merged and consumers have had time to update |

For critical issues we coordinate with you on disclosure timing.

## Hardening practices for contributors

When contributing hooks, scripts, or runtime templates:

- **Quote shell variables** — `"$var"`, not `$var`.
- **Avoid `eval` / `bash -c "$user_input"`** — never interpolate untrusted input into shell strings.
- **Set `set -u`** in shell scripts to catch unset variables.
- **Use Python's `json.load`** (not `eval`) when parsing JSON.
- **Pin MCP server versions** in `runtimes/mcp/servers.yaml` — `@latest` invites supply-chain surprises.
- **Default to least privilege** — skill `allowed-tools` should be the minimum set; hooks should fail closed; example MCP `filesystem` configs should scope to the project, not `/`.

The `template-quality-reviewer` agent and the `/audit` command flag obvious violations. See [[Hooks]] for the full hardening checklist.

## Recognition

We're happy to credit reporters in the security advisory and release notes unless you prefer to remain anonymous. SpecForge does not currently offer a paid bug bounty.

## See also

- [[Sanitization]] — the narrower content-leak threat model
- [[Hooks]] — script hardening practices
- [[MCP Integration]] — secure defaults for MCP server configs
