---
name: ralph-loop
# prettier-ignore
description: Continue iteratie loop voor BMAD stories. Itereert tot alle stories [DONE].
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# Ralph Loop

> **Doel**: Automatische iteratie over BMAD stories tot 100% completion

## Wanneer Activeren

- `/ralph-loop` of automatisch via `/start-bmad-ralph`

## Vereiste Input

**BACKLOG.md** in `stories_claude/<Process>/BACKLOG.md`. Zonder: STOP fail-closed.

## Workflow

1. Lees BACKLOG.md - Vind [TODO] of [IN_PROGRESS] stories
2. Pak volgende story - Eerst [IN_PROGRESS], dan eerste [TODO]
3. **Spawn subprocess** - Voer story uit in nieuw Claude window
4. **Proof gate (fail-closed)** - Draai `python3 tools/bmad/verify_story.py` en schrijf proof artefact (final.json)
5. Update status - Alleen `[DONE]` als proof `done=true` is; anders `[IN_PROGRESS]` of `[BLOCKED]`
6. Stop criterium - Alleen stoppen als alle stories `[DONE]` of `[BLOCKED]` zijn **en** `python3 tools/bmad/ralph_verify_backlog.py` `RALPH_PROOF_OK` geeft

Details: `python scripts/workflow.py`

## KRITIEK: Subprocess Vereist

**NOOIT** stories in huidige context. **ALTIJD** nieuw claude subprocess.

## Safeguards

| Max iterations | Max attempts/story | Circuit breaker |
|----------------|-------------------|-----------------|
| stories x 3 | 3 | 5 loops zonder progress |

## Hard Rules

1. **100% completion** - Stop NOOIT tot ALLE stories [DONE] of [BLOCKED]
2. **Subprocess per story** - Nooit in huidige context uitvoeren
3. **File limits** - Max 300 regels + max 20 functies per niet-test file (tests uitgezonderd)

## Referenties

- [knowledge/backlog-format.md](knowledge/backlog-format.md)
- `/start-bmad-ralph`
