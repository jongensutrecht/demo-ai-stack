#!/usr/bin/env python3
"""Fail if BACKLOG marks DONE without proof."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _repo_root() -> Path:
    raw = os.environ.get("BMAD_REPO_ROOT", "").strip()
    return Path(raw).resolve() if raw else Path.cwd().resolve()


def _primary_repo_root(repo_root: Path) -> Path:
    try:
        parts = list(repo_root.resolve().parts)
        if "worktrees_claude" in parts:
            idx = parts.index("worktrees_claude")
            if idx > 0:
                return Path(*parts[:idx]).resolve()
    except Exception:
        pass
    return repo_root.resolve()


def _proof_roots(repo_root: Path, process: str) -> list[Path]:
    primary = _primary_repo_root(repo_root)
    candidates = [
        repo_root / "output",
        primary / "output",
        primary / "worktrees_claude" / "merge" / process / "main-merge" / "output",
    ]
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in candidates:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        ordered.append(path)
    return ordered


def _done_story_ids(backlog_text: str) -> list[str]:
    done: list[str] = []
    for line in backlog_text.splitlines():
        if not line.strip().startswith("|"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 2 or parts[0].lower() == "story" or parts[0].startswith("---"):
            continue
        if "[DONE]" in parts[1]:
            done.append(parts[0])
    return done


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--process", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    backlog = repo_root / "stories_claude" / args.process / "BACKLOG.md"
    if not backlog.is_file():
        print(f"ERROR: BACKLOG.md not found: {backlog}", file=sys.stderr)
        return 2

    missing: list[str] = []
    invalid: list[str] = []
    for story_id in _done_story_ids(backlog.read_text(encoding="utf-8")):
        proof = None
        for root in _proof_roots(repo_root, args.process):
            candidate = root / "bmad" / args.process / args.run_id / story_id / "final.json"
            if candidate.is_file():
                proof = candidate
                break
        if proof is None:
            missing.append(story_id)
            continue
        try:
            payload = json.loads(proof.read_text(encoding="utf-8"))
        except Exception:
            invalid.append(story_id)
            continue
        if payload.get("done") is not True:
            invalid.append(story_id)

    if missing or invalid:
        if missing:
            print("ERROR: DONE stories missing proof:", file=sys.stderr)
            for story_id in missing:
                print(f"- {story_id}", file=sys.stderr)
        if invalid:
            print("ERROR: DONE stories with invalid proof:", file=sys.stderr)
            for story_id in invalid:
                print(f"- {story_id}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
