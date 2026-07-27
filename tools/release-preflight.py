#!/usr/bin/env python3
"""Run SpecRoute's public, read-only release gates and extract release notes.

This tool intentionally has no access to the gitignored private provenance
inputs used by release maintainers. The GitHub Actions release workflow records
only the audited public commit SHA and an explicit maintainer acknowledgement.

Usage:
    python3 tools/release-preflight.py \
      --version 0.4.0 \
      --release-sha "$(git rev-parse HEAD)"

    python3 tools/release-preflight.py \
      --version 0.4.0 \
      --release-sha "$(git rev-parse HEAD)" \
      --notes-output /tmp/specroute-release-notes.md

Exit codes:
    0 - every public release gate passed
    1 - one or more release gates failed
    2 - invalid command-line input
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
FENCE_RE = re.compile(r"(?ms)^```.*?^```")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
MARKDOWN_LINK_RE = re.compile(r"\]\(([^)]+)\)")
VENDOR_ROW_RE = re.compile(r"^\|[^|]+\|[^|]*`\.[a-z]+/`")

MATRIX_MIRRORS = (
    "README.md",
    "AGENTS.md",
    "wiki/Vendor-Matrix.md",
    "agentic-docs/agent-cli-integrations.md",
)
LOCAL_ONLY_EXACT_PATHS = {
    ".claude/.forbidden-strings.txt",
    ".claude/.provenance-sources.txt",
    ".claude/.provenance-allowlist.txt",
    ".claude/settings.local.json",
    "GITHUB-SETUP.md",
    "initial.md",
}
PLACEHOLDER_MARKERS = (
    "<user>",
    "<name>",
    "<repo>",
    "<private>",
    "<flattened-project-path>",
    "yourname",
    "youruser",
    "replace_with",
    "placeholder",
    "changeme",
    "example_",
    "example-",
    "example.com",
)


class GateFailure(RuntimeError):
    """A release gate failed with a user-facing explanation."""


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise GateFailure(f"git {' '.join(args)} failed: {message}")
    return result.stdout.strip()


def repository_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise GateFailure("git ls-files failed while collecting public repository files")

    files: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8", errors="surrogateescape")
        candidate = REPO_ROOT / relative
        if candidate.is_file():
            files.append(candidate)
    return files


def read(relative: str) -> str:
    path = REPO_ROOT / relative
    if not path.is_file():
        raise GateFailure(f"required release file is missing: {relative}")
    return path.read_text(encoding="utf-8")


def require_match(pattern: str, text: str, label: str, flags: int = 0) -> re.Match[str]:
    match = re.search(pattern, text, flags)
    if match is None:
        raise GateFailure(f"{label} is missing or does not match the release")
    return match


def extract_release_notes(changelog: str, version: str) -> tuple[str, str]:
    heading = re.compile(
        rf"^## \[{re.escape(version)}\] - (\d{{4}}-\d{{2}}-\d{{2}})\s*$",
        re.MULTILINE,
    )
    match = heading.search(changelog)
    if match is None:
        raise GateFailure(
            f"CHANGELOG.md has no exact release heading for [{version}] with a release date"
        )

    start = match.end()
    separator = re.search(r"^---\s*$", changelog[start:], re.MULTILINE)
    next_release = re.search(r"^## \[", changelog[start:], re.MULTILINE)
    ends = [
        candidate.start()
        for candidate in (separator, next_release)
        if candidate is not None
    ]
    end = start + min(ends) if ends else len(changelog)
    notes = changelog[start:end].strip()
    if not notes or notes.startswith("(Changes accumulating"):
        raise GateFailure(f"CHANGELOG.md release notes for {version} are empty")
    return match.group(1), notes + "\n"


def check_release_metadata(version: str) -> str:
    changelog = read("CHANGELOG.md")
    release_date, notes = extract_release_notes(changelog, version)

    release_headers = re.findall(
        r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\] - \d{4}-\d{2}-\d{2}\s*$",
        changelog,
        re.MULTILINE,
    )
    if not release_headers or release_headers[0] != version:
        raise GateFailure(
            f"CHANGELOG.md latest release is {release_headers[0] if release_headers else 'missing'}, "
            f"expected {version}"
        )

    require_match(
        rf"^\[Unreleased\]: https://github\.com/Enovatr-Labs/SpecRoute/compare/"
        rf"v{re.escape(version)}\.\.\.HEAD$",
        changelog,
        "CHANGELOG.md Unreleased comparison link",
        re.MULTILINE,
    )
    require_match(
        rf"^\[{re.escape(version)}\]: https://github\.com/Enovatr-Labs/SpecRoute/"
        rf"releases/tag/v{re.escape(version)}$",
        changelog,
        "CHANGELOG.md release link",
        re.MULTILINE,
    )
    citation = read("CITATION.cff")
    require_match(
        rf'^version:\s*"{re.escape(version)}"\s*$',
        citation,
        "CITATION.cff version",
        re.MULTILINE,
    )
    require_match(
        rf"^date-released:\s*{re.escape(release_date)}\s*$",
        citation,
        "CITATION.cff release date",
        re.MULTILINE,
    )

    readme = read("README.md")
    require_match(
        rf"^\s*version\s*=\s*\{{{re.escape(version)}\}},\s*$",
        readme,
        "README.md BibTeX version",
        re.MULTILINE,
    )
    require_match(
        rf"\(Version {re.escape(version)}\)",
        readme,
        "README.md plain-text citation version",
    )

    release_anchor_files = {
        "ROADMAP.md": (
            rf"\*\*Current version:\*\*\s*v{re.escape(version)} "
            rf"\(released {re.escape(release_date)}\)",
            "ROADMAP.md current version",
        ),
        "wiki/Roadmap.md": (
            rf"\*\*Current version\*\*:\s*v{re.escape(version)} "
            rf"\(released {re.escape(release_date)}\)",
            "wiki/Roadmap.md current version",
        ),
        "wiki/Home.md": (
            rf"\*\*Current version\*\*:\s*v{re.escape(version)} "
            rf"\(released {re.escape(release_date)}\)",
            "wiki/Home.md current version",
        ),
    }
    for relative, (pattern, label) in release_anchor_files.items():
        require_match(pattern, read(relative), label)

    print(f"  OK release metadata: v{version} ({release_date})")
    return notes


def run_gate(label: str, command: list[str]) -> None:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    if result.returncode != 0:
        detail = f"\n{output}" if output else ""
        raise GateFailure(f"{label} failed with exit code {result.returncode}{detail}")
    print(f"  OK {label}")
    if output:
        for line in output.splitlines():
            print(f"    {line}")


def frontmatter_keys(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return set()
    end = text.find("\n---\n", 4)
    if end == -1:
        return set()
    keys: set[str] = set()
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):", line)
        if match:
            keys.add(match.group(1))
    return keys


def matching_files(patterns: tuple[str, ...]) -> list[Path]:
    found: set[Path] = set()
    for pattern in patterns:
        for value in glob.glob(str(REPO_ROOT / pattern)):
            path = Path(value)
            if path.is_file() and path.name != "README.md":
                found.add(path)
    return sorted(found)


def check_frontmatter() -> None:
    failures: list[str] = []

    markdown_contracts = (
        (
            (
                ".claude/agents/*.md",
                "agents/agent-template.md",
                "agents/examples/*.md",
                "runtimes/.claude/agents/*.md",
                "runtimes/.gemini/agents/*.md",
                "runtimes/.kiro/agents/*.md",
                "runtimes/.cursor/agents/*.md",
                "runtimes/.devin/agents/*/AGENT.md",
            ),
            {"name", "description"},
            "agent",
        ),
        (
            (
                ".claude/skills/*/SKILL.md",
                ".agents/skills/*/SKILL.md",
                "skills/skill-template/SKILL.md",
                "skills/examples/*/SKILL.md",
                "runtimes/.claude/skills/*/SKILL.md",
                "runtimes/.codex/skills/*/SKILL.md",
                "runtimes/.gemini/skills/*/SKILL.md",
                "runtimes/.kiro/skills/*/SKILL.md",
                "runtimes/.cursor/skills/*/SKILL.md",
                "runtimes/.devin/skills/*/SKILL.md",
            ),
            {"name", "description"},
            "skill",
        ),
        (
            (
                "commands/command-template.claude.md",
                "commands/examples/*.claude.md",
                "runtimes/.claude/commands/*.md",
                ".claude/commands/*.md",
            ),
            {"description"},
            "command",
        ),
    )

    for patterns, required, kind in markdown_contracts:
        for path in matching_files(patterns):
            keys = frontmatter_keys(path)
            missing = sorted(required - keys)
            if missing:
                relative = path.relative_to(REPO_ROOT)
                failures.append(f"{relative}: {kind} frontmatter missing {', '.join(missing)}")

            text = path.read_text(encoding="utf-8")
            model = re.search(r"^model:\s*(\S+)\s*$", text, re.MULTILINE)
            if model and model.group(1) in {"flagship", "balanced", "fast"}:
                failures.append(
                    f"{path.relative_to(REPO_ROOT)}: model uses tier name {model.group(1)!r}"
                )

    for path in matching_files(("runtimes/.codex/agents/*.toml",)):
        text = path.read_text(encoding="utf-8")
        for key in ("name", "description", "developer_instructions"):
            if not re.search(rf"^{key}\s*=", text, re.MULTILINE):
                failures.append(f"{path.relative_to(REPO_ROOT)}: Codex agent missing {key}")

    if failures:
        raise GateFailure("frontmatter validation failed:\n  " + "\n  ".join(failures))
    print("  OK frontmatter contracts")


def extract_matrix(text: str) -> str:
    buffer: list[str] = []
    hit = False
    for line in text.splitlines():
        if line.startswith("|"):
            buffer.append(line)
            hit = hit or bool(VENDOR_ROW_RE.match(line))
            continue
        if hit:
            return "\n".join(buffer) + "\n"
        buffer = []
        hit = False
    if hit:
        return "\n".join(buffer) + "\n"
    raise GateFailure("vendor matrix block not found")


def check_vendor_matrix() -> None:
    blocks: dict[str, str] = {}
    for relative in MATRIX_MIRRORS:
        try:
            blocks[relative] = extract_matrix(read(relative))
        except GateFailure as exc:
            raise GateFailure(f"{relative}: {exc}") from exc

    reference_name = MATRIX_MIRRORS[0]
    reference = blocks[reference_name]
    drifted = [name for name, block in blocks.items() if block != reference]
    if drifted:
        raise GateFailure(
            "vendor matrix differs from README.md in: " + ", ".join(drifted)
        )
    print("  OK four-way vendor matrix parity")


def check_local_links(files: list[Path]) -> None:
    failures: list[str] = []
    for path in files:
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        text = FENCE_RE.sub("", text)
        text = INLINE_CODE_RE.sub("", text)
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1).split("#", 1)[0].strip().strip("<>")
            if (
                not target
                or target.startswith(("http://", "https://", "mailto:"))
                or "<" in target
                or target in {"path", "TODO"}
            ):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                failures.append(f"{path.relative_to(REPO_ROOT)}: {target}")
    if failures:
        raise GateFailure("broken local Markdown links:\n  " + "\n  ".join(failures))
    print("  OK local Markdown links")


def check_publication_hygiene(files: list[Path]) -> None:
    tracked = set(git("ls-files").splitlines())
    tracked_local_only = sorted(
        path
        for path in tracked
        if (
            path in LOCAL_ONLY_EXACT_PATHS
            or path.startswith(".claude/.provenance-report.")
            or (
                (
                    path.rsplit("/", 1)[-1] == ".env"
                    or path.rsplit("/", 1)[-1].startswith(".env.")
                )
                and path.rsplit("/", 1)[-1] != ".env.example"
            )
        )
    )
    failures = [f"{path}: local-only release input is tracked" for path in tracked_local_only]

    # Construct path patterns so this detector does not match its own source.
    mac_home = "Users"
    linux_home = "home"
    absolute_home_re = re.compile(
        rf"/(?:{mac_home}|{linux_home})/([A-Za-z0-9._-]+)/"
    )
    windows_home_re = re.compile(
        rf"[A-Za-z]:\\{mac_home}\\([A-Za-z0-9._-]+)\\"
    )
    flattened_home_re = re.compile(
        rf"-(?:{mac_home}|{linux_home})-([A-Za-z0-9._-]+)-"
    )
    placeholder_users = {"user", "username", "name", "you", "yourname", "youruser"}

    private_key_re = re.compile(
        "-" * 5 + r"BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY" + "-" * 5
    )
    credential_url_re = re.compile(
        r"https?://[A-Za-z0-9._~-]+:[A-Za-z0-9._~+/=-]{8,}@"
    )
    secret_patterns = (
        ("private-key material", private_key_re),
        ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
        ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
        ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
        ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
        ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
        ("credential-bearing URL", credential_url_re),
        (
            "literal credential assignment",
            re.compile(
                r"""(?ix)
                \b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)
                \s*[:=]\s*["']?[A-Za-z0-9+/_.=-]{20,}
                """
            ),
        ),
    )

    for path in files:
        try:
            if path.stat().st_size > 2_000_000:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        relative = path.relative_to(REPO_ROOT)
        for line_number, line in enumerate(text.splitlines(), 1):
            for match in absolute_home_re.finditer(line):
                if match.group(1).casefold() in placeholder_users:
                    continue
                failures.append(
                    f"{relative}:{line_number}: concrete absolute home-directory path"
                )
            for match in windows_home_re.finditer(line):
                if match.group(1).casefold() in placeholder_users:
                    continue
                failures.append(
                    f"{relative}:{line_number}: concrete absolute home-directory path"
                )
            for match in flattened_home_re.finditer(line):
                if match.group(1).casefold() in placeholder_users:
                    continue
                failures.append(
                    f"{relative}:{line_number}: concrete flattened home-directory path"
                )

            for label, pattern in secret_patterns:
                for match in pattern.finditer(line):
                    matched = match.group(0).casefold()
                    if any(marker in matched for marker in PLACEHOLDER_MARKERS):
                        continue
                    failures.append(f"{relative}:{line_number}: possible {label}")

    if failures:
        raise GateFailure(
            "public publication hygiene failed (matched values are intentionally hidden):\n  "
            + "\n  ".join(sorted(set(failures)))
        )
    print("  OK public publication hygiene")


def check_json(files: list[Path]) -> None:
    failures: list[str] = []
    checked = 0
    for path in files:
        if path.suffix != ".json":
            continue
        checked += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            failures.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
    if failures:
        raise GateFailure("invalid JSON:\n  " + "\n  ".join(failures))
    print(f"  OK JSON validity ({checked} files)")


def check_python_compile(files: list[Path]) -> None:
    failures: list[str] = []
    checked = 0
    with tempfile.TemporaryDirectory(prefix="specroute-pycompile-") as tmp:
        output_dir = Path(tmp)
        for path in files:
            if path.suffix != ".py":
                continue
            checked += 1
            relative = path.relative_to(REPO_ROOT)
            target = output_dir / (str(relative).replace(os.sep, "_") + "c")
            try:
                py_compile.compile(str(path), cfile=str(target), doraise=True)
            except py_compile.PyCompileError as exc:
                failures.append(f"{relative}: {exc.msg}")
    if failures:
        raise GateFailure("Python compilation failed:\n  " + "\n  ".join(failures))
    print(f"  OK Python compilation ({checked} files)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--version",
        required=True,
        help="stable release version without a v prefix (for example, 0.4.0)",
    )
    parser.add_argument(
        "--release-sha",
        required=True,
        help="exact 40-character commit SHA expected at HEAD",
    )
    parser.add_argument(
        "--notes-output",
        type=Path,
        help="optional path to receive release notes extracted from CHANGELOG.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if SEMVER_RE.fullmatch(args.version) is None:
        print(
            "error: --version must be a stable MAJOR.MINOR.PATCH value without a v prefix",
            file=sys.stderr,
        )
        return 2
    if SHA_RE.fullmatch(args.release_sha) is None:
        print("error: --release-sha must be exactly 40 lowercase hex characters", file=sys.stderr)
        return 2

    try:
        head = git("rev-parse", "HEAD")
        if head != args.release_sha:
            raise GateFailure(f"HEAD is {head}, expected {args.release_sha}")

        print("Release preflight")
        print(f"  OK exact commit: {head}")
        notes = check_release_metadata(args.version)
        files = repository_files()
        check_publication_hygiene(files)

        run_gate(
            "wiki parity (warnings are release-blocking)",
            [sys.executable, "tools/wiki-parity.py"],
        )
        run_gate(
            "cross-runtime skill parity",
            [sys.executable, "tools/sync-skills.py", "--dry-run"],
        )
        run_gate(
            "Claude hook/settings parity",
            ["bash", "tools/sync-hooks-to-settings.sh", "--check"],
        )

        check_frontmatter()
        check_vendor_matrix()
        check_local_links(files)
        check_json(files)
        check_python_compile(files)

        if args.notes_output is not None:
            args.notes_output.parent.mkdir(parents=True, exist_ok=True)
            args.notes_output.write_text(notes, encoding="utf-8")
            print(f"  OK release notes written to {args.notes_output}")

        print("Release preflight: PASS")
        return 0
    except GateFailure as exc:
        print(f"Release preflight: FAIL\n  {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
