# Debug - Gerichte Probleemanalyse + Auto-Fix

**On-demand debugger** - Jij wijst, ik onderzoek EN fix.

**Gebruik:**
```
/debug {probleem} {pad}           → Onderzoek + fix in specifiek pad
/debug {probleem} {bestand}       → Onderzoek + fix in specifiek bestand
/debug {probleem}                 → Vraagt waar te zoeken, dan fix
```

**Voorbeelden:**
```
/debug "TypeError bij aanroep" src/vrp_solver.py
/debug "routes komen leeg terug" src/
/debug "config wordt niet geladen" .env config.py
/debug "test faalt" tests/test_routing.py
```

---

## MODUS: GERICHT + AUTOMATISCH

```
JIJ bepaalt:          IK doe:
─────────────────────────────────────────
- Wat het probleem is  → Zoek waar het misgaat
- Waar te zoeken       → Analyseer die scope
                       → Fix AUTOMATISCH
                       → Valideer
                       → Rapporteer resultaat
```

---

## PROCEDURE

### STAP 1: SCOPE BEPALEN

**Parse `$ARGUMENTS`:**
- Extraheer probleembeschrijving
- Extraheer pad(en) - bestand of map
- Als pad ontbreekt: vraag "Waar moet ik zoeken?"

**Bevestig begrip:**
```
Ik ga onderzoeken: "{probleem}"
Scope: {bestand/map}
Klopt dit? (of geef meer richting)
```

### STAP 2: VERKENNING

**Voor een BESTAND:**
- Lees het bestand
- Zoek naar relevante code (gerelateerd aan probleem)
- Check imports, dependencies
- Identificeer verdachte secties

**Voor een MAP:**
- List bestanden
- Identificeer relevante bestanden (op naam/type)
- Lees meest waarschijnlijke kandidaten
- Volg spoor waar nodig

**Rapporteer tussentijds:**
```
Gevonden in {bestand}:{regelnummer}:
{relevante code snippet}

Dit lijkt verdacht omdat: {reden}
```

### STAP 3: BEVINDINGEN

**Rapporteer gestructureerd:**

```markdown
## Onderzoek: {probleem}

**Scope:** {wat onderzocht}
**Tijd:** {x minuten}

### Bevindingen

1. **{locatie}** - {wat gevonden}
   ```
   {code snippet}
   ```
   Analyse: {waarom dit relevant/verdacht is}

2. **{locatie}** - {wat gevonden}
   ...

### Mogelijke Oorzaken

| # | Oorzaak | Zekerheid | Locatie |
|---|---------|-----------|---------|
| 1 | {oorzaak} | Hoog/Medium/Laag | {file:line} |
| 2 | {oorzaak} | Hoog/Medium/Laag | {file:line} |

### Aanbeveling

{Wat ik denk dat het probleem is}
```

### STAP 4: AUTOMATISCH DOORGAAN NAAR FIX

**GEEN STOP - GA DIRECT DOOR**

Toon kort:
```
Bevindingen: {aantal} verdachte locaties
Meest waarschijnlijke oorzaak: {beschrijving}
→ Start automatische fix...
```

### STAP 5: FIX TOEPASSEN

- [ ] Bepaal minimale fix voor root cause
- [ ] Pas fix toe (geen refactoring, alleen het probleem)
- [ ] Documenteer wat gewijzigd is

### STAP 6: VALIDATIE

- [ ] Test of originele probleem is opgelost
- [ ] Run tests indien beschikbaar
- [ ] Check voor regressies

**Als validatie faalt:** Terug naar STAP 3, analyseer opnieuw.

### STAP 7: EINDRAPPORTAGE

Toon aan gebruiker:
```
✓ PROBLEEM OPGELOST

Root cause: {1 zin}
Locatie: {file:line}
Fix: {wat gedaan}

Rapport: docs/debug-reports/{datum}_{korte-naam}.md
```

Sla rapport op in `docs/debug-reports/`.

---

## ONDERZOEKSTECHNIEKEN

**Code analyse:**
- Lees functies/classes gerelateerd aan probleem
- Trace data flow (input → verwerking → output)
- Check error handling (of gebrek daaraan)
- Vergelijk met verwacht gedrag

**Patroon zoeken:**
- Grep naar error messages
- Zoek naar TODO/FIXME/HACK comments
- Check recent gewijzigde code (git blame)
- Zoek naar hardcoded values

**Context bouwen:**
- Wie roept deze code aan?
- Wat zijn de dependencies?
- Welke tests bestaan er?
- Wat zegt de documentatie?

---

## GEDRAGSREGELS

| DO | DON'T |
|----|-------|
| Focus op aangegeven scope | Afdwalen naar andere bestanden |
| Fix AUTOMATISCH na analyse | Vragen om toestemming |
| Valideer na elke fix | Aannemen dat het werkt |
| Geef concrete locaties (file:line) | Vage verwijzingen |
| Minimale fix, geen refactoring | Meer wijzigen dan nodig |

---

## VOORBEELDEN

**Voorbeeld 1: Specifiek bestand**
```
User: /debug "returned None terwijl list verwacht" src/utils.py

AI: Onderzoek "returned None terwijl list verwacht" in src/utils.py...

Gevonden in src/utils.py:45:
    def get_items(self):
        if not self.data:
            return  # ← HIER: implicit None return
        return list(self.data)

Root cause: Bij lege data returned de functie None ipv lege list.
→ Start automatische fix...

Fix toegepast in src/utils.py:47:
    return []  # Was: return (implicit None)

Validatie: ✓ Functie returned nu lege list

✓ PROBLEEM OPGELOST
Rapport: docs/debug-reports/2025-01-07_none-return.md
```

**Voorbeeld 2: Map scannen**
```
User: /debug "database connectie timeout" src/db/

AI: Scan src/db/ voor database connectie timeout issues...

Bestanden in scope: connection.py, queries.py, models.py

Gevonden in src/db/connection.py:23:
    timeout=5  # ← Hardcoded 5 seconden

Root cause: Timeout te kort (5s) voor trage netwerken.
→ Start automatische fix...

Fix toegepast in src/db/connection.py:23:
    timeout=30  # Was: 5

Validatie: ✓ Connectie succesvol met langere timeout

✓ PROBLEEM OPGELOST
Rapport: docs/debug-reports/2025-01-07_db-timeout.md
```

---

## INTEGRATIE MET ANDERE COMMANDS

**Alle commands fixen nu AUTOMATISCH:**

```
/error-report  → Documenteer + analyseer + fix (volledig autonoom)
/debug         → Gericht onderzoek + fix (jij wijst de scope)
/debug-report  → Analyseer bestaand rapport + fix
```

**Wanneer welke?**
- "Er ging iets mis" (vaag) → `/error-report`
- "Probleem zit in X" (gericht) → `/debug "probleem" pad/`
- "Heb al een rapport" → `/debug-report pad/rapport.md`
