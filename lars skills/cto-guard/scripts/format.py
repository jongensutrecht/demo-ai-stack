#!/usr/bin/env python3
"""CTO Guard output format details for the full Universal CTO Review v2.4.

Usage:
    python format.py          # Show all sections
    python format.py example  # Show example skeleton
    python format.py verdicts # Show verdict model
"""
from __future__ import annotations

import sys

SECTIONS = """
## Mandatory report shape

1. Executive Summary
2. Facet Scores Overview
3. Per-facet detail
4. Consolidated Gap Table
5. Prioritized Action Plan
6. Path to 10/10

### 1. Executive Summary
```markdown
## 1. Executive Summary

- Repo: `/absolute/repo/path`
- Review target: `working tree`
- Review scope: `repo_only`
- In scope:
  - runtime code under `src/`
  - tests under `tests/`
- Out of scope:
  - live cloud state
- UNKNOWN external state:
  - branch protection in GitHub (verify with `gh api ...`)
- Git state: `main @ abc1234 (dirty)`
- Overall status: `PASS`
- Overall score: `8.7`
- Confidence: `MEDIUM`
- Bottom line: feature is acceptable but maintainability + doc drift remain.
```

### 2. Facet Scores Overview
```markdown
## 2. Facet Scores Overview

| Facet | Applicability | Score | Confidence | Unresolved gaps | Note |
|------|---------------|-------|------------|-----------------|------|
| Architectuur | Applicable | 8.5 | HIGH | 1 | Boundaries mostly clear |
| Feature Flags | N/A | N/A | HIGH | 0 | No flag system exists |
| Domain/Spec Compliance | UNKNOWN | UNKNOWN | LOW | 0 | External contract not proven |
```

### 3. Per-facet detail
```markdown
## 3. Per-facet detail

### 3.1 Security
- Applicability: Applicable
- Score: 9.0
- Confidence: HIGH
- Strengths:
  - `src/auth/guard.ts:14` validates session before mutation.

#### CTO Rules Applied
| Rule / Guardrail | Why relevant |
|------------------|-------------|
| SEC-001 | mutation path touches auth |
| Repo-10x search hygiene | touched docs + runtime search contract |

#### Traceability Map
| Rule / Facet / Guardrail | Covered? | Evidence |
|--------------------------|----------|----------|
| SEC-001 | YES | `src/auth/guard.ts:14` |
| Security facet | PARTIAL | missing explicit audit event at `src/api/items.ts:88` |

#### Gaps
| ID | Primary Owner | Priority | Status | Gap | Evidence | Closure DoD | Cross-refs |
|----|---------------|----------|--------|-----|----------|-------------|------------|
| GAP-SECURITY-01 | Security | P2 | OPEN | Delete path lacks audit log | `src/api/items.ts:88` | audit event emitted in delete flow + test | GAP-OPS-02 |
```

### 4. Consolidated Gap Table
```markdown
## 4. Consolidated Gap Table

| ID | Primary Owner | Priority | Status | Summary | Evidence | Closure DoD | Cross-refs |
|----|---------------|----------|--------|---------|----------|-------------|------------|
| GAP-SECURITY-01 | Security | P2 | OPEN | Delete path lacks audit log | `src/api/items.ts:88` | add audit event + test | GAP-OPS-02 |
| GAP-DOCS-01 | Documentation | P3 | OPEN | Missing source-of-truth note for toggle contract | `docs/spec.md:1` | add contract note + link from START_HERE | None |
```

### 5. Prioritized Action Plan
```markdown
## 5. Prioritized Action Plan

### P1-CRITICAL
None

### P1-QUICK
None

### P2
- Add audit trail to delete flow (`src/api/items.ts`)
  - Why: closes Security + Ops/Reliability gap
  - Evidence: `src/api/items.ts:88`
  - Closure: event emitted + tested

### P3
- Document toggle source of truth in docs
  - Why: removes doc drift
  - Evidence: `docs/spec.md:1`
  - Closure: docs linked from START_HERE / SOURCES_OF_TRUTH
```

### 6. Path to 10/10
```markdown
## 6. Path to 10/10

- What blocks 10/10 now:
  - unresolved P2 security/ops gap
  - external branch protection still UNKNOWN
- What is already strong:
  - tests green
  - clear runtime toggle bootstrap
- Exact order of attack:
  1. close GAP-SECURITY-01
  2. close GAP-DOCS-01
  3. verify branch protection with `gh api ...`
- Proceed or block:
  - CONDITIONAL: feature may proceed, but not 10/10 yet
- Generated BMAD follow-up:
  - triggered: yes
  - `bmad_input/cto_guard_followup_toggle_review_20260317.md`
  - `bmad_input/cto_guard_followup_toggle_review_20260317.json`
  - mapping: P2 -> BMAD P1, P3 -> BMAD P3
```
"""

VERDICTS = """
## Verdict model

- COMPLIANT: no blocking violations in reviewed scope
- CONDITIONAL: acceptable with explicit unresolved gaps
- NON-COMPLIANT: blocking gaps remain; stop until fixed

## Universal CTO requirements

- Facet Scores Overview is mandatory
- P1, P2 and P3 must all be explicit
- Path to 10/10 is mandatory
- UNKNOWN claims require exactly 1 verification check
- Every claim needs evidence
"""


def main() -> None:
    if len(sys.argv) < 2:
        print("CTO Guard Output Format — Universal CTO Review v2.4")
        print("=" * 58)
        print(SECTIONS)
        return

    cmd = sys.argv[1].lower()
    if cmd == "example":
        print(SECTIONS)
    elif cmd == "verdicts":
        print(VERDICTS)
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python format.py [example|verdicts]")


if __name__ == "__main__":
    main()
