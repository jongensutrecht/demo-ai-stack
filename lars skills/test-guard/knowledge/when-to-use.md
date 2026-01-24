# When to Use Which Test Type

## Beslisboom

```
UI/Browser? → playwright + unit
API endpoint? → unit + integration + contract
Database? → integration + unit
External API? → integration (+ mock in unit)
Pure logic? → unit
Security? → NEVER-test
```

## Quick Reference

| Je wijzigt... | Unit | Integration | Playwright | Contract | NEVER |
|---------------|------|-------------|------------|----------|-------|
| UI Component | ✅ | - | ✅ | - | - |
| API Endpoint | ✅ | ✅ | - | ✅ | - |
| Database/Repo | ✅ | ✅ | - | - | - |
| Business Logic | ✅ | - | - | - | - |
| Auth/Security | ✅ | ✅ | - | - | ✅ |
| Config | ✅ | - | - | - | - |

## Script

```bash
# Laat script beslissen
python scripts/decide.py <file_path>
```
