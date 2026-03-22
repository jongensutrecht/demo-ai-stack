---
name: plan-to-bmad
# prettier-ignore
description: Onderzoek of transformeer en genereer BMAD-ready input (md+json) met verplichte Universal CTO v2.4 intake.
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion
user-invocable: true
---

# Plan to BMAD (main-merge worktree workflow)

> **Doel**: Onderzoek een issue/requirement of transformeer een bestaand plan naar BMAD-ready input (Markdown + JSON) in `bmad_input/`, maar **altijd** op een process-specifieke integration branch in `main-merge` (niet op `main`).

## Twee modi

### Modus 1: Direct onderzoek

`/plan-to-bmad "beschrijving van wat je wilt"`

- Doet repo-onderzoek en genereert BMAD input.

### Modus 2: Vanuit bestaand plan of review

`/plan-to-bmad <path-naar-plan.md>`

- Transformeert een planbestand of CTO-reviewbestand naar BMAD input.

## Hard rules (fail-closed)

1. Schrijf BMAD input **nooit** op `main`; schrijf in een **unieke** process worktree: `worktrees_claude/merge/<process>/main-merge`.
2. Modus 1: geen output zonder repo-onderzoek.
3. Elke P0 heeft EXACT 1 `[command]` + EXACT 1 `[expected]`.
4. Invariants (NOOIT) zijn verplicht.
5. Tech stack detectie: uit repo, vraag alleen bij ambiguiteit.
6. Als `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` bestaat: neem de **volledige Universal CTO intake** mee:
   - `in scope`
   - `out of scope`
   - `UNKNOWN external state`
   - relevante facetten
   - kandidaat P1/P2/P3 delta-risico's
7. Als `scripts/check_repo_10x_contract.py` of `scripts/quality_gates.py` bestaat: verwerk repo-10x guardrails expliciet in constraints en touched paths.
8. File limits: constraints bevatten max 300 regels + max 15 functies per niet-test file (tests uitgezonderd).
9. Als `docs/CTO_RULES.md` bestaat: koppel elke P0 aan >= 1 CTO Rule ID + Facet.
10. P1/P2/P3 moeten altijd expliciet aanwezig zijn (ook als `None`).
11. Geen TODO's/open eindjes in output.

## Workflow

### 0) Bootstrap: process `main-merge` worktree (verplicht)

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
GIT_COMMON_DIR="$(git -C "$REPO_ROOT" rev-parse --git-common-dir)"
COMMON_ABS="$(cd "$REPO_ROOT" && cd "$GIT_COMMON_DIR" && pwd -P)"
PRIMARY_ROOT="$(dirname "$COMMON_ABS")"

PROCESS="<process>"
WT_ROOT="${PRIMARY_ROOT}/worktrees_claude/merge/${PROCESS}"
MERGE_WT="${WT_ROOT}/main-merge"
MERGE_BRANCH="${PROCESS}"

test ! -e "$MERGE_WT"
git -C "$PRIMARY_ROOT" worktree add -b "$MERGE_BRANCH" "$MERGE_WT" main
cd "$MERGE_WT"
```

### 1) Analyse → BMAD input

1. Lees plan of description (modus detectie).
2. Onderzoek relevante files, patterns, risico's, touched paths allowlist en bronnen.
3. Lees `docs/CTO_RULES.md` als die bestaat.
4. Lees `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` volledig als die bestaat.
5. Leg Universal CTO intake vast:
   - scope map
   - facet applicability (`Applicable` / `N/A` / `UNKNOWN`)
   - kandidaat-gaps / delta-risico's met P1/P2/P3
6. Extraheer: P0/P1/P2/P3, invariants, constraints, out-of-scope.
7. Vraag ontbrekende verificatie/invariants (max 4 vragen) en STOP als incompleet.
8. Schrijf output in `MERGE_WT`:
   - `bmad_input/<process>.md`
   - `bmad_input/<process>.json`
   volgens `knowledge/bmad-template.md`.

### 2) Commit (verplicht; determinisme)

```bash
cd "$MERGE_WT"
git add bmad_input/"$PROCESS".md bmad_input/"$PROCESS".json
git commit -m "bmad_input($PROCESS): add BMAD input"
```

## Minimale Universal CTO intake die in de output moet landen

- `in scope`
- `out of scope`
- `UNKNOWN external state`
- relevante facetten
- kandidaat P1/P2/P3 risico's
- relevante CTO rule mapping
- repo-10x impact / SSOT impact
- voldoende context voor latere `Facet Scores Overview`
- eerste `Path to 10/10` richting / closure-pad

## Gerelateerde Skills

- `/cto-guard` - volledige Universal CTO Review v2.4
- `/bmad-micro` - kleine lokale wijziging zonder full BMAD
- `/bmad-bundle` - proof-gated RUN2 + merge-gating
