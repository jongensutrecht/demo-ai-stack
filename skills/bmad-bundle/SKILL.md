---
name: bmad-bundle
# prettier-ignore
description: Bundled BMAD autopilot with proof-gated Ralph Loop.
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Bundle

Doel: 1 command die stories genereert, valideert, en uitvoert met fix-loops op elke gate. Ralph kan **niet** stoppen zonder proof artefacts.

**v2.0**: CTO Story Scan + Delta-check toegevoegd.

Gebruik: `/bmad-bundle <input_md_path>`

---

## Hard Rules

### 0. WORKTREE ISOLATIE + MAIN-MERGE (VERPLICHT)
**ELKE story MOET in een eigen worktree worden uitgevoerd.**
**Mergen gebeurt ALLEEN in de `main-merge/` folder binnen de overkoepelende worktree.**

**Overkoepelende worktree naam = Process.**
Process = mapnaam van `stories_claude/<Process>/` (of `docs/processes/<Process>/PROCESS.md`).
Voorbeeld: `stories_claude/route_planning/` → `PROCESS="route_planning"`.

**Setup (eenmalig per process):**
```bash
PROCESS="route_planning"
WT_ROOT="worktrees_claude/${PROCESS}"
MERGE_WT="${WT_ROOT}/main-merge"

# Maak merge-worktree
git worktree add -b "merge-${PROCESS}" "$MERGE_WT" origin/main
```

**Per story (verplicht):**
```bash
STORY_ID="API-101"  # pas aan per story
BRANCH="story-${STORY_ID,,}"
STORY_WT="${WT_ROOT}/${STORY_ID}"

git worktree add -b "$BRANCH" "$STORY_WT" origin/main
cd "$STORY_WT"

# Verifieer isolatie
git branch --show-current  # moet $BRANCH zijn
pwd                        # moet $STORY_WT zijn
```

**Merge (alleen in main-merge):**
```bash
cd "$MERGE_WT"
git merge --no-ff "$BRANCH" -m "feat($STORY_ID): <titel>"
```

**Cleanup (na merge):**
```bash
git worktree remove "$STORY_WT"
git branch -d "$BRANCH"
```

**VERBODEN:**
- Direct committen op `main`
- Mergen in de hoofdrepo (alleen in `main-merge/`)
- Meerdere stories in 1 worktree
- Worktree stap overslaan "omdat het sneller is"

**BIJ OVERTREDING:** STOP DIRECT. Werk is ongeldig tot correct uitgevoerd in worktrees.

### 1. FILE LIMITS (VERPLICHT)
**Per niet-test file:**
- **Max 300 regels**
- **Max 20 functies**

**Tests zijn uitgezonderd:** alles onder `tests/`, of bestanden met `.test.` / `.spec.` in de naam.

**VERIFICATIE (voor commit):**
```bash
# Check regels
wc -l "$FILE"  # moet <= 300 zijn

# Check functies (Python)
rg -c "^(async )?def " "$FILE"  # moet <= 20 zijn

# Check functies (JS/TS)
rg -c "^(export )?function |=>\\s*\\{" "$FILE"  # moet <= 20 zijn
```

**BIJ OVERTREDING:** Split file in kleinere modules voordat je verder gaat.

---

### 2. SUBPROCESS PER STORY (VERPLICHT)
**NOOIT stories in huidige context uitvoeren. ALTIJD nieuw subprocess.**

**Waarom:**
- Isolatie van state tussen stories
- Cleane context per story
- Voorkomt dat fouten in story A impact hebben op story B

**HOE:**
```bash
# Gebruik Task tool met subagent
Task(
  prompt="Voer story $STORY_ID uit in worktree $STORY_WT",
  subagent_type="general-purpose"
)
```

**VERBODEN:**
- Stories direct in huidige chat uitvoeren
- Meerdere stories achter elkaar in zelfde context
- "Even snel" een story doen zonder subprocess

**BIJ OVERTREDING:** STOP. Story is ongeldig. Herstart in subprocess.

---

### 3. Proof Gate
`[DONE]` alleen als `output/bmad/<process>/<run_id>/<story_id>/final.json` bestaat, `done=true`, en metadata bevat:
- `run_id`
- `commit_hash`
- `started_at` (ISO-8601)
- `completed_at` (ISO-8601)

### 4. CTO Rules Required
`CTO_RULES.md` moet bestaan. Ontbreekt dit: **STOP** met duidelijke melding.

### 5. NO MOCKS
**VERBODEN:**
- `jest.fn()` zonder echte implementatie
- `mockResolvedValue` zonder integratie test
- `jest.spyOn` die echte functionaliteit vervangt
- Fake data die niet uit fixtures komt

**TOEGESTAAN:**
- Test fixtures met realistische data
- Integration tests met echte database (test DB)
- E2E tests met echte API calls
- Mocks ALLEEN voor externe services (LLM, email, etc.)

### 6. NO FALLBACKS
**VERBODEN:**
- `|| []` fallbacks die bugs verbergen
- `?.` optional chaining zonder null check
- `try/catch` die errors slikt
- Default values die incorrecte state maskeren

**VEREIST:**
- Expliciete error handling
- Fail-fast bij unexpected state
- Validation op inputs
- Assertions op outputs

### 7. 100% COVERAGE
**VEREIST:**
- Alle nieuwe code 100% line coverage
- Alle branches covered
- Alle edge cases getest
- Coverage check in preflight

**VERIFICATIE:**
```bash
npm run test -- --coverage --coverageThreshold='{"global":{"lines":100,"branches":100}}'
```

---

## Workflow

1. **Worktree setup** - Maak process-root + `main-merge/`, en per story een eigen worktree
2. **Repo sanity** - CTO_RULES.md aanwezig en leesbaar
3. **RUN1** - Genereer stories uit input.md
4. **CTO Story Scan** - Check story INHOUD op P1 risico's (fix-loop)
5. **CTO Guard** - Valideer story STRUCTUUR tegen CTO_RULES.md (fix-loop)
6. **Preflight** - violation scan + lint + test + coverage check (fix-loop)
7. **RUN2 (Ralph Loop)** - Voer stories uit met proof artefacts
8. **CTO Repo Scan** - Delta-check: alleen NIEUWE P1/P2 blokkeren (fix-loop)

---

## CTO Story Scan (Stap 4)

Check elke gegenereerde story op P1 risico's in de INHOUD:

| Check | Trigger | Actie |
|-------|---------|-------|
| **Security** | Story beschrijft auth/data endpoint zonder security AC | Voeg security AC toe |
| **Data Loss** | Story beschrijft DELETE/UPDATE zonder safeguard | Voeg soft-delete/backup AC toe |
| **Architecture** | Story conflicteert met bestaande patterns | Pas story aan of documenteer afwijking |

### Fix-Loop Logica

```
while story_has_p1_risk:
    identify_risk()
    fix_story()      # Voeg ontbrekende AC toe, pas beschrijving aan
    rescan_story()

# Pas door naar CTO Guard als CLEAN
```

### Voorbeeld

**Input story:**
```markdown
## AC
- [ ] DELETE /api/items/:id verwijdert item
```

**Scan output:**
```
⚠️ P1-RISK: DELETE endpoint zonder safeguard
   Missing: soft-delete, auth check, audit trail
```

**Fixed story:**
```markdown
## AC
- [ ] DELETE /api/items/:id markeert item als deleted (soft-delete)
- [ ] Alleen item owner of admin kan deleten
- [ ] Delete event wordt gelogd in audit trail
```

---

## CTO Repo Scan (Stap 8)

Na RUN2, scan de code met delta-check:

| Issue Type | Actie |
|------------|-------|
| **Nieuwe P1-CRITICAL** | FIX → RESCAN → moet CLEAN zijn voor merge |
| **Nieuwe P1-QUICK** | FIX → RESCAN |
| **Nieuwe P2** | FIX → RESCAN |
| **Bestaande issues** | Rapport → backlog (blokkeert NIET) |
| **P3** | Rapport → backlog (blokkeert NIET) |

### Delta-Check Logica

```
baseline_issues = get_issues_before_changes()
current_issues = run_cto_scan()
new_issues = current_issues - baseline_issues

while new_issues.has_p1_or_p2:
    fix_issues()
    rescan()
    new_issues = current_issues - baseline_issues

# Merge alleen als geen NIEUWE P1/P2
```

---

## Preflight Checks (Stap 6)

```bash
# Must all pass before RUN2
test -f CTO_RULES.md # exit 0
# Mock/fallback scan: gebruik knowledge/violation-detection.md (grep/rg patterns)
npm run lint          # exit 0
npm run test          # exit 0, 0 failures
npm run test:coverage # 100% lines, 100% branches
npm run build         # exit 0
```

### Fix-Loop Logica

```
while preflight_fails:
    identify_failure()
    fix_code()
    rerun_preflight()

# Pas door naar RUN2 als ALLES PASS
```

---

## Violation Response

Bij violation van hard rules:

1. **IDENTIFY** - Toon exacte violation met locatie
2. **FIX** - Los het probleem op (geen workarounds)
3. **RESCAN** - Verifieer dat fix werkt
4. **CONTINUE** - Ga door naar volgende stap

```
❌ VIOLATION: Mock detected in conversation.test.ts:45
   Found: jest.fn().mockResolvedValue({})
   Required: Real integration test or fixture

   → FIXING: Replacing mock with integration test...
   → RESCAN: Running tests...
   ✅ FIXED: All tests pass with real implementation
```

**NOOIT stoppen en wachten. ALTIJD fixen en door.**
