# E2E Validate

Modulaire E2E test validatie met 100% coverage vereiste.

## Gebruik

```
/e2e-validate           → Volledige validatie
/e2e-validate --smoke   → Alleen smoke test (<2 min)
/e2e-validate --full    → Alles + quality gates
```

## Modules

| Module | Doel |
|--------|------|
| `smoke.md` | App start check |
| `fallback-scan.md` | Verboden fallback code detectie |
| `contract-test.md` | Frontend ↔ Backend match |
| `data-integrity.md` | GPS/timestamp exact match |
| `session.md` | Login persistence |
| `offline.md` | Offline + sync |
| `regression.md` | Bestaande functionaliteit |
| `code-quality.md` | Dead code, duplicates, leaks |
| `flaky.md` | Unstable test detectie |
| `performance.md` | Response time baseline |
| `schema.md` | API vs spec validatie |
| `coverage.md` | 100% coverage gate |
| `buttons.md` | UI button inventory |
| `project-detect.md` | Project type detectie |

## Regels

1. **100% coverage** - Geen uitzonderingen
2. **Geen skips** - Alles testen
3. **Geen fallbacks** - Fail-fast
4. **Bewijs per test** - Bron documenteren
