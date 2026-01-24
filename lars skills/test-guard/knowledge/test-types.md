# Test Types - Quick Reference

| Type | Wat | Wanneer | Snelheid |
|------|-----|---------|----------|
| **Unit** | Isoleert 1 functie | Business logic | <100ms |
| **Integration** | Echte DB/API | Endpoints, repos | ~1s |
| **Playwright** | Browser test | UI flows | ~5s |
| **Contract** | API vs spec | Schema changes | ~1s |
| **NEVER** | Mag nooit gebeuren | Security, business rules | varies |

## Beslisboom

```
Raakt het UI/browser? → playwright
Raakt het API/database? → integration
Pure logic? → unit
API schema gewijzigd? → contract
Security/business critical? → NEVER-test
```

## Scripts

```bash
# Bepaal welke tests nodig zijn voor een file
python scripts/decide.py src/components/Button.tsx

# Haal voorbeeld op voor specifiek type
python scripts/examples.py unit
python scripts/examples.py playwright
python scripts/examples.py contract
python scripts/examples.py never
```

## Test Pyramid

```
     /\        E2E (10%) - weinig, langzaam
    /  \
   /____\     Integration (20%)
  /      \
 /________\   Unit (70%) - veel, snel
```
