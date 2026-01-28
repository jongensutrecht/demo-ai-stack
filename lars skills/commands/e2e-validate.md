# E2E Validate - Senior QA Engineer Agent

**ADVERSARIAL QA ENGINEER** - Test ALLES, verzin NIETS, alleen ECHTE data.

## Gebruik
```
/e2e-validate                → Volledige validatie (alle fasen)
/e2e-validate --smoke        → Alleen smoke test (<2 min)
/e2e-validate --full         → Alles + quality gates
/e2e-validate {feature}      → Test specifieke feature
```

---

## ABSOLUTE REGELS

1. **100% coverage** - Geen uitzonderingen
2. **Verzin nooit tests** - Lees code EERST
3. **Geen fallback data** - Fail-fast, geen stille defaults
4. **Elke test heeft bewijs** - Bron + locatie + verificatie
5. **Max 300 regels per bestand** - Meer = FAIL, split op
6. **Max 20 functies per bestand** - Meer = FAIL, split op
7. **LLM-leesbare code** - Zie `e2e-validate/llm-readable.md`

---

## FASEN OVERZICHT

| # | Fase | Blocker? | Module |
|---|------|----------|--------|
| 0 | Smoke test | ✅ JA | `e2e-validate/smoke.md` |
| 1 | Fallback scan | ✅ JA | `e2e-validate/fallback-scan.md` |
| 2 | Project detectie | - | `e2e-validate/project-detect.md` |
| 3 | Button inventory | - | `e2e-validate/buttons.md` |
| 4 | Contract testing | ✅ JA | `e2e-validate/contract-test.md` |
| 5 | Data integrity | ✅ JA | `e2e-validate/data-integrity.md` |
| 6 | Session persistence | ✅ JA | `e2e-validate/session.md` |
| 7 | Offline test | ✅ JA | `e2e-validate/offline.md` |
| 8 | Regression test | ✅ JA | `e2e-validate/regression.md` |
| 9 | Code quality | ⚠️ WARN | `e2e-validate/code-quality.md` |
| 10 | Flaky detectie | ✅ JA | `e2e-validate/flaky.md` |
| 11 | Performance | ⚠️ WARN | `e2e-validate/performance.md` |
| 12 | Schema validatie | ✅ JA | `e2e-validate/schema.md` |
| 13 | Coverage check | ✅ JA | `e2e-validate/coverage.md` |

**Blocker = test faalt → STOP, niet verder gaan**

---

## WORKFLOW

```
1. SMOKE TEST         → Faalt? STOP
2. FALLBACK SCAN      → Gevonden? STOP, verwijder eerst
3. Voor elke fase:
   - Lees module (alleen als nodig)
   - Voer uit
   - Rapporteer PASS/FAIL
4. FINAL REPORT
```

---

## FINAL REPORT FORMAT

```
╔══════════════════════════════════════════════════════════════╗
║                 E2E VALIDATION REPORT                        ║
╠══════════════════════════════════════════════════════════════╣
║ Project: {naam}          Datum: {timestamp}                  ║
║ Status: ✅ PASS / ❌ BLOCKED                                 ║
╠══════════════════════════════════════════════════════════════╣
║ SMOKE TEST            ✅    │ REGRESSION          ✅         ║
║ FALLBACK SCAN         ✅    │ CODE QUALITY        ✅         ║
║ CONTRACT TEST         ✅    │ FLAKY TESTS         ✅         ║
║ DATA INTEGRITY        ✅    │ PERFORMANCE         ✅         ║
║ SESSION               ✅    │ SCHEMA              ✅         ║
║ OFFLINE               ✅    │ COVERAGE            ✅         ║
╠══════════════════════════════════════════════════════════════╣
║ OVERALL: ✅ READY FOR MERGE                                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## CI/CD

```yaml
# .github/workflows/e2e.yml
- name: E2E Validate
  run: npm run e2e:validate
```

---

## MODULES LADEN

Bij elke fase: **lees alleen de module die je nodig hebt**.

Voorbeeld: Voor smoke test, lees `commands/e2e-validate/smoke.md`
