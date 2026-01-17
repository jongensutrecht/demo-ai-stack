---
name: bmad-autopilot
# prettier-ignore
description: "Ralph Loop Regular: + CTO review + worktree. Story-driven development met volledige ceremony."
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Autopilot

> **Versie**: 4.0.0
> **Doel**: Stories genereren en uitvoeren met CTO Guard validatie en Test Guard integratie

---

## Wanneer Activeren

- `/bmad-autopilot` voor volledige workflow
- `/bmad-autopilot --generate-only` voor alleen story generatie

---

## Vereiste Input

**VRAAG DE GEBRUIKER** naar het pad van het input .md bestand:
- Voorbeeld: `docs/mijn_requirements.md`
- Als geen bestand gegeven: STOP fail-closed

---

## Workflow (met CTO Guard + Test Guard)

### STAP 0 - Validatie (fail-closed)

```bash
git rev-parse --show-toplevel
ls bmad_autopilot_kit/
ls docs/CTO_RULES.md || echo "STOP: docs/CTO_RULES.md ontbreekt"
ls invariants.md || echo "WARNING: invariants.md ontbreekt - run /invariant-discovery"
ls test-requirements.yaml || echo "WARNING: test-requirements.yaml ontbreekt"
```

### STAP 1 - CTO GUARD #1: PRE-GENERATION

**Valideer input document tegen CTO regels:**
- Check: Is het plan compliant met architectuur regels?
- Check: Zijn er security risico's in het ontwerp?
- Output: `/cto-guard` rapport

Als ❌ NON-COMPLIANT: STOP fail-closed

### STAP 2 - Bepaal Process

```
Process = slug(basename(INPUT_FILE))
```

Output paden:
- Stories: `stories/<Process>/`
- BACKLOG: `stories/<Process>/BACKLOG.md`

### STAP 3 - RUN1: Genereer Stories

**Elke story heeft:**
- CTO Rule traceability per AC
- **Test Requirements sectie** (nieuw in v4)
- **Relevante Invariants sectie** (nieuw in v4)
- Eerste taak: `- [ ] Lees CLAUDE.md`
- Laatste taak: `- [ ] Run Gate A checks`

**Story Template (uitgebreid):**
```markdown
## Test Requirements

| Type | Required | Rationale |
|------|----------|-----------|
| unit | ✅ | Business logic |
| integration | ❌ | Geen externe deps |
| playwright | ✅ | UI flow |
| contract | ❌ | Geen API changes |

## Relevante Invariants

| ID | Description | NEVER-Test Exists |
|----|-------------|-------------------|
| INV-SEC-001 | Auth required | [ ] |
| INV-BIZ-001 | No negative totals | [ ] |
```

**Output:**
- Story files (OPS-001.md, OPS-002.md, ...)
- BACKLOG.md voor Ralph Loop tracking

### STAP 4 - CTO GUARD #2: POST-GENERATION

**Valideer gegenereerde stories:**
- Check: Heeft elke AC een CTO Rule referentie?
- Check: Zijn alle verification commands executable?
- Check: Heeft elke story een Test Requirements sectie?
- Output: `/cto-guard` rapport

Als ❌ NON-COMPLIANT: Fix stories of STOP

### STAP 5 - Preflight

```bash
pwsh ./tools/preflight/preflight.ps1 \
  -RepoRoot "<repo-root>" -Process "<Process>"
```

### STAP 6 - RUN2: Voer Stories Uit (Ralph Loop)

**Per story (via nieuw Claude window):**

```bash
# a) Start Claude voor story
claude --dangerously-skip-permissions \
  -p "Voer story <STORY_ID> uit. Story: stories/<Process>/<STORY_ID>.md"

# b) Agent doet:
#    - Leest CLAUDE.md
#    - Leest Test Requirements
#    - Schrijft NEVER-tests voor invariants
#    - Schrijft required tests (unit/integration/playwright)
#    - Implementeert story taken
#    - Runt Gate A (ruff + pytest + test-gate + invariant-check)
#    - Runt CTO GUARD #3 (post-execution)

# c) Update BACKLOG.md status
```

### STAP 7 - CTO GUARD #3: POST-EXECUTION (per story)

**Na Gate A, voor merge:**
- Check: Geen security violations in nieuwe code?
- Check: Tests coverage adequate?
- Check: Alle required tests aanwezig (via test-gate)?
- Check: Alle invariants gedekt (via invariant-check)?
- Output: `/cto-guard` rapport

Als ❌ NON-COMPLIANT: STOP, geen merge

---

## Gate A (Uitgebreid)

Gate A bevat nu:

```bash
# 1. Lint
ruff check .

# 2. Tests
pytest

# 3. Test Requirements Check (nieuw)
pwsh tools/test-gate/test-gate.ps1 -RepoRoot .

# 4. Invariant Coverage Check (nieuw)
pwsh tools/invariant-check/invariant-check.ps1 -RepoRoot .
```

Alle vier moeten slagen.

---

## Hard Rules

1. **CTO Guard op 3 momenten** - Pre-gen, post-gen, post-exec
2. **Gate A verplicht** - ruff + pytest + test-gate + invariant-check
3. **Fail-closed** - Bij non-compliant: STOP
4. **BACKLOG tracking** - Status updates in BACKLOG.md
5. **Sequentieel** - Stories in canonieke volgorde
6. **Test Requirements verplicht** - Elke story heeft Test Requirements sectie
7. **Invariants verplicht** - Relevante invariants gelinkt aan story

---

## Gerelateerde Skills

- `/cto-guard` - Standalone CTO validatie
- `/ralph-loop` - Continue iteratie over stories
- `/test-guard` - Test requirements validatie
- `/invariant-discovery` - Invarianten ontdekken

---

## Gerelateerde Bestanden

- `bmad_autopilot_kit/RUN1_STORY_GENERATION_PROMPT.txt`
- `docs/CTO_RULES.md` - CTO validation rules
- `docs/CONTRACT.md` - Story format contract
- `test-requirements.yaml` - Per-path test requirements
- `invariants.md` - Project invariants
- `tools/test-gate/test-gate.ps1` - Test requirements checker
- `tools/invariant-check/invariant-check.ps1` - Invariant checker
