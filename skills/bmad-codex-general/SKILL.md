---
name: bmad-codex-general
description: Repo-agnostic BMAD workflow for Claude Code (plan -> bmad_input -> worktrees -> merge worktree -> proof gate). Assumes scripts/bmad_bundle.py is present in the target repo.
metadata:
  short-description: BMAD Claude Code workflow (general)
---

# BMAD Claude Code (general)

Use this skill when running BMAD work in any repo that has the BMAD runner (`scripts/bmad_bundle.py`).

This is a generalization of the repo-specific BMAD workflows. It avoids hardcoded repo paths.

## Hard Rules (non-negotiable)

- Read repo-root `AGENTS.md` and `CTO_RULES.md` before starting (if they exist).
- Base everything from GitHub-main (`origin/main`).
- Merge only inside a dedicated merge worktree under:
  `<REPO_ROOT>/worktrees_claude/merge/<process>/main-merge`
- Do not merge into the repo main working tree (the folder you normally open) without explicit GO.
- Each story has its own worktree and branch; no multi-story worktrees.
- If continuing the same story in a new context window, you MUST write a handoff file and restart in a fresh Claude Code session (see "5b").
- Non-test files: max 300 lines and max 20 functions.
- Proof gate is mandatory: `output/bmad/<process>/<run_id>/<story_id>/final.json` with `done=true` and metadata keys.
- No mocks for business logic; IO stubs only if based on existing fixtures.
- Proof/verify attempts are capped at 3 per story by default (then the story becomes [BLOCKED]).

## Preconditions / repo detection (fail-closed)

Before any BMAD run:

1) Confirm you are in the intended repo root.
2) Confirm `origin/main` exists and you can base off it.
3) Confirm the BMAD runner exists:
   - Required: `scripts/bmad_bundle.py`
   - If missing: STOP. Either install/port the BMAD kit into the repo, or run BMAD from a repo that contains it.

## Process name (canonical)

PROCESS is the slug of the `bmad_input/<name>.md` filename:
- Strip `.md`
- Lowercase
- Replace non-alphanumeric with `_`
- Trim leading/trailing `_`

Example: `bmad_input/vrp-best-effort.md` -> `vrp_best_effort`

## Workflow

### 0) Repo policy

In the target repo root:

```bash
git rev-parse --show-toplevel
git fetch origin
test -f AGENTS.md || true
test -f CTO_RULES.md || true
test -f scripts/bmad_bundle.py
```

### 1) If starting from a plan, create BMAD input

Write both:
- `bmad_input/<process>.md`
- `bmad_input/<process>.json`

Minimum required sections in the markdown:
- Scope + out-of-scope
- Features with priority (P0/P1/P2/P3)
- Verification per P0 feature: exactly 1 `[command]` and exactly 1 `[expected]`
- Invariants (what must NEVER happen)
- Constraints: file limits, test expectations

Priority completion rule (hard):
- P1, P2 and P3 must be explicitly present (use "None" if empty). Do not stop after P1.

### 2) Generate stories (RUN1)

From the repo root:

```bash
RUN_ID="<run_id>"
python3 scripts/bmad_bundle.py init --input bmad_input/<process>.md --run-id "$RUN_ID"
```

### 3) Worktree setup (per process)

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
PROCESS="<process>"
RUN_ID="<run_id>"

WT_ROOT="${REPO_ROOT}/worktrees_claude/merge/${PROCESS}"
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

Follow repo rules. Default for runtime changes:

```bash
ruff check .
ruff format --check .
pytest -q <targeted-tests>
```

If coverage gate is in scope, run the smallest coverage command that proves the changed paths.

Docs-only changes: no tests required.

### 5b) Context-rot guard (same story: HANDOFF -> new context window)

**Triggers (start handoff wanneer een van deze geldt):**

1. **Context remaining < 25%** — check de statusline
2. **Onzekerheid** over repo state, files, of welke tests falen/slagen
3. **Contradictions** tussen wat je denkt en wat er echt in de code staat
4. **Langlopende story** die meer dan 1 context window nodig heeft

**Handoff proces:**

1. Schrijf `handoff.md` (zie template hieronder)
2. Commit eventuele WIP changes
3. Start nieuwe Claude Code sessie in de story worktree
4. Geef handoff mee: `claude "Lees eerst output/bmad/<process>/<run_id>/<story_id>/handoff.md en ga verder"`

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

Then start a fresh Claude Code session in the story worktree:

```bash
cd "$STORY_WT"
claude
```

### 6) Proof gate (mandatory)

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

git merge --no-ff "$BRANCH" -m "feat($STORY_ID): <title>"

git worktree remove "$STORY_WT"
git branch -d "$BRANCH"
```

After all stories are merged into `main-merge`, STOP and wait for explicit GO before merging into the repo main working tree.

### 8) Final merge + cleanup (ONLY after explicit GO)

From the repo root:

```bash
cd "$REPO_ROOT"
git merge --no-ff "$MERGE_BRANCH" -m "merge($PROCESS): $RUN_ID"
git worktree remove "$MERGE_WT"
rmdir "$WT_ROOT" 2>/dev/null || true
```

Notes:
- Git merges commits, not file subsets. This merges stories + docs + bmad_input + outputs that were committed.
- Never force push or rewrite history unless explicitly requested.

## Operational defaults

- Prefer `rg` for search.
- Use non-destructive git commands by default.
- Never lower thresholds or add skips to fake green.
