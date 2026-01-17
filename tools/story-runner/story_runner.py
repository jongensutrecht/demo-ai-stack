"""Minimal story runner for BMAD process/stories.

Reads a `docs/processes/<process>/PROCESS.md` and the corresponding story files
under `stories/<process>/`. Extracts per-AC verification commands and runs them
sequentially.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PROCESS_STORY_RE = re.compile(r"^\s*\d+\.\s+([A-Z]{2,5}\.\d{3})\s+-\s+")
AC_RE = re.compile(r"^\s*-\s+\*\*(AC\d+)\*\*:")
VERIFICATION_RE = re.compile(r"^\s*-\s+\*\*Verification.*?\*\*:\s+`(.+?)`\s*$")
EXPECTED_RE = re.compile(r"^\s*-\s+\*\*Expected:\*\*\s+(.*)$")


@dataclass(frozen=True)
class AcceptanceCriterion:
    story_id: str
    ac_id: str
    command: str
    expected: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_process(process_path: Path) -> list[str]:
    text = _read_text(process_path)
    story_ids: list[str] = []
    for line in text.splitlines():
        match = PROCESS_STORY_RE.match(line)
        if match:
            story_ids.append(match.group(1))
    if not story_ids:
        raise ValueError(f"No stories found in process file: {process_path}")
    return story_ids


def parse_story_verifications(story_path: Path, story_id: str) -> list[AcceptanceCriterion]:
    lines = _read_text(story_path).splitlines()
    acs: list[AcceptanceCriterion] = []

    current_ac: str | None = None
    current_cmd: str | None = None
    current_expected: str | None = None

    def flush() -> None:
        nonlocal current_ac, current_cmd, current_expected
        if current_ac is None:
            return
        if current_cmd is None or current_expected is None:
            raise ValueError(
                f"Incomplete AC in {story_path}: {current_ac} needs Verification + Expected"
            )
        acs.append(
            AcceptanceCriterion(
                story_id=story_id,
                ac_id=current_ac,
                command=current_cmd,
                expected=current_expected.strip(),
            )
        )
        current_ac = None
        current_cmd = None
        current_expected = None

    for line in lines:
        ac_match = AC_RE.match(line)
        if ac_match:
            flush()
            current_ac = ac_match.group(1)
            continue

        ver_match = VERIFICATION_RE.match(line)
        if ver_match and current_ac is not None:
            current_cmd = ver_match.group(1)
            continue

        exp_match = EXPECTED_RE.match(line)
        if exp_match and current_ac is not None:
            current_expected = exp_match.group(1)
            continue

    flush()
    if not acs:
        raise ValueError(f"No AC verifications found in story: {story_path}")
    return acs


def _powershell_command(cmd: str) -> list[str]:
    return ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd]


def run_command(command: str, cwd: Path) -> int:
    if os.name == "nt":
        proc = subprocess.run(_powershell_command(command), cwd=cwd)
    else:
        proc = subprocess.run(command, cwd=cwd, shell=True)
    return int(proc.returncode)


def show(process_path: Path) -> int:
    repo = _repo_root()
    story_ids = parse_process(process_path)
    print(f"repo={repo}")
    print(f"process={process_path}")
    for idx, story_id in enumerate(story_ids, start=1):
        story_path = repo / "stories" / process_path.parent.name / f"{story_id}.md"
        print(f"{idx}. {story_id} -> {story_path}")
    return 0


def verify(process_path: Path, fail_fast: bool) -> int:
    repo = _repo_root()
    process_name = process_path.parent.name
    story_ids = parse_process(process_path)

    all_acs: list[AcceptanceCriterion] = []
    for story_id in story_ids:
        story_path = repo / "stories" / process_name / f"{story_id}.md"
        all_acs.extend(parse_story_verifications(story_path=story_path, story_id=story_id))

    failures: list[str] = []
    for ac in all_acs:
        label = f"{ac.story_id} {ac.ac_id}"
        print(f"RUN {label}: {ac.command}")
        code = run_command(ac.command, cwd=repo)
        if code != 0:
            failures.append(f"{label} failed (exit={code}) expected={ac.expected}")
            print(f"FAIL {label}: exit={code} expected={ac.expected}", file=sys.stderr)
            if fail_fast:
                return 1
        else:
            print(f"OK  {label}")

    if failures:
        print("FAILED ACs:", file=sys.stderr)
        for fail in failures:
            print(f"- {fail}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="story_runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_show = sub.add_parser("show", help="Show canonical story order and paths")
    p_show.add_argument("--process", required=True, type=Path)

    p_verify = sub.add_parser("verify", help="Run all AC verification commands sequentially")
    p_verify.add_argument("--process", required=True, type=Path)
    p_verify.add_argument("--no-fail-fast", action="store_true")

    args = parser.parse_args(argv)
    if args.cmd == "show":
        return show(process_path=args.process)
    if args.cmd == "verify":
        return verify(process_path=args.process, fail_fast=not args.no_fail_fast)
    raise RuntimeError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
