#!/usr/bin/env python3
"""CTO Guard output format details.

Usage:
    python format.py          # Show all sections
    python format.py example  # Show full example
    python format.py verdicts # Show verdict types
"""
import sys

SECTIONS = """
## Verplichte 5 Secties

### 1. CTO RULES APPLIED
```markdown
## 1. CTO RULES APPLIED

| Rule ID | Rule Description |
|---------|------------------|
| SEC-001 | Geen public endpoints voor mutaties |
| TEST-001 | Alle code heeft tests |
```

### 2. TRACEABILITY MAP
```markdown
## 2. TRACEABILITY MAP

| Rule ID | Covered? | Evidence |
|---------|----------|----------|
| SEC-001 | YES | `adapter/routes/health.py:15` - auth=admin_key |
| TEST-001 | NO | Geen tests gevonden voor nieuwe functie |
```

### 3. VIOLATIONS
```markdown
## 3. VIOLATIONS

### Hard Violations (MUST FIX)
| ID | Rule | Violation | Location |
|----|------|-----------|----------|
| V1 | SEC-001 | Public endpoint voor mutatie | `adapter/routes/data.py:42` |

### Soft Violations (FIX OR JUSTIFY)
| ID | Rule | Violation | Location |
|----|------|-----------|----------|
| V2 | DOC-001 | Ontbrekende docstring | `utils/helper.py:10` |
```

### 4. REQUIRED ACTIONS
```markdown
## 4. REQUIRED ACTIONS

| Action | Priority | Details |
|--------|----------|---------|
| Add auth to /data endpoint | P1 | Voeg `Depends(require_admin)` toe |

**STATUS**: BLOCKED until V1 is resolved
```

### 5. CTO COMPLIANCE VERDICT
```markdown
## 5. CTO COMPLIANCE VERDICT

### NON-COMPLIANT

**Reason**: 1 hard violation (SEC-001)

**Next Steps**:
1. Fix V1 (auth op /data endpoint)
2. Re-run `/cto-guard`
```
"""

VERDICTS = """
## Verdict Types

| Verdict | Meaning | Action |
|---------|---------|--------|
| COMPLIANT | Alles voldoet | Doorgaan |
| CONDITIONAL | Soft violations | Doorgaan, fix binnen sprint |
| NON-COMPLIANT | Hard violations | BLOKKEER tot gefixed |

## Rules

- Geen impliciete compliance: Elke regel moet expliciet gecheckt
- Evidence verplicht: Elke claim heeft file:line of command output
- Blokkeren is OK: Liever blokkeren dan slechte code doorlaten
"""

def main():
    if len(sys.argv) < 2:
        print("CTO Guard Output Format")
        print("=" * 50)
        print(SECTIONS)
        return

    cmd = sys.argv[1].lower()
    if cmd == "example":
        print(SECTIONS)
    elif cmd == "verdicts":
        print(VERDICTS)
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python format.py [example|verdicts]")

if __name__ == "__main__":
    main()
