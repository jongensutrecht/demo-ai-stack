# Plan to BMAD (Codex)

Je bent Codex. Spreek Nederlands. Werk non-interactive.

## Doel

Onderzoek een issue/requirement en genereer direct BMAD-ready input.

---

## Twee Modi

- Modus 1: Direct onderzoek (REQUIREMENT)
- Modus 2: Vanuit bestaand plan (PLAN_PATH of PLAN_TEXT)

---

## Input (kies 1 modus)

### Modus 1 - Direct onderzoek

**REQUIREMENT:** (VERPLICHT - vul in voor je plakt)
```
[Beschrijf hier wat je wilt bouwen/fixen]
```

---

### Modus 2 - Vanuit bestaand plan

**PLAN_PATH:** (optioneel, voorkeur)
```
/pad/naar/plan.md
```

**PLAN_TEXT:** (optioneel)
```
[Plak hier het plan als tekst]
```

Gebruik PLAN_PATH als die is ingevuld; anders PLAN_TEXT. Als beide leeg zijn: stop en vraag om input.

---

## Workflow

### Modus 1 - Direct onderzoek

1. ONDERZOEK (codebase) - zie Onderzoek checklist
2. ONTWERP - definieer P0/P1, identificeer P1 risico's
3. VALIDEER - elke P0 heeft verificatie command + expected; voeg invarianten toe
4. OUTPUT - schrijf bmad_input/<naam>.md

### Modus 2 - Vanuit bestaand plan

1. LEES PLAN - cat PLAN_PATH of gebruik PLAN_TEXT; extraheer features/requirements/scope
2. ONDERZOEK CODEBASE - bevestig relevante files/patterns met Glob/Grep
3. DETECTEER STACK - uit repo (package.json, pyproject.toml, go.mod, Cargo.toml)
4. VALIDEER - elke P0 heeft verificatie command + expected; voeg invarianten toe
5. OUTPUT - schrijf bmad_input/<naam>.md

---

## Onderzoek checklist

Beantwoord deze vragen met bewijs:

| Vraag | Hoe | Bewijs |
|-------|-----|--------|
| Welke files worden geraakt? | `rg -l "<pattern>"` | [lijst paden] |
| Wat is de tech stack? | Lees `package.json`, `pyproject.toml`, etc. | [stack] |
| Zijn er bestaande patterns? | Lees vergelijkbare code | [beschrijving] |
| Raakt dit auth/security? | Check of auth code betrokken is | [ja/nee + bewijs] |
| Raakt dit data/database? | Check schema, migrations | [ja/nee + bewijs] |
| Conflicteert dit met CTO_RULES? | Lees `docs/CTO_RULES.md` | [ja/nee + welke regel] |

## P1 Risico Identificatie

Check voor elke feature:

| Risico | Trigger | Actie in BMAD |
|--------|---------|---------------|
| **Security** | Raakt auth, API, user data | Voeg security AC toe |
| **Data Loss** | DELETE, UPDATE, migration | Voeg safeguard AC toe |
| **Architecture** | Nieuw pattern, grote refactor | Documenteer in constraints |

---

## Features

**P0 (Must-have):** Features die MOETEN werken
- Elke P0 heeft een verificatie command + expected output

**P1 (Should-have):** Nice-to-haves
- Alleen als tijd over

---

## Output Format

Schrijf naar `bmad_input/<naam>.md`:

```markdown
# BMAD Input — [NAAM]

## Context
- **Repo:** [repo naam]
- **Doel:** [wat moet er gebeuren]
- **Tech stack:** [gedetecteerd]

## Onderzoek Samenvatting
- **Relevante files:** [lijst]
- **Bestaande patterns:** [beschrijving]
- **Risico's geïdentificeerd:** [P1 risks]

## Must-haves (P0)

### P0.1 — [Feature]
- **Requirement:** [specifiek wat moet werken]
- **Verificatie:** `[command]`
- **Expected:** `[output]`
- **Risico check:** [Security/Data Loss/Architecture - of N/A]

## Should-haves (P1)

### P1.1 — [Nice-to-have]
- **Requirement:** [specifiek]

## Inverse succesfactoren (NOOIT)

| ID | Invariant | Check |
|----|-----------|-------|
| INV-01 | [Wat NOOIT mag] | `[command]` |

## Constraints

- [ ] `npm run lint` → exit 0
- [ ] `npm run test` → exit 0
- [ ] `npm run build` → exit 0
- [ ] max 300 regels per file
- [ ] max 20 functies per file

## Touched paths (allowlist)

- `src/[paths]/`
- `tests/[paths]/`

## CTO Rules Check

- [ ] CTO-XX: [relevant rule] → [hoe dit plan voldoet]
```

---

## Hard Rules

1. **Onderzoek EERST** - Geen BMAD output zonder codebase analyse
2. **Verificatie verplicht** - Elke P0 feature heeft `[command]` + `[expected]`
3. **P1 risico check** - Security/Data Loss/Architecture risico's identificeren
4. **Tech stack detectie** - Uit repo, vraag alleen bij ambiguïteit
5. **File limits** - Constraints bevatten max 300 regels, max 20 functies

---

## Eindresultaat

- `bmad_input/<naam>.md` geschreven
- Klaar voor `/bmad-bundle` of `UITVOER_PROMPT_codex.md`

---

## Gebruik

1. Plak deze prompt in Codex terminal
2. Vul REQUIREMENT of PLAN_PATH/PLAN_TEXT in
3. Codex doet onderzoek of plan-transformatie en genereert BMAD input
4. Gebruik output als `BMAD_INPUT_FILE` voor UITVOER_PROMPT
