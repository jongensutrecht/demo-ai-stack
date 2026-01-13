---
name: bmad-autopilot
# prettier-ignore
description: Start de BMAD autopilot voor story-driven development met CTO Guard.
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
user-invocable: true
---

# BMAD Autopilot

> **Versie**: 3.0.0
> **Doel**: Stories genereren en uitvoeren met CTO Guard validatie

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

## Workflow (met CTO Guard)

### STAP 0 - Validatie (fail-closed)

```bash
git rev-parse --show-toplevel
ls bmad_autopilot_kit_claude/
ls docs/CTO_RULES.md || echo "STOP: docs/CTO_RULES.md ontbreekt"
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
- Stories: `stories_claude/<Process>/`
- BACKLOG: `stories_claude/<Process>/BACKLOG.md`

### STAP 3 - RUN1: Genereer Stories

Voer uit: `bmad_autopilot_kit_claude/RUN1_STORY_GENERATION_PROMPT_claude.txt`

**Elke story heeft:**
- CTO Rule traceability per AC
- Eerste taak: `- [ ] Lees CLAUDE.md`
- Laatste taak: `- [ ] Run Gate A checks`

**Output:**
- Story files (OPS-001.md, OPS-002.md, ...)
- BACKLOG.md voor Ralph Loop tracking

### STAP 4 - CTO GUARD #2: POST-GENERATION

**Valideer gegenereerde stories:**
- Check: Heeft elke AC een CTO Rule referentie?
- Check: Zijn alle verification commands executable?
- Output: `/cto-guard` rapport

Als ❌ NON-COMPLIANT: Fix stories of STOP

### STAP 5 - Preflight

```bash
pwsh ./bmad_autopilot_kit_claude/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1 \
  -RepoRoot "<repo-root>" -Process "<Process>"
```

### STAP 6 - RUN2: Voer Stories Uit (Ralph Loop)

**Per story (via nieuw Claude window):**

```bash
# a) Start Claude voor story
claude --dangerously-skip-permissions \
  -p "Voer story <STORY_ID> uit. Story: stories_claude/<Process>/<STORY_ID>.md"

# b) Agent doet:
#    - Leest CLAUDE.md
#    - Voert story taken uit
#    - Runt Gate A (ruff + pytest)
#    - Runt CTO GUARD #3 (post-execution)

# c) Update BACKLOG.md status
```

### STAP 7 - CTO GUARD #3: POST-EXECUTION (per story)

**Na Gate A, voor merge:**
- Check: Geen security violations in nieuwe code?
- Check: Tests coverage adequate?
- Output: `/cto-guard` rapport

Als ❌ NON-COMPLIANT: STOP, geen merge

---

## Hard Rules

1. **CTO Guard op 3 momenten** - Pre-gen, post-gen, post-exec
2. **Gate A verplicht** - ruff + pytest moet groen
3. **Fail-closed** - Bij non-compliant: STOP
4. **BACKLOG tracking** - Status updates in BACKLOG.md
5. **Sequentieel** - Stories in canonieke volgorde

---

## Gerelateerde Skills

- `/cto-guard` - Standalone CTO validatie
- `/ralph-loop` - Continue iteratie over stories

---

## Gerelateerde Bestanden

- `bmad_autopilot_kit_claude/RUN1_STORY_GENERATION_PROMPT_claude.txt`
- `docs/CTO_RULES.md` - CTO validation rules
- `docs/CONTRACT.md` - Story format contract
