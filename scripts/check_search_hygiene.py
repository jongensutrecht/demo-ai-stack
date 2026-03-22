#!/usr/bin/env python3
"""Validate repo-wide search hygiene and golden queries."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

REQUIRED_IGNORE_PATTERNS = [
    ".worktrees/",
    "worktrees_claude/",
    "node_modules/",
    ".venv/",
    "venv/",
    "__pycache__/",
    "dist/",
    "build/",
    ".next/",
    "out/",
    "coverage/",
    ".pytest_cache/",
    "logs/",
    "*.log",
    "*.zip",
    "*.tar.gz",
    ".claude/skills/",
    "lars skills/",
]

BANNED_TOP_HIT_PREFIXES = [
    ".claude/skills/",
    "lars skills/",
    "logs/",
    "artifacts/",
    "output/",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_non_comment_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _top_hit(root: Path, query: str) -> str | None:
    try:
        proc = subprocess.run(
            ["rg", "-n", "--max-count", "1", query, "."],
            cwd=root,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:  # pragma: no cover - environment issue
        raise RuntimeError("rg (ripgrep) is required for search hygiene checks") from exc
    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr.strip() or f"rg failed for query: {query}")
    line = (proc.stdout or "").strip().splitlines()
    if not line:
        return None
    return line[0].split(":", 1)[0].removeprefix("./")


def main() -> int:
    root = _repo_root()
    ignore_path = root / ".ignore"
    queries_path = root / "config" / "golden_queries.txt"

    if not ignore_path.exists():
        print("ERROR: missing .ignore")
        return 1
    if not queries_path.exists():
        print("ERROR: missing config/golden_queries.txt")
        return 1

    ignore_lines = set(_load_non_comment_lines(ignore_path))
    missing_patterns = [pattern for pattern in REQUIRED_IGNORE_PATTERNS if pattern not in ignore_lines]
    if missing_patterns:
        print("ERROR: .ignore is missing required patterns:")
        for pattern in missing_patterns:
            print(f"- {pattern}")
        return 1

    queries = _load_non_comment_lines(queries_path)
    if not queries:
        print("ERROR: config/golden_queries.txt has no active queries")
        return 1

    failures: list[str] = []
    try:
        for query in queries:
            hit = _top_hit(root, query)
            if hit is None:
                failures.append(f"query has no hits: {query}")
                continue
            if any(hit.startswith(prefix) for prefix in BANNED_TOP_HIT_PREFIXES):
                failures.append(f"query top hit lands in excluded noise: {query} -> {hit}")
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 1

    if failures:
        print("ERROR: search hygiene failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OK: search hygiene valid")
    print(f"golden_queries={len(queries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
