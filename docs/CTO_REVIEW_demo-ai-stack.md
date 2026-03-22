# demo-ai-stack CTO Review (`/home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack`)

## NOTE (2026-03-02)

Dit CTO review rapport is historisch. `docs/CTO_RULES.md` is inmiddels omgezet naar een Rule Registry; bepaalde bevindingen over "v1 vs v2 prompt drift" kunnen daardoor (gedeeltelijk) opgelost of verouderd zijn.


## 1) Executive Summary

Repo: `/home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack`  
Scanned at: `2026-02-19T13:32:53Z` (UTC)  
Branch: `main`  
Commit: `ef52cdedfe0b139780eddce97cd308116b9be5fa`  
Working tree: clean (`dirty_lines=0`)  

Overall Score: **8.70 / 10**

Context: This repository is a toolkit for “BMAD Autopilot + CTO Guard + Ralph Loop” (skills + scripts + docs + templates), not a deployable application. Evidence: `README.md:1-16`.

### Top 3 Strengths (evidence-based)

1. Cross-platform gate tooling exists (PowerShell + Bash variants for test-gate/invariant-check). Evidence (file inventory): `find tools -maxdepth 2 -type f` shows both `tools/test-gate/test-gate.ps1` + `tools/test-gate/test-gate.sh` and `tools/invariant-check/invariant-check.ps1` + `tools/invariant-check/invariant-check.sh`.
2. Multiple tools are explicitly fail-closed when required config is missing. Evidence: `tools/test-gate/test-gate.ps1:208-210`, `tools/invariant-check/invariant-check.ps1:247-250`.
3. Repo structure is clear at the top level (`skills/`, `tools/`, `templates/`, `docs/`, `bmad_autopilot_kit/`). Evidence (tree): `ls -la` of repo root shows these directories.

### Top 3 Risks (evidence-based)

1. **Data loss risk**: `tools/skills-sync/sync-skills.sh` uses `rsync -a --delete` between the repo and `~/.claude/skills`, which can delete files in the destination. Evidence: `tools/skills-sync/sync-skills.sh:67`, `tools/skills-sync/README.md:20-22`.
2. **Arbitrary command execution risk**: `tools/story-runner/story_runner.py` runs verification commands from story markdown using `shell=True` (non-Windows) and the README does not include a “do not run untrusted stories” safety warning. Evidence: `tools/story-runner/story_runner.py:211-218`, `tools/story-runner/README.md:1-9`.
3. **Spec/docs drift**: key documents and tools disagree or reference missing paths.
   - `docs/CTO_RULES.md` is a v1 scan prompt while `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` is v2. Evidence: `docs/CTO_RULES.md:1`, `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md:1-4`, and `README.md:15`.
   - BMAD AC format in contract vs tool parsers: `docs/CONTRACT.md:34-43` vs `tools/preflight/preflight.ps1:143` and `tools/story-runner/story_runner.py:20`.

### First Actions (high ROI)

1. Add safety rails to `tools/skills-sync/sync-skills.sh` so destructive sync is explicit and recoverable (backup + confirmation).
2. Make `tools/story-runner/story_runner.py` require explicit opt-in to execute shell commands; add a security warning to `tools/story-runner/README.md`.
3. Fix licensing + doc drift: add a `LICENSE` file, and align `docs/CTO_RULES.md` with v2 (or rename + update references).
4. Add minimal CI + smoke tests for the tools to prevent regressions.

### Scan Evidence (commands + output)

```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && \
  echo "branch=$(git rev-parse --abbrev-ref HEAD)" && \
  echo "commit=$(git rev-parse HEAD)" && \
  echo "dirty_lines=$(git status --porcelain | wc -l | tr -d ' ')" && \
  date -u +"scanned_at=%Y-%m-%dT%H:%M:%SZ"
```

Output:
```text
branch=main
commit=ef52cdedfe0b139780eddce97cd308116b9be5fa
dirty_lines=0
scanned_at=2026-02-19T13:32:53Z
```

```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && \
  echo "ci_workflows_count=$(find . -path './.github/workflows/*' -type f 2>/dev/null | wc -l | tr -d ' ')" && \
  echo "manifests_count=$(find . -maxdepth 4 -type f \( -name 'pyproject.toml' -o -name 'package.json' -o -name 'go.mod' -o -name 'Cargo.toml' -o -name 'requirements.txt' -o -name 'requirements-dev.txt' -o -name 'Pipfile' \) 2>/dev/null | wc -l | tr -d ' ')" && \
  echo "tests_dirs_count=$(find . -maxdepth 2 -type d \( -name tests -o -name test -o -name '__tests__' \) 2>/dev/null | wc -l | tr -d ' ')" && \
  echo "dockerfiles_count=$(find . -maxdepth 4 -type f \( -name 'Dockerfile' -o -name 'docker-compose.yml' -o -name 'compose.yml' \) 2>/dev/null | wc -l | tr -d ' ')" && \
  echo "db_files_count=$(find . -type f \( -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) 2>/dev/null | wc -l | tr -d ' ')"
```

Output:
```text
ci_workflows_count=0
manifests_count=0
tests_dirs_count=0
dockerfiles_count=0
db_files_count=0
```

Repo root (top-level) inventory:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && ls -la | sed -n '1,200p'
```

Output:
```text
total 56
drwxrwxr-x 10 mrbiggles mrbiggles 4096 Jan 31 18:53 .
drwxrwxr-x 34 mrbiggles mrbiggles 4096 Feb 18 18:35 ..
drwxrwxr-x  3 mrbiggles mrbiggles 4096 Jan 14 19:05 .claude
drwxrwxr-x  8 mrbiggles mrbiggles 4096 Feb 19 14:32 .git
-rw-rw-r--  1 mrbiggles mrbiggles  207 Jan 14 19:05 .gitignore
-rw-rw-r--  1 mrbiggles mrbiggles 3665 Jan 22 12:14 HANDOFF_2026-01-22.md
-rw-rw-r--  1 mrbiggles mrbiggles 3035 Jan 21 15:04 INSTALL.ps1
-rw-rw-r--  1 mrbiggles mrbiggles 3893 Jan 21 15:05 README.md
drwxrwxr-x  4 mrbiggles mrbiggles 4096 Feb  2 23:05 bmad_autopilot_kit
drwxrwxr-x  2 mrbiggles mrbiggles 4096 Feb 19 14:42 docs
drwxrwxr-x 13 mrbiggles mrbiggles 4096 Jan 24 19:51 lars skills
drwxrwxr-x 13 mrbiggles mrbiggles 4096 Feb  2 23:05 skills
drwxrwxr-x  2 mrbiggles mrbiggles 4096 Jan 17 20:55 templates
drwxrwxr-x  8 mrbiggles mrbiggles 4096 Jan 21 14:21 tools
```

Tools inventory:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && find tools -maxdepth 2 -type f | sort
```

Output:
```text
tools/invariant-check/README.md
tools/invariant-check/invariant-check.ps1
tools/invariant-check/invariant-check.sh
tools/preflight/README.md
tools/preflight/preflight.ps1
tools/skills-sync/README.md
tools/skills-sync/sync-skills.sh
tools/story-runner/README.md
tools/story-runner/sample_gates.txt
tools/story-runner/story_runner.py
tools/test-gate/README.md
tools/test-gate/test-gate.ps1
tools/test-gate/test-gate.sh
```

Docs process inventory (story runner assumes `docs/processes/<process>/PROCESS.md`):
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && \
  find docs -maxdepth 3 -type d | sort && \
  echo '---' && \
  find docs -maxdepth 4 -type f -name 'PROCESS.md' | sort
```

Output:
```text
docs
---
```

Repo-wide policy file scan:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && \
  find . -maxdepth 2 -type f \( \
    -iname 'AGENTS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'SECURITY.md' -o -iname 'CLAUDE.md' -o -iname 'CTO_RULES.md' -o -iname 'LICENSE*' \
  \) | sort
```

Output:
```text
./docs/CTO_RULES.md
```

License presence check:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && (ls -la LICENSE* 2>&1 || true)
```

Output:
```text
ls: cannot access 'LICENSE*': No such file or directory
```

Repo tagging/versioning signal:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && git tag | wc -l | tr -d ' ' | xargs -I{} echo "git_tags_count={}"
```

Output:
```text
git_tags_count=0
```

Skills folder duplication evidence:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && \
  echo 'skills/' && ls -1 skills | sort && \
  echo '---' && \
  echo 'lars skills/' && ls -1 "lars skills" | sort && \
  echo '---' && \
  echo '.claude/skills/' && ls -1 .claude/skills | sort
```

Output:
```text
skills/
bmad-autopilot
bmad-bundle
bmad-codex
bmad-codex-general
cto-guard
invariant-discovery
plan-to-bmad
quick-fix
ralph-loop
skill-creator
test-guard
---
lars skills/
bmad-autopilot
bmad-bundle
commands
cto-guard
debug
invariant-discovery
plan-to-bmad
quick-fix
ralph-loop
skill-creator
test-guard
---
.claude/skills/
bmad-autopilot
bmad-bundle
cto-guard
invariant-discovery
quick-fix
ralph-loop
skill-creator
test-guard
```

Empty tools directory evidence:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && ls -la tools/cto-review
```

Output:
```text
total 8
drwxrwxr-x 2 mrbiggles mrbiggles 4096 Jan 17 20:55 .
drwxrwxr-x 8 mrbiggles mrbiggles 4096 Jan 21 14:21 ..
```

`bmad_autopilot_kit/` inventory (note: files contain spaces; no `tools/` folder exists at this depth):
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && find bmad_autopilot_kit -maxdepth 2 -type f | sort
```

Output:
```text
bmad_autopilot_kit/AI_STACK_STANDARD_BMAD_WORKTREES_GUARDRAILS seq force_claude.md
bmad_autopilot_kit/BMAD_STORY_LLM_PLAYBOOK  Seq force_claude.md
bmad_autopilot_kit/PLAN_TO_BMAD_PROMPT_codex.md
bmad_autopilot_kit/README_codex.md
bmad_autopilot_kit/RUN1_STORY_GENERATION_PROMPT_claude.txt
bmad_autopilot_kit/UITVOER_PROMPT_claude.md
bmad_autopilot_kit/docs_claude/BMAD_INPUT_claude.md
bmad_autopilot_kit/docs_claude/CONTRACT_claude.md
bmad_autopilot_kit/docs_claude/bmad-autopilot-spec.md
```

`python` heredoc usage in bash tools:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && rg -n "\\bpython\\b\\s+-\\s+<<'PY'" tools | sed -n '1,200p'
```

Output:
```text
tools/test-gate/test-gate.sh:88:        python - <<'PY'
tools/test-gate/test-gate.sh:172:        python - <<'PY'
tools/test-gate/test-gate.sh:394:    python - <<'PY'
tools/invariant-check/invariant-check.sh:88:        python - <<'PY'
tools/invariant-check/invariant-check.sh:228:        python - <<'PY'
tools/invariant-check/invariant-check.sh:313:    python - <<'PY'
```

Secret scan (limited) evidence:
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && \
  rg -n --hidden --glob '!.git/**' --glob '!docs/CTO_REVIEW_demo-ai-stack.md' -S "(BEGIN (RSA|OPENSSH) PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}|AIzaSy[0-9A-Za-z-_]{35}|-----BEGIN)" . || true
```

Output:
```text
(no matches)
```

Feature flag scan (excluding this report):
```bash
cd /home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack && \
  rg -n -S "(launchdarkly|unleash|flipper|feature flag|FEATURE_FLAG|LD_[A-Z_]+)" . \
    --glob '!.git/**' \
    --glob '!docs/CTO_REVIEW_demo-ai-stack.md' || true
```

Output:
```text
(no matches)
```

## 2) Facet Scores Overview

Scoring formula (v2.0): `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md:43-69`.

| Facet | Score | P1-C | P1-Q | P2 | P3 |
|------|------:|-----:|-----:|---:|---:|
| 1) Architectuur | 9.25 | 0 | 0 | 1 | 1 |
| 2) Code Quality | 9.00 | 0 | 0 | 2 | 0 |
| 3) Complexity & Bugs | 9.00 | 0 | 0 | 2 | 0 |
| 4) Testing | 9.00 | 0 | 0 | 2 | 0 |
| 5) Dependencies | 8.50 | 0 | 1 | 2 | 0 |
| 6) Security | 7.50 | 2 | 0 | 1 | 0 |
| 7) Ops/Reliability | 8.50 | 0 | 0 | 3 | 0 |
| 8) Documentation | 7.50 | 0 | 2 | 3 | 0 |
| 9) Developer Experience | 8.50 | 0 | 0 | 3 | 0 |
| 10) Feature Flags | 10.00 | 0 | 0 | 0 | 0 |
| 11) Domain/Spec Compliance | 9.00 | 0 | 0 | 2 | 0 |

Overall Score = average(all facet scores) = **8.70 / 10**

## 3) Per-Facet Detail (Strengths + Gaps)

### 1) Architectuur

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| ARCH-S1 | Clear separation between skills, tools, templates and docs | Repo root listing shows `skills/`, `tools/`, `templates/`, `docs/`, `bmad_autopilot_kit/`. |
| ARCH-S2 | Windows installer exists for skill distribution to a global path | `INSTALL.ps1:15-45`. |
| ARCH-S3 | Tooling is grouped by intent (`tools/test-gate`, `tools/invariant-check`, `tools/story-runner`, `tools/preflight`, `tools/skills-sync`) | `find tools -maxdepth 2 -type f` output (see inventory in scan evidence). |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| ARCH-001 | P2 | OPEN | Multiple competing “sources of truth” for skills (`skills/`, `lars skills/`, `.claude/skills/`) increases drift/confusion | “Skills folder duplication evidence” command output (above) | Decide canonical source of truth (likely `skills/`), document it in `README.md`, and remove/relocate the others (or explicitly mark as examples) so `INSTALL.ps1` and sync tooling are unambiguous. |
| ARCH-002 | P3 | OPEN | Empty `tools/cto-review/` directory looks like dead/incomplete module | `ls -la tools/cto-review` shows directory exists but contains no files | Either remove the directory or add a README + implementation so it’s not dead weight. |

### 2) Code Quality

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| CQ-S1 | Strict bash mode is used in destructive sync tool | `tools/skills-sync/sync-skills.sh:1-2`. |
| CQ-S2 | PowerShell tooling uses strict mode and stop-on-error | `tools/test-gate/test-gate.ps1:38-40`, `tools/invariant-check/invariant-check.ps1:38-40`, `tools/preflight/preflight.ps1:11-13`. |
| CQ-S3 | Python story runner is small, typed, and produces structured results | `tools/story-runner/story_runner.py:8-18`, `tools/story-runner/story_runner.py:260-387`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| CQ-001 | P2 | OPEN | `tools/test-gate/test-gate.sh` uses a simplified regex-based YAML parser, which is brittle for real-world YAML | `tools/test-gate/test-gate.sh:200-240` | Either: use a real YAML parser (Python/yq) or validate that `test-requirements.yaml` must stay within a strict subset, with a deterministic config validator + tests. |
| CQ-002 | P2 | OPEN | Bash strict-mode is inconsistent (`set -euo pipefail` vs `set -uo pipefail`), increasing risk of silently-ignored failures | `tools/skills-sync/sync-skills.sh:2` vs `tools/test-gate/test-gate.sh:24` and `tools/invariant-check/invariant-check.sh:24` | Standardize strict mode across bash scripts and adjust error-handling so expected failures are explicitly handled (`|| true`) instead of accidental continuation. |

### 3) Complexity & Bugs

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| BUG-S1 | Tooling is single-purpose and documented per tool | `tools/test-gate/README.md:1-37`, `tools/invariant-check/README.md:1-38`. |
| BUG-S2 | Explicit exit codes are documented for gate tools | `tools/test-gate/README.md:64-71`, `tools/invariant-check/README.md:94-101`. |
| BUG-S3 | Story runner supports explicit `cwd=` verification format to reduce fragile relative-path assumptions | `tools/story-runner/story_runner.py:25-28`, `tools/story-runner/README.md:13-16`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| BUG-001 | P2 | OPEN | Duplicate implementations (PowerShell + Bash) without parity tests will drift over time | Tools inventory output lists both `tools/test-gate/test-gate.ps1` + `tools/test-gate/test-gate.sh` and `tools/invariant-check/invariant-check.ps1` + `tools/invariant-check/invariant-check.sh` | Add parity tests (golden inputs/outputs) or designate one implementation canonical and generate the other, or remove one to reduce maintenance surface. |
| BUG-002 | P2 | OPEN | Spaces in committed paths (e.g., `lars skills/`, and `bmad_autopilot_kit/*` filenames with spaces) increase quoting/automation breakage risk | Directory `lars skills/` exists (skills duplication output); `bmad_autopilot_kit/` inventory output shows filenames containing spaces | Rename or relocate space-containing paths (or document strict quoting requirements everywhere they’re referenced). |

### 4) Testing

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| TEST-S1 | Test requirements gate exists to enforce test presence by path rules | `tools/test-gate/README.md:1-37`. |
| TEST-S2 | Invariant coverage gate exists to enforce NEVER-tests for invariants | `tools/invariant-check/README.md:1-38`. |
| TEST-S3 | Preflight exists to validate RUN1 story output contract before execution | `tools/preflight/README.md:1-9`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| TEST-001 | P2 | OPEN | Repo has no tests for its own tooling | `tests_dirs_count=0` (scan evidence output) | Add a minimal test suite (at least for `tools/story-runner/story_runner.py` parsing and for script “golden” behavior). Provide a single command to run it locally. |
| TEST-002 | P2 | OPEN | No CI detected, so regressions in skills/tools won’t be caught automatically | `ci_workflows_count=0` (scan evidence output) | Add CI workflow(s) that run the test suite + basic lint checks for scripts, and fail on regressions. |

### 5) Dependencies

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| DEP-S1 | `tools/story-runner/story_runner.py` uses only Python stdlib (low dependency surface) | `tools/story-runner/story_runner.py:10-17`. |
| DEP-S2 | Templates exist to bootstrap `test-requirements.yaml` and invariants docs | `templates/test-requirements.yaml:1-7`, `templates/invariants-example.md:1-5`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| DEP-001 | P2 | OPEN | No dependency manifests/lockfiles in repo, reducing reproducibility of tooling expectations | `manifests_count=0` (scan evidence output) | Add minimal manifests for any runtime tooling that needs reproducibility (e.g., a small `pyproject.toml` for Python tooling), or explicitly document supported versions and a bootstrap script that checks them. |
| DEP-002 | P1-QUICK | OPEN | Scripts/READMEs invoke `python` (not `python3`) and inline heredoc python usage assumes `python` exists | `tools/story-runner/README.md:4-8`; `rg -n \"\\bpython\\b\\s+-\\s+<<'PY'\" tools` output includes `tools/test-gate/test-gate.sh:88` and `tools/invariant-check/invariant-check.sh:88` | Update scripts to detect a Python interpreter deterministically (`python3` preferred, fallback to `python`) and fail with a clear error if not available; update READMEs to match. |
| DEP-003 | P2 | OPEN | Requirements are listed but unpinned; no tooling version checks are provided | `README.md:108-114` | Add a `tools/preflight`-style environment check script (pwsh + bash) that asserts required tools + versions and prints actionable install guidance. |

### 6) Security

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| SEC-S1 | `.gitignore` contains explicit patterns discouraging secret commits (`.env`, `*.key`, `credentials.json`) | `.gitignore:23-27`. |
| SEC-S2 | Gate tooling often fails closed when required config is missing | `tools/test-gate/test-gate.ps1:208-210`, `tools/invariant-check/invariant-check.ps1:247-250`. |
| SEC-S3 | Basic secret-pattern scan did not find common key/token markers (limited) | “Secret scan (limited) evidence” output shows `(no matches)`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| SEC-001 | P1-CRITICAL | OPEN | `rsync --delete` in `sync-skills.sh` can delete user data (destination is made identical to source); high blast radius when pointed at `~/.claude/skills` | `tools/skills-sync/sync-skills.sh:67`, `tools/skills-sync/README.md:20-22` | Make deletion opt-in and recoverable: default to `--dry-run`; require an explicit `--apply` or `--i-understand-delete` flag; create timestamped backups before applying; document restore steps; add a regression test/smoke test for safe defaults. |
| SEC-002 | P1-CRITICAL | OPEN | Story runner executes shell commands from story files (`shell=True`) with no explicit safety gate; running untrusted story content can execute arbitrary commands | `tools/story-runner/story_runner.py:211-218`; usage encourages running processes (`tools/story-runner/README.md:3-9`) | Require explicit opt-in (flag) before running commands; print a loud warning; optionally restrict allowed commands or run without shell; document threat model (“do not run on untrusted story content”). |
| SEC-003 | P2 | OPEN | No `SECURITY.md` policy or disclosure guidance found | `find . -maxdepth 2 -type f (AGENTS|CONTRIBUTING|SECURITY|CLAUDE)` only returns `./docs/CTO_RULES.md` | Add `SECURITY.md` with vulnerability reporting guidance, supported versions, and a minimal security posture statement for these tools. |

### 7) Ops/Reliability

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| OPS-S1 | Tools support JSON outputs and stable exit codes suitable for automation | `tools/test-gate/README.md:64-71`, `tools/invariant-check/README.md:94-101`, `tools/story-runner/story_runner.py:222-225`. |
| OPS-S2 | Installer script uses stop-on-error behavior | `INSTALL.ps1:8`. |
| OPS-S3 | Story runner has Windows/non-Windows execution paths | `tools/story-runner/story_runner.py:211-218`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| OPS-001 | P2 | OPEN | No CI workflows detected; operational gates are not executed automatically | `ci_workflows_count=0` (scan evidence output) | Add CI that runs lint + smoke tests for tools, and validates docs links/paths. |
| OPS-002 | P2 | OPEN | No release signaling (no git tags), which makes consumer upgrades of skills hard to reason about | `git_tags_count=0` | Introduce versioning (tags + changelog) for skill/tool changes and define upgrade steps. |
| OPS-003 | P2 | OPEN | Global skill installation copies files but does not remove deleted/renamed files; strict sync requires dangerous `rsync --delete` | `INSTALL.ps1:29-37` (copy-only); `tools/skills-sync/sync-skills.sh:67` (delete-based sync) | Provide a safe “update” mechanism: either implement an installer that can reconcile deletions safely (with backup) or a packaging approach (zip/versioned release) to make updates atomic and reversible. |

### 8) Documentation

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| DOC-S1 | README includes clear workflow diagram and usage commands | `README.md:42-104`. |
| DOC-S2 | BMAD story contract is documented | `docs/CONTRACT.md:7-29`. |
| DOC-S3 | v2 universal CTO scan prompt exists and documents deterministic scoring | `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md:1-69`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| DOC-001 | P1-QUICK | OPEN | README claims MIT license but there is no `LICENSE` file in repo | `README.md:175-177`; `ls -la LICENSE*` output: “No such file or directory” | Add `LICENSE` file (MIT text) and ensure README matches. |
| DOC-002 | P1-QUICK | OPEN | `docs/CTO_RULES.md` is a v1 scan prompt while v2 exists; README describes `docs/CTO_RULES.md` as criteria | `docs/CTO_RULES.md:1`; `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md:1-4`; `README.md:15` | Align naming: either update `docs/CTO_RULES.md` to v2 content or rename both and update all references in README + skills + prompts to the canonical file. |
| DOC-003 | P2 | OPEN | Preflight README references a path under `bmad_autopilot_kit/` that does not exist in this repo | `tools/preflight/README.md:21-32`; `find bmad_autopilot_kit -maxdepth 2 -type f` shows no tools directory | Fix README to point at actual path (`tools/preflight/preflight.ps1`) or ensure installer copies the referenced path into projects. |
| DOC-004 | P2 | OPEN | Story runner README references `docs/processes/.../PROCESS.md`, but repo has no `docs/processes/` directory | `tools/story-runner/README.md:4-6`; `find docs -maxdepth 2 -type d` output only shows `docs/` | Add an example process + sample stories in-repo (or update README to state it’s expected in the target project, not here). |
| DOC-005 | P2 | OPEN | Handoff doc references `bmad_autopilot_kit_codex/` paths that do not exist in this repo | `HANDOFF_2026-01-22.md:67-71`; repo contains `bmad_autopilot_kit/PLAN_TO_BMAD_PROMPT_codex.md` instead | Update handoff doc to match actual paths or remove it from “current truth” docs. |

### 9) Developer Experience

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| DEVX-S1 | One-command installer exists for Windows users | `README.md:21-25`; `INSTALL.ps1:1-6`. |
| DEVX-S2 | Skills are enumerated and structured for global install | `README.md:11-16`; `INSTALL.ps1:15-45`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| DEVX-001 | P2 | OPEN | Installation is Windows-first; no equivalent bash installer is provided | `README.md:21-28` | Provide cross-platform install instructions or a bash installer that mirrors `INSTALL.ps1` safely. |
| DEVX-002 | P2 | OPEN | Installer copies skills + `bmad_autopilot_kit/` but does not install the `tools/` utilities into the target project, despite tools being part of the workflow | `INSTALL.ps1:56-66` (copies only kit + docs); `find tools -maxdepth 2 -type f` shows multiple tools exist | Update installer and docs so the “kit” includes all necessary tooling (or clearly document which parts are global-only vs project-local). |
| DEVX-003 | P2 | OPEN | Repo currently provides no single “smoke test” to validate an installation end-to-end (especially given missing sample processes/stories) | `tools/story-runner/README.md:4-6` references a non-existent `docs/processes/...`; `find docs -maxdepth 2 -type d` shows no processes | Add a minimal example process + story files + a `make smoke` (or pwsh/bash) command that proves core tools work in a clean checkout. |

### 10) Feature Flags

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| FLAG-S1 | No feature-flag frameworks or patterns detected (reduces runtime complexity for this toolkit repo) | “Feature flag scan (excluding this report)” evidence shows `(no matches)`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| (none) |  |  | No feature-flag related gaps detected in this repo scope |  |  |

### 11) Domain/Spec Compliance

**Strengths**

| ID | Strength | Evidence |
|---|---|---|
| SPEC-S1 | BMAD story contract exists with required sections and verification requirements | `docs/CONTRACT.md:7-29`. |
| SPEC-S2 | Tooling exists to validate story outputs (preflight) and execute verification commands (story runner) | `tools/preflight/README.md:1-9`; `tools/story-runner/story_runner.py:1-6`. |

**Gaps**

| ID | Priority | Status | Gap | Evidence | Closure DoD |
|---|---|---|---|---|---|
| SPEC-001 | P2 | OPEN | Contract AC format does not match tooling parsers (`### AC1:` in docs vs `- **AC1**` expected by tools) | `docs/CONTRACT.md:34-43` vs `tools/preflight/preflight.ps1:143` and `tools/story-runner/story_runner.py:20` | Choose the canonical AC format and update both the contract and tool parsers; add a sample story file to ensure round-trip compatibility. |
| SPEC-002 | P2 | OPEN | Tooling assumes `docs/processes/<process>/PROCESS.md` + `stories/<process>/` structure, but repo does not include a reference implementation to validate compliance | `tools/story-runner/story_runner.py:3-5`; `tools/story-runner/README.md:4-6`; `find docs -maxdepth 2 -type d` output lacks `docs/processes` | Add an in-repo example process+stories (or explicitly scope the repo as “tooling only” and move examples into `templates/` with correct paths). |

## 4) Consolidated Gap Table (P1-CRITICAL / P1-QUICK / P2 / P3)

| ID | Facet | Priority | Gap (short) | Evidence |
|---|---|---|---|---|
| SEC-001 | Security | P1-CRITICAL | `rsync --delete` can delete user data | `tools/skills-sync/sync-skills.sh:67` |
| SEC-002 | Security | P1-CRITICAL | Story runner executes shell commands from stories (RCE risk) | `tools/story-runner/story_runner.py:211-218` |
| DOC-001 | Documentation | P1-QUICK | Missing `LICENSE` file (README says MIT) | `README.md:175-177`; `ls LICENSE*` output |
| DOC-002 | Documentation | P1-QUICK | CTO rules doc is v1 while v2 exists; references drift | `docs/CTO_RULES.md:1`; `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md:1-4`; `README.md:15` |
| DEP-002 | Dependencies | P1-QUICK | `python` vs `python3` assumption in scripts/README | `tools/test-gate/test-gate.sh:88`; `tools/story-runner/README.md:4-8` |
| ARCH-001 | Architectuur | P2 | Multiple skill sources-of-truth directories | Skills duplication evidence output |
| CQ-001 | Code Quality | P2 | Regex-based YAML parsing in bash test-gate | `tools/test-gate/test-gate.sh:200-240` |
| CQ-002 | Code Quality | P2 | Inconsistent bash strict mode across scripts | `tools/test-gate/test-gate.sh:24`; `tools/skills-sync/sync-skills.sh:2` |
| BUG-001 | Complexity & Bugs | P2 | Duplicate PS1/SH implementations without parity tests | Tool inventory output |
| BUG-002 | Complexity & Bugs | P2 | Space-containing paths increase automation breakage | Skills duplication evidence; `bmad_autopilot_kit/*` filenames |
| TEST-001 | Testing | P2 | No tests for this repo’s tooling | `tests_dirs_count=0` |
| TEST-002 | Testing | P2 | No CI workflows detected | `ci_workflows_count=0` |
| DEP-001 | Dependencies | P2 | No manifests/lockfiles | `manifests_count=0` |
| DEP-003 | Dependencies | P2 | Unpinned requirements; no version checks | `README.md:108-114` |
| SEC-003 | Security | P2 | Missing `SECURITY.md` policy | Repo-wide policy file scan output only includes `./docs/CTO_RULES.md` |
| OPS-001 | Ops/Reliability | P2 | No CI pipelines to run gates | `ci_workflows_count=0` |
| OPS-002 | Ops/Reliability | P2 | No versioning/tags | `git_tags_count=0` |
| OPS-003 | Ops/Reliability | P2 | Copy-only installer causes stale skill drift; strict sync is dangerous | `INSTALL.ps1:29-37`; `tools/skills-sync/sync-skills.sh:67` |
| DOC-003 | Documentation | P2 | Preflight README path mismatch | `tools/preflight/README.md:21-32` |
| DOC-004 | Documentation | P2 | Story runner README references missing `docs/processes` | `tools/story-runner/README.md:4-6`; `find docs ...` output |
| DOC-005 | Documentation | P2 | Handoff doc references non-existent `bmad_autopilot_kit_codex/` | `HANDOFF_2026-01-22.md:67-71` |
| DEVX-001 | Developer Experience | P2 | Windows-first install; no bash installer | `README.md:21-28` |
| DEVX-002 | Developer Experience | P2 | Installer does not install tools into projects | `INSTALL.ps1:56-66` |
| DEVX-003 | Developer Experience | P2 | No end-to-end smoke test / example process to validate install | `tools/story-runner/README.md:4-6`; `find docs ...` output |
| SPEC-001 | Domain/Spec Compliance | P2 | Contract AC format mismatches tool parsers | `docs/CONTRACT.md:34-43`; `tools/preflight/preflight.ps1:143` |
| SPEC-002 | Domain/Spec Compliance | P2 | No reference implementation for assumed processes/stories structure | `tools/story-runner/story_runner.py:3-5`; `find docs ...` output |
| ARCH-002 | Architectuur | P3 | Empty `tools/cto-review/` directory | `ls -la tools/cto-review` output |

## 5) Prioritized Action Plan

1. **Fix P1-CRITICAL: safe sync + safe story execution**
   1. Make `tools/skills-sync/sync-skills.sh` safe-by-default (dry-run default, explicit apply/delete flag, backups).
   2. Add explicit opt-in to run shell commands in `tools/story-runner/story_runner.py`, plus warnings in `tools/story-runner/README.md`.
2. **Fix P1-QUICK: licensing + canonical CTO scan doc + python interpreter detection**
   1. Add `LICENSE` (MIT) and ensure README is consistent.
   2. Align `docs/CTO_RULES.md` with v2 or rename files and update all references.
   3. Make `python3` detection deterministic in scripts and docs.
3. **Address P2: make the repo reliably usable**
   1. Add CI (at least lint + smoke tests + link/path validation).
   2. Add tests for the tooling (parser tests for `story_runner.py`, golden tests for gate scripts).
   3. Reduce drift: pick a single canonical skills directory and remove duplicates; remove/rename space-paths where practical.
   4. Add a minimal `docs/processes/<process>/PROCESS.md` + sample `stories/<process>/` so tools can be validated end-to-end.
4. **P3 cleanup**
   1. Remove or implement `tools/cto-review/`.

## 6) Path to 10/10

Assuming the gaps above are addressed in priority order, expected scores (deterministic from the v2 formula):

| Stage | What’s fixed | Expected Overall Score | Verification (must be objective) |
|---|---|---:|---|
| Baseline | Current state | 8.70 | This report |
| After P1-CRITICAL | SEC-001, SEC-002 | 8.89 | Sync is safe-by-default; story runner requires explicit opt-in and warns loudly |
| After P1-QUICK | DOC-001, DOC-002, DEP-002 | 9.02 | LICENSE exists; docs reference canonical v2 scan; scripts run with `python3` reliably |
| After P2 | All P2 gaps | 9.98 | CI exists and is green; tests cover tooling; docs/paths are consistent; canonical examples exist |
| After P3 | ARCH-002 | 10.00 | No dead modules; repo is internally consistent and automated |
