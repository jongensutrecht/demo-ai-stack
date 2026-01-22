---
name: invariant-discovery
# prettier-ignore
description: Analyseer codebase en ontdek wat NOOIT mag gebeuren (invarianten).
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion
user-invocable: true
---

# Invariant Discovery

> **Doel**: Ontdek en documenteer wat NOOIT mag gebeuren in dit project

## Wanneer Activeren

- `/invariant-discovery` bij project setup
- Na major features met security/business impact
- Na security incidents

## Workflow

1. **Analyse codebase** - Zoek auth, data access, financial code
2. **Lees bestaande docs** - README, ARCHITECTURE, SECURITY
3. **Stel vragen** - Security, Business, Performance vragen
4. **Genereer invariants.md** - Volgens output format
5. **Vraag goedkeuring** - Review met gebruiker
6. **Schrijf file** - Na goedkeuring naar project root

## Discovery Vragen

```bash
python scripts/questions.py security     # Security vragen
python scripts/questions.py business     # Business vragen
python scripts/questions.py performance  # Performance vragen
python scripts/questions.py commands     # Discovery commands
```

## Output Genereren

```bash
python scripts/generate.py              # Template
python scripts/generate.py examples     # Voorbeelden
```

## Output Format

Zie [knowledge/output-format.md](knowledge/output-format.md)

## Gerelateerde Skills

- `/test-guard`, `/cto-guard`