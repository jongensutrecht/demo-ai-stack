# Security Discovery Questions

## Checklist

- [ ] Welke endpoints zijn protected?
- [ ] Welke data is user-specific?
- [ ] Welke acties zijn admin-only?
- [ ] Welke data mag NOOIT gelogd worden?
- [ ] Is er tenant isolation?

## Typische Invarianten

| ID | Invariant |
|----|-----------|
| INV-SEC-001 | Protected endpoints NEVER return data without valid token |
| INV-SEC-002 | User data is NEVER exposed to other users |
| INV-SEC-020 | Passwords are NEVER stored in plaintext |
| INV-SEC-021 | Sensitive data is NEVER logged |

## Details

Volledige vragen: `python scripts/questions.py security`
