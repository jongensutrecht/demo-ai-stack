---
name: test-guard
# prettier-ignore
description: Bepaal welke tests nodig zijn en valideer dat ze bestaan.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# Test Guard

> **Doel**: Bepaal welke tests verplicht zijn en valideer dat ze bestaan

## Wanneer Activeren

- `/test-guard` voor handmatige check
- VOORDAT je "klaar" zegt met code
- Bij elke PR/commit

## Workflow

1. **Lees config** - `test-requirements.yaml`, `invariants.md`
2. **Analyseer changes** - `git diff --name-only`
3. **Match patterns** - Bepaal required tests per file
4. **Check invariants** - Elke invariant heeft NEVER-test nodig
5. **Rapport** - Toon missing tests
6. **Actie** - Genereer test stubs indien nodig

## Hard Rules

1. **NOOIT "klaar" zeggen** zonder test-guard check
2. **NOOIT tests overslaan** die required zijn
3. **BLOKKEREN is OK** - liever blokkeren dan incomplete tests

## Beslisboom

Zie [knowledge/when-to-use.md](knowledge/when-to-use.md)

## NEVER-Test Patterns

Zie [knowledge/invariant-patterns.md](knowledge/invariant-patterns.md)

## Test Type Voorbeelden

```bash
python scripts/examples.py unit        # Unit test voorbeeld
python scripts/examples.py playwright  # E2E test voorbeeld
python scripts/decide.py              # Beslisboom
```
