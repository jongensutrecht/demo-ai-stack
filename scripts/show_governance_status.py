#!/usr/bin/env python3
"""Show the canonical governance entrypoints for this repo."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _status(rel_path: str) -> str:
    root = _repo_root()
    path = root / rel_path
    return "present" if path.exists() else "missing"


def main() -> int:
    rows = [
        ("rules_registry", "docs/CTO_RULES.md"),
        ("audit_process", "docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md"),
        ("quickstart", "docs/START_HERE.md"),
        ("sources_of_truth", "docs/SOURCES_OF_TRUTH.md"),
        ("primary_gate", "scripts/quality_gates.py"),
        ("repo_10x_gate", "scripts/check_repo_10x_contract.py"),
        ("canonical_skills", "skills/"),
    ]
    for key, rel_path in rows:
        print(f"{key}: {rel_path} [{_status(rel_path)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
