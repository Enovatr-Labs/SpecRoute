# Security Policy

SpecRoute is markdown content - templates, prompts, agent definitions, runtime layouts - not a runtime application. The threat model is narrow but real, and we take it seriously.

## What's in scope

We treat the following as security issues:

- **Malicious shell in hook templates or runtime examples.** Hook scripts (`hooks/claude/*.sh`, `runtimes/.claude/hooks/*.sh`) and any other executable shipped in this repo run on contributor and consumer machines. A backdoor or command injection in these files affects every consumer who copies them.
- **Supply-chain risk in tooling.** Scripts under `tools/` (e.g. `sync-skills.py`, MCP renderers in `runtimes/mcp/render/`) execute on consumer machines. Vulnerabilities here - arbitrary file write, code execution from untrusted YAML, etc. - qualify.
- **Prompt-injection vectors in templates.** A template that, when filled in by a consumer with adversarial input, causes their agent CLI to leak credentials or execute unintended commands.
- **Sanitization or provenance bypass.** A change that lets private identifiers, secrets, or copied private-source material evade `.claude/hooks/pre-bash-sanitize.sh`, `/sanitize`, `tools/provenance-audit.py`, or `/audit`.
- **Insecure default configurations** in `runtimes/.<vendor>/` templates that consumers are likely to copy verbatim (e.g. an MCP server config exposing `filesystem` to `/` instead of the project root).

## What's out of scope

The following are not security issues we can address here:

- Vulnerabilities in the agent CLIs themselves (Claude Code, Codex, Gemini CLI, Kiro, Cursor, Devin Desktop). Report those upstream to the respective vendors.
- Vulnerabilities in MCP servers SpecRoute references but doesn't ship (e.g. `@modelcontextprotocol/server-filesystem`). Report upstream.
- Generic prompt-injection in third-party content a consumer feeds into their agent CLI.
- Security of consumer-extracted artifacts after they fork/copy templates - the responsibility shifts at extraction time.

## Reporting a vulnerability

Please report suspected vulnerabilities **privately** before opening a public issue:

- **Email:** `security@enovatr.com` (primary), `chika@enovatr.com` (fallback)
- **GitHub:** open a private security advisory at <repo>/security/advisories/new
- **Subject line:** `[SpecRoute SECURITY] <short description>`

Include:

- The affected file(s) and version (commit SHA or tag)
- Reproduction steps or proof-of-concept
- Impact assessment (who is affected, what's exploitable)
- Suggested fix, if you have one

Please do **not**:

- Open a public GitHub issue describing the vulnerability before we've had a chance to respond
- Disclose details on social media or public mailing lists during the embargo

## Response commitment

| Step | Target time |
|---|---|
| Acknowledge receipt | within 3 business days |
| Initial assessment | within 7 business days |
| Fix or mitigation released (for confirmed issues) | typically within 30 days; complex issues may take longer with coordination |
| Public disclosure | after fix is merged and consumers have had reasonable time to update |

For critical issues we will coordinate with you on disclosure timing.

## Recognition

We're happy to credit reporters in the security advisory and release notes unless you prefer to remain anonymous. SpecRoute does not currently offer a paid bug bounty.

## Hardening practices

When contributing hooks, scripts, or runtime templates, please:

- **Quote shell variables** (`"$var"`, not `$var`) - the existing hook scripts demonstrate the pattern.
- **Avoid eval / `bash -c "$user_input"`** - never interpolate untrusted input into shell strings.
- **Set `set -u`** in shell scripts to catch unset variables.
- **Use Python's `json.load`** (not `eval`) when parsing JSON in scripts.
- **Pin MCP server versions** in `runtimes/mcp/servers.yaml` examples - `@latest` invites supply-chain surprises.
- **Default to least privilege**: hooks should fail closed; example MCP `filesystem` configs should scope to the project, not `/`.
- **Do not treat `allowed-tools` as a sandbox.** In Claude Code it **pre-approves** tools for the invoking turn - the grant clears on the next message - rather than restricting what the model may reach for. The field that removes tools from the pool is `disallowed-tools`. Keeping `allowed-tools` tight still reduces unattended auto-approval, which is worth doing, but it is not a confinement boundary and must not be relied on as one. Real confinement comes from `permissions` in `settings.json`, `disallowed-tools`, and the sandbox your runtime provides.
- **Run the private-source provenance gate before a release.** Configure source roots and reviewed-hash decisions only in the gitignored `.claude/.provenance-*` files. Never paste private paths or excerpts into public findings, issues, or pull requests.

The `template-quality-reviewer` agent and the `/audit` command flag obvious violations.
