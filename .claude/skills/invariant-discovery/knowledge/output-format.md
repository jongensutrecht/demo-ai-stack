# Invariants Output Format

Dit document beschrijft het format voor het `invariants.md` bestand.

---

## Template

```markdown
# Project Invariants

> Dit document beschrijft wat NOOIT mag gebeuren in dit project.
> Elke invariant MOET een bijbehorende NEVER-test hebben.

---

## Hoe dit document te gebruiken

1. Elke invariant is een conditie die NOOIT mag worden geschonden
2. Markeer invarianten met `- [ ]` als de test nog ontbreekt
3. Markeer invarianten met `- [x]` als de test bestaat
4. Voeg het test bestand pad toe bij elke invariant

---

## Security Invariants

> Condities die NOOIT mogen worden geschonden vanwege security.

### Authentication

- [ ] **INV-SEC-001**: [Beschrijving]
  - Test: `tests/invariants/auth/test_never_xxx.py`
  - Rationale: [Waarom is dit een invariant?]

- [ ] **INV-SEC-002**: [Beschrijving]
  - Test: `tests/invariants/auth/test_never_yyy.py`

### Authorization

- [ ] **INV-SEC-010**: [Beschrijving]
  - Test: `tests/invariants/auth/test_never_zzz.py`

### Data Protection

- [ ] **INV-SEC-020**: [Beschrijving]
  - Test: `tests/invariants/security/test_never_xxx.py`

---

## Business Invariants

> Business rules die NOOIT mogen worden geschonden.

### Financial

- [ ] **INV-BIZ-001**: [Beschrijving]
  - Test: `tests/invariants/business/test_never_xxx.py`

### State Machine

- [ ] **INV-BIZ-010**: [Beschrijving]
  - Test: `tests/invariants/business/test_never_yyy.py`

### Data Integrity

- [ ] **INV-BIZ-020**: [Beschrijving]
  - Test: `tests/invariants/business/test_never_zzz.py`

---

## Performance Invariants

> Performance grenzen die NOOIT mogen worden overschreden.

### Response Times

- [ ] **INV-PERF-001**: [Beschrijving]
  - Test: `tests/invariants/performance/test_never_xxx.py`

### Resource Usage

- [ ] **INV-PERF-010**: [Beschrijving]
  - Test: `tests/invariants/performance/test_never_yyy.py`

---

## Reliability Invariants

> Condities voor system reliability.

### Error Handling

- [ ] **INV-REL-001**: [Beschrijving]
  - Test: `tests/invariants/reliability/test_never_xxx.py`

### Data Consistency

- [ ] **INV-REL-010**: [Beschrijving]
  - Test: `tests/invariants/reliability/test_never_yyy.py`

---

## Changelog

| Datum | Wijziging | Door |
|-------|-----------|------|
| YYYY-MM-DD | Initial invariants defined | [naam] |

---

Invariants v1.0.0 - Generated with BMAD Quality Kit
```

---

## ID Conventions

### Format
```
INV-<CATEGORY>-<NUMBER>
```

### Categories

| Prefix | Category | Description |
|--------|----------|-------------|
| `SEC` | Security | Auth, authz, data protection |
| `BIZ` | Business | Business rules, financial |
| `PERF` | Performance | Response time, resources |
| `REL` | Reliability | Error handling, consistency |

### Numbering

| Range | Subcategory |
|-------|-------------|
| 001-009 | First subcategory |
| 010-019 | Second subcategory |
| 020-029 | Third subcategory |
| etc. | etc. |

---

## Example Invariants

### Security

```markdown
- [ ] **INV-SEC-001**: Authenticated endpoints NEVER return data without valid token
  - Test: `tests/invariants/auth/test_never_auth_bypass.py`
  - Rationale: Prevents unauthorized data access

- [ ] **INV-SEC-002**: User data is NEVER exposed to other users
  - Test: `tests/invariants/auth/test_never_cross_user_data.py`
  - Rationale: Privacy protection, GDPR compliance

- [ ] **INV-SEC-020**: Passwords are NEVER stored in plaintext
  - Test: `tests/invariants/security/test_never_plaintext_passwords.py`
  - Rationale: Security best practice, breach protection
```

### Business

```markdown
- [ ] **INV-BIZ-001**: Invoice totals are NEVER negative
  - Test: `tests/invariants/business/test_never_negative_invoice.py`
  - Rationale: Financial integrity

- [ ] **INV-BIZ-010**: Order status NEVER skips intermediate states
  - Test: `tests/invariants/business/test_never_skip_order_status.py`
  - Rationale: Valid state machine, audit trail
```

### Performance

```markdown
- [ ] **INV-PERF-001**: API responses NEVER exceed 500ms p99
  - Test: `tests/invariants/performance/test_never_slow_api.py`
  - Rationale: SLA requirement, user experience

- [ ] **INV-PERF-020**: Database queries NEVER exceed 100 per request
  - Test: `tests/invariants/performance/test_never_n_plus_one.py`
  - Rationale: Prevent performance degradation
```

---

## Generating the File

### Manual
1. Run `/invariant-discovery`
2. Answer questions
3. Review generated invariants
4. Approve or adjust

### Automated Template
```bash
# Copy template
cp templates/invariants.md ./invariants.md

# Edit for project
vim invariants.md
```

---

## Updating the File

### When to Update
- New feature with security/business impact
- After security incident
- After CTO review finds gaps
- During architecture changes

### How to Update
1. Add new invariant with unique ID
2. Mark `- [ ]` for missing test
3. Add test file path
4. After writing test, mark `- [x]`
5. Update changelog
