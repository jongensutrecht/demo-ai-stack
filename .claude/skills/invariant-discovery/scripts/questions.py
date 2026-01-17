#!/usr/bin/env python3
"""Invariant discovery questions.

Usage:
    python questions.py security    # Security vragen
    python questions.py business    # Business vragen
    python questions.py performance # Performance vragen
    python questions.py all         # Alle vragen
    python questions.py commands    # Discovery commands
"""
import sys

SECURITY = """
## Security Discovery Questions

### Authentication
- Welke endpoints zijn beveiligd met authenticatie?
- Mogen expired tokens OOIT geaccepteerd worden?
- Mogen invalid tokens OOIT resulteren in data access?

### Authorization
- Welke rollen zijn er (user, admin, superadmin)?
- Welke acties zijn admin-only?
- Mag een user OOIT data van een andere user zien/modificeren?
- Is er tenant isolation? Mag data van tenant A OOIT zichtbaar zijn voor tenant B?

### Data Protection
- Welke data is gevoelig (passwords, tokens, PII)?
- Mag gevoelige data OOIT in logs/error messages/URLs verschijnen?
- Welke data moet encrypted opgeslagen worden?

### Input Validation
- Zijn er database queries met user input?
- Kunnen users files uploaden?

### API Security
- Zijn er rate limits?
- Welke origins zijn toegestaan?

## Typische Security Invarianten
- INV-SEC-001: Protected endpoints NEVER return data without valid token
- INV-SEC-002: User data is NEVER exposed to other users
- INV-SEC-020: Passwords are NEVER stored in plaintext
- INV-SEC-021: Sensitive data is NEVER logged
- INV-SEC-030: SQL injection is NEVER possible
- INV-SEC-031: XSS is NEVER possible
"""

BUSINESS = """
## Business Discovery Questions

### Financial Integrity
- Welke velden representeren geld (price, amount, total)?
- Mogen deze waarden OOIT negatief zijn?
- Mogen refunds OOIT het originele bedrag overschrijden?
- Mogen dubbele betalingen OOIT voorkomen?

### State Machines
- Welke statussen zijn er (pending, confirmed, shipped, etc.)?
- Wat is de geldige state flow?
- Welke transities zijn NOOIT toegestaan?
- Welke statussen zijn eindig (completed, cancelled)?
- Mag een terminal state OOIT verlaten worden?

### Data Integrity
- Welke parent-child relaties zijn er?
- Mogen orphaned records OOIT ontstaan?
- Welke velden moeten uniek zijn?
- Mogen totalen OOIT afwijken van line items?

### Business Rules
- Zijn er minimum/maximum waarden?
- Mogen negatieve hoeveelheden OOIT voorkomen?
- Zijn er deadline/expiratie regels?

### Audit & Compliance
- Welke acties moeten gelogd worden?
- Mogen deletes OOIT zonder audit trail?

## Typische Business Invarianten
- INV-BIZ-001: Invoice totals are NEVER negative
- INV-BIZ-002: Payments are NEVER processed twice
- INV-BIZ-010: Order status NEVER skips intermediate states
- INV-BIZ-011: Completed orders are NEVER modified
- INV-BIZ-020: Parent-child relationships are NEVER orphaned
- INV-BIZ-030: Stock is NEVER oversold
"""

PERFORMANCE = """
## Performance Discovery Questions

### Response Time
- Wat is de acceptable response time voor API calls?
- Zijn er SLA requirements?
- Wat is de maximum runtime voor background jobs?

### Resource Usage
- Wat is de maximum memory per request?
- Hoeveel database connections zijn er maximaal?

### Database Performance
- Hoeveel queries zijn acceptabel per request?
- Mogen N+1 queries OOIT voorkomen?
- Wat is de maximum query duration?

### Concurrency
- Welke operaties zijn concurrency-sensitive?
- Mogen race conditions OOIT data corrumperen?
- Mogen deadlocks OOIT voorkomen?

### Scalability
- Hoeveel requests per seconde moet het systeem aan?
- Hoe groot kunnen datasets worden?

## Typische Performance Invarianten
- INV-PERF-001: API responses NEVER exceed 500ms p99
- INV-PERF-010: Memory usage NEVER exceeds 512MB per request
- INV-PERF-020: Database queries NEVER exceed 100 per request
- INV-PERF-021: N+1 queries are NEVER introduced
- INV-PERF-030: Race conditions NEVER cause data corruption
"""

COMMANDS = """
## Discovery Commands

### Security
```bash
# Auth patterns
rg -l "auth|token|session|login" --type py
rg "@require_auth|@login_required|@jwt_required" --type py

# Role checks
rg "is_admin|role.*admin|hasRole|checkPermission" --type py

# User-specific queries
rg "user_id.*=|owner_id.*=|created_by.*=" --type py

# Sensitive data
rg "password|secret|api_key|token|ssn|credit_card" --type py
```

### Business
```bash
# Status/state fields
rg "status|state" --type py | head -50
rg "enum.*Status|Status.*enum" --type py

# Financial fields
rg "price|amount|total|subtotal|tax|discount" --type py

# Unique constraints
rg "unique=True|UniqueConstraint|unique_together" --type py
```

### Performance
```bash
# Slow operations
rg "sleep|time\\.sleep" --type py
rg "for.*in.*for.*in" --type py  # Nested loops

# Database queries
rg "\\.all\\(\\)|\\.filter\\(|SELECT.*FROM" --type py

# Concurrency
rg "Lock|Semaphore|asyncio|threading" --type py
```
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python questions.py [security|business|performance|all|commands]")
        return

    cmd = sys.argv[1].lower()
    if cmd == "security":
        print(SECURITY)
    elif cmd == "business":
        print(BUSINESS)
    elif cmd == "performance":
        print(PERFORMANCE)
    elif cmd == "commands":
        print(COMMANDS)
    elif cmd == "all":
        print(SECURITY)
        print(BUSINESS)
        print(PERFORMANCE)
    else:
        print(f"Unknown: {cmd}")
        print("Usage: python questions.py [security|business|performance|all|commands]")

if __name__ == "__main__":
    main()
