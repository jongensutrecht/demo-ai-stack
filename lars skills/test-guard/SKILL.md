---
name: test-guard
# prettier-ignore
description: Bepaal welke tests nodig zijn en valideer dat ze bestaan.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# Test Guard

> **Doel**: Bepaal welke tests verplicht zijn, valideer dat ze bestaan, en blokkeer luie "klaar"-claims zonder voldoende bewijs.

## Wanneer Activeren

- `/test-guard` voor handmatige check
- VOORDAT je "klaar" zegt met code
- Bij elke PR/commit
- Bij elke runtime- of contractwijziging

## 10/10-kader voor testselectie

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Test-specifiek:

- kies de **kleinste voldoende** testset die het gewijzigde gedrag bewijst
- koppel changes aan runtime-paden, invarianten en regressierisico
- NEVER/invariant-paden zijn hard blokkerend
- "tests bestaan al" telt niet zonder inhoudelijke dekkingsvalidatie

## Workflow

1. **Lees test-SSOT**
   - `test-requirements.yaml` als aanwezig
   - `invariants.md` als aanwezig
   - repo docs zoals `docs/START_HERE.md`, `docs/SOURCES_OF_TRUTH.md`, `AGENTS.md`
   - bestaande test-configs (`pyproject.toml`, `package.json`, `pytest.ini`, `vitest.config.*`, etc.)

2. **Analyseer changes**
   - `git diff --name-only`
   - als geen diff beschikbaar is: bepaal expliciet scope-bestanden uit de taak
   - groepeer changes naar runtime pad, UI pad, contract pad, invariant pad, config/build pad

3. **Map change -> required bewijs**
   - per changed path: welk gedrag kan kapot gaan?
   - welk testtype hoort daarbij: unit, integration, e2e, API, visual, contract, migration, invariant
   - bepaal minimale benodigde set, niet de grootste set

4. **Check bestaande dekking**
   - zoek bestaande tests die dit pad aantoonbaar raken
   - valideer inhoudelijk of die tests het gedrag bewijzen
   - "zelfde bestandsnaam" of "zelfde map" telt niet als bewijs
   - tests die skippen (skip markers, CI excludes) tellen niet als dekking
   - tests die alleen code-presence checken (grep) zijn geen bewijs voor runtime-gedrag
   - als de change een breder probleem moest fixen: de testdekking moet het HELE probleem coveren, niet alleen het smalle gewijzigde stuk

5. **Check invariants / NEVER-tests**
   - elke invariant met impact op de change moet een concrete NEVER-test of equivalent bewijs hebben
   - ontbreekt die: blokkeer

6. **Rapporteer**
   - required tests
   - bestaande dekking
   - ontbrekende dekking
   - verdict: voldoende / onvolledig / blokkerend

7. **Actie**
   - genereer test stubs alleen als dat de repo-conventie volgt
   - anders: beschrijf exact welke test moet worden toegevoegd of gedraaid

## Hard Rules

1. **NOOIT "klaar" zeggen** zonder test-guard check
2. **NOOIT tests overslaan** die required zijn
3. **BLOKKEREN is OK** - liever blokkeren dan incomplete tests
4. **Universele guards gelden** — zie `~/.pi/agent/skills/_guards.md`
5. **Prefer smallest sufficient set** - run niet standaard alles; kies de kleinste set die het risico eerlijk dekt
6. **Invariant coverage is hard** - changes die NEVER-paden kunnen raken zonder NEVER-test zijn non-compliant

## Rapportformat

```markdown
# Test Guard Report

## Scope
- Changed paths: <paths>
- Runtime paths geraakt: <samenvatting>

## Required Tests
| Path / gedrag | Risico | Vereist testtype | Bewijs / command |
|---|---|---|---|
| ... | ... | ... | ... |

## Existing Coverage
- <testbestand of suite> - dekt wel/niet omdat ...

## Missing / Blocking
- <ontbrekende test of ontbrekend bewijs>

## Verdict
- `SUFFICIENT`
- `INCOMPLETE`
- `BLOCKING`
```

## Beslisboom

Zie [knowledge/when-to-use.md](knowledge/when-to-use.md)

## NEVER-Test Patterns

Zie [knowledge/invariant-patterns.md](knowledge/invariant-patterns.md)

## Test Type Voorbeelden

```bash
python scripts/examples.py unit        # Unit test voorbeeld
python scripts/examples.py playwright  # E2E test voorbeeld
python scripts/decide.py               # Beslisboom
```

## Wat géén geldig stopmoment of succesclaim is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Test-specifiek:

- "er zijn al tests" zonder inhoudelijke dekkingscheck
- de hele suite aanraden zonder change-mapping
- missing invariant tests als "later doen" noteren
