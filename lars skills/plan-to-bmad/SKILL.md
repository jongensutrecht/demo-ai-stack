---
name: plan-to-bmad
# prettier-ignore
description: Onderzoek of transformeer en genereer BMAD-ready input (md+json) met verplichte Universal CTO v2.5 intake.
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion
user-invocable: true
---

# Plan to BMAD (main-merge worktree workflow)

> **Doel**: Onderzoek een issue/requirement of transformeer een bestaand plan naar BMAD-ready input (Markdown + JSON) in `bmad_input/`, maar **altijd** op een process-specifieke integration branch in `main-merge` (niet op `main`).

## Twee modi

### Modus 1: Direct onderzoek

`/skill:plan-to-bmad "beschrijving van wat je wilt"`

- Doet repo-onderzoek en genereert BMAD input.

### Modus 2: Vanuit bestaand plan of review

`/skill:plan-to-bmad <path-naar-plan.md>`

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
12. **Universele guards gelden** — lees `~/.pi/agent/skills/_guards.md` en pas alle guards toe.
16. **Elke story met runtime-wijzigingen moet TDD specificeren** - benoem expliciet welke falende test(s) eerst geschreven moeten worden vóór implementatie. Dit maakt TDD zichtbaar in het plan, niet alleen afgedwongen door de uitvoerder.
17. **Elke story moet een regressie-scope benoemen** — benoem expliciet welke bestaande tests/paden na de change nog steeds groen moeten zijn. Minimaal: touched modules + directe afhankelijkheden + het gate-commando.
18. **ACs moeten het hele facet dekken, niet alleen een smal punt** — als een story bedoeld is om facet X te verbeteren, dan moet de AC het volledige facet meten, niet alleen één voorbeeld. Concreet: een AC die 5 van 21 strings checkt is ongeldig. Een AC die "grep vindt X in sourcecode" checkt zonder runtime-bewijs is ongeldig. Een AC die alleen nieuw gedrag afdwingt maar bestaande schendingen negeert is ongeldig.
19. **Bewijs moet bewijs zijn** — een AC-verificatie die alleen checkt of code bestaat (grep/rg) zonder te bewijzen dat het werkt (runtime/e2e/output) is geen geldig bewijs voor runtime-facetten. Onderscheid expliciet: code-presence check vs runtime-behavior proof.
20. **Verboden woorden in story ACs** — ACs mogen niet als verificatie gebruiken: `works correctly`, `renders properly`, `is fixed`, `passes`. Vervang door bewijsbare criteria met concrete command + expected output.

## 10/10-kader voor BMAD-input

Universele guards: zie `~/.pi/agent/skills/_guards.md`. BMAD-specifieke aanvulling:

- vertaalt onderzoek naar een **transformatiestrategie**, niet naar een TODO-lijst
- maakt voor een volgende uitvoerder meteen duidelijk waarom deze stories de repo/product merkbaar dichter bij 10/10 brengen

## Autonomous state machine (Pi contract)

Treat `/skill:plan-to-bmad` as an explicit preparation state machine.

### States

1. **INPUT_CLASSIFY**
   - Detect: direct problem statement vs existing plan/review file.
   - Success -> `BOOTSTRAP_WORKTREE`
   - Failure -> `BLOCKED`

2. **BOOTSTRAP_WORKTREE**
   - Create or enter the process-specific `main-merge` worktree.
   - Success -> `REPO_RESEARCH`
   - Failure -> `BLOCKED`

3. **REPO_RESEARCH**
   - Read relevant repo files, rules, patterns, sources of truth.
   - For large codebases (50+ files): use Serena (`/skill:serena`) for symbol overview and dependency tracing instead of exhaustive grep. Check `tmux has-session -t serena` first; start server if needed.
   - Success -> `CTO_INTAKE`
   - Failure -> `BLOCKED`

4. **CTO_INTAKE**
   - Build explicit Universal CTO scope map, facets, P1/P2/P3 risks, invariants, constraints.
   - Success -> `VERIFY_COMPLETENESS`

5. **VERIFY_COMPLETENESS**
   - If essential verification/invariants are missing and cannot be derived: ask at most the documented questions.
   - If still incomplete -> `BLOCKED`
   - Else -> `WRITE_BMAD_INPUT`

6. **WRITE_BMAD_INPUT**
   - Write `bmad_input/<process>.md` + `.json`.
   - Success -> `COMMIT_INPUT`
   - Failure -> `BLOCKED`

7. **COMMIT_INPUT**
   - Commit deterministically in `main-merge`.
   - Success -> `DONE`

8. **DONE / BLOCKED**
   - Terminal states only.
   - Do not stop after research notes or half-filled BMAD input.

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
2. Lees `LEARNINGS.md` in de repo root als die bestaat (laatste 10 entries). Lees `~/.pi/agent/skills/compound-learning/LEARNINGS_GLOBAL.md` als die bestaat (laatste 5 entries). Verwerk relevante learnings als extra constraints of risico's in het plan.
3. Onderzoek relevante files, patterns, risico's, touched paths allowlist en bronnen.
4. Lees `docs/CTO_RULES.md` als die bestaat.
4. Lees `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` volledig als die bestaat.
5. Als `openspec/` bestaat: lees bestaande specs (`openspec/specs/*.md`, `openspec/changes/*/specs/*/spec.md`) en bepaal per story welke specs geraakt worden. Per story die een spec raakt: benoem expliciet dat de spec mee-geüpdatet moet worden. Dit voorkomt dat je achteraf ontdekt dat een story een spec breekt.
5. Leg Universal CTO intake vast:
   - scope map
   - facet applicability (`Applicable` / `N/A` / `UNKNOWN`)
   - kandidaat-gaps / delta-risico's met P1/P2/P3
6. Extraheer: P0/P1/P2/P3, invariants, constraints, out-of-scope.
7. Vorm dit om tot **3-7 hoge-hefboommoves** met volgorde, doelbeeld en proof of done; vermijd micro-story versnippering.
8. Per story met runtime-wijzigingen: benoem welke falende test(s) eerst geschreven moeten worden (TDD).
9. Per story: benoem de regressie-scope - welke bestaande tests/paden na de change nog groen moeten zijn.
10. Vraag ontbrekende verificatie/invariants (max 4 vragen) en STOP als incompleet.
9. Schrijf output in `MERGE_WT`:
   - `bmad_input/<process>.md`
   - `bmad_input/<process>.json`
   volgens `knowledge/bmad-template.md`, plus expliciet:
   - `10/10 Kader` (wat wel / niet)
   - `Path to 10/10` (waarom deze volgorde en waarom dit geen lui plan is)

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
- per story: waarom high leverage, doelbeeld, niet-doen, proof of done
- per story met runtime-wijzigingen: welke falende test(s) eerst (TDD-spec)
- per story: regressie-scope (bestaande tests/paden die groen moeten blijven)
- per story: welke OpenSpec specs geraakt worden en mee-geüpdatet moeten worden (als `openspec/` bestaat)

## Wat géén geldig stopmoment is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Skill-specifiek:

Stop **niet** op:
- alleen repo-onderzoek zonder BMAD input files
- alleen een scope- of risico-overzicht
- een half ingevulde `.md` zonder `.json`
- een paar open TODO's/invariants die nog niet fail-closed zijn gemaakt

## Gerelateerde Skills

- `/skill:cto-guard` - volledige Universal CTO Review v2.5
- `/skill:bmm` - kleine lokale wijziging zonder full BMAD
- `/skill:bmad-bundle` - proof-gated RUN2 + merge-gating
