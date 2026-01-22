#!/usr/bin/env python3
"""
Test examples generator - progressive loading for Claude skills.
Run: python examples.py <type>
Types: unit, playwright, contract, never, all
"""

import sys

EXAMPLES = {
    "unit": '''
# Unit Test Example

```python
import pytest
from app.services.calculator import calculate_discount

class TestCalculateDiscount:
    """Unit tests for discount calculation."""

    def test_returns_zero_for_no_items(self):
        assert calculate_discount([]) == 0

    def test_applies_10_percent_over_100(self):
        result = calculate_discount([{"price": 150}])
        assert result == 15.0

    def test_never_returns_negative(self):
        """NEVER-test: discount is never negative."""
        result = calculate_discount([{"price": -50}])
        assert result >= 0
```

## Kenmerken Unit Test:
- Isoleert één functie/klasse
- Mockt dependencies
- Snel (<100ms)
- Geen database/netwerk
''',

    "playwright": '''
# Playwright E2E Test Example

```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test('user can login with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'user@test.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('NEVER shows password in URL', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[data-testid="password"]', 'secret');
    await page.click('[data-testid="submit"]');

    expect(page.url()).not.toContain('secret');
  });
});
```

## Kenmerken Playwright:
- Test echte browser interactie
- Gebruiker perspectief
- Langzamer (seconden)
- Nodig voor UI flows
''',

    "contract": '''
# Contract Test Example

```python
import pytest
from pact import Verifier

class TestAPIContract:
    """Verify API matches OpenAPI spec."""

    def test_users_endpoint_matches_contract(self):
        verifier = Verifier(provider='UserService')

        output, _ = verifier.verify_pacts(
            './pacts/consumer-userservice.json',
            provider_base_url='http://localhost:8000'
        )

        assert output == 0

    def test_response_schema_valid(self, client):
        response = client.get('/api/users/1')

        # Must match OpenAPI schema
        assert 'id' in response.json()
        assert 'email' in response.json()
        assert isinstance(response.json()['id'], int)
```

## Kenmerken Contract Test:
- Valideert API tegen spec
- Voorkomt breaking changes
- Consumer-driven
- Draait in CI
''',

    "never": '''
# NEVER-Test Patterns

## Pattern 1: Security Invariant
```python
@pytest.mark.asyncio
async def test_NEVER_returns_data_without_auth(client):
    """INV-SEC-001: Data NEVER accessible without API key."""
    response = await client.get("/api/data")
    assert response.status_code == 401
    assert "data" not in response.json()
```

## Pattern 2: Business Invariant
```python
@pytest.mark.asyncio
async def test_NEVER_negative_balance(db_session):
    """INV-BIZ-001: Account balance NEVER negative."""
    accounts = await db_session.execute(select(Account))
    for account in accounts.scalars():
        assert account.balance >= 0, f"Account {account.id} has negative balance"
```

## Pattern 3: Performance Invariant
```python
@pytest.mark.asyncio
async def test_NEVER_exceeds_response_time(client):
    """INV-PERF-001: API response NEVER exceeds 500ms."""
    import time
    start = time.time()
    await client.get("/api/health")
    duration = time.time() - start
    assert duration < 0.5
```

## Naming Convention:
- Prefix: `test_NEVER_`
- Docstring: `INV-XXX-NNN: <what NEVER happens>`
- Assert: failure condition, not success
'''
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python examples.py <type>")
        print("Types: unit, playwright, contract, never, all")
        sys.exit(1)

    example_type = sys.argv[1].lower()

    if example_type == "all":
        for name, content in EXAMPLES.items():
            print(f"\n{'='*60}")
            print(f"# {name.upper()}")
            print('='*60)
            print(content)
    elif example_type in EXAMPLES:
        print(EXAMPLES[example_type])
    else:
        print(f"Unknown type: {example_type}")
        print(f"Available: {', '.join(EXAMPLES.keys())}, all")
        sys.exit(1)


if __name__ == "__main__":
    main()
