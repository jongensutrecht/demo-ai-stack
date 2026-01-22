#!/usr/bin/env python3
"""Skill template generator.

Usage:
    python template.py           # Show full template
    python template.py tools     # Show allowed tools
    python template.py structure # Show folder structure
"""
import sys

TEMPLATE = """
## SKILL.md Template

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
{{1-2 zinnen wat de skill doet}}

## Wanneer Gebruiken
- {{trigger phrase 1}}
- {{trigger phrase 2}}

## Stappen
1. {{stap}}
2. {{stap}}
3. {{stap}}

## Referenties
- [knowledge/details.md](knowledge/details.md) - {{beschrijving}}

## Output Format
{{kort voorbeeld of verwijs naar knowledge/}}
```

## Regels

### MUST (verplicht)
- `description`: Single-line, max 80 karakters
- `# prettier-ignore` direct boven description
- Totaal SKILL.md: max 50 regels
- `user-invocable: true` voor slash commands

### SHOULD (aanbevolen)
- Details in `knowledge/*.md` (niet in SKILL.md)
- Logica in `scripts/*.py` (draait buiten context)
- Kebab-case voor skill naam

### MUST NOT (verboden)
- Multi-line description
- Grote templates/voorbeelden embedden in SKILL.md
- Meer dan 100 chars in description
"""

TOOLS = """
## Allowed Tools Opties

| Tools | Gebruik voor |
|-------|--------------|
| Read | Bestanden lezen |
| Write | Bestanden schrijven |
| Edit | Bestanden aanpassen |
| Bash | Commands uitvoeren |
| Grep | Zoeken in code |
| Glob | Bestanden vinden |
| Task | Sub-agents starten |
"""

STRUCTURE = """
## Folder Structuur

```
.claude/skills/<skill-name>/
├── SKILL.md              # Lean, max 50 regels
├── knowledge/            # Details (Claude laadt on-demand)
│   └── <topic>.md
└── scripts/              # Optioneel: Python/Bash
    └── <action>.py
```
"""

def main():
    if len(sys.argv) < 2:
        print("Skill Template")
        print("=" * 50)
        print(TEMPLATE)
        return

    cmd = sys.argv[1].lower()
    if cmd == "tools":
        print(TOOLS)
    elif cmd == "structure":
        print(STRUCTURE)
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python template.py [tools|structure]")

if __name__ == "__main__":
    main()
