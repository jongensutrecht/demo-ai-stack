# BMAD Input — Repo 10x Governance Status

## Context
- **Repo:** demo-ai-stack
- **Doel:** Voeg een kleine helper toe die canonieke governance-bronnen toont zonder grote refactor
- **Tech stack:** Python scripts + Markdown docs

## Onderzoek Samenvatting
- **Relevante files:**
  - `scripts/quality_gates.py`
  - `scripts/check_repo_contract.py`
  - `README.md`
  - `docs/START_HERE.md`
  - `docs/SOURCES_OF_TRUTH.md`
- **Bestaande patterns:** Repo-governance wordt bewaakt via kleine Python scripts en SSOT docs
- **Risico's:** Architecture = laag; grootste risico is doc drift of nieuwe repo-root ruis

## Must-haves (P0)

### P0.1 — Add governance status helper
- **Requirement:** Voeg `scripts/show_governance_status.py` toe dat de canonieke governance-bronnen en hun aanwezigheid toont
- **Verificatie:** `python3 scripts/show_governance_status.py`
- **Expected:** `rules_registry: docs/CTO_RULES.md [present]`
- **Risico check:** Architecture
- **CTO Rules:** [DOC-004, DX-002, DX-003]
- **CTO Facets:** [Documentation, Developer Experience, Architecture]

### P0.2 — Document the helper in quickstart docs
- **Requirement:** README en START_HERE noemen het helper script expliciet
- **Verificatie:** `rg -n "show_governance_status.py" README.md docs/START_HERE.md`
- **Expected:** `show_governance_status.py`
- **Risico check:** N/A
- **CTO Rules:** [DOC-003, DOC-004]
- **CTO Facets:** [Documentation, Developer Experience]

### P0.3 — Keep governance gates green
- **Requirement:** De nieuwe helper veroorzaakt geen drift; repo contract, repo-10x contract, search hygiene en file limits blijven groen
- **Verificatie:** `python3 scripts/quality_gates.py`
- **Expected:** `OK: all quality gates passed`
- **Risico check:** Architecture
- **CTO Rules:** [ARCH-002, ARCH-003, DX-002, OPS-003]
- **CTO Facets:** [Architecture, Developer Experience, Ops/Reliability]

## Should-haves (P1)
None

## Could-haves (P2)
None

## Later (P3)
None

## Inverse succesfactoren (NOOIT)

| ID | Invariant | Check | Violation |
|----|-----------|-------|-----------|
| INV-01 | Geen nieuwe repo-root rommel of non-SSOT drift | `python3 scripts/check_repo_10x_contract.py` | STOP |
| INV-02 | Geen file-limit overschrijding door helper of proof files | `python3 scripts/check_file_limits.py` | STOP |

## Constraints / guardrails
- [ ] `[primary-gate]` → `python3 scripts/quality_gates.py` → exit 0
- [ ] `[repo-10x]` → `python3 scripts/check_repo_10x_contract.py` → exit 0
- [ ] `[lint]` → `python3 -m py_compile scripts/show_governance_status.py` → exit 0
- [ ] `[test]` → helper output command(s) → exit 0
- [ ] `file-limits` → max 300 regels + max 15 functies per niet-test file

## Out-of-scope
- Grote refactor van governance scripts
- Opschonen van alle legacy mirrors
- Nieuwe CI jobs buiten de bestaande quality gate

## Touched paths allowlist
- `scripts/show_governance_status.py`
- `README.md`
- `docs/START_HERE.md`
- `config/repo_root_allowlist.txt`
- `.ignore`
- `scripts/check_file_limits.py`
- `scripts/check_repo_contract.py`

## CTO Rules Check (als docs/CTO_RULES.md bestaat)
- [ ] DOC-003 -> START_HERE blijft de operationele gids
- [ ] DOC-004 -> canonieke governance-bronnen blijven expliciet
- [ ] DX-002 -> primary gate blijft leidend
- [ ] DX-003 -> low-noise search contract blijft intact
- [ ] ARCH-002 -> repo-root blijft voorspelbaar
- [ ] ARCH-003 -> default tooling/search blijft legacy paden uitsluiten
- [ ] OPS-003 -> CI/local gate contract blijft hetzelfde

## Universal CTO Review Check (als `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` bestaat)
- [ ] In scope / out of scope / UNKNOWN external state expliciet
- [ ] Relevante facetten: Documentation, Developer Experience, Architecture, Ops/Reliability
- [ ] Nieuwe P1/P2 risico's expliciet `None`

## Repo-10x Check (als guardrails aanwezig zijn)
- [ ] README / START_HERE / SOURCES_OF_TRUTH contract blijft coherent
- [ ] Search hygiene / golden queries / allowlist blijven intact
- [ ] Geen onnodige repo-root ruis of non-SSOT drift

## Verification checklist
- [ ] Helper toont alle canonieke governance-bronnen
- [ ] Docs verwijzen naar helper
- [ ] Quality gates blijven groen

## Bronnen
- `docs/CTO_RULES.md`
- `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
- `docs/START_HERE.md`
- `docs/SOURCES_OF_TRUTH.md`
