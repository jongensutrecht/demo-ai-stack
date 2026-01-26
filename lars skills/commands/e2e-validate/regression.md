# Regression Test Module

**Doel:** Na code change, werkt het OUDE nog steeds?

## Wanneer Runnen

```
- Voor elke PR/merge
- Na dependency update
- Na refactor
- Na bug fix (check of fix geen nieuwe bugs maakt)
```

## Checklist

```
□ Alle unit tests PASS
□ Alle integration tests PASS
□ Alle E2E tests PASS
□ Smoke test PASS
□ Geen nieuwe console errors
□ Geen nieuwe TypeScript errors
□ Performance niet >20% slechter
```

## Commando's

```bash
# Run alle tests
npm run test:all

# Check TypeScript
npm run typecheck

# Check linting
npm run lint

# Compare performance
npm run perf:compare
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                  REGRESSION TEST                              ║
╠═══════════════════════════════════════════════════════════════╣
║ Unit tests:        42/42 PASS                                 ║
║ Integration:       15/15 PASS                                 ║
║ E2E:               8/8 PASS                                   ║
║ TypeScript:        0 errors                                   ║
║ Lint:              0 errors                                   ║
║ Performance:       +5% (OK, <20%)                             ║
╠───────────────────────────────────────────────────────────────╣
║ Status: ✅ NO REGRESSIONS                                     ║
╚═══════════════════════════════════════════════════════════════╝
```

## Als FAIL

Zoek welke commit de regression introduceerde:
```bash
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Test elke commit tot je de schuldige vindt
```
