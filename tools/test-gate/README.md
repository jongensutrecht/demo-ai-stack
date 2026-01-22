# Test Gate

Test Gate validates that required test types exist for changed files based on `test-requirements.yaml`.

## Usage

```powershell
# Basic usage
pwsh test-gate.ps1 -RepoRoot .

# Compare against specific branch
pwsh test-gate.ps1 -RepoRoot . -DiffBase main

# Dry run (show what would fail without failing)
pwsh test-gate.ps1 -RepoRoot . -DryRun

# Verbose output
pwsh test-gate.ps1 -RepoRoot . -Verbose

# JSON output
pwsh test-gate.ps1 -RepoRoot . -JsonOutput artifacts/debug/test-gate.json

# JSON output (bash)
./test-gate.sh --json-output artifacts/debug/test-gate.json
```

## How It Works

1. Reads `test-requirements.yaml` from repo root
2. Gets list of changed files via `git diff`
3. For each changed file:
   - Matches against rules in config
   - Determines required test types
   - Checks if corresponding test files exist
4. Reports missing tests
5. Exits with code 1 if any required tests are missing

## Configuration

The script reads from `test-requirements.yaml`:

```yaml
# Test file detection patterns
test_patterns:
  unit:
    - "tests/unit/**/*_test.py"
    - "**/*.test.ts"
  playwright:
    - "tests/e2e/**/*.spec.ts"

# Rules: which tests are required per path
rules:
  - pattern: "components/**"
    required: [unit, playwright]
  - pattern: "api/**"
    required: [unit, integration]

# Paths to exclude
exclusions:
  - "**/node_modules/**"
  - "**/__pycache__/**"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All required tests present |
| 1 | Missing required tests |
| 2 | Missing or invalid config |

## Example Output

```
==========================================
  TEST GATE - Required Tests Checker
==========================================

[INFO] RepoRoot: /path/to/repo
[INFO] Config: /path/to/repo/test-requirements.yaml
[INFO] Diff base: HEAD~1

[INFO] Loaded 5 rules from config
[INFO] Loaded 8 exclusion patterns
[INFO] Found 3 changed files

==========================================
  RESULTS
==========================================

Files checked: 2
Files skipped: 1
Violations found: 1

MISSING TESTS:

  components/Button.tsx
    Missing: playwright

[ERROR] TEST GATE FAILED - Required tests are missing

To fix:
  1. Create the missing test files
  2. Follow naming convention: <source>_test.py or <source>.test.ts
  3. Re-run test-gate
```

## Integration

### CI/CD

```yaml
# GitHub Actions
- name: Test Gate
  run: pwsh tools/test-gate/test-gate.ps1 -RepoRoot .
```

### Pre-commit Hook

```bash
#!/bin/bash
pwsh tools/test-gate/test-gate.ps1 -RepoRoot . -DiffBase HEAD
```

## Troubleshooting

### "No rules match" for all files

Check that your patterns in `test-requirements.yaml` match your project structure.

### False positives

Use the `exclusions` section to exclude files that don't need tests:

```yaml
exclusions:
  - "**/migrations/**"
  - "**/fixtures/**"
```

### Test not detected

Ensure your test file naming follows the patterns in `test_patterns`:

- Python: `test_<name>.py` or `<name>_test.py`
- TypeScript: `<name>.test.ts` or `<name>.spec.ts`
