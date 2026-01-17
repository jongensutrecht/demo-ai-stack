# Contract Test Example

## OpenAPI Validation met Dredd

### OpenAPI Spec

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: integer
        email:
          type: string
          format: email
        name:
          type: string
        created_at:
          type: string
          format: date-time
```

### Dredd Test

```bash
# Install
npm install -g dredd

# Run
dredd openapi.yaml http://localhost:8080
```

### Dredd Hooks (Python)

```python
# dredd_hooks.py

import dredd_hooks as hooks
import json

@hooks.before_all
def setup(transactions):
    """Setup before all transactions."""
    # Create test data, get auth token, etc.
    pass

@hooks.before("/users/{id} > GET > 200")
def before_get_user(transaction):
    """Setup for GET /users/{id}."""
    # Ensure user exists
    transaction['request']['uri'] = '/users/1'

@hooks.before("/users/{id} > GET > 404")
def before_get_user_not_found(transaction):
    """Setup for GET /users/{id} 404."""
    transaction['request']['uri'] = '/users/99999'
```

---

## Pact Consumer-Driven Contracts

### Consumer Test (Frontend)

```typescript
// tests/contract/userService.pact.ts

import { Pact, Matchers } from '@pact-foundation/pact';
import path from 'path';
import { UserService } from '../src/services/userService';

const { like, eachLike } = Matchers;

describe('UserService Contract', () => {
  const provider = new Pact({
    consumer: 'WebApp',
    provider: 'UserService',
    port: 1234,
    log: path.resolve(process.cwd(), 'logs', 'pact.log'),
    dir: path.resolve(process.cwd(), 'pacts'),
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());
  afterEach(() => provider.verify());

  describe('getUser', () => {
    it('returns user when found', async () => {
      // Arrange: Define expected interaction
      await provider.addInteraction({
        state: 'user with id 1 exists',
        uponReceiving: 'a request for user 1',
        withRequest: {
          method: 'GET',
          path: '/users/1',
          headers: {
            Accept: 'application/json',
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            id: like(1),
            email: like('user@example.com'),
            name: like('John Doe'),
          },
        },
      });

      // Act
      const service = new UserService('http://localhost:1234');
      const user = await service.getUser(1);

      // Assert
      expect(user.id).toBe(1);
      expect(user.email).toMatch(/@/);
    });

    it('returns 404 when user not found', async () => {
      await provider.addInteraction({
        state: 'user with id 999 does not exist',
        uponReceiving: 'a request for non-existent user',
        withRequest: {
          method: 'GET',
          path: '/users/999',
        },
        willRespondWith: {
          status: 404,
          body: {
            error: like('User not found'),
          },
        },
      });

      const service = new UserService('http://localhost:1234');

      await expect(service.getUser(999)).rejects.toThrow('not found');
    });
  });

  describe('listUsers', () => {
    it('returns array of users', async () => {
      await provider.addInteraction({
        state: 'users exist',
        uponReceiving: 'a request for all users',
        withRequest: {
          method: 'GET',
          path: '/users',
        },
        willRespondWith: {
          status: 200,
          body: eachLike({
            id: like(1),
            email: like('user@example.com'),
            name: like('John'),
          }),
        },
      });

      const service = new UserService('http://localhost:1234');
      const users = await service.listUsers();

      expect(users).toBeInstanceOf(Array);
      expect(users.length).toBeGreaterThan(0);
    });
  });
});
```

### Provider Verification (Backend)

```python
# tests/contract/test_pact_verification.py

import pytest
from pact import Verifier

PACT_BROKER_URL = "http://pact-broker.local"
PROVIDER_URL = "http://localhost:8080"

@pytest.fixture(scope="module")
def pact_verifier():
    return Verifier(
        provider="UserService",
        provider_base_url=PROVIDER_URL,
    )

def test_pact_verification(pact_verifier):
    """Verify provider against consumer contracts."""

    # Setup provider states
    pact_verifier.set_state(
        PROVIDER_URL + "/_pact/provider-states",
        teardown=True
    )

    # Verify all pacts from broker
    success, logs = pact_verifier.verify_with_broker(
        broker_url=PACT_BROKER_URL,
        publish_version="1.0.0",
        enable_pending=True,
    )

    assert success, f"Pact verification failed:\n{logs}"
```

### Provider State Handler

```python
# app/pact_states.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/_pact/provider-states", methods=["POST"])
def provider_states():
    """Handle provider state setup."""
    state = request.json.get("state")

    handlers = {
        "user with id 1 exists": setup_user_1,
        "user with id 999 does not exist": lambda: None,
        "users exist": setup_users,
    }

    handler = handlers.get(state)
    if handler:
        handler()
        return jsonify({"result": "ok"})

    return jsonify({"error": f"Unknown state: {state}"}), 400

def setup_user_1():
    """Create user with id 1."""
    db.users.insert({
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe"
    })

def setup_users():
    """Create multiple users."""
    db.users.insert_many([
        {"id": 1, "email": "user1@example.com", "name": "User 1"},
        {"id": 2, "email": "user2@example.com", "name": "User 2"},
    ])
```

---

## Schemathesis (Property-Based API Testing)

```python
# tests/contract/test_api_schema.py

import schemathesis

schema = schemathesis.from_path("openapi.yaml")

@schema.parametrize()
def test_api_conforms_to_schema(case):
    """All API responses conform to OpenAPI schema."""
    case.call_and_validate()
```

---

## Key Points

1. **Consumer-First**: Consumers define expected behavior
2. **Provider Verification**: Providers must satisfy consumer contracts
3. **State Management**: Setup test data for each scenario
4. **Matchers**: Use flexible matchers (`like`, `eachLike`) for resilient tests
5. **Pact Broker**: Central storage for contracts
