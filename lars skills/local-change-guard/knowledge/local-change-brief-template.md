# Local Change Brief Template

Gebruik dit vóór je direct in de huidige working tree gaat editen.

```markdown
## Local Change Brief
- Doel: [1 zin]
- Touched paths allowlist:
  - `path/a`
  - `path/b`
- Out of scope:
  - [wat we bewust niet doen]
- Relevante CTO Rules:
  - [SEC-001, DATA-001, ARCH-001, ...]
- Relevante Universal CTO facetten:
  - [Architecture, Reliability, Security, Operability, DX, ...]

### File budget table
> Geen edit starten voordat deze tabel met echte cijfers is ingevuld.

| Path | Test? | Current lines | Current defs | Target after change | Evidence source | Plan |
|---|---:|---:|---:|---:|---|---|
| `path/a.py` | no | 182 | 9 | <= 220 / <= 11 | `scripts/check_file_limits.py` / AST-check | kleine edit in-place |
| `path/b.py` | no | 287 | 14 | <= 300 / <= 15 | `scripts/check_file_limits.py` / AST-check | eerst extract naar nieuwe helper |

### Verificatie
- `[primary-gate from repo docs]`
- `scripts/check_file_limits.py` (als aanwezig)
- `[smallest targeted lint/test/build command]`

### Escalate if
- nieuwe exception nodig is
- touched paths buiten allowlist lopen
- file budget niet hard bewijsbaar blijft
- wijziging spec/infra/auth/migration-werk blijkt te zijn
```

## Minimale discipline
- Budget eerst, code daarna.
- Als een legacy offender geraakt wordt: niet laten groeien.
- Geen nieuwe exception-entry in deze route.
- Geen “klaar” zonder gates + budget-check + CTO delta review.
