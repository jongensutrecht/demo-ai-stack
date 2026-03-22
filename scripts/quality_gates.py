#!/usr/bin/env python3
"""Run the primary repo quality gate."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

CHECKS = [
    ["python3", "scripts/validate_cto_rules_registry.py"],
    ["python3", "scripts/check_repo_contract.py"],
    ["python3", "scripts/check_repo_10x_contract.py"],
    ["python3", "scripts/check_search_hygiene.py"],
    ["python3", "scripts/check_file_limits.py"],
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    root = _repo_root()
    failures: list[str] = []
    print("== Demo AI Stack primary quality gate ==")
    for command in CHECKS:
        label = " ".join(command)
        print(f"RUN {label}")
        proc = subprocess.run(command, cwd=root, capture_output=True, text=True)
        if proc.stdout.strip():
            print(proc.stdout.strip())
        if proc.returncode != 0:
            failures.append(label)
            if proc.stderr.strip():
                print(proc.stderr.strip(), file=sys.stderr)
            print(f"FAIL {label}", file=sys.stderr)
        else:
            print(f"OK  {label}")

    if failures:
        print("FAILED checks:", file=sys.stderr)
        for label in failures:
            print(f"- {label}", file=sys.stderr)
        return 1

    print("OK: all quality gates passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
