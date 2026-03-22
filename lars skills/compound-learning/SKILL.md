---
name: compound-learning
description: Extraheer learnings uit runs, reviews en audits en sla ze op zodat toekomstige sessies slimmer starten. Automatisch na bmad-bundle, cto-guard, jaw-drop-audit of jaw-drop-ui-audit.
allowed-tools: Read, Bash, Write, Edit
user-invocable: true
---

# Compound Learning

> **Doel**: Na elke significante run worden concrete learnings opgeslagen zodat toekomstige sessies dezelfde fouten niet herhalen en dezelfde patronen sneller herkennen.

## Wanneer activeren

### Automatisch (na afloop van)
- `bmad-bundle` — na DONE of BLOCKED
- `cto-guard` — na volledige review
- `jaw-drop-audit` — na verdict + plan
- `jaw-drop-ui-audit` — na verdict + plan

### Handmatig
```
/skill:compound-learning
/skill:compound-learning <pad-naar-review-of-run-output>
```

## Waar learnings worden opgeslagen

| Scope | Locatie | Wanneer |
|---|---|---|
| Repo-specifiek | `LEARNINGS.md` in repo root | standaard |
| Repo-specifiek (Serena) | `.serena/memories/learnings.md` | als Serena actief is |
| Globaal | `~/.pi/agent/skills/compound-learning/LEARNINGS_GLOBAL.md` | cross-repo patronen |

## Wat een learning is

Een learning is een **concrete, bewezen observatie** uit een echte run, review of audit die toekomstige sessies beter maakt.

### Format per entry

```markdown
### <datum> — <skill> — <repo>
**Categorie**: pattern | edge-case | false-positive | missing-guard | repo-specifiek
**Wat**: <concrete observatie in 1-2 zinnen>
**Waarom relevant**: <impact op toekomstige runs>
**Guard/check**: <wat je voortaan moet checken of doen>
**Bron**: <welke review/audit/run/story dit opleverde>
```

## Wat een learning NIET is

- een herhaling van wat al in `_guards.md` of skill-instructies staat
- een generieke best practice
- een dagboekentry of statusupdate
- een TODO of actie-item (die horen in backlog/stories)
- een speculatieve observatie zonder bewijs uit een echte run

## Workflow

### 1. Verzamel ruwe observaties
Na de afgeronde skill, scan:
- CTO review gaps en canonical gaps
- audit facet-scores en de bijbehorende bewijzen
- story BLOCKED-redenen
- remediation loops die nodig waren
- edge cases die guards misten
- false positives die productiviteit kostten
- patronen die in meerdere stories/facetten terugkwamen

### 2. Filter op echte waarde
Behoud alleen observaties die:
- concreet en specifiek zijn (niet "tests zijn belangrijk")
- bewezen zijn door een echte run (niet theoretisch)
- actionable zijn (er is iets concreets dat je voortaan anders kunt doen)
- niet al gedekt worden door bestaande guards/skills

### 3. Schrijf learnings
Per learning het format hierboven. Maximaal 5 learnings per run — kies de meest impactvolle.

### 4. Dedupliceer
Check bestaande `LEARNINGS.md`:
- als een learning al bestaat: update bewijs/datum, voeg niet opnieuw toe
- als een learning verouderd is: archiveer naar `## Archief` onderaan het bestand

### 5. Archiveer bij overflow
- Repo-specifiek: max 50 actieve entries. Bij overflow: oudste naar `## Archief`.
- Globaal: max 30 actieve entries. Bij overflow: oudste naar `## Archief`.

## Hoe learnings terugvloeien

### Bij start van elke substantiële skill
Skills die plannen, reviews, audits of changes produceren:
- lees de laatste 10 entries uit de repo-specifieke `LEARNINGS.md` als die bestaat
- lees de laatste 5 entries uit `LEARNINGS_GLOBAL.md` als die bestaat
- gebruik deze als extra context bij planning, review of audit

### Concreet
- `cto-guard`: check of bekende patronen uit learnings terugkomen in de review
- `bmad-bundle`: neem relevante learnings mee als constraints in stories
- `jaw-drop-*`: check of eerder geïdentificeerde UI/code-patronen weer opduiken
- `plan-to-bmad`: verwerk relevante learnings in scope/risico-analyse

## Hard rules

1. **Alleen bewezen observaties** — geen speculatie, geen "zou kunnen"
2. **Max 5 per run** — kies de meest impactvolle, geen exhaustieve dump
3. **Universele guards gelden** — zie `~/.pi/agent/skills/_guards.md`
4. **Geen duplicaten** — check bestaande learnings voordat je toevoegt
5. **Archiveer, verwijder niet** — oude learnings gaan naar archief, worden niet gewist

## Initieel bestand aanmaken

Als `LEARNINGS.md` nog niet bestaat in de repo:

```markdown
# Learnings

Concrete, bewezen observaties uit runs, reviews en audits die toekomstige sessies slimmer maken.

---

(nog geen learnings — wordt automatisch gevuld na de eerste bmad-bundle, cto-guard of audit run)

---

## Archief
```

## Wat géén geldig stopmoment of output is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Skill-specifiek:

- een learning die alleen "we moeten beter testen" zegt
- een dump van alle review-opmerkingen zonder filtering
- learnings opschrijven zonder te dedupliceren tegen bestaande entries
