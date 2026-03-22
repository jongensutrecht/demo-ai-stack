---
name: bmad-bundle
# prettier-ignore
description: Bundled BMAD autopilot met proof-gated Ralph Loop en verplichte Universal CTO Review v2.4 gates.
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Bundle

Doel: deterministische BMAD-run met:
- process-specifieke `main-merge` integration worktree
- per-story worktrees/branches
- proof gate via `output/bmad/<process>/<run_id>/<story_id>/final.json`
- **volledige Universal CTO Review v2.4** vóór story-uitvoering én vóór final merge

Gebruik: `/bmad-bundle <input_md_path>`

## Hard Rules (fail-closed)

1. **Nooit** BMAD artefacten committen op `main`.
2. RUN2 **moet** draaien vanuit `main-merge`.
3. `[DONE]` alleen als proof bestaat en `done=true`.
4. Lees en respecteer altijd:
   - `docs/CTO_RULES.md`
   - `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` (als aanwezig)
   - `scripts/quality_gates.py` (primary gate, als aanwezig)
   - `scripts/check_repo_10x_contract.py` (als aanwezig)
   - `scripts/check_file_limits.py` (als aanwezig)
5. **Volledige CTO Guard review is verplicht** op twee momenten:
   - vóór RUN2 op BMAD input + stories
   - na RUN2 / vóór final merge op de werkelijke delta
6. Storys mogen niet alleen CTO rule mapping hebben; ze moeten ook Universal CTO context behouden:
   - `in scope`
   - `out of scope`
   - `UNKNOWN external state`
   - relevante facetten
   - relevante P1/P2/P3 risico's
7. P3 mag nooit verdwijnen uit rapportage; als er geen P3 is, schrijf expliciet `None`.
8. File limits blijven hard: max 300 regels + max 15 functies per niet-test file.

## Workflow

### 0) Bootstrap `main-merge` worktree (uniek per process)

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
GIT_COMMON_DIR="$(git -C "$REPO_ROOT" rev-parse --git-common-dir)"
COMMON_ABS="$(cd "$REPO_ROOT" && cd "$GIT_COMMON_DIR" && pwd -P)"
PRIMARY_ROOT="$(dirname "$COMMON_ABS")"

INPUT_MD="<input_md_path>"
PROCESS="$(python3 -c 'import os,re,sys; p=os.path.basename(sys.argv[1]); p=p[:-3] if p.endswith(".md") else p; p=p.strip().lower(); p=re.sub(r"[^a-z0-9]","_",p); p=re.sub(r"_+","_",p).strip("_"); print(p)' "$INPUT_MD")"
RUN_ID="$(python3 -c 'from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))')"

WT_ROOT="${PRIMARY_ROOT}/worktrees_claude/merge/${PROCESS}"
MERGE_WT="${WT_ROOT}/main-merge"
MERGE_BRANCH="${PROCESS}"

test ! -e "$MERGE_WT"
git -C "$PRIMARY_ROOT" worktree add -b "$MERGE_BRANCH" "$MERGE_WT" main
cd "$MERGE_WT"
```

### 1) Governance preflight (verplicht)

Controleer minimaal:
- `docs/CTO_RULES.md`
- `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` (als aanwezig)
- `scripts/bmad_bundle.py`
- `scripts/quality_gates.py` (als aanwezig)
- `scripts/check_repo_10x_contract.py` (als aanwezig)
- `scripts/check_file_limits.py` (als aanwezig)

Run waar aanwezig:

```bash
test -f scripts/quality_gates.py && python3 scripts/quality_gates.py || true
test -f scripts/check_repo_10x_contract.py && python3 scripts/check_repo_10x_contract.py || true
test -f scripts/check_file_limits.py && python3 scripts/check_file_limits.py || true
```

### 2) Init run metadata

```bash
cd "$MERGE_WT"
python3 scripts/bmad_bundle.py init --input "$INPUT_MD" --run-id "$RUN_ID"
```

### 3) RUN1: stories + BACKLOG schrijven

Stories moeten naast standaard AC/verificatie ook Universal CTO context behouden.
Minimaal per story of per process-spec:
- relevante CTO Rules
- relevante facetten
- expliciete `in scope` / `out of scope` / `UNKNOWN external state`
- expliciete P1/P2/P3 risico's of `None`

```bash
cd "$MERGE_WT"
git add stories_claude/"$PROCESS"/
git commit -m "stories($PROCESS): add RUN1 bundle ($RUN_ID)"
```

### 4) CTO Guard review #1 (verplicht vóór RUN2)

Review target:
- `bmad_input/<process>.md`
- `bmad_input/<process>.json`
- `stories_claude/<process>/**`

De review moet de **volledige Universal CTO Review v2.4 output** bevatten:
- Executive Summary
- Facet Scores Overview
- Per-facet detail
- Consolidated Gap Table
- Prioritized Action Plan
- Path to 10/10

Fail-closed:
- unresolved P1 / P2 in de story bundle -> fix eerst, pas daarna RUN2
- P3 -> expliciet rapporteren, maar blokkeert niet

### 5) RUN2 (proof-gated loop; geen eindpunt)

```bash
cd "$MERGE_WT"
python3 scripts/bmad_bundle.py run2 --process "$PROCESS" --run-id "$RUN_ID"
python3 scripts/bmad_bundle.py check --process "$PROCESS" --run-id "$RUN_ID"
```

Tijdens RUN2 geldt:
- huidige story eerst afmaken
- volgende story pas na `DONE` of `BLOCKED`
- als context oploopt op een actieve story: same-story handoff naar een verse sessie, daarna dezelfde story hervatten

### 6) Quality gates + CTO end checks (verplicht)

Run in `main-merge`:

```bash
python3 scripts/quality_gates.py
test -f scripts/check_repo_10x_contract.py && python3 scripts/check_repo_10x_contract.py || true
test -f scripts/check_file_limits.py && python3 scripts/check_file_limits.py || true
```

### 7) CTO Guard review #2 (verplicht vóór final merge)

Review target:
- de werkelijke code/doc delta in `main-merge`
- proof artefacts
- backlog status

Deze review gebruikt opnieuw de **volledige Universal CTO Review v2.4 output**.

Merge policy:
- nieuwe unresolved `P1-CRITICAL`, `P1-QUICK` of `P2` -> **blokkeer merge**
- `P3` -> expliciet naar backlog / action plan, blokkeert niet
- `UNKNOWN external state` -> expliciet tonen met exact 1 verificatie-check

### 8) Final merge (alleen na expliciete GO)

```bash
cd "$REPO_ROOT"
git checkout main
git merge --no-ff "$MERGE_BRANCH" -m "merge($PROCESS): $RUN_ID"
git worktree remove "$MERGE_WT"
```

## Minimale done-definitie

Een BMAD bundle run is pas echt klaar als:
- proof gate groen is
- repo-native gates groen zijn
- CTO Guard review #1 volledig is uitgevoerd
- CTO Guard review #2 volledig is uitgevoerd
- P1/P2 blockers weg zijn
- P3 expliciet is gerapporteerd (of `None`)
 -m "merge($PROCESS): $RUN_ID"
git worktree remove "$MERGE_WT"
```

## Minimale done-definitie

Een BMAD bundle run is pas echt klaar als:
- proof gate groen is
- repo-native gates groen zijn
- CTO Guard review #1 volledig is uitgevoerd
- CTO Guard review #2 volledig is uitgevoerd
- P1/P2 blockers weg zijn
- P3 expliciet is gerapporteerd (of `None`)
