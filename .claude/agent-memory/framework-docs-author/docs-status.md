# Framework Docs Author - Docs Status

Tracks which documentation files exist, which are TODO, and which need refresh after structural changes.

## Document inventory

### Top-level context files

| File | Status | Notes |
|---|---|---|
| `README.md` | drafted | Vendor matrix, artifact taxonomy, getting-started, repo structure. Refresh when matrix changes. |
| `CLAUDE.md` | drafted | Short root context; delegates intent to `AGENTS.md` (when AGENTS.md ships). |
| `GEMINI.md` | TODO | Delegation shim → AGENTS.md. ~15–25 lines max. |
| `AGENTS.md` | TODO | Canonical vendor-neutral context file. Single source of truth root. |
| `CONTRIBUTING.md` | drafted | Contribution workflow + quality bar. |
| `CODE_OF_CONDUCT.md` | TODO | Standard Contributor Covenant 2.1. |
| `SECURITY.md` | TODO | Reporting channel + threat model (mostly: malicious shell in hook templates, supply-chain via tools/). |
| `ROADMAP.md` | TODO | 3-phase roadmap: skeleton → worked example + runtimes → community contributions. |

### `agentic-docs/` deep references

| File | Status | Priority |
|---|---|---|
| `philosophy.md` | TODO | medium - explains why spec-driven |
| `spec-driven-development.md` | TODO | medium - PRD → triplet → tasks flow |
| `agentic-coding-model.md` | TODO | medium - how artifacts compose |
| `automation-decision-framework.md` | TODO | **highest leverage** - Skill vs Agent vs Command vs Hook 4-row matrix |
| `documentation-structure.md` | TODO | low - where new docs go |
| `two-tier-docs-pattern.md` | TODO | low - short root + namespaced reference |
| `multi-vendor-context-files.md` | TODO | high - AGENTS.md + delegation shims |
| `agent-cli-integrations.md` | TODO | high - how to wire SpecRoute into each tool |
| `cross-vendor-sync.md` | TODO | medium - owned jointly with `runtime-architect` |
| `agent-memory.md` | TODO | low - per-agent persistent context |

### `workflows/`

| File | Status |
|---|---|
| `prd-to-production.md` | TODO |
| `spec-to-implementation.md` | TODO |
| `agent-review-loop.md` | TODO |
| `testing-and-validation.md` | TODO |
| `release-readiness.md` | TODO |

## Recommended drafting order

1. `automation-decision-framework.md` - most cross-referenced, others depend on it
2. `AGENTS.md` + `multi-vendor-context-files.md` together (mutually reinforcing)
3. `philosophy.md` + `spec-driven-development.md` + `agentic-coding-model.md` (concept trio)
4. `agent-cli-integrations.md` - concrete wiring per vendor
5. `workflows/prd-to-production.md` - exercises the full flow
6. Remaining workflows
7. Remaining `agentic-docs/` references

## Refresh triggers

- **Matrix change** (new vendor added or column added): refresh `README.md`, `agent-cli-integrations.md`, `multi-vendor-context-files.md` in lock-step.
- **New artifact type** (a new top-level dir under SpecRoute): refresh `agentic-coding-model.md`, `automation-decision-framework.md`, and the README's artifact taxonomy.
- **Frontmatter contract change** (new required field on agent/skill/command): refresh the corresponding template README and any docs that quote the contract.
