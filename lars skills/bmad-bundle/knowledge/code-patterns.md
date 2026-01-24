# BMAD Code Patterns

## Tests: Good vs Bad

### ❌ BAD: Mock-heavy test

```typescript
// VERBODEN - te veel mocks, test test niks echt
describe('UserService', () => {
  it('should get user', async () => {
    const mockDb = jest.fn().mockResolvedValue({ id: '1', name: 'Test' });
    const mockCache = jest.fn().mockResolvedValue(null);

    const result = await getUser('1', mockDb, mockCache);

    expect(result.name).toBe('Test');
  });
});
```

### ✅ GOOD: Integration test

```typescript
// TOEGESTAAN - echte database, echte functionaliteit
describe('UserService', () => {
  beforeAll(async () => {
    await testDb.seed(fixtures.users);
  });

  afterAll(async () => {
    await testDb.cleanup();
  });

  it('should get user from database', async () => {
    const result = await getUser(fixtures.users.admin.id);

    expect(result).toEqual(fixtures.users.admin);
  });

  it('should throw when user not found', async () => {
    await expect(getUser('nonexistent')).rejects.toThrow('User not found');
  });
});
```

---

## Error Handling: Good vs Bad

### ❌ BAD: Silent fallback

```typescript
// VERBODEN - bug wordt gemaskeerd
async function getItems(userId: string) {
  const response = await fetch(`/api/items?user=${userId}`);
  const data = await response.json();
  return data.items || []; // ← Bug: wat als API error?
}
```

### ✅ GOOD: Explicit error handling

```typescript
// TOEGESTAAN - fail-fast, duidelijke errors
async function getItems(userId: string): Promise<Item[]> {
  const response = await fetch(`/api/items?user=${userId}`);

  if (!response.ok) {
    throw new ApiError(`Failed to fetch items: ${response.status}`);
  }

  const data = await response.json();

  if (!Array.isArray(data.items)) {
    throw new ValidationError('Invalid response: items must be array');
  }

  return data.items;
}
```

---

## Data: Good vs Bad

### ❌ BAD: Inline fake data

```typescript
// VERBODEN - data niet realistisch, niet herbruikbaar
it('should process user', () => {
  const user = {
    id: '123',
    name: 'Test User',
    email: 'test@test.com',
  };

  const result = processUser(user);
  expect(result.processed).toBe(true);
});
```

### ✅ GOOD: Test fixtures

```typescript
// tests/fixtures/users.ts
export const users = {
  admin: {
    id: 'usr_admin_001',
    name: 'Admin User',
    email: 'admin@photobooth.nl',
    role: 'admin',
    active: true,
    createdAt: new Date('2024-01-01'),
  },
  staff: {
    id: 'usr_staff_001',
    name: 'Staff Member',
    email: 'staff@photobooth.nl',
    role: 'staff',
    active: true,
    createdAt: new Date('2024-01-15'),
  },
} as const;

// In test:
import { users } from '../fixtures/users';

it('should process admin user', () => {
  const result = processUser(users.admin);
  expect(result.processed).toBe(true);
  expect(result.permissions).toContain('admin');
});
```

---

## Coverage: What to test

### ✅ All branches covered

```typescript
// Function met 3 branches
function getPriorityLabel(priority: Priority): string {
  if (priority === 'high') return 'Hoog';      // Branch 1
  if (priority === 'med') return 'Medium';     // Branch 2
  return 'Laag';                                // Branch 3
}

// Tests moeten ALLE branches coveren:
describe('getPriorityLabel', () => {
  it('returns Hoog for high priority', () => {
    expect(getPriorityLabel('high')).toBe('Hoog');
  });

  it('returns Medium for med priority', () => {
    expect(getPriorityLabel('med')).toBe('Medium');
  });

  it('returns Laag for low priority', () => {
    expect(getPriorityLabel('low')).toBe('Laag');
  });
});
```

### ✅ Edge cases covered

```typescript
// Edge cases voor array function
describe('getFirstItem', () => {
  it('returns first item from array', () => {
    expect(getFirstItem([1, 2, 3])).toBe(1);
  });

  it('throws for empty array', () => {
    expect(() => getFirstItem([])).toThrow('Array is empty');
  });

  it('throws for null input', () => {
    expect(() => getFirstItem(null)).toThrow('Input required');
  });

  it('handles single item array', () => {
    expect(getFirstItem([42])).toBe(42);
  });
});
```

---

## Mocks: When allowed

### ✅ External service mock (TOEGESTAAN)

```typescript
// Externe LLM service - mag gemocked worden
describe('TriageService', () => {
  const mockLLM = {
    parse: jest.fn(), // external: LLM API
  };

  beforeEach(() => {
    mockLLM.parse.mockReset();
  });

  it('should handle LLM timeout', async () => {
    mockLLM.parse.mockRejectedValue(new Error('Timeout'));

    const result = await triageItem('test input', mockLLM);

    expect(result.status).toBe('needs_review');
    expect(result.error).toBe('LLM timeout');
  });
});
```

### ✅ Network boundary mock (TOEGESTAAN)

```typescript
// Fetch naar externe API - mag gemocked worden
beforeEach(() => {
  // external: third-party weather API
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: () => Promise.resolve({ temp: 20 }),
  });
});
```
