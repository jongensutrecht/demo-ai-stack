---
name: skill-creator
# prettier-ignore
description: Maak een nieuwe Claude Code skill met correcte structuur en best practices.
allowed-tools: Read, Write, Bash
user-invocable: true
---

# Skill Creator

## Doel
Genereer een nieuwe skill folder met SKILL.md volgens de standaard.

## Wanneer Gebruiken
- `/skill-creator`
- "maak een nieuwe skill"
- "genereer skill template"

## Input Nodig
Vraag de gebruiker om:
1. **Skill naam** (kebab-case, bijv. `route-analyzer`)
2. **Korte beschrijving** (max 80 chars, single-line)
3. **Doel** (1-2 zinnen)
4. **Trigger phrases** (wanneer activeren)

## Stappen

1. Valideer skill naam (kebab-case, geen spaties)
2. Maak folder: `.claude/skills/<naam>/`
3. Maak `knowledge/` subfolder
4. Genereer `SKILL.md` volgens [template](knowledge/template.md)
5. Toon resultaat aan gebruiker

## Output
```
.claude/skills/<naam>/
├── SKILL.md
└── knowledge/
    └── (leeg, voor details)
```

## Regels (HARD)
- Description MOET single-line zijn
- `# prettier-ignore` BOVEN description
- SKILL.md max 50 regels
- Details in knowledge/*.md, NIET in SKILL.md
