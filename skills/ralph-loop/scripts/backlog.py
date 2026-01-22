#!/usr/bin/env python3
"""BACKLOG.md format details.

Usage:
    python backlog.py          # Show template
    python backlog.py example  # Show filled example
    python backlog.py status   # Show status transitions
"""
import sys

TEMPLATE = """
## BACKLOG.md Template

Location: `stories_claude/<Process>/BACKLOG.md`

```markdown
# BACKLOG - <Process>

| Story | Status | Attempts | Notes |
|-------|--------|----------|-------|
| OPS-001 | [TODO] | 0 | |
| OPS-002 | [TODO] | 0 | |
| OPS-003 | [TODO] | 0 | |
```
"""

EXAMPLE = """
## Filled Example

```markdown
# BACKLOG - my_feature

| Story | Status | Attempts | Notes |
|-------|--------|----------|-------|
| OPS-001 | [DONE] | 1 | |
| OPS-002 | [DONE] | 2 | 1e poging: test failure |
| OPS-003 | [IN_PROGRESS] | 1 | |
| OPS-004 | [BLOCKED] | 3 | pytest timeout, needs investigation |
| OPS-005 | [TODO] | 0 | depends on OPS-003 |
```
"""

STATUS = """
## Statussen

| Status | Betekenis | Actie |
|--------|-----------|-------|
| [TODO] | Nog niet gestart | Oppakken |
| [IN_PROGRESS] | Bezig | Hervatten |
| [DONE] | Compleet met groene tests | Skip |
| [BLOCKED] | 3x gefaald of dependency issue | Skip + escalate |

## Status Transitions

```
[TODO] -> [IN_PROGRESS] -> [DONE]
               |
          [BLOCKED] (na 3 failures)
```

## Attempts Tracking

- Increment bij elke poging
- Bij `attempts >= 3` en niet [DONE]: zet naar [BLOCKED]

## Notes Column

Gebruik voor:
- Failure reasons
- Blocker descriptions
- Dependencies

## Completion Criteria

Ralph Loop stopt wanneer:
- Alle stories [DONE] of [BLOCKED]
- OF max iterations bereikt
- OF circuit breaker triggered (5 loops zonder progress)
"""

def main():
    if len(sys.argv) < 2:
        print("BACKLOG.md Format")
        print("=" * 50)
        print(TEMPLATE)
        return

    cmd = sys.argv[1].lower()
    if cmd == "example":
        print(EXAMPLE)
    elif cmd == "status":
        print(STATUS)
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python backlog.py [example|status]")

if __name__ == "__main__":
    main()
