---
name: bmad-bundle
# prettier-ignore
description: Bundled BMAD autopilot met proof-gated Ralph Loop en verplichte Universal CTO Review v2.5 gates.
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Bundle

Doel: deterministische BMAD-run met:
- process-specifieke `main-merge` integration worktree
- per-story worktrees/branches
- proof gate via `output/bmad/<process>/<run_id>/<story_id>/final.json`
- **volledige Universal CTO Review v2.5** vóór story-uitvoering én vóór final merge

Gebruik: `/skill:bmad-bundle <input_md_path>`

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
9. **Universele guards gelden** - lees `~/.pi/agent/skills/_guards.md` en pas alle guards toe op stories, reviews en uitvoering.

## 10/10-kader voor BMAD bundle

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Bundle-specifieke aanvulling:

- reviews zijn volledig en sturen de inhoud echt bij; ze zijn geen formaliteit
- de finale delta is merge-ready én aantoonbaar sterker op craft, maintainability en repo-discipline
- CTO review mag niet gereduceerd worden tot een kort verdict zonder gap table / path to 10/10

## Autonomous state machine (Pi contract)

Treat `/skill:bmad-bundle` as an explicit state machine, not as prose.

### States

1. **BOOTSTRAP**
   - Preconditions: input file exists, repo governance files readable.
   - Action: create process slug, `RUN_ID`, and `main-merge` worktree.
   - Success -> `GOVERNANCE_PREFLIGHT`
   - Failure -> `BLOCKED`

2. **GOVERNANCE_PREFLIGHT**
   - Action: read required governance files and run mandatory preflight checks.
   - Success -> `RUN1_GENERATE`
   - Failure -> `BLOCKED`

3. **RUN1_GENERATE**
   - Action: generate `stories_claude/<process>/` + `BACKLOG.md`.
   - Hard rule: all stories must be `ready-for-dev`; `drafted` is fail-closed.
   - Hard rule: stories must be high-leverage, non-generic, and include goal image + proof expectation; reject lazy micro-story fragmentation.
   - Hard rule: ACs must cover the FULL facet the story targets, not just one narrow example. If a story aims to fix naming consistency, the AC must check ALL naming violations, not 5 of 21. If a story aims to fix error handling, the AC must cover all error paths, not just the happy path.
   - Hard rule: AC verification must match the claim. Code-presence checks (grep/rg) are not valid proof for runtime behavior. Runtime claims need runtime proof (e2e, API calls, logs, screenshots).
   - Success -> `CTO_REVIEW_1`
   - Failure -> `BLOCKED`

4. **CTO_REVIEW_1**
   - Action: full CTO Guard review on BMAD input + stories.
   - Success -> `RUN2_SELECT_STORY`
   - Failure -> `BLOCKED`

5. **RUN2_SELECT_STORY**
   - Action: select exactly one active story from backlog.
   - If no open story remains -> `QUALITY_AND_REVIEW_2`
   - Else -> `STORY_TRACK_START`

6. **STORY_TRACK_START**
   - Action: call `bmad_story_state` with process/run/story/worktree/branch before implementation starts.
   - Success -> `STORY_IMPLEMENT`

7. **STORY_IMPLEMENT**
   - Action: implement the story in its story worktree.
   - Update `bmad_story_state` during execution with `nextStep`, `nextCommands`, `lastChecks`, `lastCtoVerdict`.
   - On context pressure -> `HANDOFF`
   - Hard rule: if implementation drifts into cosmetic-only work or loses the original high-leverage goal, remediate scope immediately before continuing.
   - Hard rule: for runtime changes, write a failing test for the desired behavior BEFORE writing implementation code (TDD red-green).
   - Hard rule: for refactors, renames, or moves in codebases with 50+ files, use Serena (`/skill:serena`) for symbol lookup, referencing symbols and rename operations instead of manual grep+edit. Check `tmux has-session -t serena` first; start server if needed.
   - Hard rule: if the story identified OpenSpec specs that are affected, update those specs AS PART of the implementation — not after. Code change + spec update is one atomic unit.
   - Success -> `STORY_VERIFY`
   - Failure -> `STORY_REMEDIATE` or `BLOCKED` depending on evidence

8. **STORY_VERIFY**
   - Action: run proof/verification for the current story.
   - Hard rule: for stories with runtime changes, verification MUST include e2e testing against a running app — not just unit tests, lint, or type checks. Start the app (tmux, fixed port), run real requests/browser tests, and capture proof in `test-results/`. Unit tests alone are not sufficient proof that the feature works.
   - Hard rule: no mocks as final proof. Mocks are for unit isolation only. The story verify step must prove the feature works end-to-end against real runtime.
   - Hard rule: if the story touches UI, capture before/after screenshots as proof.
   - Hard rule: after ACs pass, verify the FULL facet scope — not just the narrow AC. If the story targeted "naming consistency" and the AC checked 5 strings, scan for ALL remaining violations before marking done. AC groen ≠ facet opgelost. The AC is the floor, the facet improvement is the goal.
   - Hard rule: if remaining violations exist outside the AC scope, either fix them in this story or explicitly document them as known remaining gap with count and evidence.
   - Hard rule: run the facet-coverage sweep below and include the output in proof. Story is NOT done if the sweep shows remaining violations that are not explicitly documented.

### Facet-coverage sweep (verplicht in STORY_VERIFY)

Na AC groen, draai een geautomatiseerde sweep voor het facet dat deze story targetde.
Schrijf het resultaat naar `output/bmad/<process>/<run_id>/<story_id>/facet-sweep.json`.

```bash
python3 - <<'SWEEP'
import json, subprocess, sys, os

# --- Configuratie: vul in per story ---
FACET = os.environ.get("FACET", "unknown")
DESCRIPTION = os.environ.get("FACET_DESC", "")
# Violation-detecting commands: elk command retourneert 1 regel per violation.
# Pas deze lijst aan per story/facet. Voorbeelden:
# - naming: rg -l 'TODO|FIXME|HACK' src/ --glob '!tests/'
# - NL strings: rg -n "hardcoded_nl_pattern" src/
# - error handling: rg -n 'except:$|except Exception:$' src/ --glob '!tests/'
# - file limits: python3 scripts/check_file_limits.py 2>&1 | grep FAIL
COMMANDS = json.loads(os.environ.get("SWEEP_COMMANDS", "[]"))

results = []
total_violations = 0
for cmd in COMMANDS:
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        lines = [l for l in out.stdout.strip().splitlines() if l.strip()]
        results.append({"command": cmd, "violations": len(lines), "sample": lines[:10]})
        total_violations += len(lines)
    except Exception as e:
        results.append({"command": cmd, "error": str(e)})

sweep = {
    "facet": FACET,
    "description": DESCRIPTION,
    "total_violations": total_violations,
    "passed": total_violations == 0,
    "checks": results,
}

out_dir = os.environ.get("SWEEP_OUT", ".")
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, "facet-sweep.json")
with open(path, "w") as f:
    json.dump(sweep, f, indent=2)
print(json.dumps(sweep, indent=2))
if total_violations > 0:
    print(f"\n⚠ {total_violations} remaining violations for facet '{FACET}'", file=sys.stderr)
    sys.exit(1)
SWEEP
```

**Hoe te gebruiken per story:**
1. Stel environment vars in met het facet en de detectie-commands:
   ```bash
   export FACET="naming_consistency"
   export FACET_DESC="All source files use English naming, no Dutch abbreviations"
   export SWEEP_COMMANDS='["rg -l dutch_pattern src/ --glob !tests/", "rg -n TODO src/"]'
   export SWEEP_OUT="output/bmad/<process>/<run_id>/<story_id>"
   ```
2. Draai het script.
3. `passed: true` → story mag door.
4. `passed: false` → fix remaining violations of documenteer ze expliciet met count in de story.

**De agent pakt de SWEEP_COMMANDS uit de standaard catalogus:** `knowledge/facet-sweep-commands.md`. Die catalogus bevat voorgedefinieerde detectie-commands voor alle 10 jaw-drop facetten, alle repo-10x facetten (A-I), en JS/TS varianten. De agent hoeft alleen het juiste facet op te zoeken en eventueel repo-specifieke commands toe te voegen. Alleen als het facet niet in de catalogus staat, mag de agent zelf commands bedenken — en moet documenteren waarom.

   - Success -> `STORY_MERGE`
   - Recoverable failure -> `STORY_REMEDIATE`
   - Non-recoverable failure -> `BLOCKED`

9. **STORY_REMEDIATE**
   - Action: fix the current story only, then re-run `STORY_VERIFY`.
   - Must be a productive repair loop with new evidence.
   - Repeated unrecoverable failure -> `BLOCKED`

10. **STORY_MERGE**
   - Action: merge completed story into `main-merge`, mark story via `bmad_story_state` as `done`.
   - **Immediately** transition to `RUN2_SELECT_STORY`. Do NOT stop, report, or ask the user. Just continue.
   - Failure -> `BLOCKED`

11. **HANDOFF**
   - Trigger: context usage >= 80% OR you cannot safely continue in this session.
   - Trigger is NOT: "a story just finished". Finishing a story is not a handoff reason.
   - Action: same-story continuation to fresh session.
   - Hard rule: resume into the SAME story, not the next story.
   - Success -> `STORY_IMPLEMENT`
   - Failure -> `BLOCKED`

12. **QUALITY_AND_REVIEW_2**
   - Action: run end gates + full CTO Guard review #2 on real delta.
   - Success -> `WAIT_FOR_GO`
   - Failure -> `BLOCKED`

13. **WAIT_FOR_GO**
   - Action: stop only before final merge to `main`.
   - Explicit GO -> `FINAL_MERGE`

14. **FINAL_MERGE**
   - Action: final merge only after explicit GO.
   - Success -> `DONE`

15. **DONE / BLOCKED**
   - Terminal states only.
   - Do not stop on plan, RUN1, single-story completion, first verify fail, or first CTO review.

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
- `LEARNINGS.md` in repo root (als aanwezig) — lees laatste 10 entries en verwerk als extra constraints/risico's
- `~/.pi/agent/skills/compound-learning/LEARNINGS_GLOBAL.md` (als aanwezig) — lees laatste 5 entries

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
- expliciet **waarom deze move high leverage is**
- expliciet **doelbeeld na implementatie**
- expliciet **niet doen / anti-scope-creep grenzen**
- expliciet **proof of done**
- per story: welke OpenSpec specs geraakt worden en mee-geüpdatet moeten worden (als `openspec/` bestaat). Dit is geen afterthought — als een story gedrag wijzigt dat in een spec staat, moet de spec-update onderdeel zijn van de story, niet een losse cleanup achteraf.

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

De review moet de **volledige Universal CTO Review v2.5 output** bevatten:
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
- **Na story DONE/BLOCKED: pak DIRECT de volgende story.** Niet stoppen, niet rapporteren, niet vragen. Gewoon doorgaan. De enige reden om te pauzeren is context-druk (zie hieronder).
- **Bij start van elke story**: zet `bmad_story_state` met process/run/story/worktree/branch
- update `bmad_story_state` tijdens uitvoering met `nextStep`, `nextCommands`, `lastChecks`, `lastCtoVerdict`
- markeer story via `bmad_story_state` als `done` of `blocked` voordat je naar de volgende story gaat
- **Handoff is ALLEEN bij context-druk (>= 80%)**, niet na elke story. Als context ruim is: doorwerken. Handoff = je kunt niet meer verder in deze sessie, niet "ik ben klaar met een story".
- Normale compaction is NIET de primaire route voor actieve BMAD stories

### 5b) Context Handoff (bij sessie-wissel)

**Trigger**: >= 80% context usage, of bij onzekerheid over repo state / failing tests / volgende stap.

**Locatie**: `output/bmad/<process>/<run_id>/<story_id>/handoff.md`

**Template** (gebaseerd op Claude Code, Cursor, Aider, Devin, OpenHands best practices):

```markdown
# Handoff

## Objective
<één zin: wat moet deze story bereiken>

## Done definition
- <acceptance criterion 1>
- <acceptance criterion 2>

## Current state
- Process: <process>
- Run: <run_id>
- Story: <story_id>
- Worktree: <absolute path>
- Branch: <branch name>
- Commit: <sha indien relevant>
- Files in focus: <paths>

## Verified (evidence-backed)
- <feit> - evidence: <command/artifact>
- <feit> - evidence: <command/artifact>

## Assumptions (niet geverifieerd)
- <hypothese>

## Unknowns (open vragen)
- <wat moet nog uitgezocht>

## Completed so far
- <change/test/result>
- <change/test/result>

## Decisions
- <beslissing> - because <reden> - evidence: <pointer>

## Next step (exact, copy-paste)
- Run: `<exact command>`
- Inspect: <wat te checken>
- Expected: <verwacht resultaat>

## Constraints / do-not-break
- <invariant>
- <user decision>
- <non-goal>

## Blockers
- <indien aanwezig>

## Evidence pointers
- <artifact path 1>
- <artifact path 2>
```

**Principes**:
- **Checkpoint, geen summary**: alleen wat nodig is om correct door te gaan
- **Feiten vs aannames scheiden**: voorkom hallucinatie in nieuwe sessie
- **Exact volgende stap**: één duidelijke actie, geen vijf vage opties
- **Evidence wijzen, niet kopiëren**: geen giant logs in handoff

### 6) Quality gates + CTO end checks (verplicht)

Run in `main-merge`:

```bash
python3 scripts/quality_gates.py
test -f scripts/check_repo_10x_contract.py && python3 scripts/check_repo_10x_contract.py || true
test -f scripts/check_file_limits.py && python3 scripts/check_file_limits.py || true
```

### 6a) OpenSpec validatie (verplicht als openspec/ bestaat)

Als de repo een `openspec/` directory heeft: valideer dat alle specs nog kloppen na de hele run.

```bash
test -d openspec/ && openspec validate --all --strict --no-interactive
```

- Moet groen zijn. Stale of gebroken specs na een run = niet merge-ready.
- Als een story gedrag heeft gewijzigd maar de spec niet is geüpdatet: dat is een regressie-bom. Fix de spec.

### 6b) E2e regressie suite (verplicht als de repo e2e tests heeft)

Na alle stories, draai de **volledige** e2e/integration test suite tegen een draaiende app — niet alleen de per-story tests.

```bash
# Start de app als die niet al draait
# Gebruik tmux + fixed port zoals gedocumenteerd in de repo

# Python repos:
test -f pytest.ini -o -f pyproject.toml && python3 -m pytest tests/ -x -q

# Node repos:
test -f package.json && npm test

# Playwright e2e (als aanwezig):
test -d e2e/ && npx playwright test
test -d tests/e2e/ && npx playwright test tests/e2e/

# Repo-specifiek script (als aanwezig):
test -f scripts/verify.sh && ./scripts/verify.sh
```

Dit vangt regressies die per-story tests niet dekken: interacties tussen stories, gebroken paden die geen story raakte, en side effects.

- Moet groen zijn. Falende e2e = niet merge-ready.
- Als tests falen op paden die geen story raakte: dat is een regressie. Fix het of documenteer als known gap met bewijs.

### 6c) Docker build (verplicht als Dockerfile/docker-compose aanwezig)

Als de repo een `Dockerfile` of `docker-compose.yml` heeft: **herbouw na elke story en vóór final merge**.

Run in `main-merge`:

```bash
# docker-compose repo:
docker compose build

# Alleen Dockerfile:
docker build -t <image-naam> .

# Of via repo-specifiek script:
test -f scripts/verify.sh && ./scripts/verify.sh
test -f scripts/deploy.sh && ./scripts/deploy.sh --dry-run
```

- Build moet slagen. Falende build = story is **niet DONE**.
- Als `scripts/verify.sh` of `scripts/deploy.sh` bestaan: gebruik die (ze runnen gates + build).
- Docker build is onderdeel van de proof gate, niet optioneel.

### 7) CTO Guard review #2 (verplicht vóór final merge)

Review target:
- de werkelijke code/doc delta in `main-merge`
- proof artefacts
- backlog status

Deze review gebruikt opnieuw de **volledige Universal CTO Review v2.5 output**.

Merge policy:
- nieuwe unresolved `P1-CRITICAL`, `P1-QUICK` of `P2` -> **blokkeer merge**
- `P3` -> expliciet naar backlog / action plan, blokkeert niet
- `UNKNOWN external state` -> expliciet tonen met exact 1 verificatie-check

### 7b) Jaw-drop audit (verplicht vóór final merge)

Na de CTO Guard review, voer een jaw-drop code audit uit op de delta:

- Lees `/home/mrbiggles/.pi/agent/skills/jaw-drop-audit/SKILL.md`
- Beoordeel de gewijzigde code op de 10 craft-facetten
- Overall score < 7.0 → rapporteer concrete verbeterpunten, blokkeer niet maar documenteer
- Overall score ≥ 7.0 → door naar merge
- AI-fingerprint check is verplicht onderdeel

Dit is een craft-check, geen compliance-check. De CTO Guard bewaakt structuur. De jaw-drop audit bewaakt of de code **mooi** is.

### 8) Final merge (alleen na expliciete GO)

```bash
cd "$REPO_ROOT"
git checkout main
git merge --no-ff "$MERGE_BRANCH" -m "merge($PROCESS): $RUN_ID"
git worktree remove "$MERGE_WT"
```

## Path to 10/10 (verplicht denkkader tijdens de run)

Tijdens RUN1, CTO reviews en RUN2 moet expliciet toetsbaar blijven:
- waarom deze story-volgorde de hoogste hefboom heeft
- welke structurele gaps eerst verdwijnen en welke polish bewust later komt
- waarom de bundle niet vervalt in micro-story drukte of cosmetische voortgang
- wat 10/10 voor deze process-run concreet WEL en NIET betekent

## Minimale done-definitie

Een BMAD bundle run is pas echt klaar als:
- proof gate groen is
- repo-native gates groen zijn
- **e2e tests tegen draaiende app zijn groen** voor elke story met runtime changes (unit tests alleen is niet genoeg)
- **facet-coverage sweep is groen** (`facet-sweep.json` per story, `passed: true`) of resterende violations zijn expliciet gedocumenteerd met count
- **OpenSpec validatie groen** (als `openspec/` bestaat) — `openspec validate --all --strict --no-interactive` moet passen
- **volledige e2e/regressie suite groen** tegen draaiende app — niet alleen per-story tests maar de hele suite
- **docker build groen is** (als Dockerfile/docker-compose aanwezig)
- CTO Guard review #1 volledig is uitgevoerd
- CTO Guard review #2 volledig is uitgevoerd
- **jaw-drop audit is uitgevoerd** met score en AI-fingerprint check
- alle stories zijn naar `DONE` of hard `BLOCKED` getransitioned
- P1/P2 blockers weg zijn
- P3 expliciet is gerapporteerd (of `None`)
- **compound-learning is uitgevoerd** — max 5 learnings geëxtraheerd en opgeslagen in `LEARNINGS.md` (repo) en/of `LEARNINGS_GLOBAL.md` (globaal). Zie `/skill:compound-learning`.

## Wat géén geldig stopmoment is

Stop **niet** op:
- alleen init/preflight
- alleen RUN1 output
- een enkele story die klaar is terwijl backlog nog open staat
- eerste verify-fail zonder remediation-besluit
- eerste CTO review zonder vervolgactie
- een handoff-bericht zonder daadwerkelijke hervatting
- een statusrapport aan de gebruiker terwijl de state machine nog niet in `DONE` of `BLOCKED` staat
Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`.
