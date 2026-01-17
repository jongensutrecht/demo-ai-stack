# Invariant Test Patterns

## Wat is een NEVER-Test?

Test dat iets **NOOIT** mag gebeuren. Checkt failure, niet success.

## Naming Convention

```
test_NEVER_<wat_nooit_mag_gebeuren>
```

Docstring: `INV-XXX-NNN: <beschrijving>`

## Categories

| Category | Prefix | Voorbeeld |
|----------|--------|-----------|
| Security | INV-SEC | Auth bypass, data leak |
| Business | INV-BIZ | Negative amounts, invalid state |
| Performance | INV-PERF | Timeout, memory limit |
| Reliability | INV-REL | Crash, data loss |

## Script

```bash
# Haal NEVER-test voorbeelden op
python scripts/examples.py never
```

## Locatie

```
tests/invariants/
├── security/
│   └── test_inv_sec_001_auth.py
├── business/
│   └── test_inv_biz_001_amounts.py
└── conftest.py
```
