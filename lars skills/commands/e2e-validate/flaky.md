# Flaky Test Detectie Module

**Doel:** Vind tests die soms wel, soms niet werken.

## Wat is Flaky?

```
Run 1: ✅ PASS
Run 2: ❌ FAIL
Run 3: ✅ PASS
       ↑ FLAKY - resultaat varieert
```

## Detectie

```bash
# Run elke test 3x
for i in {1..3}; do
  npm test 2>&1 | tee run_$i.log
done

# Vergelijk resultaten
diff run_1.log run_2.log
```

## Oorzaken

| Oorzaak | Voorbeeld | Fix |
|---------|-----------|-----|
| Race condition | Async code, geen await | Voeg await toe |
| Timing | setTimeout in test | Gebruik waitFor |
| External service | API soms traag | Mock of retry |
| Random data | Math.random() in test | Seed random |
| Date/time | new Date() | Mock tijd |
| Order dependency | Test A moet voor B | Isoleer tests |

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                  FLAKY TEST DETECTION                         ║
╠═══════════════════════════════════════════════════════════════╣
║ Total tests: 42                                               ║
║ Runs: 3                                                       ║
╠───────────────────────────────────────────────────────────────╣
║ FLAKY TESTS:                                                  ║
║ ❌ test_gps_sync: 2/3 passed (timing issue?)                  ║
║ ❌ test_login_redirect: 1/3 passed (race condition?)          ║
╠───────────────────────────────────────────────────────────────╣
║ Status: ❌ 2 FLAKY TESTS - must fix before merge              ║
╚═══════════════════════════════════════════════════════════════╝
```

## Regel

**FLAKY = FAIL**

Een test die soms faalt is onbetrouwbaar en moet gefixed worden.
