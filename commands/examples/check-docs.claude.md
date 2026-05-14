---
description: Check markdown docs for common SpecRoute readiness issues and report findings.
---

# Check Docs

Run a read-only documentation health check for the current repository.

## What to check

1. Markdown files exist for the expected SpecRoute top-level directories.
2. Example files do not contain unresolved placeholder markers.
3. Root context files stay short and delegate deeper reference material to `agentic-docs/`.
4. Vendor matrix rows match across `README.md`, `AGENTS.md`, and `agentic-docs/agent-cli-integrations.md`.

## Suggested shell checks

```bash
rg -n "[T]ODO" examples prds/examples specs/examples agents/examples skills/examples commands/examples
rg -n "Vendor \\| Runtime dir \\| Root context file" README.md AGENTS.md agentic-docs/agent-cli-integrations.md
wc -l AGENTS.md CLAUDE.md GEMINI.md
```

Report findings in severity order. Do not edit files.
