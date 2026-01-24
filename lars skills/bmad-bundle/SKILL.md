---
name: bmad-bundle
# prettier-ignore
description: Bundled BMAD autopilot with proof-gated Ralph Loop.
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Bundle

Doel: 1 command die RUN1 -> preflight -> RUN2 (Ralph Loop) uitvoert, waarbij Ralph **niet** kan stoppen zonder proof artefacts.

Gebruik: `/bmad-bundle <input_md_path>`

---

## Hard Rules

### 1. Proof Gate
`[DONE]` alleen als `output/bmad/<process>/<run_id>/<story_id>/final.json` bestaat en `done=true`.

### 2. NO MOCKS
**VERBODEN:**
- `jest.fn()` zonder echte implementatie
- `mockResolvedValue` zonder integratie test
- `jest.spyOn` die echte functionaliteit vervangt
- Fake data die niet uit fixtures komt

**TOEGESTAAN:**
- Test fixtures met realistische data
- Integration tests met echte database (test DB)
- E2E tests met echte API calls
- Mocks ALLEEN voor externe services (LLM, email, etc.)

### 3. NO FALLBACKS
**VERBODEN:**
- `|| []` fallbacks die bugs verbergen
- `?.` optional chaining zonder null check
- `try/catch` die errors slikt
- Default values die incorrecte state maskeren

**VEREIST:**
- Expliciete error handling
- Fail-fast bij unexpected state
- Validation op inputs
- Assertions op outputs

### 4. 100% COVERAGE
**VEREIST:**
- Alle nieuwe code 100% line coverage
- Alle branches covered
- Alle edge cases getest
- Coverage check in preflight

**VERIFICATIE:**
```bash
npm run test -- --coverage --coverageThreshold='{"global":{"lines":100,"branches":100}}'
```

---

## Workflow

1. **RUN1** - Genereer stories uit input.md
2. **CTO Guard** - Valideer tegen CTO_RULES.md
3. **Preflight** - lint + test + coverage check
4. **RUN2 (Ralph Loop)** - Voer stories uit met proof artefacts

---

## Preflight Checks

```bash
# Must all pass before RUN2
npm run lint          # exit 0
npm run test          # exit 0, 0 failures
npm run test:coverage # 100% lines, 100% branches
npm run build         # exit 0
```

---

## Violation Response

Bij violation van hard rules:

1. **STOP** - Geen verder werk
2. **REPORT** - Toon exacte violation
3. **FIX REQUIRED** - Geen workarounds

```
❌ VIOLATION: Mock detected in conversation.test.ts:45
   Found: jest.fn().mockResolvedValue({})
   Required: Real integration test or fixture

   BLOCKED until fixed.
```
