# When to Use Which Test Type

Dit document bevat de beslisboom voor het kiezen van testsoorten.

---

## Beslisboom

```
START: Welk type change heb je gemaakt?
│
├─► UI/Browser gerelateerd?
│   ├─► JA → Playwright/E2E test VERPLICHT
│   │   └─► Ook unit test als component logica heeft
│   └─► NEE ↓
│
├─► Raakt het een API endpoint?
│   ├─► JA → Meerdere tests nodig:
│   │   ├─► Unit test voor business logic
│   │   ├─► Integration test voor database/external calls
│   │   └─► Contract test voor API schema
│   └─► NEE ↓
│
├─► Database interactie?
│   ├─► JA → Integration test VERPLICHT
│   │   └─► Unit test voor query building logica
│   └─► NEE ↓
│
├─► Externe API/service call?
│   ├─► JA → Integration test VERPLICHT
│   │   └─► Mock in unit tests
│   └─► NEE ↓
│
├─► Pure business logic / utility?
│   ├─► JA → Unit test VERPLICHT
│   │   └─► Geen integration nodig
│   └─► NEE ↓
│
└─► Security/auth gerelateerd?
    └─► JA → NEVER-test VERPLICHT
        └─► Test dat ongeautoriseerde access NOOIT mogelijk is
```

---

## Quick Reference Table

| Je wijzigt... | Unit | Integration | E2E/Playwright | Contract |
|---------------|------|-------------|----------------|----------|
| UI Component | ✅ | - | ✅ | - |
| Page/Route | ✅ | - | ✅ | - |
| API Endpoint | ✅ | ✅ | - | ✅ |
| Database Query | ✅ | ✅ | - | - |
| External API Call | ✅ | ✅ | - | - |
| Business Logic | ✅ | - | - | - |
| Utility Function | ✅ | - | - | - |
| Auth/Security | ✅ | ✅ | ✅ | - |
| Configuration | ✅ | - | - | - |

---

## Specifieke Scenario's

### Scenario 1: Nieuwe React/Vue Component

**Required**: unit + playwright

```bash
# Wijziging
src/components/Button.tsx

# Benodigde tests
src/components/Button.test.tsx      # Unit: props, events, rendering
tests/e2e/components/button.spec.ts # Playwright: visual, interaction
```

**Unit test checkt**:
- Props worden correct verwerkt
- Events worden correct gefired
- Conditional rendering werkt

**Playwright test checkt**:
- Component is zichtbaar
- Klikken werkt
- Styling is correct
- Accessibility

---

### Scenario 2: Nieuwe API Endpoint

**Required**: unit + integration + contract

```bash
# Wijziging
api/routes/users.py

# Benodigde tests
tests/unit/test_users_logic.py       # Business logic
tests/integration/test_users_api.py  # Database + full endpoint
tests/contract/test_users_schema.py  # API contract
```

**Unit test checkt**:
- Validatie logica
- Business rules
- Error handling

**Integration test checkt**:
- Database operaties
- Full request/response cycle
- Auth flow

**Contract test checkt**:
- Response schema matcht OpenAPI
- Required fields aanwezig
- Types correct

---

### Scenario 3: Database Repository

**Required**: unit + integration

```bash
# Wijziging
repositories/user_repository.py

# Benodigde tests
tests/unit/test_user_repository_query.py     # Query building
tests/integration/test_user_repository.py    # Echte DB operaties
```

**Unit test checkt**:
- Query parameters correct
- SQL/ORM constructie

**Integration test checkt**:
- CRUD operaties werken
- Transacties correct
- Constraints gerespecteerd

---

### Scenario 4: Pure Utility Function

**Required**: unit only

```bash
# Wijziging
utils/format.py

# Benodigde tests
tests/unit/test_format.py
```

**Unit test checkt**:
- Alle input varianten
- Edge cases
- Error cases

---

### Scenario 5: Auth/Security Change

**Required**: unit + integration + NEVER-tests

```bash
# Wijziging
auth/middleware.py

# Benodigde tests
tests/unit/test_auth_middleware.py           # Logic
tests/integration/test_auth_flow.py          # Full flow
tests/invariants/auth/test_never_bypass.py   # NEVER-tests
```

**NEVER-tests checken**:
- Toegang zonder token → 401
- Expired token → 401
- Invalid token → 401
- Wrong role → 403
- Cross-user access → 403

---

## Common Mistakes

### ❌ Alleen unit tests voor UI

```
Wijziging: Button.tsx
Tests: Button.test.tsx (unit only)
```

**Probleem**: Rendering bugs gemist, styling issues, browser compatibility.

**Fix**: Voeg Playwright test toe.

---

### ❌ Geen contract test voor API

```
Wijziging: /api/users endpoint
Tests: test_users.py (integration only)
```

**Probleem**: API schema kan breken zonder dat tests falen.

**Fix**: Voeg contract test tegen OpenAPI spec toe.

---

### ❌ Mocks in integration tests

```python
# SLECHT: Dit is geen echte integration test
def test_user_save(mock_db):
    repo = UserRepository(mock_db)  # Mock!
    repo.save(user)
```

**Probleem**: Echte database gedrag niet getest.

**Fix**: Gebruik echte test database.

---

### ❌ Geen NEVER-tests voor security

```
Wijziging: auth/login.py
Tests: test_login_success.py
```

**Probleem**: Alleen happy path getest, security bypass mogelijk.

**Fix**: Voeg NEVER-tests toe voor alle auth bypasses.

---

## Checklist bij Code Review

- [ ] Elk gewijzigd bestand heeft de juiste testsoorten
- [ ] UI changes hebben Playwright tests
- [ ] API changes hebben contract tests
- [ ] DB changes hebben integration tests
- [ ] Security changes hebben NEVER-tests
- [ ] Tests testen behavior, niet implementation
