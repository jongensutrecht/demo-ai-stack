---
name: debug
# prettier-ignore
description: Gerichte probleemanalyse - onderzoek ZONDER te fixen.
allowed-tools: Read, Grep, Glob, Task, Bash
user-invocable: true
---

# Debug - Gerichte Probleemanalyse

> **REGEL #1: NIETS AANPASSEN. Alleen onderzoeken en rapporteren.**

## Wanneer Gebruiken

- `/debug <probleem beschrijving>`
- `/debug` (vraagt om context)

## Analyse Framework

### 1. Probleem Definiëren
- Wat is het EXACTE symptoom?
- Wanneer gebeurt het? (altijd, soms, onder welke condities?)
- Wat is het VERWACHTE gedrag vs ACTUELE gedrag?

### 2. 5 Whys - Root Cause
Vraag 5x "waarom?" tot je bij de kern bent:
```
Symptoom → Why? → Why? → Why? → Why? → ROOT CAUSE
```

### 3. Blast Radius Check
- Welke andere code raakt dit?
- Welke functies/modules zijn afhankelijk?
- Kan dit elders ook spelen?

### 4. Silent Failure Scan
- Worden errors ergens gesluikt? (`catch` zonder log)
- Zijn er `|| []` of `|| {}` fallbacks die problemen maskeren?
- Returned iets `null/undefined` waar dat niet verwacht wordt?

### 5. Assumption Check
- Welke aannames maak IK over de code?
- Welke aannames maakt DE CODE die fout kunnen zijn?
- Is de data wel zoals verwacht?

### 6. Gerelateerde Issues
- Zijn er MEER problemen dan het gemelde?
- Wat valt nog meer op tijdens onderzoek?
- Zijn er warnings/deprecations?

## Output Format

```markdown
## Debug Rapport: [korte titel]

### Symptoom
[Exacte beschrijving wat er misgaat]

### Root Cause (5 Whys)
1. Why: ...
2. Why: ...
3. Why: ...
4. Why: ...
5. ROOT CAUSE: ...

### Bewijs
- [file:line] - [wat je zag]
- [file:line] - [wat je zag]

### Blast Radius
- [wat nog meer geraakt wordt]

### Silent Failures Gevonden
- [ ] Geen / [x] Ja: [beschrijving]

### Gerelateerde Issues
- [andere problemen die opvielen]

### Aanbevolen Fix (NIET UITVOEREN)
[Wat zou de oplossing zijn - ter info]
```

## Hard Rules

1. **GEEN code wijzigen** - alleen lezen en analyseren
2. **GEEN "snelle fix"** - eerst volledig begrip
3. **Altijd 5 Whys doorlopen** - niet stoppen bij symptoom
4. **Check ALTIJD silent failures** - dit is vaak de boosdoener
5. **Rapporteer ALLES** wat opvalt, ook als het niet direct gerelateerd lijkt
