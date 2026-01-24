---
name: plan-to-bmad
# prettier-ignore
description: Transformeer een plan naar BMAD-ready input met succesfactoren.
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion
user-invocable: true
---

# Plan to BMAD

> **Doel**: Transformeer elk plan naar BMAD-ready input format

## Wanneer Gebruiken

- `/plan-to-bmad` na plan mode
- `/plan-to-bmad <path>` voor plan uit browser/handmatig

## Input

Plan kan komen van:
- `.claude/plans/*.md` (Claude Code)
- Browser chat (copy-paste naar file)
- Handmatig geschreven spec

## Workflow

1. **Lees plan** - Vraag pad indien niet gegeven
2. **Extraheer** - Features, requirements, scope
3. **Vraag verificatie** - Per feature: command + expected output
4. **Vraag invarianten** - Wat mag NOOIT? (of verwijs naar `/invariant-discovery`)
5. **Schrijf output** - Naar `bmad_input/<naam>.md`

## Output

Zie [knowledge/bmad-template.md](knowledge/bmad-template.md)

## Gerelateerde Skills

- `/bmad-bundle` - Verwerkt de output
- `/invariant-discovery` - Diepere invariant analyse
