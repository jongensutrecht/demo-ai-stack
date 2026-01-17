---
name: quick-fix
description: "Ralph Loop Light: test-loop zonder ceremony. Voor kleine bugs, UI fixes, config changes."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# Quick Fix

> **Versie**: 2.0.0
> **Doel**: Kleine fixes snel doorvoeren MET tests, ZONDER ceremony

---

## Wanneer Gebruiken

✅ **Wel quick-fix:**
- Kleine bug (< 50 regels code)
- Button/UI fix
- Config aanpassing
- Dependency update
- API endpoint fix

❌ **Geen quick-fix, gebruik `/bmad-autopilot`:**
- Nieuwe feature
- Meerdere gerelateerde changes
- Architectuur wijziging
- Onzekerheid over aanpak

**Vuistregel:** Als je twijfelt → `/bmad-autopilot`

---

## Wat Skippen We?

| BMAD Ceremony | Quick-fix |
|---------------|-----------|
| Story files | ❌ Skip |
| Worktrees | ❌ Skip |
| CTO review | ❌ Skip |
| Nieuwe agent | ❌ Skip |
| **Tests schrijven** | ✅ **Verplicht** |
| **Test loop** | ✅ **Verplicht** |

---

## Workflow

### STAP 1 - Begrijp de Fix

```
Lees het probleem.
Identificeer EXACT welke file(s) en regel(s).
Bepaal welk type test nodig is:
- UI/Component → Playwright e2e test
- API endpoint → Integration test
- Business logic → Unit test
```

### STAP 2 - Check State

```bash
git status  # Moet schoon zijn
```

### STAP 3 - Fix Loop

```
HERHAAL (max 3x):
  1. Schrijf/update test die fix verifieert
  2. Run test → MOET FALEN (bewijst dat test werkt)
  3. Maak de fix
  4. Run test → MOET SLAGEN
  5. Run ALLE tests

  ALS alle tests groen:
    → STAP 4
  ANDERS:
    → Fix issues, herhaal
```

### STAP 4 - Valideer Alles

```bash
# Lint
ruff check . --fix

# ALLE tests inclusief nieuwe test
pytest tests/ -x --tb=short

# Test gates
bash tools/test-gate/test-gate.sh 2>/dev/null || true
bash tools/invariant-check/invariant-check.sh 2>/dev/null || true
```

**Succes = ALLE checks groen.** Geen uitzonderingen.

### STAP 5 - Commit

```bash
git add -A
git commit -m "<type>(<scope>): <beschrijving>

- Added test: <test file>
- Fixed: <wat was kapot>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Succescriteria

| Criterium | Vereist |
|-----------|---------|
| Nieuwe test geschreven | ✅ Ja |
| Test faalde VOOR fix | ✅ Ja |
| Test slaagt NA fix | ✅ Ja |
| Alle bestaande tests groen | ✅ Ja |
| Ruff check groen | ✅ Ja |

---

## Voorbeeld: Button Fix

**Input:** "Start button doet niks als je klikt"

```
STAP 1:
  - File: components/StartButton.tsx
  - Test nodig: Playwright e2e

STAP 2: git status → clean

STAP 3 - Loop:
  Iteratie 1:
    1. Schrijf: tests/e2e/start-button.spec.ts
       → test('start button triggers action')
    2. Run test → FAIL (button is broken)
    3. Fix: StartButton.tsx onClick handler
    4. Run test → PASS
    5. Run alle tests → PASS

  → Succes na 1 iteratie

STAP 4: ruff ✓, pytest ✓

STAP 5: git commit -m "fix(ui): start button onClick handler

- Added test: tests/e2e/start-button.spec.ts
- Fixed: onClick was not calling startAction()

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Safeguards

| Check | Actie |
|-------|-------|
| > 50 regels changed | STOP → `/bmad-autopilot` |
| 3 iteraties gefaald | STOP → `/bmad-autopilot` |
| Geen test geschreven | STOP → schrijf test eerst |
| Test faalt niet voor fix | STOP → test verifieert niks |

---

## Vergelijking

| Aspect | `/quick-fix` | `/bmad-autopilot` |
|--------|--------------|-------------------|
| Stories | Nee | Ja |
| Worktrees | Nee | Ja |
| CTO review | Nee | 3x |
| Nieuwe agent | Nee | Ja per story |
| **Test schrijven** | **Ja** | **Ja** |
| **Iteratie loop** | **Ja (max 3)** | **Ja (max 3 per story)** |
| Max scope | 50 regels | Onbeperkt |
