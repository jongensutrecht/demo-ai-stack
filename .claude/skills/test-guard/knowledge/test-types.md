# Test Types

Dit document beschrijft de verschillende testsoorten en wanneer ze te gebruiken.

---

## Unit Tests

**Wat**: Test individuele functies/klassen in isolatie.

**Kenmerken**:
- Geen externe dependencies (database, API's, filesystem)
- Mock/stub alle dependencies
- Snel (< 100ms per test)
- Deterministisch (altijd zelfde resultaat)

**Wanneer**:
- Pure business logic
- Utility functies
- Data transformaties
- Validatie logica

**Voorbeeld (Python)**:
```python
def test_calculate_tax():
    result = calculate_tax(100, rate=0.21)
    assert result == 21.0
```

**Voorbeeld (TypeScript)**:
```typescript
describe('calculateTax', () => {
  it('calculates 21% tax', () => {
    expect(calculateTax(100, 0.21)).toBe(21);
  });
});
```

---

## Integration Tests

**Wat**: Test interactie tussen componenten en externe systemen.

**Kenmerken**:
- Echte database (vaak in-memory of test container)
- Echte API calls (vaak naar test/mock server)
- Langzamer dan unit tests
- Test "happy path" + error scenarios

**Wanneer**:
- Database queries/mutations
- API endpoints
- Service layer
- Repositories/adapters

**Voorbeeld (Python)**:
```python
@pytest.fixture
def db():
    conn = create_test_db()
    yield conn
    conn.close()

def test_user_repository_save(db):
    repo = UserRepository(db)
    user = User(name="Test")
    repo.save(user)
    assert repo.find_by_name("Test") is not None
```

---

## E2E Tests (Playwright/Cypress)

**Wat**: Test complete user flows door de hele applicatie.

**Kenmerken**:
- Echte browser
- Echte UI interactie
- Langzaamst van alle tests
- Test vanuit gebruikersperspectief

**Wanneer**:
- UI componenten
- User flows (login, checkout, etc.)
- Forms en validatie
- Navigation

**Voorbeeld (Playwright)**:
```typescript
test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await page.fill('#email', 'test@example.com');
  await page.click('[data-testid="pay"]');
  await expect(page.locator('.success')).toBeVisible();
});
```

---

## Contract Tests

**Wat**: Valideer dat API implementatie matcht met specificatie.

**Kenmerken**:
- Test API tegen OpenAPI/Swagger spec
- Consumer-driven contracts (Pact)
- Voorkomt breaking changes
- Snel, geen echte calls nodig

**Wanneer**:
- API endpoints
- Microservice communicatie
- Externe API integraties
- Versie upgrades

**Voorbeeld (Dredd)**:
```bash
# Test API tegen OpenAPI spec
dredd openapi.yaml http://localhost:8080
```

**Voorbeeld (Pact)**:
```typescript
const pact = new Pact({
  consumer: 'Frontend',
  provider: 'UserService'
});

test('get user', async () => {
  await pact.addInteraction({
    state: 'user exists',
    uponReceiving: 'a request for user 1',
    withRequest: {
      method: 'GET',
      path: '/users/1'
    },
    willRespondWith: {
      status: 200,
      body: {
        id: 1,
        name: like('John')
      }
    }
  });
});
```

---

## NEVER-Tests (Invariant Tests)

**Wat**: Test dat iets NOOIT mag gebeuren.

**Kenmerken**:
- Negatieve test cases
- Security critical
- Business rule critical
- Vaak property-based

**Wanneer**:
- Security invariants (auth bypass, data leak)
- Business invariants (negative values, invalid states)
- Performance invariants (timeouts, memory)

**Voorbeeld**:
```python
def test_NEVER_user_sees_other_user_data():
    user1 = create_user()
    user2 = create_user()

    # User1 probeert data van user2 te zien
    response = client.get(
        f"/users/{user2.id}",
        headers={"Authorization": f"Bearer {user1.token}"}
    )

    # Dit mag NOOIT slagen
    assert response.status_code == 403
```

---

## Test Pyramid

```
        /\
       /  \
      / E2E \          <- Weinig, langzaam, duur
     /________\
    /          \
   / Integration\      <- Gemiddeld
  /______________\
 /                \
/      Unit        \   <- Veel, snel, goedkoop
/____________________\
```

**Ratio richtlijn**: 70% unit, 20% integration, 10% e2e

---

## Best Practices

1. **Test behavior, niet implementation**
   - Goed: "user can login"
   - Slecht: "login calls hashPassword with correct args"

2. **Arrange-Act-Assert pattern**
   ```python
   def test_something():
       # Arrange
       user = create_user()

       # Act
       result = user.do_something()

       # Assert
       assert result == expected
   ```

3. **One assertion per test** (meestal)
   - Maakt failures duidelijk
   - Exceptions: related assertions die samen horen

4. **Descriptive test names**
   - `test_user_cannot_access_other_user_data`
   - Niet: `test_auth_1`

5. **Test data isolatie**
   - Elke test maakt eigen data
   - Geen shared state tussen tests
   - Clean up na tests
