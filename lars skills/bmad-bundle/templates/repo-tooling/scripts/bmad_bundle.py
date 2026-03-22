#!/usr/bin/env python3
"""Codex-friendly BMAD bundle orchestration."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Row:
    story_id: str
    status: str
    attempts: int
    notes: str


def _repo_root(raw: str | None = None) -> Path:
    if raw:
        return Path(raw).resolve()
    env = os.environ.get("BMAD_REPO_ROOT", "").strip()
    return Path(env).resolve() if env else Path.cwd().resolve()


def _primary_root(repo: Path) -> Path:
    parts = list(repo.resolve().parts)
    if "worktrees_claude" in parts:
        idx = parts.index("worktrees_claude")
        if idx > 0:
            return Path(*parts[:idx]).resolve()
    return repo.resolve()


def _slug(name: str) -> str:
    value = re.sub(r"_+", "_", re.sub(r"[^a-z0-9]", "_", name.strip().lower())).strip("_")
    if not value:
        raise SystemExit("ERROR: empty process slug")
    return value


def _process_from_input(repo: Path, input_path: Path) -> str:
    try:
        rel = input_path.resolve().relative_to(repo.resolve())
        if len(rel.parts) >= 4 and rel.parts[:2] == ("openspec", "changes") and rel.name == "proposal.md":
            return _slug(rel.parts[2])
    except Exception:
        pass
    return _slug(input_path.stem)


def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _backlog(repo: Path, process: str) -> Path:
    return repo / "stories_claude" / process / "BACKLOG.md"


def _parse_backlog(text: str) -> tuple[list[str], list[Row], list[str]]:
    prefix, rows, suffix = [], [], []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table and rows:
                suffix.append(line)
            else:
                prefix.append(line)
            continue
        in_table = True
        parts = [p.strip() for p in stripped.strip("|").split("|")]
        if len(parts) < 4 or parts[0].lower() == "story" or parts[0].startswith("---"):
            if rows:
                suffix.append(line)
            else:
                prefix.append(line)
            continue
        rows.append(Row(parts[0], parts[1], int(parts[2] or 0), parts[3]))
    return prefix, rows, suffix


def _render_backlog(prefix: list[str], rows: list[Row], suffix: list[str]) -> str:
    lines = list(prefix)
    if not any(line.strip().startswith("| Story |") for line in prefix):
        lines.extend(["| Story | Status | Attempts | Notes |", "|-------|--------|----------|-------|"])
    lines.extend(f"| {r.story_id} | {r.status} | {r.attempts} | {r.notes} |" for r in rows)
    lines.extend(suffix)
    return "\n".join(lines).rstrip() + "\n"


def _next_story(rows: list[Row]) -> str | None:
    for row in rows:
        if "[IN_PROGRESS]" in row.status:
            return row.story_id
    for row in rows:
        if any(token in row.status for token in ("[TODO]", "[READY]", "READY")):
            return row.story_id
    return None


def _git(repo: Path, *args: str) -> str:
    cp = subprocess.run(["git", "-C", str(repo), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {cp.stderr.strip()}")
    return (cp.stdout or "").strip()


def _dirty_paths(repo: Path) -> list[str]:
    return [line[3:].strip().split(" -> ")[-1] for line in _git(repo, "status", "--porcelain").splitlines() if line.strip()]


def _assert_clean(repo: Path, allowed_prefixes: tuple[str, ...] = ()) -> None:
    bad = []
    for path in _dirty_paths(repo):
        norm = path.replace("\\", "/")
        if any(norm.startswith(prefix) for prefix in allowed_prefixes):
            continue
        bad.append(norm)
    if bad:
        raise SystemExit("ERROR: dirty worktree not allowed:\n- " + "\n- ".join(bad))


def _integration_wt(primary: Path, process: str) -> Path:
    return primary / "worktrees_claude" / "merge" / process / "main-merge"


def _story_wt(primary: Path, process: str, story_id: str) -> Path:
    return primary / "worktrees_claude" / "merge" / process / story_id


def _ensure_worktree(primary: Path, worktree: Path, branch: str, start: str) -> None:
    worktree.parent.mkdir(parents=True, exist_ok=True)
    listing = _git(primary, "worktree", "list", "--porcelain")
    if f"worktree {worktree}" in listing:
        return
    has_branch = subprocess.run(["git", "-C", str(primary), "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"]).returncode == 0
    cmd = ["git", "-C", str(primary), "worktree", "add"]
    cmd += [str(worktree), branch] if has_branch else ["-b", branch, str(worktree), start]
    if subprocess.run(cmd, cwd=str(primary)).returncode != 0:
        raise SystemExit(f"ERROR: failed to provision worktree {worktree}")


def _commit_if_dirty(repo: Path, message: str, pathspec: str | None = None) -> None:
    if not _dirty_paths(repo):
        return
    add_cmd = ["git", "-C", str(repo), "add", pathspec] if pathspec else ["git", "-C", str(repo), "add", "-A"]
    if subprocess.run(add_cmd, cwd=str(repo)).returncode != 0:
        raise SystemExit(f"ERROR: git add failed in {repo}")
    has_staged = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--quiet"], cwd=str(repo)).returncode != 0
    if not has_staged:
        return
    if subprocess.run(["git", "-C", str(repo), "commit", "-m", message], cwd=str(repo)).returncode != 0:
        raise SystemExit(f"ERROR: git commit failed in {repo}")


def _proof_done(output_root: Path, process: str, run_id: str, story_id: str) -> bool:
    proof = output_root / "bmad" / process / run_id / story_id / "final.json"
    if not proof.is_file():
        return False
    try:
        return json.loads(proof.read_text(encoding="utf-8")).get("done") is True
    except Exception:
        return False


def _verify_story(repo_for_story: Path, output_root: Path, process: str, run_id: str, story_id: str, timeout: int) -> bool:
    env = dict(os.environ)
    env["BMAD_REPO_ROOT"] = str(repo_for_story)
    env["BMAD_OUTPUT_ROOT"] = str(output_root)
    cmd = [sys.executable, str((repo_for_story / "tools" / "bmad" / "verify_story.py").resolve()), "--process", process, "--story-id", story_id, "--run-id", run_id, "--timeout", str(timeout)]
    code = subprocess.run(cmd, cwd=str(repo_for_story), env=env).returncode
    return code == 0 and _proof_done(output_root, process, run_id, story_id)


def _update_backlog(repo: Path, process: str, story_id: str, done: bool) -> None:
    backlog = _backlog(repo, process)
    prefix, rows, suffix = _parse_backlog(backlog.read_text(encoding="utf-8"))
    updated = []
    for row in rows:
        if row.story_id != story_id:
            updated.append(row)
            continue
        attempts = row.attempts if done else row.attempts + 1
        status = "[DONE]" if done else ("[BLOCKED]" if attempts >= 3 else "[IN_PROGRESS]")
        notes = row.notes if done else ((row.notes + "; " if row.notes else "") + "proof_failed")
        updated.append(Row(row.story_id, status, attempts, notes))
    backlog.write_text(_render_backlog(prefix, updated, suffix), encoding="utf-8")


def _story_prompt(story_path: Path, process: str, story_id: str) -> str:
    return (
        f"Implement BMAD story {story_id} for process {process}.\n"
        f"Work only inside this git worktree: {story_path.parent.parent.parent}\n\n"
        "Hard rules:\n"
        "- Read and obey AGENTS.md and the story file below.\n"
        "- Respect the story's touched-paths allowlist.\n"
        "- No broad refactors. No destructive git commands. No merges.\n"
        "- Finish only when the story Verification commands pass.\n\n"
        f"--- BEGIN STORY ({story_path.name}) ---\n{story_path.read_text(encoding='utf-8')}\n--- END STORY ---\n"
    )


def _resolve_codex_binary() -> str:
    codex = shutil.which("codex")
    if codex is None:
        raise SystemExit("ERROR: codex command not found on PATH")
    primary = Path(codex).resolve()
    for raw_dir in os.environ.get("PATH", "").split(os.pathsep):
        if not raw_dir:
            continue
        candidate = Path(raw_dir) / "codex"
        if not candidate.is_file() or not os.access(candidate, os.X_OK):
            continue
        if candidate.resolve() != primary:
            return str(candidate)
    return str(primary)


def _run_codex(story_wt: Path, process: str, story_id: str, log_dir: Path) -> int:
    codex_bin = _resolve_codex_binary()
    log_dir.mkdir(parents=True, exist_ok=True)
    out_path, err_path, msg_path = log_dir / "codex.stdout.log", log_dir / "codex.stderr.log", log_dir / "last_message.txt"
    story_path = story_wt / "stories_claude" / process / f"{story_id}.md"
    cmd = [codex_bin, "exec", "--dangerously-bypass-approvals-and-sandbox", "-C", str(story_wt), "-o", str(msg_path), "-"]
    with out_path.open("w", encoding="utf-8") as out, err_path.open("w", encoding="utf-8") as err:
        proc = subprocess.Popen(cmd, cwd=str(story_wt), stdin=subprocess.PIPE, stdout=out, stderr=err, text=True)
        assert proc.stdin is not None
        proc.stdin.write(_story_prompt(story_path, process, story_id))
        proc.stdin.close()
        return int(proc.wait())


def cmd_init(args: argparse.Namespace) -> int:
    if args.auto:
        print("ERROR: --auto is forbidden for Codex BMAD bundle", file=sys.stderr)
        return 2
    repo = _repo_root(args.repo_root)
    input_path = (repo / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input).resolve()
    if not input_path.is_file():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        return 2
    process, run_id = _process_from_input(repo, input_path), (args.run_id or _run_id())
    (repo / "output" / "bmad" / process / run_id).mkdir(parents=True, exist_ok=True)
    print(json.dumps({"process": process, "run_id": run_id, "input": str(input_path)}, indent=2))
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    repo, backlog = _repo_root(args.repo_root), _backlog(_repo_root(args.repo_root), args.process)
    if not backlog.is_file():
        print(f"ERROR: BACKLOG.md not found: {backlog}", file=sys.stderr)
        return 2
    _, rows, _ = _parse_backlog(backlog.read_text(encoding="utf-8"))
    story_id = _next_story(rows)
    print(story_id or "")
    return 0 if story_id else 1


def cmd_verify(args: argparse.Namespace) -> int:
    repo = _repo_root(args.repo_root)
    done = _verify_story(repo, repo / "output", args.process, args.run_id, args.story_id, args.timeout)
    if not args.dry_run:
        _update_backlog(repo, args.process, args.story_id, done)
    print(json.dumps({"process": args.process, "story_id": args.story_id, "run_id": args.run_id, "done": done}, indent=2))
    return 0 if done else 1


def cmd_check(args: argparse.Namespace) -> int:
    repo, backlog = _repo_root(args.repo_root), _backlog(_repo_root(args.repo_root), args.process)
    if not backlog.is_file():
        print(f"ERROR: BACKLOG.md not found: {backlog}", file=sys.stderr)
        return 2
    _, rows, _ = _parse_backlog(backlog.read_text(encoding="utf-8"))
    open_tags = ("[TODO]", "[READY]", "READY", "[IN_PROGRESS]", "[BLOCKED]")
    if any(any(tag in row.status for tag in open_tags) for row in rows):
        print("NOT_COMPLETE")
        return 1
    env = dict(os.environ)
    env["BMAD_REPO_ROOT"] = str(repo)
    cmd = [sys.executable, str((repo / "tools" / "bmad" / "ralph_verify_backlog.py").resolve()), "--process", args.process, "--run-id", args.run_id]
    code = subprocess.run(cmd, cwd=str(repo), env=env).returncode
    if code == 0:
        print("RALPH_COMPLETE")
    return code


def cmd_run2(args: argparse.Namespace) -> int:
    repo, primary = _repo_root(args.repo_root), _primary_root(_repo_root(args.repo_root))
    process, run_id = args.process, args.run_id
    integration = _integration_wt(primary, process)
    if repo.resolve() != integration.resolve() or _git(repo, "branch", "--show-current") != process:
        print(f"ERROR: RUN2 must be executed from {integration} on branch {process}", file=sys.stderr)
        return 2
    _assert_clean(repo, allowed_prefixes=("output/", "logs/"))
    while True:
        backlog = _backlog(repo, process)
        if not backlog.is_file():
            print(f"ERROR: BACKLOG.md not found: {backlog}", file=sys.stderr)
            return 2
        _, rows, _ = _parse_backlog(backlog.read_text(encoding="utf-8"))
        story_id = _next_story(rows)
        if story_id is None:
            return cmd_check(argparse.Namespace(process=process, run_id=run_id, repo_root=str(repo)))
        branch, story_wt = f"{process}-{story_id}", _story_wt(primary, process, story_id)
        _ensure_worktree(primary, story_wt, branch, process)
        _assert_clean(story_wt)
        _run_codex(story_wt, process, story_id, repo / "logs" / "bmad" / process / run_id / story_id)
        done = _verify_story(story_wt, repo / "output", process, run_id, story_id, args.timeout)
        if done:
            _commit_if_dirty(story_wt, f"bmad({process}): {story_id}")
            if subprocess.run(["git", "-C", str(repo), "merge", "--no-ff", "--no-edit", branch], cwd=str(repo)).returncode != 0:
                print(f"ERROR: merge failed for {branch}", file=sys.stderr)
                return 2
        _update_backlog(repo, process, story_id, done)
        _commit_if_dirty(repo, f"bmad({process}): backlog {story_id}", f"stories_claude/{process}/BACKLOG.md")
        if not done:
            return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bmad_bundle")
    sub = parser.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=None)
    p_init = sub.add_parser("init", parents=[common]); p_init.add_argument("--input", required=True); p_init.add_argument("--run-id", default=None); p_init.add_argument("--auto", action="store_true"); p_init.set_defaults(func=cmd_init)
    p_next = sub.add_parser("next", parents=[common]); p_next.add_argument("--process", required=True); p_next.set_defaults(func=cmd_next)
    p_verify = sub.add_parser("verify", parents=[common]); p_verify.add_argument("--process", required=True); p_verify.add_argument("--story-id", required=True); p_verify.add_argument("--run-id", required=True); p_verify.add_argument("--timeout", type=int, default=2400); p_verify.add_argument("--dry-run", action="store_true"); p_verify.set_defaults(func=cmd_verify)
    p_check = sub.add_parser("check", parents=[common]); p_check.add_argument("--process", required=True); p_check.add_argument("--run-id", required=True); p_check.set_defaults(func=cmd_check)
    p_run2 = sub.add_parser("run2", parents=[common]); p_run2.add_argument("--process", required=True); p_run2.add_argument("--run-id", required=True); p_run2.add_argument("--timeout", type=int, default=2400); p_run2.set_defaults(func=cmd_run2)
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
