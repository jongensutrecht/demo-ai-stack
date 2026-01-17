# Invariant Test Patterns

Dit document beschrijft hoe je NEVER-tests schrijft voor invarianten.

---

## Wat is een NEVER-Test?

Een NEVER-test valideert dat iets **NOOIT** mag gebeuren. In tegenstelling tot normale tests die checken dat iets werkt, checken NEVER-tests dat iets **NIET** werkt.

---

## Naming Convention

```
test_NEVER_<wat_nooit_mag_gebeuren>
```

Voorbeelden:
- `test_NEVER_user_sees_other_user_data`
- `test_NEVER_negative_invoice_total`
- `test_NEVER_unauthorized_admin_access`
- `test_NEVER_sql_injection`

---

## Pattern 1: Auth Bypass Prevention

**Invariant**: Authenticated endpoints NEVER return data without valid token.

```python
# tests/invariants/auth/test_never_auth_bypass.py

import pytest
from httpx import AsyncClient

class TestNeverAuthBypass:
    """Invariant: Protected endpoints NEVER return data without auth."""

    @pytest.mark.parametrize("endpoint", [
        "/api/users",
        "/api/orders",
        "/api/dashboard",
        "/api/settings",
    ])
    async def test_NEVER_access_without_token(self, client: AsyncClient, endpoint: str):
        """No token → NEVER return data."""
        response = await client.get(endpoint)

        assert response.status_code == 401, \
            f"INVARIANT VIOLATION: {endpoint} returned {response.status_code} without token"

    @pytest.mark.parametrize("endpoint", [
        "/api/users",
        "/api/orders",
    ])
    async def test_NEVER_access_with_expired_token(
        self, client: AsyncClient, expired_token: str, endpoint: str
    ):
        """Expired token → NEVER return data."""
        response = await client.get(
            endpoint,
            headers={"Authorization": f"Bearer {expired_token}"}
        )

        assert response.status_code == 401, \
            f"INVARIANT VIOLATION: {endpoint} accepted expired token"

    async def test_NEVER_access_with_invalid_token(self, client: AsyncClient):
        """Invalid token → NEVER return data."""
        response = await client.get(
            "/api/users",
            headers={"Authorization": "Bearer invalid.token.here"}
        )

        assert response.status_code == 401
```

---

## Pattern 2: Cross-User Data Leak Prevention

**Invariant**: User data is NEVER exposed to other users.

```python
# tests/invariants/auth/test_never_cross_user_data.py

class TestNeverCrossUserData:
    """Invariant: Users NEVER see other users' data."""

    async def test_NEVER_view_other_user_profile(
        self, client: AsyncClient, user_a_token: str, user_b: User
    ):
        """User A → NEVER see User B's profile."""
        response = await client.get(
            f"/api/users/{user_b.id}",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        # Should be 403 Forbidden, not 200 with data
        assert response.status_code == 403, \
            f"INVARIANT VIOLATION: User A could view User B's profile"

    async def test_NEVER_list_other_user_orders(
        self, client: AsyncClient, user_a_token: str, user_b: User
    ):
        """User A → NEVER see User B's orders."""
        response = await client.get(
            "/api/orders",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        if response.status_code == 200:
            orders = response.json()
            for order in orders:
                assert order["user_id"] != user_b.id, \
                    f"INVARIANT VIOLATION: User A saw User B's order {order['id']}"
```

---

## Pattern 3: Negative Value Prevention

**Invariant**: Invoice totals are NEVER negative.

```python
# tests/invariants/business/test_never_negative_invoice.py

import pytest
from decimal import Decimal

class TestNeverNegativeInvoice:
    """Invariant: Invoice totals NEVER become negative."""

    def test_NEVER_create_negative_invoice(self, invoice_service):
        """Creating invoice with negative total → NEVER allowed."""
        with pytest.raises(ValueError, match="negative"):
            invoice_service.create(
                customer_id=1,
                items=[{"amount": Decimal("-100.00")}]
            )

    def test_NEVER_refund_exceeds_total(self, invoice_service, paid_invoice):
        """Refund > original amount → NEVER allowed."""
        original_total = paid_invoice.total

        with pytest.raises(ValueError, match="exceeds"):
            invoice_service.refund(
                invoice_id=paid_invoice.id,
                amount=original_total + Decimal("1.00")
            )

    def test_NEVER_discount_below_zero(self, invoice_service, invoice):
        """Discount that results in negative → NEVER applied."""
        with pytest.raises(ValueError):
            invoice_service.apply_discount(
                invoice_id=invoice.id,
                discount_percent=150  # 150% discount would be negative
            )
```

---

## Pattern 4: State Machine Violation Prevention

**Invariant**: Order status NEVER skips intermediate states.

```python
# tests/invariants/business/test_never_skip_order_status.py

import pytest
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Valid transitions
VALID_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],  # Terminal state
    OrderStatus.CANCELLED: [],  # Terminal state
}

class TestNeverSkipOrderStatus:
    """Invariant: Order status transitions follow valid paths only."""

    @pytest.mark.parametrize("from_status,to_status", [
        (OrderStatus.PENDING, OrderStatus.SHIPPED),      # Skip confirmed
        (OrderStatus.PENDING, OrderStatus.DELIVERED),    # Skip 2 states
        (OrderStatus.CONFIRMED, OrderStatus.DELIVERED),  # Skip shipped
        (OrderStatus.DELIVERED, OrderStatus.PENDING),    # Reverse
        (OrderStatus.CANCELLED, OrderStatus.CONFIRMED),  # From terminal
    ])
    def test_NEVER_invalid_status_transition(
        self, order_service, order, from_status, to_status
    ):
        """Invalid state transitions → NEVER allowed."""
        order.status = from_status

        with pytest.raises(ValueError, match="Invalid transition"):
            order_service.update_status(order.id, to_status)
```

---

## Pattern 5: SQL Injection Prevention

**Invariant**: SQL injection is NEVER possible.

```python
# tests/invariants/security/test_never_sql_injection.py

import pytest

SQL_INJECTION_PAYLOADS = [
    "'; DROP TABLE users; --",
    "1 OR 1=1",
    "1; DELETE FROM orders WHERE 1=1",
    "' UNION SELECT * FROM passwords --",
    "admin'--",
]

class TestNeverSQLInjection:
    """Invariant: SQL injection NEVER works."""

    @pytest.mark.parametrize("payload", SQL_INJECTION_PAYLOADS)
    async def test_NEVER_sql_injection_in_search(
        self, client: AsyncClient, valid_token: str, payload: str
    ):
        """SQL injection in search → NEVER executes."""
        response = await client.get(
            "/api/search",
            params={"q": payload},
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        # Should return empty results or 400, not crash or leak data
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            # Verify no unexpected data leaked
            data = response.json()
            assert "password" not in str(data).lower()

    @pytest.mark.parametrize("payload", SQL_INJECTION_PAYLOADS)
    async def test_NEVER_sql_injection_in_login(
        self, client: AsyncClient, payload: str
    ):
        """SQL injection in login → NEVER bypasses auth."""
        response = await client.post(
            "/api/login",
            json={"username": payload, "password": payload}
        )

        # Should be 401 Unauthorized, not 200
        assert response.status_code == 401
```

---

## Pattern 6: Performance Degradation Prevention

**Invariant**: API responses NEVER exceed 500ms p99.

```python
# tests/invariants/performance/test_never_slow_api.py

import pytest
import time
import statistics

class TestNeverSlowAPI:
    """Invariant: API response time NEVER exceeds thresholds."""

    @pytest.mark.parametrize("endpoint", [
        "/api/health",
        "/api/users/me",
        "/api/orders",
    ])
    async def test_NEVER_slow_response(
        self, client: AsyncClient, valid_token: str, endpoint: str
    ):
        """Response time → NEVER exceeds 500ms."""
        times = []

        for _ in range(10):
            start = time.perf_counter()
            await client.get(
                endpoint,
                headers={"Authorization": f"Bearer {valid_token}"}
            )
            elapsed = (time.perf_counter() - start) * 1000  # ms
            times.append(elapsed)

        p99 = statistics.quantiles(times, n=100)[98]

        assert p99 < 500, \
            f"INVARIANT VIOLATION: {endpoint} p99 = {p99:.0f}ms > 500ms"
```

---

## Pattern 7: Data Integrity Prevention

**Invariant**: Partial writes NEVER corrupt state.

```python
# tests/invariants/reliability/test_never_partial_corruption.py

import pytest
import asyncio

class TestNeverPartialCorruption:
    """Invariant: Partial failures NEVER leave corrupted state."""

    async def test_NEVER_partial_order_creation(
        self, db, order_service, products
    ):
        """Failed order creation → NEVER creates partial data."""
        initial_order_count = await db.count("orders")
        initial_item_count = await db.count("order_items")

        # Force failure mid-transaction
        with pytest.raises(Exception):
            await order_service.create_order(
                customer_id=1,
                items=[
                    {"product_id": products[0].id, "qty": 1},  # Valid
                    {"product_id": 99999, "qty": 1},           # Invalid - will fail
                ]
            )

        # Verify no partial data left behind
        final_order_count = await db.count("orders")
        final_item_count = await db.count("order_items")

        assert final_order_count == initial_order_count, \
            "INVARIANT VIOLATION: Partial order was created"
        assert final_item_count == initial_item_count, \
            "INVARIANT VIOLATION: Partial order items were created"
```

---

## Test File Organization

```
tests/
└── invariants/
    ├── __init__.py
    ├── conftest.py           # Shared fixtures
    │
    ├── auth/
    │   ├── __init__.py
    │   ├── test_never_auth_bypass.py
    │   └── test_never_cross_user_data.py
    │
    ├── security/
    │   ├── __init__.py
    │   ├── test_never_sql_injection.py
    │   └── test_never_xss.py
    │
    ├── business/
    │   ├── __init__.py
    │   ├── test_never_negative_invoice.py
    │   └── test_never_skip_order_status.py
    │
    ├── performance/
    │   ├── __init__.py
    │   └── test_never_slow_api.py
    │
    └── reliability/
        ├── __init__.py
        └── test_never_partial_corruption.py
```

---

## Running NEVER-Tests

```bash
# Run all invariant tests
pytest tests/invariants/ -v

# Run specific category
pytest tests/invariants/security/ -v

# Run with coverage
pytest tests/invariants/ --cov=src --cov-report=term-missing

# Run in CI (fail fast)
pytest tests/invariants/ -x --tb=short
```

---

## Common Mistakes

### ❌ Testing that something works (not NEVER)

```python
# SLECHT: Dit is een positieve test, geen NEVER-test
def test_user_can_see_own_data():
    response = client.get("/api/me")
    assert response.status_code == 200
```

### ✅ Testing that something NEVER happens

```python
# GOED: Dit test dat iets NOOIT mag
def test_NEVER_user_sees_other_user_data():
    response = client.get(f"/api/users/{other_user.id}")
    assert response.status_code == 403
```

---

## Checklist

- [ ] Elke invariant in `invariants.md` heeft een NEVER-test
- [ ] Test naam begint met `test_NEVER_`
- [ ] Test valideert dat iets NIET gebeurt
- [ ] Assertion messages zijn duidelijk
- [ ] Tests zijn in `tests/invariants/` folder
