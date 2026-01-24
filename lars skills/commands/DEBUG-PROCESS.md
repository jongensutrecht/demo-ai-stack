# Debug Process - Quick Reference

## Het Proces

```
┌─────────────────────────────────────────┐
│         JE HEBT EEN PROBLEEM            │
└─────────────────────────────────────────┘
                    │
      ┌─────────────┴─────────────┐
      │                           │
      ▼                           ▼
 Weet NIET waar            Weet WEL waar
      │                           │
      ▼                           ▼
┌─────────────────┐    ┌─────────────────────┐
│ /error-report   │    │ /debug "X" pad/     │
│ "beschrijving"  │    │                     │
└─────────────────┘    └─────────────────────┘
      │                           │
      └─────────────┬─────────────┘
                    │
                    ▼
          ┌─────────────────┐
          │  AUTOMATISCH:   │
          │  → Analyseren   │
          │  → Fixen        │
          │  → Valideren    │
          │  → Rapporteren  │
          └─────────────────┘
                    │
                    ▼
             ✓ OPGELOST
```

---

## Commands

| Command | Wanneer | Wat gebeurt er |
|---------|---------|----------------|
| `/error-report "beschrijving"` | Weet niet waar probleem zit | Volledig autonoom: uitzoeken → fixen → rapport |
| `/debug "probleem" pad/` | Weet wel waar te zoeken | Gericht: daar analyseren → fixen → rapport |
| `/debug-report rapport.md` | Heb al een rapport | Rapport analyseren → fixen |

---

## Voorbeelden

```bash
# Vaag probleem - laat AI uitzoeken
/error-report "VRP solver crashed"

# Gericht probleem - wijs de locatie
/debug "KeyError booth_id" src/vrp_solver.py
/debug "routes leeg" src/
/debug "test faalt" tests/test_routing.py

# Bestaand rapport verder verwerken
/debug-report docs/debug-reports/2025-01-07_crash.md
```

---

## Output

Alle rapporten komen in: `docs/debug-reports/`

Formaat: `{YYYY-MM-DD}_{korte-naam}.md`

---

## Geen Tussenstops

- Geen "wil je dat ik...?" vragen
- Geen goedkeuring nodig voor fixes
- Automatisch valideren na fix
- Alleen eindresultaat rapporteren
