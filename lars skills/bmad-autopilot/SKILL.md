---
name: start-bmad-ralph
# prettier-ignore
description: Start de BMAD autopilot voor story-driven development met CTO Guard.
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Autopilot

> **Doel**: Stories genereren en uitvoeren met CTO Guard validatie

## Wanneer Activeren

- `/start-bmad-ralph` voor volledige workflow
- `/start-bmad-ralph --generate-only` voor alleen story generatie

## Vereiste Input

**VRAAG DE GEBRUIKER** naar het pad van het input .md bestand.
Als geen bestand gegeven: STOP fail-closed.

## Workflow Overzicht

1. **Validatie** - Check repo, CTO_RULES.md aanwezig
2. **CTO Guard #1** - Pre-generation validatie van input
3. **RUN1** - Genereer stories + BACKLOG.md
4. **CTO Guard #2** - Post-generation validatie
5. **Preflight** - Run preflight script
6. **RUN2** - Voer stories uit via Ralph Loop
7. **CTO Guard #3** - Post-execution per story

Details: `python scripts/workflow.py`

## Hard Rules

1. **ALLE stories afwerken** - Stop NOOIT voordat BACKLOG 100% [DONE] of [BLOCKED]
2. **CTO Guard op 3 momenten** - Pre-gen, post-gen, post-exec
3. **Gate A verplicht** - ruff + pytest moet groen
4. **Fail-closed** - Bij non-compliant of twijfel: vraag, stop niet

## Gerelateerde Skills

- `/cto-guard` - Standalone CTO validatie
- `/ralph-loop` - Continue iteratie over stories
