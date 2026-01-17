# Performance Discovery Questions

## Checklist

- [ ] Wat is de max response time?
- [ ] Wat is de max memory per request?
- [ ] Wat is de max queries per request?
- [ ] Mogen N+1 queries voorkomen?
- [ ] Mogen race conditions data corrumperen?

## Typische Invarianten

| ID | Invariant |
|----|-----------|
| INV-PERF-001 | API responses NEVER exceed 500ms p99 |
| INV-PERF-010 | Memory usage NEVER exceeds 512MB per request |
| INV-PERF-020 | Database queries NEVER exceed 100 per request |
| INV-PERF-030 | Race conditions NEVER cause data corruption |

## Details

Volledige vragen: `python scripts/questions.py performance`
