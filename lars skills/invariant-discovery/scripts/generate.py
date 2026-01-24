#!/usr/bin/env python3
"""Generate invariants.md template.

Usage:
    python generate.py          # Show template
    python generate.py ids      # Show ID conventions
    python generate.py examples # Show example invariants
"""
import sys

TEMPLATE = """
# Project Invariants

> Dit document beschrijft wat NOOIT mag gebeuren in dit project.
> Elke invariant MOET een bijbehorende NEVER-test hebben.

---

## Security Invariants

### Authentication
- [ ] **INV-SEC-001**: [Beschrijving]
  - Test: `tests/invariants/auth/test_never_xxx.py`

### Authorization
- [ ] **INV-SEC-010**: [Beschrijving]
  - Test: `tests/invariants/auth/test_never_yyy.py`

### Data Protection
- [ ] **INV-SEC-020**: [Beschrijving]
  - Test: `tests/invariants/security/test_never_zzz.py`

---

## Business Invariants

### Financial
- [ ] **INV-BIZ-001**: [Beschrijving]
  - Test: `tests/invariants/business/test_never_xxx.py`

### State Machine
- [ ] **INV-BIZ-010**: [Beschrijving]
  - Test: `tests/invariants/business/test_never_yyy.py`

---

## Performance Invariants

### Response Times
- [ ] **INV-PERF-001**: [Beschrijving]
  - Test: `tests/invariants/performance/test_never_xxx.py`

---

## Changelog

| Datum | Wijziging | Door |
|-------|-----------|------|
| YYYY-MM-DD | Initial invariants defined | [naam] |
"""

IDS = """
## ID Conventions

Format: INV-<CATEGORY>-<NUMBER>

### Categories
| Prefix | Category | Description |
|--------|----------|-------------|
| SEC | Security | Auth, authz, data protection |
| BIZ | Business | Business rules, financial |
| PERF | Performance | Response time, resources |
| REL | Reliability | Error handling, consistency |

### Numbering
| Range | Subcategory |
|-------|-------------|
| 001-009 | First subcategory |
| 010-019 | Second subcategory |
| 020-029 | Third subcategory |
"""

EXAMPLES = """
## Example Invariants

### Security
- [ ] **INV-SEC-001**: Authenticated endpoints NEVER return data without valid token
  - Test: `tests/invariants/auth/test_never_auth_bypass.py`
  - Rationale: Prevents unauthorized data access

- [ ] **INV-SEC-002**: User data is NEVER exposed to other users
  - Test: `tests/invariants/auth/test_never_cross_user_data.py`
  - Rationale: Privacy protection, GDPR compliance

### Business
- [ ] **INV-BIZ-001**: Invoice totals are NEVER negative
  - Test: `tests/invariants/business/test_never_negative_invoice.py`
  - Rationale: Financial integrity

- [ ] **INV-BIZ-010**: Order status NEVER skips intermediate states
  - Test: `tests/invariants/business/test_never_skip_order_status.py`
  - Rationale: Valid state machine, audit trail

### Performance
- [ ] **INV-PERF-001**: API responses NEVER exceed 500ms p99
  - Test: `tests/invariants/performance/test_never_slow_api.py`
  - Rationale: SLA requirement, user experience
"""

def main():
    if len(sys.argv) < 2:
        print(TEMPLATE)
        return

    cmd = sys.argv[1].lower()
    if cmd == "ids":
        print(IDS)
    elif cmd == "examples":
        print(EXAMPLES)
    else:
        print(f"Unknown: {cmd}")
        print("Usage: python generate.py [ids|examples]")

if __name__ == "__main__":
    main()
