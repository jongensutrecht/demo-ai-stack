#!/usr/bin/env python3
"""Validate repo-governance contract files and repo-root allowlist."""

from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_FILES = [
    "README.md",
    "SECURITY.md",
    ".ignore",
    "docs/CTO_RULES.md",
    "docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md",
    "docs/START_HERE.md",
    "docs/SOURCES_OF_TRUTH.md",
    "docs/FILE_LIMITS_EXCEPTIONS.md",
    "config/golden_queries.txt",
    "config/repo_root_allowlist.txt",
    "scripts/quality_gates.py",
    "scripts/check_file_limits.py",
    "scripts/check_search_hygiene.py",
    "scripts/check_repo_contract.py",
    "scripts/check_repo_10x_contract.py",
    "scripts/show_governance_status.py",
    "scripts/validate_cto_rules_registry.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_allowlist(path: Path) -> set[str]:
    entries: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        entries.add(line.rstrip("/"))
    return entries


def main() -> int:
    root = _repo_root()
    missing = [rel for rel in REQUIRED_FILES if not (root / rel).exists()]
    readme_text = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").exists() else ""
    if "## Licentie" in readme_text or "## License" in readme_text:
        if not (root / "LICENSE").exists():
            missing.append("LICENSE")
    if missing:
        print("ERROR: missing required files:")
        for rel in missing:
            print(f"- {rel}")
        return 1

    allowlist = _load_allowlist(root / "config" / "repo_root_allowlist.txt")
    actual = {
        path.name
        for path in root.iterdir()
        if path.name not in {".git"}
    }
    unexpected = sorted(name for name in actual if name not in allowlist)
    if unexpected:
        print("ERROR: unexpected repo-root entries:")
        for name in unexpected:
            print(f"- {name}")
        return 1

    print("OK: repo contract valid")
    print(f"checked_files={len(REQUIRED_FILES)}")
    print(f"allowed_top_level={len(allowlist)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
