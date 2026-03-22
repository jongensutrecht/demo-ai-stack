---
name: create-skill
# prettier-ignore
description: Maak een nieuwe repo-canonieke Claude Code skill met correcte structuur.
allowed-tools: Read, Write, Bash
user-invocable: true
---

# Create Skill

## Doel
Genereer een nieuwe skill folder onder de canonieke repo-bron: `skills/<naam>/`.

## Wanneer Gebruiken
- `/create-skill`
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
2. Maak folder: `skills/<naam>/`
3. Maak `knowledge/` subfolder
4. Genereer `SKILL.md` volgens [template](knowledge/template.md)
5. Toon resultaat aan gebruiker

## Output
```text
skills/<naam>/
├── SKILL.md
└── knowledge/
    └── (leeg, voor details)
```

## Regels (HARD)
- Description MOET single-line zijn
- `# prettier-ignore` BOVEN description
- SKILL.md max 50 regels
- Details in `knowledge/*.md`, NIET in `SKILL.md`
- `skills/` is de canonieke repo-bron; distributie naar `~/.claude/skills` gebeurt via installer/sync tooling
