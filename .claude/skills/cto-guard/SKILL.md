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
- Een story file (`stories/<process>/OPS-001.md`)
- Een code diff (`git diff`)
- Een plan document

## Stappen
1. Laad `docs/CTO_RULES.md`
2. Extraheer relevante regels voor de input
3. Valideer input tegen elke regel
4. Check Test Requirements compliance (nieuw)
5. Check Invariant coverage (nieuw)
6. Genereer rapport volgens [output format](knowledge/output-format.md)

## Uitgebreide Checks (v2.0)

### Test Compliance
- Heeft de story een Test Requirements sectie?
- Komen de required tests overeen met `test-requirements.yaml`?
- Bestaan de test files voor elke required test type?

### Invariant Compliance
- Zijn relevante invariants gelinkt aan de story?
- Bestaan er NEVER-tests voor deze invariants?
- Zijn alle invariants in `invariants.md` gedekt?

## Output
Zie [knowledge/output-format.md](knowledge/output-format.md) voor het 6-secties format.

## Verdict
- ✅ **COMPLIANT** - Werk mag doorgaan
- ⚠️ **CONDITIONAL** - Werk mag door met genoemde fixes
- ❌ **NON-COMPLIANT** - BLOKKEER tot opgelost
