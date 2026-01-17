# CTO Guard Output Format

## Verplichte 5 Secties

1. **CTO RULES APPLIED** - Welke regels gecheckt
2. **TRACEABILITY MAP** - Rule ID → Covered? → Evidence
3. **VIOLATIONS** - Hard (MUST FIX) en Soft (FIX OR JUSTIFY)
4. **REQUIRED ACTIONS** - Actie, prioriteit, details
5. **CTO COMPLIANCE VERDICT** - Eindoordeel

## Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| COMPLIANT | Alles voldoet | Doorgaan |
| CONDITIONAL | Soft violations | Doorgaan, fix binnen sprint |
| NON-COMPLIANT | Hard violations | BLOKKEER tot gefixed |

## Rules

- **Evidence verplicht**: file:line of command output
- **Blokkeren is OK**: Liever blokkeren dan slechte code doorlaten

## Details

Volledige voorbeelden: `python scripts/format.py`
