# Invariants Output Format

## Template Structuur

```markdown
# Project Invariants

## Security Invariants
- [ ] **INV-SEC-001**: [Beschrijving]
  - Test: `tests/invariants/auth/test_never_xxx.py`

## Business Invariants
- [ ] **INV-BIZ-001**: [Beschrijving]
  - Test: `tests/invariants/business/test_never_xxx.py`

## Performance Invariants
- [ ] **INV-PERF-001**: [Beschrijving]
  - Test: `tests/invariants/performance/test_never_xxx.py`
```

## ID Format

`INV-<CATEGORY>-<NUMBER>`

| Prefix | Category |
|--------|----------|
| SEC | Security |
| BIZ | Business |
| PERF | Performance |
| REL | Reliability |

## Details

Volledige template en voorbeelden: `python scripts/generate.py`
