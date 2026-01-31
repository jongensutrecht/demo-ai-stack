# BMAD Input Template

## Output Format (Markdown)

```markdown
# BMAD Input — [PROJECT NAAM]

## Context
- **Repo:** [repo naam]
- **Doel:** [uit plan]
- **Tech stack:** [detecteren of vragen]

## Onderzoek Samenvatting (alleen Modus 1)
- **Relevante files:** [lijst]
- **Bestaande patterns:** [beschrijving]
- **Risico's:** [Security/Data Loss/Architecture of N/A]

## Must-haves (P0)

### P0.1 — [Feature]
- **Requirement:** [specifiek wat moet werken]
- **Verificatie:** `[command]`
- **Expected:** `[output]`
- **Risico check:** [Security/Data Loss/Architecture of N/A]
- **CTO Rule:** [SEC-001/DATA-001/ARCH-001/etc. of N/A]
- **CTO Facet:** [Security/Data Loss/Architecture/Testing/Operations/Docs/Performance of N/A]

## Should-haves (P1)

(Als er geen items zijn: schrijf expliciet `None`.)

### P1.1 — [Nice-to-have]
- **Requirement:** [specifiek]

## Could-haves (P2)

(Als er geen items zijn: schrijf expliciet `None`.)

### P2.1 — [Nice-to-have]
- **Requirement:** [specifiek]

## Later (P3)

(Als er geen items zijn: schrijf expliciet `None`.)

### P3.1 — [Later]
- **Requirement:** [specifiek]

## Inverse succesfactoren (NOOIT)

| ID | Invariant | Check | Violation |
|----|-----------|-------|-----------|
| INV-01 | [Wat NOOIT mag] | `[command]` | STOP |

## Constraints / guardrails

- [ ] `[lint]` → exit 0
- [ ] `[typecheck]` → exit 0
- [ ] `[test]` → exit 0
- [ ] `file-limits` → max 300 regels + max 20 functies per niet-test file

## Out-of-scope
- [Wat we NIET doen]

## Touched paths allowlist
- `src/[paths]/`
- `tests/[paths]/`

## CTO Rules Check (als docs/CTO_RULES.md bestaat)
- [ ] [CTO Rule ID] -> [hoe dit plan voldoet]

## Verification checklist
- [ ] [User flow werkt]
- [ ] [Edge case handled]

## Bronnen
- [paden naar relevante docs]
```

## Output Format (JSON)

```json
{
  "project": {
    "name": "[PROJECT NAAM]",
    "repo": "[repo naam]",
    "goal": "[uit plan]",
    "tech_stack": ["[detecteren of vragen]"]
  },
  "research_summary": {
    "relevant_files": ["[paden]"],
    "patterns": ["[beschrijving]"],
    "risks": ["[Security/Data Loss/Architecture of N/A]"]
  },
  "must_haves": [
    {
      "id": "P0.1",
      "title": "[Feature]",
      "requirement": "[specifiek wat moet werken]",
      "risk_check": "[Security/Data Loss/Architecture of N/A]",
      "cto_rule": "[SEC-001/DATA-001/ARCH-001/etc. of N/A]",
      "cto_facet": "[Security/Data Loss/Architecture/Testing/Operations/Docs/Performance of N/A]",
      "verification": {
        "command": "[command]",
        "expected": "[output]"
      }
    }
  ],
  "should_haves": [
    {
      "id": "P1.1",
      "title": "[Nice-to-have]",
      "requirement": "[specifiek]"
    }
  ],
  "could_haves": [
    {
      "id": "P2.1",
      "title": "[Nice-to-have]",
      "requirement": "[specifiek]"
    }
  ],
  "later": [
    {
      "id": "P3.1",
      "title": "[Later]",
      "requirement": "[specifiek]"
    }
  ],
  "invariants": [
    {
      "id": "INV-01",
      "invariant": "[Wat NOOIT mag]",
      "check": "[command]",
      "violation": "STOP"
    }
  ],
  "constraints": [
    "[lint] -> exit 0",
    "[typecheck] -> exit 0",
    "[test] -> exit 0",
    "file-limits: max 300 lines, max 20 functions (non-tests)"
  ],
  "out_of_scope": ["[Wat we NIET doen]"],
  "touched_paths_allowlist": ["src/[paths]/", "tests/[paths]/"],
  "cto_rules_check": ["[CTO Rule ID] -> [hoe dit plan voldoet]"] ,
  "verification_checklist": ["[User flow werkt]", "[Edge case handled]"],
  "sources": ["[paden naar relevante docs]"]
}
```

## Vragen bij ontbrekende info

**Verificatie:**
- Hoe verifieer ik dat [feature] werkt?
- Welk command? Wat is expected output?

**Invarianten:**
- Wat mag ABSOLUUT NIET gebeuren?
- Welke bestaande functionaliteit moet intact blijven?

**Tech stack:**
- Welke tech stack is leidend als detectie ambigu is?

Voor uitgebreide invariant analyse: `/invariant-discovery`
