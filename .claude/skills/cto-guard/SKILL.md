---
name: cto-guard
# prettier-ignore
description: Valideer werk tegen CTO regels. Blokkeert non-compliant code/stories.
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# CTO Guard

## Doel
Valideer input (stories, code, plans) tegen CTO regels uit `docs/CTO_RULES.md`.

## Wanneer Gebruiken
- `/cto-guard` voor handmatige validatie
- Automatisch in BMAD workflow (pre-gen, post-gen, post-exec)

## Input
Geef aan wat je wilt valideren:
- Een story file (`stories_claude/<process>/OPS-001.md`)
- Een code diff (`git diff`)
- Een plan document

## Stappen
1. Laad `docs/CTO_RULES.md`
2. Extraheer relevante regels voor de input
3. Valideer input tegen elke regel
4. Genereer rapport volgens [output format](knowledge/output-format.md)

## Output
Zie [knowledge/output-format.md](knowledge/output-format.md) voor het 5-secties format.

## Verdict
- ✅ **COMPLIANT** - Werk mag doorgaan
- ⚠️ **CONDITIONAL** - Werk mag door met genoemde fixes
- ❌ **NON-COMPLIANT** - BLOKKEER tot opgelost
