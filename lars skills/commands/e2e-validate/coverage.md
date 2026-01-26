# Coverage Verification Module

**Doel:** 100% van alles getest. Geen uitzonderingen.

## Wat Moet 100%?

| Categorie | Hoe Tellen |
|-----------|------------|
| Buttons | Alle klikbare elementen in UI |
| Endpoints | Alle routes in api/ |
| Invariants | Alle regels uit CLAUDE.md/invariants.md |
| Contracts | Alle API calls in frontend |

## Checklist

```
□ Buttons:     18/18 (100%)
□ Endpoints:   12/12 (100%)
□ Invariants:   5/5  (100%)
□ Contracts:   12/12 (100%)
```

## Coverage Gate

```javascript
const coverage = {
  buttons: tested / total,
  endpoints: tested / total,
  invariants: tested / total,
  contracts: tested / total
}

const allPassing = Object.values(coverage).every(c => c === 1.0)

if (!allPassing) {
  console.error('❌ BLOCKED - Coverage incomplete')
  process.exit(1)
}
```

## Rapport

```
╔══════════════════════════════════════════════════════════════╗
║                  COVERAGE VERIFICATION                       ║
╠══════════════════════════════════════════════════════════════╣
║ Buttons:      18/18  (100%) ✅                               ║
║ Endpoints:    12/12  (100%) ✅                               ║
║ Invariants:    5/5   (100%) ✅                               ║
║ Contracts:    12/12  (100%) ✅                               ║
╠══════════════════════════════════════════════════════════════╣
║ Status: ✅ 100% COVERAGE                                     ║
╚══════════════════════════════════════════════════════════════╝
```

## Als <100%

```
╔══════════════════════════════════════════════════════════════╗
║ ❌ COVERAGE INCOMPLETE - BLOCKED                             ║
╠══════════════════════════════════════════════════════════════╣
║ Buttons: 16/18 (89%)                                         ║
║ Missing:                                                     ║
║   - Settings button (/settings)                              ║
║   - Logout button (Header)                                   ║
╠══════════════════════════════════════════════════════════════╣
║ ACTIE: Schrijf ontbrekende tests VOORDAT je merged.          ║
╚══════════════════════════════════════════════════════════════╝
```

**GEEN MERGE zonder 100%**
