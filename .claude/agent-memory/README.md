# Agent Memory

Per-agent persistent context for the SpecRoute implementation team. Each subdirectory matches a `.claude/agents/<name>.md` agent and holds free-form markdown notes the agent should re-read at the start of each conversation.

## Layout

```
.claude/agent-memory/
├── README.md                       (this file)
├── <agent-name>/
│   └── <topic>.md                  free-form notes, descriptive filenames
```

## What goes in here

- **State that persists across conversations** but doesn't belong in the codebase: which decisions have been made, which TODOs the agent owns, where it left off.
- **Cross-agent coordination notes**: which agent has the lock on a shared file.
- **Pointers to authoritative external state**: the user-level memory directory at `~/.claude/projects/-Users-chika-LocalDev-SpecRoute/memory/`, which holds the canonical sanitization rules.

## What does NOT go in here

- Anything that would leak in a public repo. These files **are tracked** - they ship as part of SpecRoute. Treat them with the same sanitization bar as any other tracked file. Do not write upstream private project names, internal paths, or domain-specific business logic into these notes.
- Live secrets, tokens, credentials.
- Information that belongs in a real artifact (PRD, spec, doc) - write the artifact instead.
- Information that belongs in user-level memory (cross-project facts about the user) - those live in `~/.claude/projects/-Users-chika-LocalDev-SpecRoute/memory/` and stay out of git.

## Currently populated

- `sanitization-auditor/` - pointer to user-level memory; checklist
- `runtime-architect/` - supported vendor matrix progress
- `framework-docs-author/` - docs status

Other agents have memory dirs as needed; empty dirs are not pre-created.
