#!/usr/bin/env python3
"""Copy the standard BMAD bundle repo-tooling pack into a target repo/worktree."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_DIR / 'templates' / 'repo-tooling'
TEMPLATE_FILES = [
    'README.md',
    'scripts/bmad_bundle.py',
    'scripts/check_file_limits.py',
    'scripts/quality_gates.py',
    'tools/bmad/verify_story.py',
    'tools/bmad/ralph_verify_backlog.py',
    'tools/guard/file_limits_allowlist.json',
    'tools/guard/file_limits_gate.py',
    'tools/guard/gates.py',
    'tools/guard/quality_gates.json',
]


def _copy_one(repo_root: Path, rel: str, force: bool) -> str:
    src = TEMPLATE_ROOT / rel
    dst = repo_root / rel
    if not src.is_file():
        raise SystemExit(f'TEMPLATE_MISSING: {src}')
    if dst.exists() and not force:
        return f'SKIP {rel}'
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f'COPY {rel}'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('repo_root', help='Target repo/worktree root')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.is_dir():
        print(f'ERROR: repo root not found: {repo_root}', file=sys.stderr)
        return 2

    print(f'BOOTSTRAP_TARGET {repo_root}')
    copied = skipped = 0
    for rel in TEMPLATE_FILES:
        result = _copy_one(repo_root, rel, args.force)
        print(result)
        if result.startswith('COPY '):
            copied += 1
        else:
            skipped += 1

    print(f'BOOTSTRAP_OK copied={copied} skipped={skipped}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
