---
name: plan-to-bmad
# prettier-ignore
description: Onderzoek een issue en genereer direct BMAD-ready input.
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, Bash, Task
user-invocable: true
---

# Plan to BMAD

> **Doel**: Onderzoek een issue/requirement en genereer direct BMAD-ready input

## Twee Modi

### Modus 1: Direct onderzoek (NIEUW)
```
/plan-to-bmad "beschrijving van wat je wilt"
```
Doet onderzoek + genereert BMAD input in één stap.

### Modus 2: Vanuit bestaand plan
```
/plan-to-bmad <path-naar-plan.md>
```
Transformeert bestaand plan naar BMAD input.

---

## Workflow (Modus 1 - Direct)

```
/plan-to-bmad "Voeg dark mode toe aan de app"
        ↓
1. ONDERZOEK
   - Analyseer codebase (Glob, Grep, Read)
   - Identificeer relevante files
   - Detecteer tech stack
   - Begrijp bestaande patterns
        ↓
2. ONTWERP
   - Definieer P0 (must-have) features
   - Definieer P1 (should-have) features
   - Identificeer risico's (Security, Data Loss, Architecture)
        ↓
3. VALIDEER
   - Vraag verificatie commands per P0
   - Vraag invarianten (wat mag NOOIT?)
        ↓
4. OUTPUT
   - Schrijf bmad_input/<naam>.md
   - Klaar voor /bmad-bundle
```

---

## Hard Rules

1. **Onderzoek EERST**: Geen BMAD output zonder codebase analyse
2. **Verificatie verplicht**: elke P0 feature heeft `[command]` + `[expected]`
3. **P1 risico check**: Security/Data Loss/Architecture risico's identificeren
4. **Tech stack detectie**: uit repo, vraag alleen bij ambiguïteit
5. **File limits**: constraints bevatten max 300 regels, max 20 functies

---

## Onderzoek Checklist

Voordat je output schrijft, beantwoord:

| Vraag | Hoe |
|-------|-----|
| Welke files worden geraakt? | `Glob` + `Grep` |
| Wat is de tech stack? | `package.json`, `pyproject.toml`, etc. |
| Zijn er bestaande patterns? | Lees vergelijkbare code |
| Raakt dit auth/security? | Check of auth code betrokken is |
| Raakt dit data/database? | Check schema, migrations |
| Conflicteert dit met CTO_RULES? | Lees `docs/CTO_RULES.md` |

---

## P1 Risico Identificatie

Check voor elke feature:

| Risico | Trigger | Actie in BMAD |
|--------|---------|---------------|
| **Security** | Raakt auth, API, user data | Voeg security AC toe |
| **Data Loss** | DELETE, UPDATE, migration | Voeg safeguard AC toe |
| **Architecture** | Nieuw pattern, grote refactor | Documenteer in constraints |

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

## Voorbeeld

**Input:**
```
/plan-to-bmad "Voeg soft-delete toe aan items"
```

**Onderzoek output:**
```
Analyseren codebase...
- Gevonden: src/app/api/items/[id]/route.ts (DELETE endpoint)
- Gevonden: prisma/schema.prisma (Item model)
- Pattern: Geen bestaande soft-delete
- Risico: Data Loss (P1-CRITICAL zonder safeguard)
- CTO Rules: CTO-01 (No-Loss) is relevant
```

**BMAD output in `bmad_input/soft-delete-items.md`:**
```markdown
# BMAD Input — Soft Delete Items

## Context
- **Repo:** to-do-jvdp
- **Doel:** Items soft-deleten ipv hard-deleten
- **Tech stack:** Next.js 14, Prisma, PostgreSQL

## Onderzoek Samenvatting
- **Relevante files:**
  - src/app/api/items/[id]/route.ts
  - prisma/schema.prisma
- **Bestaande patterns:** Geen soft-delete aanwezig
- **Risico's:** Data Loss (huidige DELETE is permanent)

## Must-haves (P0)

### P0.1 — Add deletedAt column
- **Requirement:** Item model krijgt nullable deletedAt timestamp
- **Verificatie:** `npx prisma migrate status`
- **Expected:** No pending migrations
- **Risico check:** Data Loss → migration moet reversible zijn

### P0.2 — Update DELETE endpoint
- **Requirement:** DELETE zet deletedAt, verwijdert niet
- **Verificatie:** `curl -X DELETE /api/items/test-id && curl /api/items/test-id`
- **Expected:** Item bestaat nog met deletedAt set
- **Risico check:** N/A

### P0.3 — Filter deleted items
- **Requirement:** Alle queries filteren op deletedAt IS NULL
- **Verificatie:** `npm run test -- --grep "soft delete"`
- **Expected:** All tests pass
- **Risico check:** N/A

## Inverse succesfactoren (NOOIT)

| ID | Invariant | Check |
|----|-----------|-------|
| INV-01 | Hard delete NOOIT zonder admin flag | `rg "DELETE FROM items" --type ts` |

## Constraints

- [ ] `npm run lint` → exit 0
- [ ] `npm run test` → exit 0
- [ ] `npm run build` → exit 0
- [ ] max 300 regels per file
- [ ] max 20 functies per file

## Touched paths

- `prisma/schema.prisma`
- `prisma/migrations/`
- `src/app/api/items/`
- `tests/api/items/`

## CTO Rules Check

- [ ] CTO-01 (No-Loss): ✅ Soft-delete voorkomt data loss
- [ ] CTO-08 (Audit Trail): Voeg delete event toe aan item_events
```

---

## Gerelateerde Skills

- `/bmad-bundle` - Verwerkt de BMAD input
- `/invariant-discovery` - Diepere invariant analyse
- `/cto-guard` - Valideer tegen CTO rules
