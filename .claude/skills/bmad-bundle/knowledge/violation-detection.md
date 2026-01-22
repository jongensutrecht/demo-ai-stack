# Violation Detection Rules

## Mock Detection

### Grep patterns voor verboden mocks:

```bash
# Detecteer verboden mock patterns
grep -rn "jest\.fn()" tests/ --include="*.ts" --include="*.tsx"
grep -rn "mockResolvedValue" tests/ --include="*.ts" --include="*.tsx"
grep -rn "mockImplementation" tests/ --include="*.ts" --include="*.tsx"
grep -rn "jest\.spyOn" tests/ --include="*.ts" --include="*.tsx"
```

### Uitzonderingen (TOEGESTAAN):

```typescript
// ✅ Mock voor externe service (LLM)
const mockLLM = jest.fn().mockResolvedValue({ parsed: true });

// ✅ Mock voor externe service (fetch naar externe API)
global.fetch = jest.fn(); // Alleen voor externe URLs

// ✅ Test fixture
const testUser = fixtures.users.admin;
```

### Violations (VERBODEN):

```typescript
// ❌ Mock voor interne functie
jest.spyOn(userService, 'getUser').mockResolvedValue(fakeUser);

// ❌ Mock zonder reden
const mockFn = jest.fn();

// ❌ Fake data inline
const user = { id: '123', name: 'Test' }; // Moet uit fixtures komen
```

---

## Fallback Detection

### Grep patterns voor verboden fallbacks:

```bash
# Detecteer verboden fallback patterns
grep -rn "\|\| \[\]" src/ --include="*.ts" --include="*.tsx"
grep -rn "\|\| {}" src/ --include="*.ts" --include="*.tsx"
grep -rn "\?\." src/ --include="*.ts" --include="*.tsx" | grep -v "// safe:"
grep -rn "catch.*{}" src/ --include="*.ts" --include="*.tsx"
```

### Uitzonderingen (TOEGESTAAN):

```typescript
// ✅ Expliciete null check + fallback
if (items === null || items === undefined) {
  throw new Error('Items required');
}
const safeItems = items; // Nu gegarandeerd niet null

// ✅ Optional chaining met expliciete check
const name = user?.name; // safe: user validated above
if (!name) throw new Error('Name required');

// ✅ Catch met logging
catch (error) {
  console.error('[Module] Error:', error);
  throw error; // Re-throw!
}
```

### Violations (VERBODEN):

```typescript
// ❌ Silent fallback
const items = data.items || [];

// ❌ Optional chaining zonder check
const name = user?.profile?.name; // Kan undefined zijn!

// ❌ Error swallowing
catch (error) {
  // Niks doen
}

// ❌ Default dat bug maskeert
const count = response?.count ?? 0;
```

---

## Coverage Check

### Preflight coverage command:

```bash
npm run test -- --coverage \
  --coverageThreshold='{"global":{"lines":100,"branches":100,"functions":100,"statements":100}}' \
  --collectCoverageFrom='src/**/*.{ts,tsx}' \
  --collectCoverageFrom='!src/**/*.d.ts'
```

### Coverage report moet tonen:

```
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   100   |   100    |   100   |   100   |
--------------------|---------|----------|---------|---------|
```

### Bij < 100%:

```
❌ COVERAGE VIOLATION
   File: src/lib/capture/conversation.ts
   Lines: 95% (missing: 142, 156, 203)
   Branches: 88% (missing: 45, 67)

   BLOCKED: Add tests for uncovered lines before proceeding.
```

---

## Automated Check Script

```bash
#!/bin/bash
# bmad-preflight-check.sh

echo "=== BMAD Preflight Checks ==="

# 1. Mock detection
echo "Checking for forbidden mocks..."
MOCKS=$(grep -rn "jest\.fn()" tests/ --include="*.ts" 2>/dev/null | grep -v "// external:")
if [ -n "$MOCKS" ]; then
  echo "❌ MOCK VIOLATION:"
  echo "$MOCKS"
  exit 1
fi

# 2. Fallback detection
echo "Checking for forbidden fallbacks..."
FALLBACKS=$(grep -rn "\|\| \[\]" src/ --include="*.ts" 2>/dev/null | grep -v "// safe:")
if [ -n "$FALLBACKS" ]; then
  echo "❌ FALLBACK VIOLATION:"
  echo "$FALLBACKS"
  exit 1
fi

# 3. Coverage check
echo "Checking coverage..."
npm run test -- --coverage --coverageThreshold='{"global":{"lines":100}}' --silent
if [ $? -ne 0 ]; then
  echo "❌ COVERAGE VIOLATION: < 100%"
  exit 1
fi

echo "✅ All preflight checks passed"
exit 0
```
