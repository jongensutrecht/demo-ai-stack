# BMAD Micro Brief Template

Gebruik dit vóór je een kleine wijziging uitvoert.

```markdown
## BMAD Micro Brief
- Doel: [1 zin]
- Touched paths allowlist:
  - `path/a`
  - `path/b`
- Out of scope:
  - [wat we bewust niet doen]
- CTO Rules:
  - [DOC-004, DX-002, ...]
- Universal CTO facetten:
  - [Documentation, Developer Experience, ...]
- Verificatie:
  - `python3 scripts/quality_gates.py` (als aanwezig)
  - `[targeted lint/test/build command]`
```

## Escalate naar full BMAD als
- touched paths > 5 files
- auth/API/data/infra/spec geraakt wordt
- je tijdens de wijziging nieuwe P1/P2 risico's ontdekt
- de wijziging geen kleine lokale edit meer is
