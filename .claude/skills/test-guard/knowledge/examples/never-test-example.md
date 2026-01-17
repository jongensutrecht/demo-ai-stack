# NEVER-Test Complete Example

Dit is een volledig voorbeeld van een NEVER-test suite voor een e-commerce applicatie.

---

## Bestandsstructuur

```
tests/
└── invariants/
    ├── __init__.py
    ├── conftest.py
    │
    ├── auth/
    │   ├── __init__.py
    │   ├── test_never_auth_bypass.py
    │   └── test_never_cross_user_data.py
    │
    ├── business/
    │   ├── __init__.py
    │   ├── test_never_negative_values.py
    │   └── test_never_invalid_state.py
    │
    └── security/
        ├── __init__.py
        └── test_never_injection.py
```

---

## conftest.py

```python
# tests/invariants/conftest.py

import pytest
from httpx import AsyncClient
from app.main import app
from app.models import User, Order
from app.database import get_test_db

@pytest.fixture
async def db():
    """Provide test database connection."""
    async with get_test_db() as conn:
        yield conn
        # Cleanup after test
        await conn.rollback()

@pytest.fixture
async def client():
    """Async HTTP client for API testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def user_a(db) -> User:
    """Create test user A."""
    user = User(
        email="user_a@example.com",
        password_hash="hashed_password"
    )
    await db.add(user)
    await db.commit()
    return user

@pytest.fixture
async def user_a_token(user_a) -> str:
    """JWT token for user A."""
    from app.auth import create_token
    return create_token(user_a)

@pytest.fixture
async def user_b(db) -> User:
    """Create test user B."""
    user = User(
        email="user_b@example.com",
        password_hash="hashed_password"
    )
    await db.add(user)
    await db.commit()
    return user

@pytest.fixture
async def user_b_order(db, user_b) -> Order:
    """Create order owned by user B."""
    order = Order(
        user_id=user_b.id,
        total=100.00,
        status="pending"
    )
    await db.add(order)
    await db.commit()
    return order

@pytest.fixture
def expired_token() -> str:
    """JWT token that is expired."""
    from app.auth import create_token
    from datetime import datetime, timedelta
    return create_token(
        User(id=1),
        expires_at=datetime.now() - timedelta(hours=1)
    )
```

---

## test_never_auth_bypass.py

```python
# tests/invariants/auth/test_never_auth_bypass.py

"""
Invariant Tests: Authentication Bypass Prevention

These tests ensure that authentication NEVER fails to protect resources.
Every test in this file validates a NEVER condition.
"""

import pytest
from httpx import AsyncClient

# All protected endpoints that should NEVER be accessible without auth
PROTECTED_ENDPOINTS = [
    ("GET", "/api/users/me"),
    ("GET", "/api/orders"),
    ("POST", "/api/orders"),
    ("GET", "/api/settings"),
    ("PUT", "/api/settings"),
    ("GET", "/api/dashboard"),
]

class TestNeverAuthBypass:
    """
    Invariant: Protected endpoints NEVER return data without valid authentication.

    References:
    - invariants.md: INV-SEC-001
    - OWASP: Broken Authentication
    """

    @pytest.mark.parametrize("method,endpoint", PROTECTED_ENDPOINTS)
    async def test_NEVER_access_without_token(
        self, client: AsyncClient, method: str, endpoint: str
    ):
        """
        Protected endpoints NEVER return data without a token.

        Expected: 401 Unauthorized
        NEVER: 200 OK with data
        """
        if method == "GET":
            response = await client.get(endpoint)
        elif method == "POST":
            response = await client.post(endpoint, json={})
        elif method == "PUT":
            response = await client.put(endpoint, json={})

        assert response.status_code == 401, (
            f"INVARIANT VIOLATION [INV-SEC-001]: "
            f"{method} {endpoint} returned {response.status_code} without token. "
            f"Expected 401 Unauthorized."
        )

    @pytest.mark.parametrize("method,endpoint", PROTECTED_ENDPOINTS)
    async def test_NEVER_access_with_expired_token(
        self, client: AsyncClient, expired_token: str, method: str, endpoint: str
    ):
        """
        Protected endpoints NEVER accept expired tokens.

        Expected: 401 Unauthorized
        NEVER: 200 OK with data
        """
        headers = {"Authorization": f"Bearer {expired_token}"}

        if method == "GET":
            response = await client.get(endpoint, headers=headers)
        elif method == "POST":
            response = await client.post(endpoint, json={}, headers=headers)
        elif method == "PUT":
            response = await client.put(endpoint, json={}, headers=headers)

        assert response.status_code == 401, (
            f"INVARIANT VIOLATION [INV-SEC-001]: "
            f"{method} {endpoint} accepted expired token. "
            f"Response: {response.status_code}"
        )

    @pytest.mark.parametrize("invalid_token", [
        "invalid",
        "Bearer invalid",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature",
        "null",
        "",
        " ",
    ])
    async def test_NEVER_access_with_invalid_token(
        self, client: AsyncClient, invalid_token: str
    ):
        """
        Protected endpoints NEVER accept malformed tokens.

        Expected: 401 Unauthorized
        NEVER: 200 OK or server error
        """
        response = await client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {invalid_token}"}
        )

        assert response.status_code == 401, (
            f"INVARIANT VIOLATION [INV-SEC-001]: "
            f"Accepted invalid token '{invalid_token[:20]}...'. "
            f"Response: {response.status_code}"
        )
```

---

## test_never_cross_user_data.py

```python
# tests/invariants/auth/test_never_cross_user_data.py

"""
Invariant Tests: Cross-User Data Access Prevention

These tests ensure that users NEVER see other users' data.
"""

import pytest
from httpx import AsyncClient
from app.models import User, Order

class TestNeverCrossUserData:
    """
    Invariant: Users NEVER access other users' data.

    References:
    - invariants.md: INV-SEC-002
    - OWASP: Broken Access Control
    """

    async def test_NEVER_view_other_user_profile(
        self,
        client: AsyncClient,
        user_a_token: str,
        user_b: User
    ):
        """
        User A NEVER sees User B's profile.

        Expected: 403 Forbidden or 404 Not Found
        NEVER: 200 OK with User B's data
        """
        response = await client.get(
            f"/api/users/{user_b.id}",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        # Accept 403 (forbidden) or 404 (pretend it doesn't exist)
        assert response.status_code in [403, 404], (
            f"INVARIANT VIOLATION [INV-SEC-002]: "
            f"User A could access User B's profile. "
            f"Response: {response.status_code}, Body: {response.text[:100]}"
        )

    async def test_NEVER_view_other_user_orders(
        self,
        client: AsyncClient,
        user_a_token: str,
        user_b_order: Order
    ):
        """
        User A NEVER sees User B's orders in their order list.

        Expected: Only own orders in response
        NEVER: Other user's orders included
        """
        response = await client.get(
            "/api/orders",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        assert response.status_code == 200

        orders = response.json()
        for order in orders:
            assert order["user_id"] != user_b_order.user_id, (
                f"INVARIANT VIOLATION [INV-SEC-002]: "
                f"User A's order list contains User B's order {order['id']}"
            )

    async def test_NEVER_access_other_user_order_details(
        self,
        client: AsyncClient,
        user_a_token: str,
        user_b_order: Order
    ):
        """
        User A NEVER accesses User B's specific order.

        Expected: 403 Forbidden or 404 Not Found
        NEVER: 200 OK with order details
        """
        response = await client.get(
            f"/api/orders/{user_b_order.id}",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        assert response.status_code in [403, 404], (
            f"INVARIANT VIOLATION [INV-SEC-002]: "
            f"User A could access User B's order. "
            f"Response: {response.status_code}"
        )

    async def test_NEVER_modify_other_user_order(
        self,
        client: AsyncClient,
        user_a_token: str,
        user_b_order: Order
    ):
        """
        User A NEVER modifies User B's order.

        Expected: 403 Forbidden or 404 Not Found
        NEVER: 200 OK with modification success
        """
        response = await client.put(
            f"/api/orders/{user_b_order.id}",
            json={"status": "cancelled"},
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        assert response.status_code in [403, 404], (
            f"INVARIANT VIOLATION [INV-SEC-002]: "
            f"User A could modify User B's order. "
            f"Response: {response.status_code}"
        )

    async def test_NEVER_delete_other_user_order(
        self,
        client: AsyncClient,
        user_a_token: str,
        user_b_order: Order
    ):
        """
        User A NEVER deletes User B's order.

        Expected: 403 Forbidden or 404 Not Found
        NEVER: 200/204 with deletion success
        """
        response = await client.delete(
            f"/api/orders/{user_b_order.id}",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        assert response.status_code in [403, 404], (
            f"INVARIANT VIOLATION [INV-SEC-002]: "
            f"User A could delete User B's order. "
            f"Response: {response.status_code}"
        )
```

---

## test_never_negative_values.py

```python
# tests/invariants/business/test_never_negative_values.py

"""
Invariant Tests: Negative Value Prevention

These tests ensure that financial values are NEVER negative.
"""

import pytest
from decimal import Decimal
from app.services import InvoiceService, PaymentService

class TestNeverNegativeValues:
    """
    Invariant: Financial values NEVER become negative.

    References:
    - invariants.md: INV-BIZ-001, INV-BIZ-003
    """

    @pytest.fixture
    def invoice_service(self, db):
        return InvoiceService(db)

    @pytest.fixture
    def payment_service(self, db):
        return PaymentService(db)

    def test_NEVER_create_invoice_with_negative_total(self, invoice_service):
        """
        Invoice NEVER created with negative total.

        Expected: ValueError raised
        NEVER: Invoice with negative total created
        """
        with pytest.raises(ValueError, match="negative|must be positive"):
            invoice_service.create(
                customer_id=1,
                items=[{"description": "Item", "amount": Decimal("-100.00")}]
            )

    def test_NEVER_negative_line_item(self, invoice_service):
        """
        Invoice line items NEVER have negative amounts.

        Note: Discounts should use explicit discount_amount field.
        """
        with pytest.raises(ValueError):
            invoice_service.add_line_item(
                invoice_id=1,
                description="Discount",
                amount=Decimal("-50.00")  # Wrong: should use discount field
            )

    async def test_NEVER_refund_exceeds_payment(self, payment_service, db):
        """
        Refund NEVER exceeds original payment amount.

        Expected: ValueError raised
        NEVER: Refund processed for more than paid
        """
        # Setup: Create payment of 100.00
        payment = await payment_service.create_payment(
            invoice_id=1,
            amount=Decimal("100.00")
        )

        # Try to refund more than paid
        with pytest.raises(ValueError, match="exceeds|cannot refund"):
            await payment_service.refund(
                payment_id=payment.id,
                amount=Decimal("150.00")  # More than paid
            )

    async def test_NEVER_multiple_refunds_exceed_payment(self, payment_service, db):
        """
        Cumulative refunds NEVER exceed original payment.

        Expected: ValueError on second refund that would exceed total
        NEVER: Total refunds > original payment
        """
        # Setup: Payment of 100.00
        payment = await payment_service.create_payment(
            invoice_id=1,
            amount=Decimal("100.00")
        )

        # First refund: 60.00 (OK)
        await payment_service.refund(payment.id, Decimal("60.00"))

        # Second refund: 50.00 would exceed (60 + 50 = 110 > 100)
        with pytest.raises(ValueError, match="exceeds"):
            await payment_service.refund(payment.id, Decimal("50.00"))

    def test_NEVER_discount_exceeds_subtotal(self, invoice_service):
        """
        Discount NEVER results in negative total.

        Expected: ValueError or cap at zero
        NEVER: Invoice with negative total after discount
        """
        invoice = invoice_service.create(
            customer_id=1,
            items=[{"description": "Item", "amount": Decimal("100.00")}]
        )

        with pytest.raises(ValueError, match="exceeds|negative"):
            invoice_service.apply_discount(
                invoice_id=invoice.id,
                discount_percent=150  # 150% would be negative
            )
```

---

## Running the Tests

```bash
# Run all invariant tests
pytest tests/invariants/ -v

# Run with detailed output
pytest tests/invariants/ -v --tb=long

# Run specific category
pytest tests/invariants/auth/ -v

# Run specific invariant
pytest tests/invariants/ -k "INV-SEC-001" -v

# Run with coverage
pytest tests/invariants/ --cov=app --cov-report=html

# Fail fast on first violation
pytest tests/invariants/ -x
```

---

## Key Takeaways

1. **Naming**: `test_NEVER_<violation>` makes intent clear
2. **Assertion Messages**: Include invariant ID for traceability
3. **Comprehensive**: Test all edge cases for each invariant
4. **Fixtures**: Reusable test data setup
5. **Documentation**: Reference invariants.md in docstrings
