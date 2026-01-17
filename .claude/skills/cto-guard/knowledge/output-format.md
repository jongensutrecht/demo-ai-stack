# CTO Guard Output Format

## Verplichte 6 Secties

### 1. CTO RULES APPLIED
```markdown
## 1. CTO RULES APPLIED

| Rule ID | Rule Description |
|---------|------------------|
| SEC-001 | Geen public endpoints voor mutaties |
| TEST-001 | Alle code heeft tests |
| TEST-002 | Required test types aanwezig |
| INV-001 | Invariants hebben NEVER-tests |
| ...     | ... |
```

### 2. TRACEABILITY MAP
```markdown
## 2. TRACEABILITY MAP

| Rule ID | Covered? | Evidence |
|---------|----------|----------|
| SEC-001 | ✅ YES | `adapter/routes/health.py:15` - auth=admin_key |
| TEST-001 | ❌ NO | Geen tests gevonden voor nieuwe functie |
| TEST-002 | ✅ YES | unit + playwright tests aanwezig |
| INV-001 | ⚠️ PARTIAL | 3/5 invariants hebben NEVER-tests |
| ...     | ... | ... |
```

### 3. VIOLATIONS
```markdown
## 3. VIOLATIONS

### Hard Violations (MUST FIX)
| ID | Rule | Violation | Location |
|----|------|-----------|----------|
| V1 | SEC-001 | Public endpoint voor mutatie | `adapter/routes/data.py:42` |
| V2 | TEST-002 | Missing playwright test | `components/Button.tsx` |

### Soft Violations (FIX OR JUSTIFY)
| ID | Rule | Violation | Location |
|----|------|-----------|----------|
| V3 | DOC-001 | Ontbrekende docstring | `utils/helper.py:10` |
```

### 4. TEST COMPLIANCE (NIEUW)
```markdown
## 4. TEST COMPLIANCE

### Test Requirements Check
| File | Required Tests | Present | Status |
|------|---------------|---------|--------|
| components/Button.tsx | unit, playwright | unit | ❌ Missing playwright |
| api/users.py | unit, integration | unit, integration | ✅ OK |

### Invariant Coverage Check
| Invariant ID | NEVER-Test | Status |
|--------------|------------|--------|
| INV-SEC-001 | test_never_auth_bypass.py | ✅ OK |
| INV-BIZ-001 | - | ❌ MISSING |

### Summary
- Test Requirements: 5/6 compliant
- Invariant Coverage: 8/10 covered
```

### 5. REQUIRED ACTIONS
```markdown
## 5. REQUIRED ACTIONS

| Action | Priority | Details |
|--------|----------|---------|
| Add auth to /data endpoint | P1 | Voeg `Depends(require_admin)` toe |
| Add playwright test for Button | P1 | Create `Button.spec.ts` |
| Add NEVER-test for INV-BIZ-001 | P1 | Create `test_never_negative_invoice.py` |
| Add tests for helper.py | P2 | Minimaal 80% coverage |

**STATUS**: ❌ BLOCKED until V1, V2 are resolved
```

### 6. CTO COMPLIANCE VERDICT
```markdown
## 6. CTO COMPLIANCE VERDICT

### ❌ NON-COMPLIANT

**Reason**:
- 1 hard violation (SEC-001)
- 1 missing required test type (TEST-002)
- 2 invariants without NEVER-tests

**Next Steps**:
1. Fix V1 (auth op /data endpoint)
2. Add playwright test for Button.tsx
3. Add NEVER-tests for missing invariants
4. Re-run `/cto-guard`
5. Alleen bij ✅ COMPLIANT doorgaan
```

## Verdict Types

| Verdict | Meaning | Action |
|---------|---------|--------|
| ✅ COMPLIANT | Alles voldoet | Doorgaan |
| ⚠️ CONDITIONAL | Soft violations | Doorgaan, fix binnen sprint |
| ❌ NON-COMPLIANT | Hard violations | BLOKKEER tot gefixed |

## Extended Rules (v2.0)

### Test Compliance Rules

| Rule ID | Description | Hard/Soft |
|---------|-------------|-----------|
| TEST-001 | Alle code heeft tests | Hard |
| TEST-002 | Required test types aanwezig per path | Hard |
| TEST-003 | Minimum coverage thresholds | Soft |

### Invariant Rules

| Rule ID | Description | Hard/Soft |
|---------|-------------|-----------|
| INV-001 | Elke invariant heeft NEVER-test | Hard |
| INV-002 | Stories linken naar relevante invariants | Soft |

## Rules

- **Geen impliciete compliance**: Elke regel moet expliciet gecheckt
- **Evidence verplicht**: Elke claim heeft file:line of command output
- **Blokkeren is OK**: Liever blokkeren dan slechte code doorlaten
- **Test compliance is hard**: Missing required tests = blocked
