# BMAD Input Template

## Output Format

```markdown
# BMAD Input — [PROJECT NAAM]

## Context
- **Repo:** [repo naam]
- **Doel:** [uit plan]
- **Tech stack:** [detecteren of vragen]

## Must-haves (P0)

### P0.1 — [Feature]
- **Requirement:** [specifiek wat moet werken]
- **Verificatie:** `[command]`
- **Expected:** `[output]`

## Should-haves (P1)

### P1.1 — [Nice-to-have]
- **Requirement:** [specifiek]

## Inverse succesfactoren (NOOIT)

| ID | Invariant | Check | Violation |
|----|-----------|-------|-----------|
| INV-01 | [Wat NOOIT mag] | `[command]` | STOP |

## Constraints / guardrails

- [ ] `[lint]` → exit 0
- [ ] `[typecheck]` → exit 0
- [ ] `[test]` → exit 0

## Out-of-scope
- [Wat we NIET doen]

## Touched paths allowlist
- `src/[paths]/`
- `tests/[paths]/`

## Verification checklist
- [ ] [User flow werkt]
- [ ] [Edge case handled]

## Bronnen
- [paden naar relevante docs]
```

## Vragen bij ontbrekende info

**Verificatie:**
- Hoe verifieer ik dat [feature] werkt?
- Welk command? Wat is expected output?

**Invarianten:**
- Wat mag ABSOLUUT NIET gebeuren?
- Welke bestaande functionaliteit moet intact blijven?

Voor uitgebreide invariant analyse: `/invariant-discovery`
