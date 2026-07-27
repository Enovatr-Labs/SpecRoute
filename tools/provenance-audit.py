#!/usr/bin/env python3
"""Detect private-source leakage without printing private source material.

The audit compares a public target repository with one or more private source
repositories supplied at runtime. Private paths, identifiers, and source excerpts
are never written to the report. Findings identify only the public target path,
line, match class, and a content hash suitable for a local allowlist.

Examples:
    python3 tools/provenance-audit.py \
      --source-list .claude/.provenance-sources.txt \
      --terms-file .claude/.forbidden-strings.txt \
      --history

    python3 tools/provenance-audit.py --source /path/to/private/repo

Exit codes:
    0 - no unallowlisted findings
    1 - findings detected
    2 - invalid configuration or an audit could not complete
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import zlib
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path


TEXT_SUFFIXES = {
    ".css",
    ".go",
    ".html",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".kts",
    ".md",
    ".py",
    ".rb",
    ".rs",
    ".scss",
    ".sh",
    ".sql",
    ".swift",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
SKIP_PARTS = {
    ".git",
    ".gradle",
    ".next",
    ".swiftpm",
    ".venv",
    "DerivedData",
    "Pods",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "venv",
}
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*|\d+")
CODE_BLOCK_RE = re.compile(r"(?ms)^```[^\n]*\n(.*?)^```")
PARAGRAPH_RE = re.compile(r"(?ms)(?:^|\n\s*\n)([^\n].*?)(?=\n\s*\n|\Z)")


@dataclass(frozen=True)
class Fragment:
    kind: str
    line: int
    normalized: str


@dataclass(frozen=True)
class TargetDocument:
    label: str
    content: str


def run_git(repo: Path, *args: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return result.stdout


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).casefold()


def tokens(text: str) -> list[str]:
    return [token.casefold() for token in TOKEN_RE.findall(text)]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fragments(text: str) -> Iterator[Fragment]:
    for line_number, line in enumerate(text.splitlines(), 1):
        normalized = normalize(line)
        if len(normalized) >= 120:
            yield Fragment("line", line_number, normalized)

    for match in PARAGRAPH_RE.finditer(text):
        normalized = normalize(match.group(1))
        if len(normalized) >= 240:
            line_number = text.count("\n", 0, match.start(1)) + 1
            yield Fragment("paragraph", line_number, normalized)

    for match in CODE_BLOCK_RE.finditer(text):
        normalized = normalize(match.group(1))
        if len(normalized) >= 160:
            line_number = text.count("\n", 0, match.start(1)) + 1
            yield Fragment("code", line_number, normalized)


def current_repo_documents(repo: Path) -> Iterator[tuple[str, str]]:
    raw = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"],
        cwd=repo,
        capture_output=True,
        check=False,
    )
    if raw.returncode != 0:
        raise RuntimeError("git ls-files failed")

    for item in raw.stdout.split(b"\0"):
        if not item:
            continue
        rel = item.decode("utf-8", errors="surrogateescape")
        path = repo / rel
        if path.suffix.casefold() not in TEXT_SUFFIXES or any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            if path.stat().st_size > 2_000_000:
                continue
            yield rel, path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeError):
            continue


def historical_repo_documents(repo: Path) -> Iterator[tuple[str, str]]:
    objects = run_git(repo, "rev-list", "--objects", "--all")
    seen: set[str] = set()
    candidates: list[tuple[str, str]] = []
    for row in objects.splitlines():
        oid, _, rel = row.partition(" ")
        if not rel or oid in seen:
            continue
        seen.add(oid)
        rel_path = Path(rel)
        if (
            rel_path.suffix.casefold() not in TEXT_SUFFIXES
            or any(part in SKIP_PARTS for part in rel_path.parts)
        ):
            continue
        candidates.append((oid, rel))

    # Keep one cat-file process open for the entire history. Spawning `git
    # cat-file` twice per blob makes a release audit take tens of minutes on a
    # mature private source repository; the batch protocol streams the same
    # objects with constant memory and one process.
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if process.stdin is None or process.stdout is None:
        process.kill()
        raise RuntimeError("could not start Git object reader")
    try:
        for oid, rel in candidates:
            process.stdin.write(oid.encode("ascii") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii", errors="replace").strip()
            parts = header.split()
            if len(parts) != 3:
                continue
            _, object_type, size_text = parts
            try:
                size = int(size_text)
            except ValueError:
                continue
            content_bytes = process.stdout.read(size)
            process.stdout.read(1)  # batch protocol's trailing newline
            if object_type != "blob" or size > 2_000_000:
                continue
            yield (
                f"history:{oid[:12]}:{rel}",
                content_bytes.decode("utf-8", errors="ignore"),
            )
    finally:
        process.stdin.close()
        process.stdout.close()
        process.wait()


def load_lines(path: Path | None) -> list[str]:
    if path is None or not path.is_file():
        return []
    values: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = raw.strip()
        if value and not value.startswith("#"):
            values.append(value)
    return values


def resolve_sources(args: argparse.Namespace) -> list[Path]:
    raw_sources = list(args.source)
    raw_sources.extend(load_lines(args.source_list))
    resolved: list[Path] = []
    for raw in raw_sources:
        path = Path(raw).expanduser().resolve()
        if not (path / ".git").exists():
            raise ValueError("every private source must be a Git repository")
        if path not in resolved:
            resolved.append(path)
    if not resolved:
        raise ValueError("provide --source or --source-list")
    return resolved


def init_database(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        CREATE TABLE exact_fragments (
            hash TEXT PRIMARY KEY
        );
        CREATE TABLE source_blocks (
            id INTEGER PRIMARY KEY,
            shingle_count INTEGER NOT NULL,
            shingles BLOB NOT NULL
        );
        CREATE TABLE source_minhashes (
            shingle TEXT NOT NULL,
            block_id INTEGER NOT NULL
        );
        CREATE INDEX source_minhashes_hash ON source_minhashes(shingle);
        CREATE TABLE long_runs (
            hash TEXT PRIMARY KEY
        );
        """
    )


def shingle_hashes(block_tokens: list[str], width: int) -> list[str]:
    if len(block_tokens) < width:
        return []
    return [
        digest("\x1f".join(block_tokens[index : index + width]))
        for index in range(len(block_tokens) - width + 1)
    ]


def pack_shingles(values: list[str]) -> bytes:
    return zlib.compress("\n".join(values).encode("ascii"), level=1)


def unpack_shingles(value: bytes) -> set[str]:
    return set(zlib.decompress(value).decode("ascii").splitlines())


def index_sources(
    connection: sqlite3.Connection,
    sources: Iterable[Path],
    include_history: bool,
) -> tuple[int, int]:
    document_count = 0
    fragment_count = 0
    for source in sources:
        iterators: list[Iterable[tuple[str, str]]] = [current_repo_documents(source)]
        if include_history:
            iterators.append(historical_repo_documents(source))
        for documents in iterators:
            for _, content in documents:
                document_count += 1
                for fragment in fragments(content):
                    fragment_count += 1
                    connection.execute(
                        "INSERT OR IGNORE INTO exact_fragments(hash) VALUES (?)",
                        (digest(fragment.normalized),),
                    )
                    if fragment.kind not in {"paragraph", "code"}:
                        continue
                    block_tokens = tokens(fragment.normalized)
                    # Near-copy indexing is intended for human-scale prose and
                    # code blocks. Minified/generated blobs can contain hundreds
                    # of thousands of tokens and add no useful provenance signal.
                    if not 100 <= len(block_tokens) <= 2_000:
                        continue
                    short = sorted(set(shingle_hashes(block_tokens, 12)))
                    if short:
                        cursor = connection.execute(
                            "INSERT INTO source_blocks(shingle_count, shingles) VALUES (?, ?)",
                            (len(short), pack_shingles(short)),
                        )
                        block_id = int(cursor.lastrowid)
                        connection.executemany(
                            "INSERT INTO source_minhashes(shingle, block_id) VALUES (?, ?)",
                            ((value, block_id) for value in short[:32]),
                        )
                    connection.executemany(
                        "INSERT OR IGNORE INTO long_runs(hash) VALUES (?)",
                        ((value,) for value in shingle_hashes(block_tokens, 40)),
                    )
                if document_count % 250 == 0:
                    connection.commit()
    connection.commit()
    return document_count, fragment_count


def near_match(
    connection: sqlite3.Connection,
    block_tokens: list[str],
    threshold: float,
) -> tuple[bool, bool]:
    target_shingles = sorted(set(shingle_hashes(block_tokens, 12)))
    if len(block_tokens) < 100 or not target_shingles:
        return False, False

    long_hashes = sorted(set(shingle_hashes(block_tokens, 40)))
    for offset in range(0, len(long_hashes), 500):
        chunk = long_hashes[offset : offset + 500]
        placeholders = ",".join("?" for _ in chunk)
        if connection.execute(
            f"SELECT 1 FROM long_runs WHERE hash IN ({placeholders}) LIMIT 1",
            chunk,
        ).fetchone():
            return False, True

    # Bottom-k minhashing narrows the search to likely candidates. For the
    # configured 0.85 Jaccard threshold, two blocks are overwhelmingly likely
    # to share at least one of their 32 smallest cryptographic shingle hashes.
    # Candidate similarity is then computed exactly from a compressed shingle
    # set, so minhash approximation can never create a false finding.
    sample = target_shingles[:32]
    placeholders = ",".join("?" for _ in sample)
    candidate_ids = {
        int(row[0])
        for row in connection.execute(
            "SELECT DISTINCT block_id FROM source_minhashes "
            f"WHERE shingle IN ({placeholders})",
            sample,
        )
    }
    target_set = set(target_shingles)
    for block_id in candidate_ids:
        row = connection.execute(
            "SELECT shingles FROM source_blocks WHERE id = ?",
            (block_id,),
        ).fetchone()
        if row is None:
            continue
        source_set = unpack_shingles(row[0])
        shared = len(target_set & source_set)
        union = len(target_set | source_set)
        if union and shared / union >= threshold:
            return True, False
    return False, False


def target_documents(repo: Path, include_history: bool) -> Iterator[TargetDocument]:
    for label, content in current_repo_documents(repo):
        yield TargetDocument(label, content)
    if include_history:
        for label, content in historical_repo_documents(repo):
            yield TargetDocument(label, content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--source", action="append", default=[], help="private Git repository")
    parser.add_argument("--source-list", type=Path, help="gitignored file with one source path per line")
    parser.add_argument("--terms-file", type=Path, help="gitignored forbidden identifier list")
    parser.add_argument("--allowlist", type=Path, help="gitignored file containing finding hash prefixes")
    parser.add_argument("--history", action="store_true", help="include reachable Git history")
    parser.add_argument("--near-threshold", type=float, default=0.85)
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if not (target / ".git").exists():
        print("error: target is not a Git repository", file=sys.stderr)
        return 2
    try:
        sources = resolve_sources(args)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    allowlist = set(load_lines(args.allowlist))
    forbidden_terms = [value.casefold() for value in load_lines(args.terms_file)]
    findings: list[tuple[str, int, str, str]] = []
    scanned_documents = 0
    scanned_fragments = 0

    with tempfile.TemporaryDirectory(prefix="specroute-provenance-") as temp_dir:
        database_path = Path(temp_dir) / "index.sqlite3"
        connection = sqlite3.connect(database_path)
        init_database(connection)
        source_documents, source_fragments = index_sources(connection, sources, args.history)

        for document in target_documents(target, args.history):
            scanned_documents += 1
            folded_content = document.content.casefold()
            for term in forbidden_terms:
                if term and term in folded_content:
                    finding_hash = digest(f"term:{document.label}:{term}")
                    if not any(finding_hash.startswith(prefix) for prefix in allowlist):
                        findings.append((document.label, 1, "private-identifier", finding_hash))

            for fragment in fragments(document.content):
                scanned_fragments += 1
                finding_hash = digest(fragment.normalized)
                if any(finding_hash.startswith(prefix) for prefix in allowlist):
                    continue
                if connection.execute(
                    "SELECT 1 FROM exact_fragments WHERE hash = ?",
                    (finding_hash,),
                ).fetchone():
                    findings.append((document.label, fragment.line, f"exact-{fragment.kind}", finding_hash))
                    continue
                if fragment.kind in {"paragraph", "code"}:
                    jaccard, long_run = near_match(
                        connection,
                        tokens(fragment.normalized),
                        args.near_threshold,
                    )
                    if jaccard:
                        findings.append(
                            (document.label, fragment.line, "near-copy-jaccard", finding_hash)
                        )
                    elif long_run:
                        findings.append(
                            (document.label, fragment.line, "near-copy-40-token-run", finding_hash)
                        )
        connection.close()

    unique_findings = sorted(set(findings))
    print("Private provenance audit")
    print(f"  private sources: {len(sources)} configured")
    print(f"  source documents indexed: {source_documents}")
    print(f"  source fragments indexed: {source_fragments}")
    print(f"  public documents scanned: {scanned_documents}")
    print(f"  public fragments scanned: {scanned_fragments}")
    print(f"  findings: {len(unique_findings)}")
    for label, line, kind, finding_hash in unique_findings:
        print(f"  FAIL {label}:{line} [{kind}] hash={finding_hash[:16]}")
    if unique_findings:
        print("Review each finding locally; never paste private source excerpts into a public report.")
        return 1
    print("  PASS: no unallowlisted private-source overlap detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
