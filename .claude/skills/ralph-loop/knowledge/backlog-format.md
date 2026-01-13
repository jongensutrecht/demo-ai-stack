# BACKLOG.md Format

## Locatie
`stories_claude/<Process>/BACKLOG.md`

## Template

```markdown
# BACKLOG - <Process>

| Story | Status | Attempts | Notes |
|-------|--------|----------|-------|
| OPS-001 | [TODO] | 0 | |
| OPS-002 | [TODO] | 0 | |
| OPS-003 | [TODO] | 0 | |
```

## Statussen

| Status | Betekenis | Actie |
|--------|-----------|-------|
| `[TODO]` | Nog niet gestart | Oppakken |
| `[IN_PROGRESS]` | Bezig | Hervatten |
| `[DONE]` | Compleet met groene tests | Skip |
| `[BLOCKED]` | 3x gefaald of dependency issue | Skip + escalate |

## Status Transitions

```
[TODO] → [IN_PROGRESS] → [DONE]
                ↓
           [BLOCKED] (na 3 failures)
```

## Attempts Tracking

- Increment bij elke poging
- Bij `attempts >= 3` en niet [DONE]: zet naar [BLOCKED]

## Notes Column

Gebruik voor:
- Failure reasons
- Blocker descriptions
- Dependencies

## Voorbeeld Ingevuld

```markdown
# BACKLOG - my_feature

| Story | Status | Attempts | Notes |
|-------|--------|----------|-------|
| OPS-001 | [DONE] | 1 | |
| OPS-002 | [DONE] | 2 | 1e poging: test failure |
| OPS-003 | [IN_PROGRESS] | 1 | |
| OPS-004 | [BLOCKED] | 3 | pytest timeout, needs investigation |
| OPS-005 | [TODO] | 0 | depends on OPS-003 |
```

## Completion Criteria

Ralph Loop stopt wanneer:
- Alle stories `[DONE]` of `[BLOCKED]`
- OF max iterations bereikt
- OF circuit breaker triggered (5 loops zonder progress)
