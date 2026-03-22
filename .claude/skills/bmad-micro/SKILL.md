---
name: bmad-micro
# prettier-ignore
description: Kleine BMAD-route voor mini-wijzigingen met top-tier quality guards, zonder planfile of worktree.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# BMAD Micro

> **Doel**: Voer kleine wijzigingen snel uit **zonder** volledig BMAD-plan en **zonder** eigen worktree, maar **wel** met CTO/universal/repo-10x kwaliteitsbewaking.

## Wanneer gebruiken

**Wel:** button tweak, CSS-fix, copy change, kleine bugfix, kleine config-aanpassing, mini refactor in bestaande file.

**Niet:** nieuwe feature met meerdere schermen/flows, auth, API-contract, migrations, infra, data model, grote refactor, >5 files, of werk dat een eigen branch/worktree verdient.

Als één van die dingen geldt: **STOP** en gebruik `/plan-to-bmad` + `/bmad-bundle`.

## Hard rules

1. **Geen full BMAD ceremony**
   - geen `bmad_input/*.md`
   - geen stories/process files
   - geen aparte worktree

2. **Wel een micro-brief vóór codewijziging**
   Schrijf eerst in-chat of in notities exact deze 6 punten:
   - doel in 1 zin
   - touched paths allowlist
   - out-of-scope
   - relevante CTO Rules
   - relevante universal CTO facetten
   - verificatiecommands

3. **Primary quality gate blijft leidend**
   - als `scripts/quality_gates.py` bestaat: run die vóór afronden
   - draai daarnaast de kleinste relevante lint/test/build checks voor de gewijzigde paden

4. **CTO / universal / repo-10x meenemen**
   - lees `docs/CTO_RULES.md`
   - lees `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` volledig als die bestaat
   - run `python3 scripts/check_repo_10x_contract.py` als die bestaat
   - laat Universal CTO intake expliciet landen in de micro-brief (scope map, facets, P1/P2/P3)

5. **File limits blijven hard**
   - non-test files: max 300 regels, max 15 functies/methods

6. **Escalate vroeg, niet laat**
   Escaleer meteen naar full BMAD als:
   - scope groeit tijdens werk
   - touched paths > 5 files
   - je auth/data/spec/infra raakt
   - je een bestaande slechte structuur alleen met grotere refactor netjes krijgt
   - de wijziging niet meer “klein en lokaal” is

## Micro workflow

1. **Inspecteer** relevante files en bestaande patterns
2. **Maak micro-brief** met quality guards
3. **Voer kleine wijziging uit** in huidige working tree
4. **Valideer diff** tegen:
   - relevante CTO rules
   - relevante universal facetten
   - repo-10x guardrails
5. **Run verificatie**
   - `python3 scripts/quality_gates.py` als aanwezig
   - plus kleinste relevante runtime checks
6. **Rapporteer kort**
   - wat gewijzigd is
   - welke checks groen zijn
   - of je bewust niet naar full BMAD hoefde te escaleren

## Veiligheidsdrempel

Gebruik BMAD Micro alleen als je eerlijk kunt zeggen:
- “dit is een kleine, lokale wijziging”
- “ik verwacht geen architectuurkeuze”
- “ik kan kwaliteit bewaken zonder story/worktree overhead”

Als dat niet waar is: **geen discussie, meteen full BMAD**.
