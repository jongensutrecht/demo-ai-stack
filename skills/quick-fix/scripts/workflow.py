#!/usr/bin/env python3
"""Quick-fix workflow details.

Usage:
    python workflow.py          # Show workflow
    python workflow.py example  # Show voorbeeld
    python workflow.py compare  # Vergelijk met bmad-autopilot
"""
import sys

WORKFLOW = """
## Quick-fix Workflow

### STAP 1 - Begrijp de Fix
- Lees het probleem
- Identificeer EXACT welke file(s) en regel(s)
- Bepaal test type: Playwright (UI), Integration (API), Unit (logic)

### STAP 2 - Check State
```bash
git status  # Moet schoon zijn
```

### STAP 3 - Fix Loop (max 3x)
```
1. Schrijf/update test die fix verifieert
2. Run test → MOET FALEN (bewijst dat test werkt)
3. Maak de fix
4. Run test → MOET SLAGEN
5. Run ALLE tests
```

### STAP 4 - Valideer Alles
```bash
ruff check . --fix
pytest tests/ -x --tb=short
```

### STAP 5 - Commit
```bash
git add -A
git commit -m "<type>(<scope>): <beschrijving>

- Added test: <test file>
- Fixed: <wat was kapot>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

## Succescriteria

| Criterium | Vereist |
|-----------|---------|
| Nieuwe test geschreven | JA |
| Test faalde VOOR fix | JA |
| Test slaagt NA fix | JA |
| Alle bestaande tests groen | JA |
| Ruff check groen | JA |
"""

EXAMPLE = """
## Voorbeeld: Button Fix

**Input:** "Start button doet niks als je klikt"

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
"""

COMPARE = """
## Vergelijking

| Aspect | /quick-fix | /bmad-autopilot |
|--------|------------|-----------------|
| Stories | Nee | Ja |
| Worktrees | Nee | Ja |
| CTO review | Nee | 3x |
| Nieuwe agent | Nee | Ja per story |
| Test schrijven | JA | JA |
| Iteratie loop | Ja (max 3) | Ja (max 3 per story) |
| Max scope | 50 regels | Onbeperkt |

## Safeguards

| Check | Actie |
|-------|-------|
| > 50 regels changed | STOP → /bmad-autopilot |
| 3 iteraties gefaald | STOP → /bmad-autopilot |
| Geen test geschreven | STOP → schrijf test eerst |
| Test faalt niet voor fix | STOP → test verifieert niks |
"""

def main():
    if len(sys.argv) < 2:
        print(WORKFLOW)
        return

    cmd = sys.argv[1].lower()
    if cmd == "example":
        print(EXAMPLE)
    elif cmd == "compare":
        print(COMPARE)
    else:
        print(f"Unknown: {cmd}")
        print("Usage: python workflow.py [example|compare]")

if __name__ == "__main__":
    main()
