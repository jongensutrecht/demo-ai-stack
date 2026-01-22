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
ls bmad_autopilot_kit_claude/
ls docs/CTO_RULES.md || echo "STOP: docs/CTO_RULES.md ontbreekt"
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

## STAP 3 - RUN1: Genereer Stories

Voer uit: `bmad_autopilot_kit_claude/RUN1_STORY_GENERATION_PROMPT_claude.txt`

Elke story heeft:
- CTO Rule traceability per AC
- Eerste taak: `- [ ] Lees CLAUDE.md`
- Laatste taak: `- [ ] Run Gate A checks`

Output:
- Story files (OPS-001.md, OPS-002.md, ...)
- BACKLOG.md voor Ralph Loop tracking

## STAP 4 - CTO GUARD #2: POST-GENERATION

Valideer gegenereerde stories:
- Check: Heeft elke AC een CTO Rule referentie?
- Check: Zijn alle verification commands executable?
- Output: `/cto-guard` rapport

Als NON-COMPLIANT: Fix stories of STOP

## STAP 5 - Preflight

```bash
pwsh ./bmad_autopilot_kit_claude/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1 \\
  -RepoRoot "<repo-root>" -Process "<Process>" \\
  -JsonOutput ".\\artifacts\\debug\\preflight.json"
```

## STAP 6 - RUN2: Voer Stories Uit (Ralph Loop)

Per story (via nieuw Claude window):

```bash
# a) Start Claude voor story
claude --dangerously-skip-permissions \\
  -p "Voer story <STORY_ID> uit. Story: stories_claude/<Process>/<STORY_ID>.md"

# b) Agent doet:
#    - Leest CLAUDE.md
#    - Voert story taken uit
#    - Runt Gate A (ruff + pytest)
#    - Runt CTO GUARD #3 (post-execution)

# c) Update BACKLOG.md status
```

## STAP 7 - CTO GUARD #3: POST-EXECUTION (per story)

Na Gate A, voor merge:
- Check: Geen security violations in nieuwe code?
- Check: Tests coverage adequate?
- Output: `/cto-guard` rapport

Als NON-COMPLIANT: STOP, geen merge
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
- NON-COMPLIANT: STOP, geen merge
"""

COMMANDS = """
## Validation Commands

```bash
# Check repo
git rev-parse --show-toplevel
ls bmad_autopilot_kit_claude/
ls docs/CTO_RULES.md

# Preflight
pwsh ./bmad_autopilot_kit_claude/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1 \\
  -RepoRoot "<repo-root>" -Process "<Process>" \\
  -JsonOutput ".\\artifacts\\debug\\preflight.json"

# Story execution
claude --dangerously-skip-permissions \\
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
