---
name: ralph-loop
# prettier-ignore
description: Continue iteratie loop voor BMAD stories. Itereert tot alle stories [DONE].
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# Ralph Loop

> **Versie**: 1.0.0
> **Doel**: Automatische iteratie over BMAD stories tot completion

---

## Wanneer Activeren

- `/ralph-loop` voor handmatige start
- Automatisch via `/start-bmad-ralph`

---

## Vereiste Input

**BACKLOG.md moet bestaan** in `stories_claude/<Process>/BACKLOG.md`

Als geen BACKLOG: STOP fail-closed met instructie om eerst `/bmad-autopilot` te runnen.

---

## Workflow

### STAP 1 - Lees BACKLOG.md

```bash
# Vind open stories
grep -E "\[TODO\]|\[IN_PROGRESS\]" stories_claude/<Process>/BACKLOG.md
```

### STAP 2 - Pak Volgende Story

Prioriteit:
1. Eerst `[IN_PROGRESS]` (hervatten)
2. Dan eerste `[TODO]`

### STAP 3 - Voer Story Uit

```bash
# Start nieuw Claude window voor story
claude --dangerously-skip-permissions \
  -p "Voer story <STORY_ID> uit. Story: stories_claude/<Process>/<STORY_ID>.md"
```

### STAP 4 - Update Status

Na story completion:
- Success → `[DONE]`
- Failure (3x) → `[BLOCKED]`
- Nog bezig → `[IN_PROGRESS]`

### STAP 5 - Check Completion

```
Als alle stories [DONE] of [BLOCKED]:
  Output: <promise>RALPH_COMPLETE</promise>
Anders:
  Terug naar STAP 2
```

---

## BACKLOG.md Format

Zie [knowledge/backlog-format.md](knowledge/backlog-format.md)

---

## Safeguards

| Safeguard | Waarde |
|-----------|--------|
| Max iterations | `stories × 3` |
| Max attempts per story | 3 |
| Circuit breaker | 5 loops zonder progress → STOP |

---

## Gerelateerde Skills

- `/bmad-autopilot` - Genereert stories en BACKLOG.md
- `/cto-guard` - Valideert code na elke story
