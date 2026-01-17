---
name: ralph-loop
# prettier-ignore
description: Continue iteratie loop voor BMAD stories. Itereert tot alle stories [DONE].
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# Ralph Loop

> **Versie**: 2.0.0
> **Doel**: Automatische iteratie over BMAD stories tot completion met test enforcement

---

## Wanneer Activeren

- `/ralph-loop` voor handmatige start
- Automatisch via `/bmad-autopilot`

---

## Vereiste Input

**BACKLOG.md moet bestaan** in `stories/<Process>/BACKLOG.md`

Als geen BACKLOG: STOP fail-closed met instructie om eerst `/bmad-autopilot` te runnen.

---

## Workflow

### STAP 1 - Lees BACKLOG.md

```bash
# Vind open stories
grep -E "\[TODO\]|\[IN_PROGRESS\]" stories/<Process>/BACKLOG.md
```

### STAP 2 - Pak Volgende Story

Prioriteit:
1. Eerst `[IN_PROGRESS]` (hervatten)
2. Dan eerste `[TODO]`

### STAP 3 - Voer Story Uit

⚠️ **KRITIEK - LEES DIT EERST:**
- **NOOIT** stories zelf uitvoeren in de huidige context window
- **ALTIJD** een nieuw claude subprocess spawnen per story
- **WACHT** tot subprocess klaar is voordat je doorgaat (blocking call)
- De subprocess heeft zijn eigen verse context en voert de story uit
- Jij (de orchestrator) doet ALLEEN: spawn → wait → update status → next

```bash
# Start nieuw Claude window voor story (VERPLICHT)
claude --dangerously-skip-permissions \
  -p "Voer story <STORY_ID> uit. Story: stories/<Process>/<STORY_ID>.md"
```

**Story Agent Workflow (in subprocess):**
1. Lees CLAUDE.md
2. Lees story file
3. **Lees Test Requirements sectie**
4. **Schrijf NEVER-tests voor gelinkte invariants**
5. **Schrijf required tests (unit/integration/playwright)**
6. Implementeer story taken
7. **Run Gate A (uitgebreid):**
   - ruff check
   - pytest
   - test-gate.ps1
   - invariant-check.ps1
8. CTO Guard #3 post-execution check

**Waarom subprocess?**
- Elke story krijgt verse context (geen rommel van vorige stories)
- Voorkomt context exhaustion
- Isolatie: als story faalt, blijft orchestrator intact

### STAP 4 - Update Status

Na story completion:
- Success → `[DONE]`
- Failure (3x) → `[BLOCKED]`
- Nog bezig → `[IN_PROGRESS]`

### STAP 5 - Check Completion

```
Als alle stories [DONE] of [BLOCKED]:
  Output: <promise>RALPH_COMPLETE</promise>
Anders:
  Terug naar STAP 2
```

---

## BACKLOG.md Format

Zie [knowledge/backlog-format.md](knowledge/backlog-format.md)

---

## Gate A (Uitgebreid)

Elke story moet deze gate passeren:

```bash
# 1. Lint
ruff check .

# 2. All tests
pytest

# 3. Test Requirements Gate
pwsh tools/test-gate/test-gate.ps1 -RepoRoot .
# Exit 1 als required tests ontbreken

# 4. Invariant Coverage Gate
pwsh tools/invariant-check/invariant-check.ps1 -RepoRoot .
# Exit 1 als invariants geen NEVER-tests hebben
```

Alle vier moeten exit 0 geven.

---

## Safeguards

| Safeguard | Waarde |
|-----------|--------|
| Max iterations | `stories × 3` |
| Max attempts per story | 3 |
| Circuit breaker | 5 loops zonder progress → STOP |

---

## Failure Handling

### Test Gate Failure
```
Story OPS-003 failed test-gate:
- Missing playwright test for components/Modal.tsx

Action: Create tests/e2e/modal.spec.ts
Retry: 1/3
```

### Invariant Check Failure
```
Story OPS-004 failed invariant-check:
- Uncovered invariant: INV-SEC-001

Action: Create tests/invariants/auth/test_never_auth_bypass.py
Retry: 1/3
```

---

## Gerelateerde Skills

- `/bmad-autopilot` - Genereert stories en BACKLOG.md
- `/cto-guard` - Valideert code na elke story
- `/test-guard` - Test requirements validatie
