# `.gemini/commands/` - Gemini CLI custom commands

One TOML file per command. This replaces the obsolete `gemini_cli_config.json` command map (which mapped names to shell commands); current Gemini CLI commands are prompt templates.

```
.gemini/commands/
├── review-spec.toml          ->  /review-spec
└── git/
    └── commit.toml           ->  /git:commit
```

## TOML contract

| Field | Required | Notes |
|---|---|---|
| `prompt` | Yes | The instruction sent to the model. Single or multi-line (`"""..."""`). |
| `description` | No | One-line text shown in `/help`. Auto-generated if omitted. |

## Namespacing

The path under `.gemini/commands/` becomes the command name, with directory separators converted to colons. A file at `.gemini/commands/git/commit.toml` is invoked as `/git:commit`. Use subdirectories to group related commands.

## Arguments

`{{args}}` in the `prompt` is replaced with the user's text after the command name. Outside shell blocks it injects raw; inside `!{...}` shell blocks it is shell-escaped. Example: `/review-spec specs/auth/requirements.md` substitutes that path into `{{args}}`.

## Porting from `.claude/commands/`

A Claude command is markdown with frontmatter and a `$ARGUMENTS` token. To port: move the body into `prompt`, move the `description` frontmatter field to the top-level `description` key, and replace `$ARGUMENTS` with `{{args}}`.

`review-spec.toml` ships here as a worked reference. Replace or extend it with your project's commands.
