#!/usr/bin/env python3
"""BMAD proof gate: verify story commands and write final.json.

Inputs
- Story file: stories_claude/<process>/<story_id>.md (from BMAD_REPO_ROOT)
- Output: output/bmad/<process>/<run_id>/<story_id>/final.json

Environment
- BMAD_REPO_ROOT: repo/worktree root where story + code live
- BMAD_OUTPUT_ROOT: optional output root directory (defaults to <repo_root>/output)
- BMAD_VENV_PYTHON: optional venv python path; if set, we prepend its bin-dir to PATH
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Check:
    kind: str
    cwd: Path
    command: str
    expected: str


def _repo_root() -> Path:
    raw = os.environ.get("BMAD_REPO_ROOT", "").strip()
    return Path(raw).resolve() if raw else Path.cwd().resolve()


def _main_repo_root(repo_root: Path) -> Path:
    try:
        parts = list(repo_root.resolve().parts)
        if "worktrees_claude" in parts:
            idx = parts.index("worktrees_claude")
            if idx > 0:
                return Path(*parts[:idx]).resolve()
    except Exception:
        pass
    return repo_root


def _output_roots(repo_root: Path) -> list[Path]:
    raw = os.environ.get("BMAD_OUTPUT_ROOT", "").strip()
    main_root = _main_repo_root(repo_root)
    primary = Path(raw).resolve() if raw else (main_root / "output")
    secondary = main_root / "output"
    return [primary] if primary == secondary else [primary, secondary]


def _prepare_env(env: dict[str, str]) -> dict[str, str]:
    venv_python = os.environ.get("BMAD_VENV_PYTHON", "").strip()
    if not venv_python:
        return env
    py = Path(venv_python).resolve()
    updated = dict(env)
    updated["PATH"] = str(py.parent) + os.pathsep + env.get("PATH", "")
    updated["VIRTUAL_ENV"] = str(py.parent.parent)
    return updated


def _parse_checks(story_text: str, repo_root: Path) -> list[Check]:
    lines = story_text.splitlines()
    checks: list[Check] = []
    verify_repo_re = re.compile(r"Verification \(repo-root\):\s*`([^`]+)`")
    verify_cwd_re = re.compile(r"Verification \(cwd=([^\)]+)\):\s*`([^`]+)`")
    expected_re = re.compile(r"Expected:\s*`([^`]+)`")

    def find_expected(start: int) -> str:
        for idx in range(start, min(start + 6, len(lines))):
            match = expected_re.search(lines[idx])
            if match:
                return match.group(1)
        raise ValueError("Verification command without Expected value")

    for idx, line in enumerate(lines):
        match = verify_repo_re.search(line)
        if match:
            checks.append(Check("repo-root", repo_root, match.group(1).strip(), find_expected(idx + 1)))
            continue
        match = verify_cwd_re.search(line)
        if match:
            cwd = Path(match.group(1).strip())
            resolved = (repo_root / cwd).resolve() if not cwd.is_absolute() else cwd
            checks.append(Check("cwd", resolved, match.group(2).strip(), find_expected(idx + 1)))
    return checks


def _expected_matches(expected: str, stdout: str, exit_code: int) -> bool:
    normalized = expected.strip().lower()
    if normalized in {"exit 0", "code 0", "status 0", "returncode 0"}:
        return exit_code == 0
    return exit_code == 0 and expected in stdout


def _run_check(check: Check, timeout_s: int) -> dict[str, Any]:
    started = time.time()
    proc = subprocess.run(
        ["bash", "-lc", check.command],
        cwd=str(check.cwd),
        env=_prepare_env(os.environ.copy()),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_s,
    )
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    ok = _expected_matches(check.expected, stdout, proc.returncode)
    return {
        "kind": check.kind,
        "cwd": str(check.cwd),
        "command": check.command,
        "expected": check.expected,
        "ok": bool(ok),
        "exit_code": int(proc.returncode),
        "stdout": stdout,
        "stderr": stderr,
        "duration_ms": int((time.time() - started) * 1000),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--process", required=True)
    parser.add_argument("--story-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    story_path = repo_root / "stories_claude" / args.process / f"{args.story_id}.md"
    if not story_path.is_file():
        print(f"ERROR: story file not found: {story_path}", file=sys.stderr)
        return 2

    try:
        checks = _parse_checks(story_path.read_text(encoding="utf-8"), repo_root)
    except Exception as exc:
        print(f"ERROR: cannot parse checks: {exc}", file=sys.stderr)
        return 2
    if not checks:
        print("ERROR: no Verification(...) commands found", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    done = True
    for check in checks:
        try:
            result = _run_check(check, timeout_s=int(args.timeout))
        except subprocess.TimeoutExpired:
            result = {
                "kind": check.kind,
                "cwd": str(check.cwd),
                "command": check.command,
                "expected": check.expected,
                "ok": False,
                "exit_code": None,
                "stdout": "",
                "stderr": "timeout",
                "duration_ms": int(args.timeout) * 1000,
            }
        results.append(result)
        if not result.get("ok"):
            done = False

    payload = {
        "done": bool(done),
        "process": str(args.process),
        "run_id": str(args.run_id),
        "story_id": str(args.story_id),
        "checks": results,
    }
    for out_root in _output_roots(repo_root):
        proof_dir = out_root / "bmad" / args.process / args.run_id / args.story_id
        proof_dir.mkdir(parents=True, exist_ok=True)
        (proof_dir / "final.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0 if done else 2


if __name__ == "__main__":
    raise SystemExit(main())
