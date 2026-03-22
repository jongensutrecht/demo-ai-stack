#!/usr/bin/env python3
"""Validate non-test file limits using simple per-language counting rules."""

from __future__ import annotations

import ast
import fnmatch
import json
import re
import subprocess
from pathlib import Path

MAX_LINES = 300
MAX_FUNCTIONS = 15
EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".claude",
    "lars skills",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    "out",
    "coverage",
    ".pytest_cache",
    "logs",
    "artifacts",
    "output",
    "test-results",
}
EXCLUDED_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".tar", ".gz", ".pdf"}
JSON_BLOCK_RE = re.compile(r"```json\n(.*?)\n```", re.DOTALL)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_ls_files(root: Path) -> list[Path]:
    output = subprocess.check_output(["git", "ls-files"], cwd=root, text=True)
    return [root / line for line in output.splitlines() if line.strip()]


def _is_test(path: Path) -> bool:
    rel = path.as_posix()
    return (
        rel.startswith("tests/")
        or "/tests/" in rel
        or rel.endswith("_test.py")
        or rel.endswith(".test.ts")
        or rel.endswith(".spec.ts")
        or rel.endswith("Test.php")
    )


def _is_excluded(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return True
    return path.suffix.lower() in EXCLUDED_SUFFIXES


def _load_exceptions(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    match = JSON_BLOCK_RE.search(text)
    if not match:
        raise SystemExit("ERROR: docs/FILE_LIMITS_EXCEPTIONS.md is missing a fenced JSON block")
    data = json.loads(match.group(1))
    if not isinstance(data, list):
        raise SystemExit("ERROR: file-limit exceptions JSON must be a list")
    return data


def _is_exception(rel: str, exceptions: list[dict]) -> bool:
    for item in exceptions:
        pattern = item.get("path")
        if not isinstance(pattern, str) or not pattern.strip():
            continue
        if fnmatch.fnmatch(rel, pattern):
            return True
    return False


def _count_python_functions(text: str, rel: str) -> int:
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise SystemExit(f"ERROR: cannot parse Python file for function count: {rel}: {exc}")
    return sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))


def _count_shell_functions(text: str) -> int:
    count = 0
    for line in text.splitlines():
        if re.match(r"^\s*function\s+[A-Za-z_][A-Za-z0-9_-]*\b", line):
            count += 1
        elif re.match(r"^\s*[A-Za-z_][A-Za-z0-9_-]*\s*\(\)\s*\{", line):
            count += 1
    return count


def _count_powershell_functions(text: str) -> int:
    return sum(
        1
        for line in text.splitlines()
        if re.match(r"^\s*function\s+[A-Za-z_][A-Za-z0-9_-]*\b", line, re.IGNORECASE)
    )


def _function_count(path: Path, text: str, rel: str) -> int:
    if path.suffix == ".py":
        return _count_python_functions(text, rel)
    if path.suffix == ".sh":
        return _count_shell_functions(text)
    if path.suffix == ".ps1":
        return _count_powershell_functions(text)
    return 0


def main() -> int:
    root = _repo_root()
    exceptions = _load_exceptions(root / "docs" / "FILE_LIMITS_EXCEPTIONS.md")
    offenders: list[tuple[str, int, int]] = []

    for path in _git_ls_files(root):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if _is_test(path.relative_to(root)) or _is_excluded(path, root) or _is_exception(rel, exceptions):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        line_count = len(text.splitlines())
        func_count = _function_count(path, text, rel)
        if line_count > MAX_LINES or func_count > MAX_FUNCTIONS:
            offenders.append((rel, line_count, func_count))

    if offenders:
        print("ERROR: file-limit offenders:")
        for rel, lines, funcs in offenders:
            print(f"- {rel}: lines={lines}, functions={funcs}")
        return 1

    print("OK: file limits valid")
    print(f"max_lines={MAX_LINES}")
    print(f"max_functions={MAX_FUNCTIONS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
