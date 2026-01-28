# Performance Module

**Doel:** Meet en track response times, detecteer regressies.

## Wat Meten

| Metric | Target | Fail |
|--------|--------|------|
| API response | <500ms | >1000ms |
| Page load | <3s | >5s |
| Time to interactive | <3s | >5s |

## Meten

```javascript
// API timing
const start = performance.now()
await fetch('/api/shifts')
const duration = performance.now() - start
console.log(`API: ${duration}ms`)

// Page load (Playwright)
const metrics = await page.metrics()
console.log(`Load: ${metrics.TaskDuration}ms`)
```

## Baseline Opslaan

```json
// docs/perf-baseline.json
{
  "timestamp": "2026-01-26",
  "endpoints": {
    "/api/shifts": { "avg": 234, "p95": 450 },
    "/api/gps": { "avg": 89, "p95": 150 }
  },
  "pages": {
    "/dashboard": { "load": 1200, "tti": 1800 },
    "/login": { "load": 800, "tti": 1000 }
  }
}
```

## Vergelijk met Baseline

```
HUIDIGE RUN vs BASELINE:

/api/shifts:  234ms → 289ms  (+23%) ⚠️ WARNING
/api/gps:     89ms  → 92ms   (+3%)  ✅ OK
/dashboard:   1.2s  → 1.3s   (+8%)  ✅ OK
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                  PERFORMANCE TEST                             ║
╠═══════════════════════════════════════════════════════════════╣
║ API avg response:    234ms    ✅ (<500ms)                     ║
║ Page load avg:       1.2s     ✅ (<3s)                        ║
║ Regression:          +8%      ✅ (<20%)                       ║
╠───────────────────────────────────────────────────────────────╣
║ Status: ✅ PASS                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## Als >20% Regression

Onderzoek:
- Welke commit introduceerde het?
- Nieuwe dependencies?
- Meer data?
- N+1 queries?
