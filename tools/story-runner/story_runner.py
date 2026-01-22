"""Minimal story runner for BMAD process/stories.

Reads a `docs/processes/<process>/PROCESS.md` and the corresponding story files
under `stories/<process>/`. Extracts per-AC verification commands and runs them
sequentially.
"""

from __future__ import annotations

import argparse
import os
import re
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PROCESS_STORY_RE = re.compile(r"^\s*\d+[.)]\s+([A-Z][A-Z0-9_]*[\.-]\d{3})\b")
AC_RE = re.compile(r"^\s*-\s+\*\*(AC\d+):?\*\*:?")
VERIFICATION_REPO_RE = re.compile(
    r"^\s*-\s+(?:\*\*)?Verification\s*\(repo-root\)(?:\*\*)?:\s+(.+?)\s*$",
    re.IGNORECASE,
)
VERIFICATION_CWD_RE = re.compile(
    r"^\s*-\s+(?:\*\*)?Verification\s*\(cwd=([^)]+)\)(?:\*\*)?:\s+(.+?)\s*$",
    re.IGNORECASE,
)
VERIFICATION_GENERIC_RE = re.compile(
    r"^\s*-\s+(?:\*\*)?Verification(?:\*\*)?:\s+(.+?)\s*$",
    re.IGNORECASE,
)
EXPECTED_RE = re.compile(r"^\s*-\s+(?:\*\*)?Expected(?:\*\*)?:\s+(.+?)\s*$", re.IGNORECASE)
EXPECTED_EXIT_RE = re.compile(r"\bexit(?:\s*code|code)?\s*[:=]?\s*(\d+)\b", re.IGNORECASE)
OUTPUT_SNIPPET_LIMIT = 2000


@dataclass(frozen=True)
class AcceptanceCriterion:
    story_id: str
    ac_id: str
    command: str
    expected: str
    cwd: Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_backticks(value: str) -> str:
    trimmed = value.strip()
    if len(trimmed) >= 2 and trimmed[0] == "`" and trimmed[-1] == "`":
        return trimmed[1:-1].strip()
    return trimmed


def _parse_expected(expected: str) -> tuple[str, int | None, str]:
    cleaned = expected.strip()
    match = EXPECTED_EXIT_RE.search(cleaned)
    if match:
        return ("exit", int(match.group(1)), cleaned)
    return ("output", None, cleaned)


def _format_output(output: str) -> str:
    trimmed = output.strip()
    if len(trimmed) <= OUTPUT_SNIPPET_LIMIT:
        return trimmed
    return f"{trimmed[:OUTPUT_SNIPPET_LIMIT]}\n...<truncated>"


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


def parse_story_verifications(
    story_path: Path, story_id: str, repo_root: Path
) -> list[AcceptanceCriterion]:
    lines = _read_text(story_path).splitlines()
    acs: list[AcceptanceCriterion] = []

    current_ac: str | None = None
    current_cmd: str | None = None
    current_expected: str | None = None
    current_cwd: Path | None = None
    current_ac_line = 0
    current_cmd_line: int | None = None
    current_expected_line: int | None = None

    def flush() -> None:
        nonlocal current_ac, current_cmd, current_expected, current_cwd
        nonlocal current_ac_line, current_cmd_line, current_expected_line
        if current_ac is None:
            return
        if current_cmd is None:
            raise ValueError(
                f"Missing Verification for {current_ac} (line {current_ac_line}) in {story_path}"
            )
        if current_expected is None:
            line_ref = f"line {current_cmd_line}" if current_cmd_line else "unknown line"
            raise ValueError(
                f"Missing Expected for {current_ac} ({line_ref}) in {story_path}"
            )
        acs.append(
            AcceptanceCriterion(
                story_id=story_id,
                ac_id=current_ac,
                command=current_cmd,
                expected=current_expected.strip(),
                cwd=current_cwd or repo_root,
            )
        )
        current_ac = None
        current_cmd = None
        current_expected = None
        current_cwd = None
        current_ac_line = 0
        current_cmd_line = None
        current_expected_line = None

    for line_no, line in enumerate(lines, start=1):
        ac_match = AC_RE.match(line)
        if ac_match:
            flush()
            current_ac = ac_match.group(1)
            current_ac_line = line_no
            continue

        if current_ac is None:
            continue

        ver_cwd_match = VERIFICATION_CWD_RE.match(line)
        if ver_cwd_match:
            if current_cmd is not None:
                raise ValueError(
                    f"Multiple Verification lines for {current_ac} "
                    f"(lines {current_cmd_line}, {line_no}) in {story_path}"
                )
            cwd_raw = ver_cwd_match.group(1).strip()
            current_cwd = (
                Path(cwd_raw)
                if Path(cwd_raw).is_absolute()
                else (repo_root / cwd_raw)
            )
            current_cmd = _strip_backticks(ver_cwd_match.group(2))
            current_cmd_line = line_no
            continue

        ver_repo_match = VERIFICATION_REPO_RE.match(line)
        if ver_repo_match:
            if current_cmd is not None:
                raise ValueError(
                    f"Multiple Verification lines for {current_ac} "
                    f"(lines {current_cmd_line}, {line_no}) in {story_path}"
                )
            current_cwd = repo_root
            current_cmd = _strip_backticks(ver_repo_match.group(1))
            current_cmd_line = line_no
            continue

        ver_generic_match = VERIFICATION_GENERIC_RE.match(line)
        if ver_generic_match:
            if current_cmd is not None:
                raise ValueError(
                    f"Multiple Verification lines for {current_ac} "
                    f"(lines {current_cmd_line}, {line_no}) in {story_path}"
                )
            current_cwd = repo_root
            current_cmd = _strip_backticks(ver_generic_match.group(1))
            current_cmd_line = line_no
            continue

        exp_match = EXPECTED_RE.match(line)
        if exp_match:
            if current_cmd is None:
                raise ValueError(
                    f"Expected without Verification (line {line_no}) in {story_path}"
                )
            if current_expected is not None:
                raise ValueError(
                    f"Multiple Expected lines for {current_ac} "
                    f"(lines {current_expected_line}, {line_no}) in {story_path}"
                )
            current_expected = _strip_backticks(exp_match.group(1))
            current_expected_line = line_no
            continue

    flush()
    if not acs:
        raise ValueError(f"No AC verifications found in story: {story_path}")
    return acs


def _powershell_command(cmd: str) -> list[str]:
    return ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd]


def run_command(command: str, cwd: Path) -> tuple[int, str]:
    if os.name == "nt":
        proc = subprocess.run(
            _powershell_command(command), cwd=cwd, capture_output=True, text=True
        )
    else:
        proc = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return int(proc.returncode), output


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def show(process_path: Path) -> int:
    repo = _repo_root()
    story_ids = parse_process(process_path)
    print(f"repo={repo}")
    print(f"process={process_path}")
    for idx, story_id in enumerate(story_ids, start=1):
        story_path = repo / "stories" / process_path.parent.name / f"{story_id}.md"
        print(f"{idx}. {story_id} -> {story_path}")
    return 0


def verify(process_path: Path, fail_fast: bool, json_output: Path | None) -> int:
    repo = _repo_root()
    process_name = process_path.parent.name
    story_ids = parse_process(process_path)

    all_acs: list[AcceptanceCriterion] = []
    for story_id in story_ids:
        story_path = repo / "stories" / process_name / f"{story_id}.md"
        all_acs.extend(
            parse_story_verifications(
                story_path=story_path, story_id=story_id, repo_root=repo
            )
        )

    failures: list[str] = []
    results: list[dict] = []
    for ac in all_acs:
        label = f"{ac.story_id} {ac.ac_id}"
        print(f"RUN {label}: {ac.command}")
        code, output = run_command(ac.command, cwd=ac.cwd)
        expected_type, expected_code, expected_text = _parse_expected(ac.expected)
        output_snippet = _format_output(output)
        record = {
            "story_id": ac.story_id,
            "ac_id": ac.ac_id,
            "command": ac.command,
            "expected": ac.expected,
            "expected_type": expected_type,
            "expected_exit_code": expected_code,
            "expected_text": expected_text if expected_type == "output" else None,
            "cwd": str(ac.cwd),
            "exit_code": code,
            "output_snippet": output_snippet,
            "ok": True,
            "error": None,
        }

        exit_checked = False
        if expected_type == "exit":
            if code != expected_code:
                failures.append(
                    f"{label} failed (exit={code}) expected={expected_text}"
                )
                record["ok"] = False
                record["error"] = f"exit={code} expected={expected_text}"
                print(
                    f"FAIL {label}: exit={code} expected={expected_text}",
                    file=sys.stderr,
                )
                print(f"OUTPUT:\n{output_snippet}", file=sys.stderr)
                if fail_fast:
                    results.append(record)
                    if json_output:
                        write_json(
                            json_output,
                            {
                                "tool": "story-runner",
                                "repo_root": str(repo),
                                "process": str(process_path),
                                "results": results,
                                "failures": failures,
                                "exit_code": 1,
                            },
                        )
                    return 1
                results.append(record)
                continue
            exit_checked = True
        else:
            if expected_text and expected_text not in output:
                failures.append(f"{label} missing expected output: {expected_text}")
                record["ok"] = False
                record["error"] = f"missing expected output: {expected_text}"
                print(
                    f"FAIL {label}: missing expected output: {expected_text}",
                    file=sys.stderr,
                )
                print(f"OUTPUT:\n{output_snippet}", file=sys.stderr)
                if fail_fast:
                    results.append(record)
                    if json_output:
                        write_json(
                            json_output,
                            {
                                "tool": "story-runner",
                                "repo_root": str(repo),
                                "process": str(process_path),
                                "results": results,
                                "failures": failures,
                                "exit_code": 1,
                            },
                        )
                    return 1
                results.append(record)
                continue

        if not exit_checked and code != 0:
            failures.append(f"{label} failed (exit={code}) expected={ac.expected}")
            record["ok"] = False
            record["error"] = f"exit={code} expected={ac.expected}"
            print(f"FAIL {label}: exit={code} expected={ac.expected}", file=sys.stderr)
            print(f"OUTPUT:\n{output_snippet}", file=sys.stderr)
            if fail_fast:
                results.append(record)
                if json_output:
                    write_json(
                        json_output,
                        {
                            "tool": "story-runner",
                            "repo_root": str(repo),
                            "process": str(process_path),
                            "results": results,
                            "failures": failures,
                            "exit_code": 1,
                        },
                    )
                return 1
        else:
            print(f"OK  {label}")
        results.append(record)

    if failures:
        print("FAILED ACs:", file=sys.stderr)
        for fail in failures:
            print(f"- {fail}", file=sys.stderr)
        if json_output:
            write_json(
                json_output,
                {
                    "tool": "story-runner",
                    "repo_root": str(repo),
                    "process": str(process_path),
                    "results": results,
                    "failures": failures,
                    "exit_code": 1,
                },
            )
        return 1
    if json_output:
        write_json(
            json_output,
            {
                "tool": "story-runner",
                "repo_root": str(repo),
                "process": str(process_path),
                "results": results,
                "failures": failures,
                "exit_code": 0,
            },
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="story_runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_show = sub.add_parser("show", help="Show canonical story order and paths")
    p_show.add_argument("--process", required=True, type=Path)

    p_verify = sub.add_parser("verify", help="Run all AC verification commands sequentially")
    p_verify.add_argument("--process", required=True, type=Path)
    p_verify.add_argument("--no-fail-fast", action="store_true")
    p_verify.add_argument("--json-output", type=Path, default=None)

    args = parser.parse_args(argv)
    if args.cmd == "show":
        return show(process_path=args.process)
    if args.cmd == "verify":
        try:
            return verify(
                process_path=args.process,
                fail_fast=not args.no_fail_fast,
                json_output=args.json_output,
            )
        except Exception as exc:  # pragma: no cover - CLI error path
            if args.json_output:
                write_json(
                    args.json_output,
                    {
                        "tool": "story-runner",
                        "repo_root": str(_repo_root()),
                        "process": str(args.process),
                        "error": str(exc),
                        "exit_code": 2,
                    },
                )
            raise
    raise RuntimeError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
