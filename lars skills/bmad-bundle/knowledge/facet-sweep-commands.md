# Facet Sweep Commands — standaard violation-detectie per facet

Gebruik deze catalogus in STORY_VERIFY. De agent kiest het facet dat de story targetde en pakt de bijbehorende commands. Alleen als het facet hier niet in staat, moet de agent zelf commands bedenken.

## Jaw-drop audit facetten (code)

### 1. Architecture & Structure
```json
[
  "find src/ -name '*.py' -o -name '*.ts' -o -name '*.js' | head -500 | xargs grep -l 'import.*from.*\\.\\./' | head -20",
  "rg -l 'utils|helpers|misc|common|shared' src/ --glob '!tests/' --glob '!node_modules/'",
  "rg -c 'class ' src/ --glob '*.py' | awk -F: '$2>3' | head -20"
]
```

### 2. Code Elegance
```json
[
  "rg -n '# TODO|# FIXME|# HACK|# XXX|# TEMP' src/ --glob '!tests/'",
  "rg -c 'if.*elif.*elif.*elif' src/ --glob '*.py' | awk -F: '$2>0'",
  "rg -n 'pass$' src/ --glob '*.py' --glob '!tests/' --glob '!__init__.py'"
]
```

### 3. Naming & Semantics
```json
[
  "rg -l 'def (get|do|run|handle|process|manage|execute)\\b' src/ --glob '*.py' --glob '!tests/'",
  "rg -n '[a-z]{1,2} = ' src/ --glob '*.py' --glob '!tests/' | rg -v 'i =|j =|k =|e =|f =|_ =' | head -20",
  "rg -rn '(straat|stad|naam|nummer|datum|tijd|adres|klant|factuur|offerte|bericht|verzend|ontvang|bewerk|verwijder|opslaan|ophalen|aanmaken|bijwerken)' src/ --glob '*.py' --glob '!tests/' --glob '!*.md' | head -30"
]
```

### 4. Error Handling & Resilience
```json
[
  "rg -n 'except:$|except Exception:$|except Exception as e: *$' src/ --glob '*.py' --glob '!tests/'",
  "rg -n 'pass$' src/ --glob '*.py' --glob '!tests/' --glob '!__init__.py'",
  "rg -n 'except.*:' src/ --glob '*.py' --glob '!tests/' | rg -v 'logger|log_|raise|return|print' | head -20"
]
```

### 5. Testing & Quality
```json
[
  "rg -l '@pytest.mark.skip|pytest.skip|@unittest.skip|skipTest' tests/",
  "rg -n 'assert True|assert 1' tests/ | head -20",
  "rg -l 'mock|Mock|patch|MagicMock' tests/ | wc -l"
]
```

### 6. Performance & Efficiency
```json
[
  "rg -n 'for.*in.*fetchAll|for.*in.*find\\(' src/ --glob '!tests/' | head -20",
  "rg -n 'sleep\\(|time\\.sleep' src/ --glob '!tests/'",
  "rg -n 'SELECT \\*' src/ --glob '!tests/'"
]
```

### 7. Security Posture
```json
[
  "rg -rn '(password|secret|token|api_key)\\s*=' src/ --glob '!tests/' --glob '!*.example' --glob '!*.md' | rg -v 'environ|getenv|os\\.env|config\\.' | head -20",
  "rg -n 'eval\\(|exec\\(' src/ --glob '!tests/'",
  "rg -n 'verify=False|VERIFY_SSL.*False' src/ --glob '!tests/'"
]
```

### 8. Developer Experience (DX)
```json
[
  "test -f docs/START_HERE.md && echo OK || echo 'MISSING: docs/START_HERE.md'",
  "test -f docs/SOURCES_OF_TRUTH.md && echo OK || echo 'MISSING: docs/SOURCES_OF_TRUTH.md'",
  "test -f scripts/quality_gates.py && echo OK || echo 'MISSING: scripts/quality_gates.py'"
]
```

### 9. Git & Commit Discipline
```json
[
  "git log --oneline -20 | rg -v '^[a-f0-9]+ (feat|fix|refactor|test|docs|chore|style|ci|build|perf)\\(' | head -10",
  "git log --oneline -50 | rg -i 'wip|tmp|temp|fix fix|oops|undo' | head -10"
]
```

### 10. Consistency & Craft
```json
[
  "rg -c 'logger|logging' src/ --glob '*.py' --glob '!tests/' | awk -F: '$2==0' | head -20",
  "rg -l 'print(' src/ --glob '*.py' --glob '!tests/' --glob '!scripts/'",
  "rg -rn 'TODO|FIXME|HACK|XXX|TEMP' src/ --glob '!tests/' | wc -l"
]
```

## Repo-10x contract facetten

### A. Gates
```json
[
  "test -f scripts/quality_gates.py && python3 scripts/quality_gates.py 2>&1 | tail -5 || echo 'NO GATE SCRIPT'",
  "test -f Makefile && grep -c 'gates\\|lint\\|test' Makefile || echo 'NO MAKEFILE'"
]
```

### B. Search hygiene
```json
[
  "test -f .ignore && echo OK || echo 'MISSING: .ignore'",
  "test -f config/golden_queries.txt && echo OK || echo 'MISSING: config/golden_queries.txt'",
  "rg -l 'test_pattern' worktrees_claude/ archive/ 2>/dev/null | wc -l"
]
```

### C. Root hygiene
```json
[
  "ls -1 . | wc -l",
  "ls -1 . | rg -v '^(src|tests|docs|scripts|config|packages|deploy|security|caddy|secrets|\\..*|README|CLAUDE|AGENTS|Makefile|Dockerfile|docker-compose|pyproject|package|requirements|uv\\.lock|LICENSE|RUNBOOK)' | head -20"
]
```

### D. Sources of truth
```json
[
  "test -f docs/SOURCES_OF_TRUTH.md && echo OK || echo 'MISSING'",
  "test -f docs/SOURCES_OF_TRUTH.md && rg -c 'entrypoint|config|dependencies|tests|CI' docs/SOURCES_OF_TRUTH.md || echo 0"
]
```

### E. Onboarding
```json
[
  "test -f docs/START_HERE.md && echo OK || echo 'MISSING'",
  "test -f docs/START_HERE.md && rg -c 'setup|run|gate|troubleshoot' docs/START_HERE.md || echo 0"
]
```

### F. Secrets/artifacts in git
```json
[
  "git ls-files | rg '\\.(env|pem|key|p12|pfx|jks)$' | rg -v 'example|template' | head -10",
  "git ls-files | rg '\\.(zip|tar|gz|jar|whl|pyc|class)$' | head -10",
  "rg -rn '(AKIA|sk-|ghp_|gho_|glpat-)' --glob '!*.md' --glob '!*.example' . 2>/dev/null | head -5"
]
```

### G. Worktrees excluded
```json
[
  "cat .ignore 2>/dev/null | rg 'worktrees' || echo 'worktrees NOT in .ignore'",
  "cat pyproject.toml 2>/dev/null | rg 'worktrees' || echo 'worktrees NOT excluded in pyproject.toml'"
]
```

### H. CI/branch protection
```json
[
  "gh api repos/{owner}/{repo}/branches/main/protection 2>/dev/null | python3 -c 'import sys,json; d=json.load(sys.stdin); print(\"required_checks:\", bool(d.get(\"required_status_checks\")))' 2>/dev/null || echo 'UNKNOWN: gh auth needed'"
]
```

### I. File limits
```json
[
  "test -f scripts/check_file_limits.py && python3 scripts/check_file_limits.py 2>&1 | grep -c 'FAIL' || echo 'NO FILE LIMITS SCRIPT'",
  "find src/ -name '*.py' -not -path '*/tests/*' | xargs wc -l 2>/dev/null | awk '$1>300{print}' | head -20"
]
```

## JS/TS variant (voor Node.js repos)

### Naming (JS/TS)
```json
[
  "rg -rn '(straat|stad|naam|nummer|datum|tijd|adres|klant|factuur)' src/ web/src/ --glob '*.ts' --glob '*.tsx' --glob '*.js' --glob '!*.test.*' --glob '!*.spec.*' | head -30",
  "rg -l 'utils|helpers|misc|common' src/ web/src/ --glob '*.ts' --glob '*.js' --glob '!node_modules/'"
]
```

### Error handling (JS/TS)
```json
[
  "rg -n 'catch.*\\{\\s*\\}|catch.*\\{\\s*\\/\\/' src/ web/src/ --glob '*.ts' --glob '*.js' --glob '!tests/' --glob '!*.test.*' | head -20",
  "rg -n 'catch\\s*\\(' src/ web/src/ --glob '*.ts' --glob '*.js' --glob '!tests/' | rg -v 'console|log|throw|return|reject' | head -20"
]
```

### File limits (JS/TS)
```json
[
  "find src/ web/src/ -name '*.ts' -o -name '*.tsx' -o -name '*.js' | grep -v test | grep -v spec | grep -v node_modules | xargs wc -l 2>/dev/null | awk '$1>300{print}' | head -20"
]
```

## Gebruik

De agent hoeft niet zelf commands te verzinnen. Stappen:

1. Bepaal welk facet de story targetde
2. Zoek dat facet op in dit bestand
3. Gebruik de bijbehorende commands als `SWEEP_COMMANDS`
4. Voeg repo-specifieke commands toe als het facet specifieker is dan de standaard
5. Alleen als het facet hier niet staat: bedenk zelf commands en documenteer waarom
