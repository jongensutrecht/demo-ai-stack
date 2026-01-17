#!/usr/bin/env python3
"""Ralph Loop workflow details.

Usage:
    python workflow.py           # Show full workflow
    python workflow.py subprocess # Show subprocess details
    python workflow.py safeguards # Show safeguards
"""
import sys

WORKFLOW = """
## Workflow Details

### STAP 1 - Lees BACKLOG.md

```bash
# Vind open stories
grep -E "\\[TODO\\]|\\[IN_PROGRESS\\]" stories_claude/<Process>/BACKLOG.md
```

### STAP 2 - Pak Volgende Story

Prioriteit:
1. Eerst `[IN_PROGRESS]` (hervatten)
2. Dan eerste `[TODO]`

### STAP 3 - Voer Story Uit

KRITIEK: NOOIT stories zelf uitvoeren in de huidige context window.
ALTIJD een nieuw claude subprocess spawnen per story.

```bash
claude --dangerously-skip-permissions \\
  -p "Voer story <STORY_ID> uit. Story: stories_claude/<Process>/<STORY_ID>.md"
```

### STAP 4 - Update Status

Na story completion:
- Success -> [DONE]
- Failure (3x) -> [BLOCKED]
- Nog bezig -> [IN_PROGRESS]

### STAP 5 - Check Completion

Als alle stories [DONE] of [BLOCKED]:
  Output: <promise>RALPH_COMPLETE</promise>
Anders:
  Terug naar STAP 2
"""

SUBPROCESS = """
## Waarom Subprocess?

KRITIEK - LEES DIT EERST:
- NOOIT stories zelf uitvoeren in de huidige context window
- ALTIJD een nieuw claude subprocess spawnen per story
- WACHT tot subprocess klaar is voordat je doorgaat (blocking call)
- De subprocess heeft zijn eigen verse context en voert de story uit
- Jij (de orchestrator) doet ALLEEN: spawn -> wait -> update status -> next

Voordelen:
- Elke story krijgt verse context (geen rommel van vorige stories)
- Voorkomt context exhaustion
- Isolatie: als story faalt, blijft orchestrator intact

Command:
```bash
claude --dangerously-skip-permissions \\
  -p "Voer story <STORY_ID> uit. Story: stories_claude/<Process>/<STORY_ID>.md"
```
"""

SAFEGUARDS = """
## Safeguards

| Safeguard | Waarde |
|-----------|--------|
| Max iterations | `stories x 3` |
| Max attempts per story | 3 |
| Circuit breaker | 5 loops zonder progress -> STOP |

## Status Transitions

```
[TODO] -> [IN_PROGRESS] -> [DONE]
               |
          [BLOCKED] (na 3 failures)
```

## Hard Rules (NIET ONDERHANDELBAAR)

1. 100% completion vereist - Stop NOOIT voordat ALLE stories [DONE] of [BLOCKED]
2. Geen prioriteit-skip - P1, P2, EN P3 worden ALLEMAAL uitgevoerd
3. Agent beslist niet - Geen stories overslaan of als "optioneel" markeren
4. Subprocess per story - Nooit stories in huidige context uitvoeren
"""

def main():
    if len(sys.argv) < 2:
        print("Ralph Loop Workflow")
        print("=" * 50)
        print(WORKFLOW)
        return

    cmd = sys.argv[1].lower()
    if cmd == "subprocess":
        print(SUBPROCESS)
    elif cmd == "safeguards":
        print(SAFEGUARDS)
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python workflow.py [subprocess|safeguards]")

if __name__ == "__main__":
    main()
