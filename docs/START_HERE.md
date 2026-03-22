# Demo AI Stack START_HERE

Deze repo is een **toolkit** voor BMAD + CTO Guard + Ralph Loop. De canonieke bron voor repo-governance en skill-content staat in deze repo; mirrors en legacy exports zijn niet de SSOT.

## 1. Wat is de snelste route?

### Alleen de repo-governance controleren
```bash
python3 scripts/quality_gates.py
```

Expected:
- `OK: all quality gates passed`

### De CTO Rule Registry valideren
```bash
python3 scripts/validate_cto_rules_registry.py
```

### Een skill-pack naar je lokale Claude-installatie kopiëren
```powershell
.\INSTALL.ps1
```

### De toolkit in een doelproject plaatsen
```powershell
.\INSTALL.ps1 -ProjectPath C:\path\to\target-repo
```

### Kleine wijziging met quality guards maar zonder full BMAD
```text
/bmad-micro
```

## 2. Canonieke bronnen

- Rules registry: `docs/CTO_RULES.md`
- Audit-proces: `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
- Repo contract / SSOT map: `docs/SOURCES_OF_TRUTH.md`
- Primary gate: `scripts/quality_gates.py`
- Canonieke repo skills: `skills/`

## 3. Setup

### Verwacht lokaal aanwezig
- Python 3
- Git
- PowerShell voor `INSTALL.ps1` op Windows

### Optioneel maar aanbevolen
- GitHub CLI (`gh`) voor branch-protection verificatie
- `rg` / ripgrep voor snelle search-validatie

## 4. Runbook

### Repo health check
```bash
python3 scripts/quality_gates.py
```

Dit omvat ook de repo-10x contractcheck:
```bash
python3 scripts/check_repo_10x_contract.py
```

### Canonieke governance-bronnen snel tonen
```bash
python3 scripts/show_governance_status.py
```

### Alleen file limits checken
```bash
python3 scripts/check_file_limits.py
```

### Alleen repo contract checken
```bash
python3 scripts/check_repo_contract.py
```

### Alleen search hygiene checken
```bash
python3 scripts/check_search_hygiene.py
```

## 5. Troubleshooting

### `ERROR: missing docs/CTO_RULES.md`
De repo is incompleet of je zit niet in de repo-root. Controleer eerst:
```bash
git rev-parse --show-toplevel
```

### `quality_gates.py` faalt op file limits
Lees `docs/FILE_LIMITS_EXCEPTIONS.md`. Voeg alleen uitzonderingen toe met rationale, owner en vervaldatum/`never_expires`.

### Search hygiene faalt
Controleer:
- `.ignore`
- `config/golden_queries.txt`
- legacy/mirror paden die niet in default search horen

### Registry validator faalt
Controleer dat `docs/CTO_RULES.md` exact één YAML block onder `## Registry (SSOT)` bevat.

## 6. Belangrijke waarschuwingen

- `skills/` is de **enige canonieke repo-bron** voor skills.
- `.claude/skills/` en `lars skills/` zijn niet de SSOT; behandel ze als mirror/legacy totdat ze volledig zijn opgeschoond.
- Voer story-verificatiecommando's niet uit op onbetrouwbare input zonder expliciete opt-in.
