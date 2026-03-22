#!/usr/bin/env python3
"""BMAD Autopilot workflow details.

Usage:
    python workflow.py          # Show full workflow
    python workflow.py steps    # Show step details
    python workflow.py cto      # Show CTO Guard moments
    python workflow.py commands # Show all bash commands
"""

import sys

WORKFLOW_STEPS = """
## STAP 0 - Validatie (fail-closed)

```bash
git rev-parse --show-toplevel
ls bmad_autopilot_kit/
ls docs/CTO_RULES.md || echo "STOP: docs/CTO_RULES.md ontbreekt"
python3 scripts/validate_cto_rules_registry.py || echo "STOP: CTO Rule Registry invalid"
test -f scripts/quality_gates.py && python3 scripts/quality_gates.py || true
```

## STAP 1 - CTO GUARD #1: PRE-GENERATION

Valideer input document tegen CTO regels:
- Check: Is het plan compliant met architectuur regels?
- Check: Zijn er security risico's in het ontwerp?
- Output: `/cto-guard` rapport

Als NON-COMPLIANT: STOP fail-closed

## STAP 2 - Bepaal Process

```
Process = slug(basename(INPUT_FILE))
```

Output paden:
- Stories: `stories_claude/<Process>/`
- BACKLOG: `stories_claude/<Process>/BACKLOG.md`

## STAP 3 - RUN1: Genereer Stories (geen eindpunt)

Voer uit: `bmad_autopilot_kit/RUN1_STORY_GENERATION_PROMPT_claude.txt`

Elke story heeft:
- CTO Rule traceability per AC
- Eerste taak: `- [ ] Lees CLAUDE.md`
- Laatste taak: `- [ ] Run primary quality gate: python3 scripts/quality_gates.py`

Output:
- Story files (OPS-001.md, OPS-002.md, ...)
- BACKLOG.md voor Ralph Loop tracking

## STAP 4 - CTO GUARD #2: POST-GENERATION (interne gate, geen eindpunt)

Valideer gegenereerde stories:
- Check: Heeft elke AC een CTO Rule referentie?
- Check: Zijn alle verification commands executable?
- Output: `/cto-guard` rapport

Als NON-COMPLIANT: fix stories binnen dezelfde doorlopende run

## STAP 5 - Preflight (interne gate, geen eindpunt)

```bash
pwsh ./bmad_autopilot_kit/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1 \
  -RepoRoot "<repo-root>" -Process "<Process>" \
  -JsonOutput ".\\artifacts\\debug\\preflight.json"
```

## STAP 6 - RUN2: Voer Stories Uit (Ralph Loop, geen eindpunt)

Per story (via nieuw Claude window):

```bash
# a) Start Claude voor story
claude --dangerously-skip-permissions \
  -p "Voer story <STORY_ID> uit. Story: stories_claude/<Process>/<STORY_ID>.md"

# b) Agent doet:
#    - Leest CLAUDE.md
#    - Voert story taken uit
#    - Runt primary quality gate: python3 scripts/quality_gates.py (als aanwezig)
#    - Runt daarnaast de kleinste relevante runtime checks voor gewijzigde paden
#    - Runt CTO GUARD #3 (post-execution)
#    - Werkt story-state bij

# c) Update BACKLOG.md status
```

Belangrijk:
- Ga na RUN1 en RUN2 direct door binnen dezelfde autopilot-run.
- Als de huidige story nog niet `DONE` of `BLOCKED` is, ga niet naar de volgende story.
- Bij contextdruk: same-story handoff naar verse sessie; hervat dezelfde story.
- Stop pas vlak vóór final merge naar `main`.

## STAP 7 - CTO GUARD #3: POST-EXECUTION (per story)

Na de primary quality gate, voor merge:
- Check: Geen security violations in nieuwe code?
- Check: Tests coverage adequate?
- Output: `/cto-guard` rapport

Als NON-COMPLIANT: STOP, geen merge van die story
"""

CTO_MOMENTS = """
## CTO Guard Momenten

| Moment | Trigger | Check |
|--------|---------|-------|
| #1 PRE-GENERATION | Voor story generatie | Input document compliance |
| #2 POST-GENERATION | Na story generatie | Stories hebben CTO rules |
| #3 POST-EXECUTION | Na elke story | Code voldoet aan regels |

## Verdicts

- COMPLIANT: Doorgaan
- CONDITIONAL: Doorgaan met fixes
- NON-COMPLIANT: STOP, geen merge van die story
"""

COMMANDS = """
## Validation Commands

```bash
# Check repo
git rev-parse --show-toplevel
ls bmad_autopilot_kit/
ls docs/CTO_RULES.md
python3 scripts/validate_cto_rules_registry.py

# Primary quality gate (if present)
test -f scripts/quality_gates.py && python3 scripts/quality_gates.py || true

# Preflight
pwsh ./bmad_autopilot_kit/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1 \
  -RepoRoot "<repo-root>" -Process "<Process>" \
  -JsonOutput ".\\artifacts\\debug\\preflight.json"

# Story execution
claude --dangerously-skip-permissions \
  -p "Voer story <STORY_ID> uit. Story: stories_claude/<Process>/<STORY_ID>.md"
```
"""


def main():
    if len(sys.argv) < 2:
        print("BMAD Autopilot Workflow")
        print("=" * 50)
        print(WORKFLOW_STEPS)
        return

    cmd = sys.argv[1].lower()
    if cmd == "steps":
        print(WORKFLOW_STEPS)
    elif cmd == "cto":
        print(CTO_MOMENTS)
    elif cmd == "commands":
        print(COMMANDS)
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python workflow.py [steps|cto|commands]")


if __name__ == "__main__":
    main()
