#!/usr/bin/env python3
"""Validate repo-10x contract links for LLM and human usability."""

from __future__ import annotations

from pathlib import Path

REQUIRED_REFERENCES: dict[str, list[str]] = {
    "README.md": [
        "docs/CTO_RULES.md",
        "docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md",
        "docs/START_HERE.md",
        "docs/SOURCES_OF_TRUTH.md",
        "scripts/quality_gates.py",
        "skills/",
    ],
    "docs/START_HERE.md": [
        "docs/CTO_RULES.md",
        "docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md",
        "docs/SOURCES_OF_TRUTH.md",
        "scripts/quality_gates.py",
    ],
    "docs/SOURCES_OF_TRUTH.md": [
        "docs/CTO_RULES.md",
        "docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md",
        "scripts/quality_gates.py",
        "skills/",
        "config/golden_queries.txt",
        ".ignore",
    ],
    "INSTALL.ps1": [
        "docs\\CTO_RULES.md",
        "docs\\UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md",
        "docs\\START_HERE.md",
        "docs\\SOURCES_OF_TRUTH.md",
        "scripts\\quality_gates.py",
        "config\\golden_queries.txt",
        ".ignore",
    ],
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    root = _repo_root()
    failures: list[str] = []
    for rel, refs in REQUIRED_REFERENCES.items():
        path = root / rel
        if not path.exists():
            failures.append(f"missing required file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for ref in refs:
            if ref not in text:
                failures.append(f"missing reference in {rel}: {ref}")

    if failures:
        print("ERROR: repo-10x contract failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OK: repo-10x contract valid")
    print(f"checked_docs={len(REQUIRED_REFERENCES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
