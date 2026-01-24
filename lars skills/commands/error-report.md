# Error Report Generator + Auto-Debug

Genereer foutenrapport EN los automatisch op. Geen handmatige tussenstappen.

**Gebruik:** `/error-report [beschrijving]` of `/error-report` (interactief)

**Flow:** Rapport maken → Analyseren → Fixen → Valideren → Klaar

---

## PROCEDURE (VOLG EXACT - VOLLEDIG AUTOMATISCH)

### STAP 1: INPUT VERZAMELEN

Als `$ARGUMENTS` leeg is, vraag:
1. **Wat ging er mis?** (korte beschrijving)
2. **Wanneer?** (tijdens welke actie/command)
3. **Reproduceerbaar?** (ja/nee/soms)

Als `$ARGUMENTS` gevuld is, gebruik die als startpunt.

### STAP 2: CONTEXT OPHALEN

Verzamel AUTOMATISCH (geen user input nodig):

```
[ ] Console output/error messages (laatste relevante output)
[ ] Relevante logbestanden (check output/, logs/, *.log)
[ ] Recente file changes (git diff als git repo)
[ ] Huidige working directory status
[ ] Relevante config files (.env, config.py, etc.)
```

### STAP 3: CLASSIFICATIE

Bepaal automatisch:

| Veld | Opties |
|------|--------|
| **Type** | Runtime Error / Logic Bug / Test Failure / Config Issue / Integration Error / Performance / Unknown |
| **Ernst** | Critical (blokkeert werk) / High (workaround mogelijk) / Medium (irritant) / Low (cosmetisch) |
| **Scope** | Single file / Module / Cross-module / System-wide |
| **Reproduceerbaarheid** | Always / Sometimes / Rare / Unknown |

### STAP 4: RAPPORT GENEREREN

Maak bestand: `docs/debug-reports/{YYYY-MM-DD}_{korte-naam}.md`

**Template:**

```markdown
# Error Report: {korte beschrijving}

**Datum:** {datum}
**Type:** {type}
**Ernst:** {ernst}
**Scope:** {scope}
**Reproduceerbaarheid:** {reproduceerbaarheid}

---

## Symptomen

{Wat de gebruiker zag/ervaarde}

## Context

**Command/Actie die faalde:**
```
{command of actie}
```

**Error output:**
```
{volledige error message indien beschikbaar}
```

**Relevante bestanden:**
- {bestand1}: {waarom relevant}
- {bestand2}: {waarom relevant}

## Omgeving

- **Working directory:** {pad}
- **Relevante configs:** {lijst}
- **Recent gewijzigd:** {bestanden indien git beschikbaar}

## Eerste Observaties

{Jouw initiële analyse - wat valt op?}

```

### STAP 5: AUTOMATISCH DOORGAAN NAAR DEBUG

**GEEN STOP - GA DIRECT DOOR**

Toon kort:
```
Rapport: docs/debug-reports/{filename}.md
Type: {type} | Ernst: {ernst}
→ Start automatische debug...
```

---

## FASE 2: AUTOMATISCHE DEBUG (uit /debug-report)

### STAP 6: TRIAGE

- [ ] Classificeer fout (Syntax/Runtime/Logic/Integration/Config/Data)
- [ ] Bepaal scope (welke bestanden betrokken?)
- [ ] Quick wins check (typos, missing imports, config mismatch?)

### STAP 7: EVIDENCE GATHERING

- [ ] Trace error naar origin
- [ ] Lees ALLE relevante code (geen aannames)
- [ ] Check inputs, outputs, transformaties
- [ ] Bouw timeline (wanneer werkte het wel?)

### STAP 8: HYPOTHESES

Genereer minimaal 3 hypotheses:
| # | Hypothese | Waarschijnlijkheid | Test |
|---|-----------|-------------------|------|
| 1 | ... | Hoog/Medium/Laag | ... |
| 2 | ... | Hoog/Medium/Laag | ... |
| 3 | ... | Hoog/Medium/Laag | ... |

### STAP 9: VERIFICATIE

Test elke hypothese tot root cause gevonden:
- [ ] Hypothese 1: BEVESTIGD / UITGESLOTEN
- [ ] Hypothese 2: BEVESTIGD / UITGESLOTEN
- [ ] Hypothese 3: BEVESTIGD / UITGESLOTEN

### STAP 10: FIX TOEPASSEN

**GEEN GOEDKEURING VRAGEN - DIRECT FIXEN**

- [ ] Bepaal minimale fix
- [ ] Pas fix toe
- [ ] Documenteer wat gewijzigd is

### STAP 11: VALIDATIE

- [ ] Test of originele probleem is opgelost
- [ ] Run tests indien beschikbaar (pytest etc.)
- [ ] Check voor regressies

**Als validatie faalt:** Terug naar STAP 8, nieuwe hypotheses.

### STAP 12: RAPPORT AFRONDEN

Update het rapport met:
```markdown
---
## Debug Resultaat

**Status:** OPGELOST / DEELS OPGELOST / NIET OPGELOST
**Root Cause:** {beschrijving}
**Fix:** {wat gewijzigd in welk bestand}
**Verificatie:** Passed / Failed

### Lessons Learned
{Wat leren we hiervan?}
```

### STAP 13: EINDRAPPORTAGE

Toon aan gebruiker:
```
✓ PROBLEEM OPGELOST

Root cause: {1 zin}
Fix: {wat gedaan}
Bestanden: {lijst}

Volledig rapport: docs/debug-reports/{filename}.md
```

---

## GEDRAGSREGELS

- **WEES GRONDIG** - Verzamel alle relevante context, niet alleen het minimum
- **WEES OBJECTIEF** - Rapporteer feiten, geen aannames
- **WEES SPECIFIEK** - Exacte error messages, niet "er was een fout"
- **VRAAG BIJ TWIJFEL** - Liever één extra vraag dan een incompleet rapport

---

## VOORBEELD

**Input:** `/error-report VRP solver geeft geen routes terug`

**Output:** `docs/debug-reports/2025-01-07_vrp-no-routes.md` met volledige context

