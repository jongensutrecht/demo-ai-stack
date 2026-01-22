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

### 0. WORKTREE ISOLATIE (VERPLICHT)
**ELKE story MOET in een eigen worktree worden uitgevoerd.**

**VOORDAT je code aanraakt:**
```bash
# 1. Maak worktree + branch voor story
STORY_ID="API-101"  # pas aan per story
BRANCH="story-${STORY_ID,,}"
WT_PATH="../$(basename $PWD)_wt_${STORY_ID}"

git worktree add -b "$BRANCH" "$WT_PATH" origin/main
cd "$WT_PATH"

# 2. Verifieer isolatie
git branch --show-current  # moet $BRANCH zijn
pwd                        # moet $WT_PATH zijn
```

**NA voltooiing story:**
```bash
# 3. Merge naar main (alleen na alle ACs groen)
cd "$REPO"  # terug naar main repo
git merge --no-ff "$BRANCH" -m "feat($STORY_ID): <titel>"

# 4. Cleanup worktree
git worktree remove "$WT_PATH"
git branch -d "$BRANCH"
```

**VERBODEN:**
- Direct committen op `main` voor story werk
- Meerdere stories in 1 worktree
- Worktree stap overslaan "omdat het sneller is"
- Rationaliseren waarom worktree "niet nodig" is

**BIJ OVERTREDING:** STOP DIRECT. Revert commits. Begin opnieuw correct.

---

### 1. FILE SIZE LIMITS (VERPLICHT)
**Per file:**
- **Max 300 regels**
- **Max 15 functies**

**VERIFICATIE (voor commit):**
```bash
# Check regels
wc -l "$FILE"  # moet <= 300 zijn

# Check functies (Python)
grep -c "^def \|^async def " "$FILE"  # moet <= 15 zijn
```

**BIJ OVERTREDING:** Split file in kleinere modules voordat je verder gaat.

---

### 2. SUBPROCESS PER STORY (VERPLICHT)
**NOOIT stories in huidige context uitvoeren. ALTIJD nieuw subprocess.**

**Waarom:**
- Isolatie van state tussen stories
- Cleane context per story
- Voorkomt dat fouten in story A impact hebben op story B

**HOE:**
```bash
# Gebruik Task tool met subagent
Task(
  prompt="Voer story $STORY_ID uit in worktree $WT_PATH",
  subagent_type="general-purpose"
)
```

**VERBODEN:**
- Stories direct in huidige chat uitvoeren
- Meerdere stories achter elkaar in zelfde context
- "Even snel" een story doen zonder subprocess

**BIJ OVERTREDING:** STOP. Story is ongeldig. Herstart in subprocess.

---

### 3. Proof Gate
`[DONE]` alleen als `output/bmad/<process>/<run_id>/<story_id>/final.json` bestaat en `done=true`.

### 4. NO MOCKS
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

### 5. NO FALLBACKS
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

### 6. 100% COVERAGE
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
