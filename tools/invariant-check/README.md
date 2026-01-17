# Invariant Check

Invariant Check validates that all invariants defined in `invariants.md` have corresponding NEVER-tests.

## Usage

```powershell
# Basic usage
pwsh invariant-check.ps1 -RepoRoot .

# Specify custom invariants file location
pwsh invariant-check.ps1 -RepoRoot . -InvariantsFile docs/invariants.md

# Dry run (show what would fail without failing)
pwsh invariant-check.ps1 -RepoRoot . -DryRun

# Verbose output
pwsh invariant-check.ps1 -RepoRoot . -Verbose
```

## How It Works

1. Reads `invariants.md` from repo root
2. Parses all invariant definitions (format: `- [ ] **INV-XXX-NNN**: Description`)
3. Searches for NEVER-test files in `tests/invariants/`
4. Matches invariants to tests by:
   - Explicit test file path in invariants.md
   - Invariant ID mentioned in test file
   - Category matching (loose match)
5. Reports uncovered invariants
6. Exits with code 1 if any invariants lack tests

## Configuration

### Invariants File Format

```markdown
## Security Invariants

- [ ] **INV-SEC-001**: Authenticated endpoints NEVER return data without token
  - Test: `tests/invariants/auth/test_never_auth_bypass.py`

- [x] **INV-SEC-002**: User data is NEVER exposed to other users
  - Test: `tests/invariants/auth/test_never_cross_user_data.py`

## Business Invariants

- [ ] **INV-BIZ-001**: Invoice totals are NEVER negative
  - Test: `tests/invariants/business/test_never_negative_invoice.py`
```

### Test File Structure

```
tests/
└── invariants/
    ├── auth/
    │   ├── test_never_auth_bypass.py
    │   └── test_never_cross_user_data.py
    ├── business/
    │   └── test_never_negative_invoice.py
    └── security/
        └── test_never_sql_injection.py
```

### Test Naming Convention

NEVER-tests should:
- Start with `test_NEVER_` or contain `NEVER` in the name
- Reference the invariant ID in comments or docstrings
- Be placed in category-appropriate subdirectory

Example:
```python
# tests/invariants/auth/test_never_auth_bypass.py

class TestNeverAuthBypass:
    """
    Invariant: INV-SEC-001
    Protected endpoints NEVER return data without valid authentication.
    """

    def test_NEVER_access_without_token(self, client):
        response = client.get("/api/users")
        assert response.status_code == 401
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All invariants have NEVER-tests |
| 1 | Some invariants lack NEVER-tests |

## Example Output

```
==========================================
  INVARIANT CHECK - NEVER-Test Coverage
==========================================

[INFO] RepoRoot: /path/to/repo
[INFO] Invariants: /path/to/repo/invariants.md
[INFO] Tests Dir: /path/to/repo/tests/invariants

[INFO] Found 10 invariants in file
[INFO] Found 7 potential NEVER-test files

==========================================
  RESULTS
==========================================

Total invariants: 10
Covered: 7
Uncovered: 3

UNCOVERED INVARIANTS:

  Security:
    - INV-SEC-003: Admin endpoints are NEVER accessible without admin role
      Expected: tests/invariants/auth/test_never_admin_bypass.py

  Business:
    - INV-BIZ-002: Payments are NEVER processed twice
    - INV-BIZ-003: Refunds NEVER exceed original amount

Coverage: 70%

[ERROR] INVARIANT CHECK FAILED - Uncovered invariants found

To fix:
  1. Create NEVER-test files for each uncovered invariant
  2. Use pattern: test_NEVER_<description>.py
  3. Place in: tests/invariants/<category>/
  4. Update invariants.md checkbox to [x] when done
```

## Integration

### CI/CD

```yaml
# GitHub Actions
- name: Invariant Check
  run: pwsh tools/invariant-check/invariant-check.ps1 -RepoRoot .
```

### Pre-commit Hook

```bash
#!/bin/bash
pwsh tools/invariant-check/invariant-check.ps1 -RepoRoot .
```

## Troubleshooting

### "No invariants found in file"

Ensure invariants are formatted correctly:
```markdown
- [ ] **INV-XXX-NNN**: Description
```

The format requires:
- Checkbox: `- [ ]` or `- [x]`
- Bold ID: `**INV-XXX-NNN**`
- Colon and description

### Test not detected

Ensure your test file:
1. Contains `test_NEVER` or `NEVER` in filename or content
2. References the invariant ID in comments
3. Is in `.py` or `.ts` format
4. Is under `tests/` directory

### False positive (test exists but not detected)

Add explicit test file reference in invariants.md:
```markdown
- [ ] **INV-SEC-001**: Description
  - Test: `tests/my_custom_path/test_auth.py`
```
