---
name: invariant-discovery
# prettier-ignore
description: Analyseer codebase en ontdek wat NOOIT mag gebeuren (invarianten).
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion
user-invocable: true
---

# Invariant Discovery

> **Versie**: 1.0.0
> **Doel**: Ontdek en documenteer wat NOOIT mag gebeuren in dit project

---

## Wanneer Activeren

- `/invariant-discovery` bij project setup
- Na major feature additions met security/business impact
- Na security incidents
- Bij CTO review die gaps vindt

---

## Wat zijn Invarianten?

Invarianten zijn condities die **NOOIT** mogen worden geschonden:

| Type | Voorbeelden |
|------|-------------|
| **Security** | User data NOOIT zichtbaar voor andere users |
| **Business** | Invoice totals NOOIT negatief |
| **Performance** | API response NOOIT > 500ms |
| **Reliability** | Partial writes NOOIT corrupt state |

---

## Workflow

### STAP 1 - Analyse Codebase

Analyseer de codebase om potentiële risico's te identificeren:

```bash
# Zoek auth patterns
rg -l "auth|token|session|login" --type py
rg -l "middleware|guard|protect" --type ts

# Zoek data access patterns
rg -l "user_id|owner_id|created_by" --type py
rg "\.filter\(.*user" --type py

# Zoek financial code
rg -l "price|amount|total|invoice|payment" --type py

# Zoek state machines
rg "status|state" --type py
rg "enum.*Status" --type py
```

### STAP 2 - Lees Bestaande Docs

```bash
# Check for existing docs
cat README.md
cat docs/ARCHITECTURE.md 2>/dev/null || true
cat docs/SECURITY.md 2>/dev/null || true
cat spec/*.md 2>/dev/null || true
```

### STAP 3 - Stel Vragen

**Gebruik AskUserQuestion** met de vragen uit de knowledge files:

1. **Security Questions** (knowledge/security-questions.md)
2. **Business Questions** (knowledge/business-questions.md)
3. **Performance Questions** (knowledge/performance-questions.md)

### STAP 4 - Genereer invariants.md

Genereer `invariants.md` volgens het format in knowledge/output-format.md.

### STAP 5 - Vraag Goedkeuring

```
Ik heb de volgende invarianten geïdentificeerd:

## Security
- INV-SEC-001: [beschrijving]
- INV-SEC-002: [beschrijving]

## Business
- INV-BIZ-001: [beschrijving]

Wil je deze invarianten goedkeuren of aanpassen?
```

### STAP 6 - Schrijf File

Na goedkeuring, schrijf `invariants.md` naar de project root.

---

## Discovery Checklist

### Security

- [ ] Welke endpoints zijn protected?
- [ ] Welke data is user-specific?
- [ ] Welke acties zijn admin-only?
- [ ] Welke data mag NOOIT gelogd worden?

### Business

- [ ] Welke waarden mogen NOOIT negatief?
- [ ] Welke state transitions zijn ongeldig?
- [ ] Welke operaties mogen NOOIT dubbel?
- [ ] Welke data moet altijd consistent?

### Performance

- [ ] Wat is de max response time?
- [ ] Wat is de max memory per request?
- [ ] Wat is de max queries per request?

### Reliability

- [ ] Welke operaties moeten atomair?
- [ ] Wat mag NOOIT partial blijven?
- [ ] Welke errors moeten altijd gehandled?

---

## Output

Het resultaat is een `invariants.md` bestand met:

1. Alle ontdekte invarianten
2. Gecategoriseerd (Security/Business/Performance/Reliability)
3. Met unieke IDs (INV-SEC-001, INV-BIZ-001, etc.)
4. Met checkbox voor test coverage tracking

---

## Gerelateerde Skills

- `/test-guard` - Valideert dat invarianten test coverage hebben
- `/cto-guard` - CTO review tegen regels

---

## Gerelateerde Bestanden

- `knowledge/security-questions.md` - Security discovery vragen
- `knowledge/business-questions.md` - Business rule discovery vragen
- `knowledge/performance-questions.md` - Performance discovery vragen
- `knowledge/output-format.md` - Format voor invariants.md
