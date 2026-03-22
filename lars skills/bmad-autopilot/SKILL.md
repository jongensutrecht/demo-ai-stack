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

1. **Validatie** - Check repo, docs/CTO_RULES.md aanwezig (Rule Registry) + validator groen; lees ook `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` als die bestaat
2. **CTO Guard #1** - Pre-generation volledige Universal CTO Review van input
3. **RUN1** - Genereer stories + BACKLOG.md (geen eindpunt)
4. **CTO Guard #2** - Post-generation validatie (interne gate, geen eindpunt)
5. **Preflight** - Run preflight script (interne gate, geen eindpunt)
6. **RUN2** - Voer stories uit via Ralph Loop (bewijs-gedreven: proof artefacts verplicht; geen eindpunt)
7. **CTO Guard #3** - Post-execution per story
8. **Same-story handoff bij contextdruk** - hervat dezelfde story in verse sessie; nooit direct naar volgende story

Details: `python scripts/workflow.py`

## Hard Rules

1. **ALLE stories afwerken** - Stop NOOIT voordat BACKLOG 100% [DONE] of [BLOCKED]
2. **CTO Guard op 3 momenten** - Pre-gen, post-gen, post-exec
3. **Primary quality gate verplicht** - `python3 scripts/quality_gates.py` moet groen zijn als dat entrypoint bestaat
4. **Repo-specifieke runtime checks blijven verplicht** - naast de primary gate draai je de kleinste relevante lint/test checks voor gewijzigde runtime paden
5. **Fail-closed** - Bij non-compliant of twijfel: vraag, stop niet
6. **File limits** - Max 300 regels + max 15 functies per niet-test file (tests uitgezonderd)
7. **Actieve story blijft leidend** - ga nooit naar de volgende story zolang de huidige niet `DONE` of `BLOCKED` is
8. **Pi handoff-policy** - gebruik same-story handoff naar verse sessie als contextdruk oploopt; compaction is niet de primaire route voor actieve stories

## Gerelateerde Skills

- `/cto-guard` - Standalone CTO validatie
- `/ralph-loop` - Continue iteratie over stories
rd` - Standalone CTO validatie
- `/ralph-loop` - Continue iteratie over stories
