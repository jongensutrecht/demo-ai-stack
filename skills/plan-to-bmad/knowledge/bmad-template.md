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

## Scope Map
- **In scope:** [lijst]
- **Out of scope:** [lijst]
- **UNKNOWN external state:** [lijst of `None`]

## Universal CTO Intake
- **Applicable facets:** [Architectuur, Security, ...]
- **N/A facets:** [Feature Flags, ...] of `None`
- **UNKNOWN facets:** [Domain/Spec Compliance, ...] of `None`
- **Candidate P1 risks:** [lijst] of `None`
- **Candidate P2 risks:** [lijst] of `None`
- **Candidate P3 risks:** [lijst] of `None`

## Must-haves (P0)

### P0.1 — [Feature]
- **Requirement:** [specifiek wat moet werken]
- **Verificatie:** `[command]`
- **Expected:** `[output]`
- **Risico check:** [Security/Data Loss/Architecture of N/A]
- **CTO Rules:** [SEC-001, DATA-001, ...] (moeten bestaan in `docs/CTO_RULES.md`) of `N/A` + rationale
- **CTO Facets:** [Security, Ops/Reliability, ...] (volgens registry facet_vocab) of `N/A`

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

- [ ] `[primary-gate]` → `python3 scripts/quality_gates.py` als aanwezig → exit 0
- [ ] `[repo-10x]` → `python3 scripts/check_repo_10x_contract.py` als aanwezig → exit 0
- [ ] `[lint]` → exit 0
- [ ] `[typecheck]` → exit 0
- [ ] `[test]` → exit 0
- [ ] `file-limits` → max 300 regels + max 15 functies per niet-test file

## Out-of-scope
- [Wat we NIET doen]

## Touched paths allowlist
- `src/[paths]/`
- `tests/[paths]/`

## CTO Rules Check (als docs/CTO_RULES.md bestaat)
- [ ] [CTO Rule ID] -> [hoe dit plan voldoet]

## Universal CTO Review Check (als `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` bestaat)
- [ ] In scope / out of scope / UNKNOWN external state expliciet
- [ ] Relevante facetten benoemd
- [ ] Kandidaat P1/P2/P3 risico's benoemd of expliciet `None`
- [ ] Path to compliant closure duidelijk genoeg voor story-generatie

## Repo-10x Check (als guardrails aanwezig zijn)
- [ ] README / START_HERE / SOURCES_OF_TRUTH contract blijft coherent
- [ ] Search hygiene / golden queries / allowlist blijven intact
- [ ] Geen onnodige repo-root ruis of non-SSOT drift

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
  "scope_map": {
    "in_scope": ["[scope item]"],
    "out_of_scope": ["[out-of-scope item]"],
    "unknown_external_state": ["[unknown item]"]
  },
  "universal_cto_intake": {
    "applicable_facets": ["Security"],
    "na_facets": ["Feature Flags"],
    "unknown_facets": ["Domain/Spec Compliance"],
    "candidate_p1_risks": ["[risk]"],
    "candidate_p2_risks": ["[risk]"],
    "candidate_p3_risks": ["[risk]"],
    "facet_score_seeds": ["Code Quality under pressure because ..."],
    "path_to_10x_seed": ["Close P2 maintainability gap first", "Verify external unknowns last"]
  },
  "must_haves": [
    {
      "id": "P0.1",
      "title": "[Feature]",
      "requirement": "[specifiek wat moet werken]",
      "risk_check": "[Security/Data Loss/Architecture of N/A]",
      "cto_rules": ["SEC-001"],
      "cto_rule": "[LEGACY: optional]",
      "cto_facets": ["Security"],
      "cto_facet": "[LEGACY: optional]",
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
    "[primary-gate] -> python3 scripts/quality_gates.py if present -> exit 0",
    "[repo-10x] -> python3 scripts/check_repo_10x_contract.py if present -> exit 0",
    "[lint] -> exit 0",
    "[typecheck] -> exit 0",
    "[test] -> exit 0",
    "file-limits: max 300 lines, max 15 functions (non-tests)"
  ],
  "out_of_scope": ["[Wat we NIET doen]"],
  "touched_paths_allowlist": ["src/[paths]/", "tests/[paths]/"],
  "cto_rules_check": ["[CTO Rule ID] -> [hoe dit plan voldoet]"],
  "universal_cto_review_check": [
    "In scope / out of scope / UNKNOWN external state expliciet",
    "Relevante facetten benoemd",
    "Kandidaat P1/P2/P3 risico's benoemd of expliciet None",
    "Path to compliant closure duidelijk genoeg voor story-generatie"
  ],
  "repo_10x_check": [
    "README / START_HERE / SOURCES_OF_TRUTH contract blijft coherent",
    "Search hygiene / golden queries / allowlist blijven intact",
    "Geen onnodige repo-root ruis of non-SSOT drift"
  ],
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

**Universal CTO scope:**
- Wat is aantoonbaar out of scope?
- Welke externe state blijft UNKNOWN zonder extra runtime-bewijs?

**Tech stack:**
- Welke tech stack is leidend als detectie ambigu is?

Voor uitgebreide invariant analyse: `/invariant-discovery`
