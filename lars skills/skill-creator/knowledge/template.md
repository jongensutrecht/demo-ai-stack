# Skill Template

## SKILL.md Format

```markdown
---
name: {{SKILL_NAME}}
# prettier-ignore
description: {{SHORT_DESCRIPTION_MAX_80_CHARS}}
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# {{Skill Title}}

## Doel
{{1-2 zinnen}}

## Wanneer Gebruiken
- {{trigger}}

## Stappen
1. {{stap}}

## Referenties
- [knowledge/details.md](knowledge/details.md)
```

## Regels

| Type | Regel |
|------|-------|
| MUST | description single-line, max 80 chars |
| MUST | `# prettier-ignore` boven description |
| MUST | SKILL.md max 50 regels |
| SHOULD | Details in knowledge/*.md |
| SHOULD | Logica in scripts/*.py |

## Details

Volledige template: `python scripts/template.py`
