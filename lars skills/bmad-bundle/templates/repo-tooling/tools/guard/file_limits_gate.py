#!/usr/bin/env python3
"""Fail-closed file limits gate with explicit legacy baseline."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST_PATH = PROJECT_ROOT / "tools" / "guard" / "file_limits_allowlist.json"
SOURCE_SUFFIXES = {".js", ".ts", ".tsx", ".mjs", ".py"}
SKIP_SUFFIXES = {".d.ts"}
SKIP_EXACT = set()
SCAN_ROOTS = ("api", "lib", "web/src", "scripts", "tools", "server.mjs")
JS_PATTERNS = [
    re.compile(r"^\s*(?:export\s+)?(?:default\s+)?async\s+function\s+[A-Za-z_$][\w$]*\s*\("),
    re.compile(r"^\s*(?:export\s+)?(?:default\s+)?function\s+[A-Za-z_$][\w$]*\s*\("),
    re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+[A-Za-z_$][\w$]*\s*=\s*(?:async\s*)?\([^\n]*=>"),
    re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+[A-Za-z_$][\w$]*\s*=\s*(?:async\s*)?[A-Za-z_$][\w$]*\s*=>"),
    re.compile(r"^\s*(?:async\s+)?(?!if\b|for\b|while\b|switch\b|catch\b|constructor\b)[A-Za-z_$][\w$]*\s*\([^;=]*\)\s*\{"),
]
PY_PATTERN = re.compile(r"^\s*(?:async\s+)?def\s+[A-Za-z_][\w_]*\s*\(")


def _git_files(args: list[str]) -> list[str]:
    cp = subprocess.run(["git", "-C", str(PROJECT_ROOT), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        raise SystemExit(f"FILE_LIMITS_FAILED: {' '.join(args)}\n{cp.stderr.strip()}")
    return [line.strip() for line in (cp.stdout or "").splitlines() if line.strip()]


def _load_allowlist() -> dict:
    return json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))


def _is_test_file(rel: str) -> bool:
    return any(token in rel for token in ("/__tests__/", "/tests/", ".test.", ".spec."))


def _in_scope(rel: str) -> bool:
    if rel in SKIP_EXACT or any(rel.endswith(sfx) for sfx in SKIP_SUFFIXES):
        return False
    if _is_test_file(rel):
        return False
    return any(rel == root or rel.startswith(root + "/") for root in SCAN_ROOTS)


def _iter_source_files() -> list[Path]:
    tracked = _git_files(["ls-files", *SCAN_ROOTS])
    untracked = _git_files(["ls-files", "--others", "--exclude-standard", *SCAN_ROOTS])
    files = []
    for rel in sorted(set(tracked + untracked)):
        path = PROJECT_ROOT / rel
        if not path.is_file() or path.suffix not in SOURCE_SUFFIXES or not _in_scope(rel):
            continue
        files.append(path)
    return files


def _count_functions(path: Path, lines: list[str]) -> int:
    if path.suffix == ".py":
        return sum(1 for line in lines if PY_PATTERN.search(line))
    return sum(1 for line in lines if any(pattern.search(line) for pattern in JS_PATTERNS))


def main() -> int:
    cfg = _load_allowlist()
    max_lines = int(cfg["max_lines"])
    max_functions = int(cfg["max_functions"])
    legacy = cfg.get("legacy", {})
    failures: list[str] = []
    warnings: list[str] = []

    for path in _iter_source_files():
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        line_count = len(lines)
        function_count = _count_functions(path, lines)
        over_limit = line_count > max_lines or function_count > max_functions
        baseline = legacy.get(rel)

        if baseline is None:
            if over_limit:
                failures.append(
                    f"NEW_LIMIT_VIOLATION {rel} lines={line_count}/{max_lines} functions={function_count}/{max_functions}"
                )
            continue

        baseline_lines = int(baseline["max_lines"])
        baseline_functions = int(baseline["max_functions"])
        if line_count > baseline_lines or function_count > baseline_functions:
            failures.append(
                f"REGRESSION {rel} lines={line_count}>{baseline_lines} functions={function_count}>{baseline_functions}"
            )
        elif not over_limit:
            warnings.append(f"IMPROVED {rel} now within limits; remove from allowlist when convenient")

    if failures:
        print("FILE_LIMITS_FAILED")
        for failure in failures:
            print(f"- {failure}")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("FILE_LIMITS_OK")
    for warning in warnings:
        print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
