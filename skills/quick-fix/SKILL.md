---
name: ralph-loop-light
# prettier-ignore
description: Ralph Loop Light: test-loop zonder ceremony. Voor kleine bugs, UI fixes.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# Quick Fix

> **Doel**: Kleine fixes snel doorvoeren MET tests, ZONDER ceremony

## Wanneer Gebruiken

**Wel:** Kleine bug (<50 regels), UI fix, config, dependency update
**Niet:** Nieuwe feature, architectuur wijziging → `/start-bmad-ralph`

## Wat Skippen We?

| Skip | Verplicht |
|------|-----------|
| Stories, Worktrees, CTO review | ❌ |
| **Tests schrijven** | ✅ |
| **Test loop** | ✅ |

## Workflow

1. **Begrijp** - Welke file(s), welk test type nodig
2. **Check** - `git status` moet schoon zijn
3. **Fix Loop** (max 3x):
   - Schrijf test → Run → MOET FALEN
   - Maak fix → Run → MOET SLAGEN
   - Run ALLE tests
4. **Valideer** - `ruff check`, `pytest`
5. **Commit**

Details: `python scripts/workflow.py`

## Safeguards

| Check | Actie |
|-------|-------|
| > 50 regels | STOP → `/start-bmad-ralph` |
| 3 iteraties fail | STOP → `/start-bmad-ralph` |
| Geen test | STOP → schrijf test eerst |
| File > 300 regels of > 20 functies (niet-test) | STOP → splits file (tests uitgezonderd) |

## Voorbeeld

`python scripts/workflow.py example`
