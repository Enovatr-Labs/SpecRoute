# `.codex/scripts/`

Project-internal scripts that Codex's runtime invokes. Common patterns:

- **Cross-runtime sync**: a thin wrapper around `tools/sync-skills.py` so Codex users can run sync without context-switching:

  ```bash
  #!/usr/bin/env bash
  exec python3 tools/sync-skills.py "$@"
  ```

- **Pre-execution validators**: scripts that Codex skills invoke before destructive operations.

- **Helper utilities** scoped to specific skills (those should usually live under the skill's own `scripts/` subdir, not here).

## Reference

The cross-runtime sync utility lives at [`../../../tools/sync-skills.py`](../../../tools/sync-skills.py). Wrap it with a Codex-friendly script if your team prefers calling it from `.codex/`.
