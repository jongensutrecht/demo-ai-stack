---
name: bmad-codex
# prettier-ignore
description: Codex BMAD workflow (worktrees + proof gate) for photobooth_project_claude
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Codex (photobooth_project_claude)

Use this command to run the Codex BMAD workflow in this repo.

## Hard Rules (Non-Negotiable)

- Read repo-root `AGENTS.md` and `CTO_RULES.md` before starting.
- Base everything from GitHub-main (`origin/main`).
- Merge only inside the merge worktree under the PC path:
  `/home/mrbiggles/dev/github.com/jongensutrecht/photobooth_project_claude/worktrees_claude/merge/<process>/main-merge`.
- Do not merge into the PC-main-folder without explicit GO.
- Each story has its own worktree and branch; no multi-story worktrees.
- If continuing the same story in a new context window, you MUST write a handoff file and restart in a fresh session (see "5b").
- Non-test files: max 300 lines and max 20 functions.
- Proof gate is mandatory: `output/bmad/<process>/<run_id>/<story_id>/final.json` with `done=true` and metadata keys.
- No mocks for business logic; IO stubs only if based on existing fixtures.
- Ralph proof/verify attempts are capped at 3 per story by default (then the story becomes `[BLOCKED]`).

## Process Name (Canonical)

`PROCESS` is the slug of the `bmad_input/<name>.md` filename:
- Strip `.md`
- Lowercase
- Replace non-alphanumeric with `_`
- Trim leading/trailing `_`

Example: `bmad_input/vrp-best-effort.md` -> `vrp_best_effort`

## Workflow

### 1) If starting from a plan, create BMAD input

Write both:
- `bmad_input/<process>.md`
- `bmad_input/<process>.json`

Minimum required sections in the markdown:
- Scope + out of scope
- Features with priority (P0/P1/P2/P3)
- Verification per P0 feature: `[command]` + `[expected]`
- Invariants (what must NEVER happen)
- Constraints: file limits, test expectations

Priority completion rule (hard):
- P1, P2 and P3 must be explicitly present (use "None" if empty). Do not stop after P1.

### 2) Generate stories (RUN1)

From the PC-main-folder:

```bash
RUN_ID="<run_id>"
python3 scripts/bmad_bundle.py init --input bmad_input/<process>.md --run-id "$RUN_ID"
```

### 3) Worktree setup (per process)

```bash
PROCESS="<process>"
RUN_ID="<run_id>"
WT_ROOT="/home/mrbiggles/dev/github.com/jongensutrecht/photobooth_project_claude/worktrees_claude/merge/${PROCESS}"
MERGE_WT="${WT_ROOT}/main-merge"
MERGE_BRANCH="merge-${PROCESS}-${RUN_ID}"

git worktree add -b "$MERGE_BRANCH" "$MERGE_WT" origin/main
```

### 4) Story worktree (per story)

```bash
STORY_ID="API-101"
BRANCH="story-${STORY_ID,,}-${RUN_ID}"
STORY_WT="${WT_ROOT}/${STORY_ID}"

git worktree add -b "$BRANCH" "$STORY_WT" origin/main
cd "$STORY_WT"

git branch --show-current  # must be $BRANCH
pwd                        # must be $STORY_WT
```

If `$STORY_WT` exists, stop and clean it first; do not reuse paths.

### 5) Implement + tests (per story)

Follow repo rules:
- Runtime code changes: `ruff check .`, `ruff format --check .`, and targeted `pytest` for the changed path.
- Use `pytest --cov` for the relevant modules if coverage is in scope.
- Docs-only changes: no tests needed.

### 5b) Context-rot guard (same story: HANDOFF -> new context window)

Goal: keep one story moving without "context rot" by restarting with a minimal, deterministic state handoff.

Trigger: any time you notice uncertainty/contradictions about current repo state, files, failing tests, or next steps.

Write handoff (required):

```bash
HANDOFF="output/bmad/${PROCESS}/${RUN_ID}/${STORY_ID}/handoff.md"
mkdir -p "$(dirname "$HANDOFF")"

git status --porcelain
git diff --stat

cat > "$HANDOFF" <<'EOF'
# HANDOFF (same story, new context window)

Story: <STORY_ID>
Process: <PROCESS>
Run: <RUN_ID>
Worktree: <absolute path>
Branch: <branch name>

Goal / ACs:
- ...

Current status:
- Tests: <what fails / what passes>
- Lint/format: <what fails / what passes>

What changed (files + intent):
- <path>: ...

Commands already run (+ outcome):
- <cmd> -> <result>

Next steps (exact, copy-paste commands):
1) <cmd>
2) <cmd>

Invariants / do-not-do:
- Do not merge into main.
- Keep changes within this story only.
EOF
```

### 6) Proof gate

Ensure `output/bmad/<process>/<run_id>/<story_id>/final.json` exists and has:
- `done=true`
- `run_id`, `commit_hash`, `started_at`, `completed_at`

Verify at the end of the run:

```bash
python3 scripts/bmad_bundle.py check --process "$PROCESS" --run-id "$RUN_ID"
```

### 7) Merge (ONLY in main-merge worktree)

```bash
cd "$MERGE_WT"

git merge --no-ff "$BRANCH" -m "feat($STORY_ID): <titel>"

git worktree remove "$STORY_WT"
git branch -d "$BRANCH"
```

After all stories are merged into `main-merge`, stop and wait for explicit GO before merging into the PC-main-folder.

### 8) Final merge + cleanup (ONLY after explicit GO)

From the PC-main-folder (this is the final merge into `main`):

```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/photobooth_project_claude

# Merge the integration branch into main
git merge --no-ff "$MERGE_BRANCH" -m "merge($PROCESS): $RUN_ID"

# Cleanup integration worktree (keep the branch for now; see note below)
git worktree remove "$MERGE_WT"

# Optional: remove now-empty process folder (only if empty)
rmdir "$WT_ROOT" 2>/dev/null || true
```

Note:
- This merge brings everything from `$MERGE_BRANCH` into `main` (runtime code + docs + `bmad_input/**` + `stories_claude/**`).
- `git branch -d "$MERGE_BRANCH"` can fail until `main` is pushed to GitHub-main (`origin/main`).

## Operational Defaults

- Prefer `rg` for search.
- Use `apply_patch` for single-file edits.
- Never use destructive git commands unless explicitly instructed.
