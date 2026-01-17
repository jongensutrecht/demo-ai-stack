---
name: test-guard
# prettier-ignore
description: Bepaal welke tests nodig zijn en valideer dat ze bestaan.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# Test Guard

> **Versie**: 1.0.0
> **Doel**: Bepaal welke tests verplicht zijn en valideer dat ze bestaan

---

## Wanneer Activeren

- `/test-guard` voor handmatige check
- VOORDAT je "klaar" zegt met code
- Bij elke PR/commit
- Wanneer je twijfelt over test coverage

---

## Workflow

### STAP 1 - Lees Configuratie

```bash
# Lees test requirements
cat test-requirements.yaml

# Lees invariants
cat invariants.md
```

### STAP 2 - Analyseer Changed Files

```bash
# Bepaal welke bestanden gewijzigd zijn
git diff --name-only HEAD~1
# Of voor staged changes
git diff --name-only --staged
```

### STAP 3 - Match Tegen Patterns

Voor elk gewijzigd bestand:
1. Match tegen patterns in `test-requirements.yaml`
2. Bepaal welke testsoorten required zijn
3. Check of die tests bestaan

### STAP 4 - Check Invariant Coverage

Voor elke invariant in `invariants.md`:
1. Parse invariant ID en beschrijving
2. Check of er een NEVER-test bestaat
3. Markeer uncovered invariants

### STAP 5 - Rapport

Genereer rapport:

```markdown
## Test Guard Report

### Changed Files
| File | Required Tests | Status |
|------|---------------|--------|
| src/components/Button.tsx | unit, playwright | ❌ Missing playwright |

### Invariant Coverage
| Invariant | Test Exists | Test File |
|-----------|-------------|-----------|
| INV-SEC-001 | ❌ NO | - |
| INV-BIZ-001 | ✅ YES | tests/invariants/... |

### Verdict
❌ **BLOCKED** - Missing tests:
- Playwright test for Button.tsx
- NEVER-test for INV-SEC-001
```

### STAP 6 - Actie

**Als tests ontbreken:**
1. Stel voor welke tests te schrijven
2. Vraag: "Zal ik deze tests genereren?"
3. Genereer test stubs indien goedgekeurd

**Als alles OK:**
1. Toon ✅ PASS
2. Ga door met implementatie

---

## Hard Rules

1. **NOOIT "klaar" zeggen** zonder test-guard check
2. **NOOIT tests overslaan** die required zijn
3. **ALTIJD invariant coverage** checken
4. **BLOKKEREN** is OK - liever blokkeren dan incomplete tests

---

## Test Type Beslisboom

Zie [knowledge/when-to-use.md](knowledge/when-to-use.md) voor de beslisboom.

---

## NEVER-Test Patterns

Zie [knowledge/invariant-patterns.md](knowledge/invariant-patterns.md) voor hoe NEVER-tests te schrijven.

---

## Gerelateerde Bestanden

- `test-requirements.yaml` - Test requirements per path
- `invariants.md` - Wat mag NOOIT
- `tools/test-gate/test-gate.ps1` - CLI enforcement tool
- `tools/invariant-check/invariant-check.ps1` - Invariant checker
