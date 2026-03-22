# Demo AI Stack

> BMAD Autopilot + CTO Guard + repo-governance toolkit voor Claude Code

Deze repo is een **deelbare toolkit** voor story-driven development met CTO traceability, quality gates en repo-governance.

## Wat is canoniek?

| Onderwerp | Canonieke bron |
|---|---|
| CTO Rule Registry | `docs/CTO_RULES.md` |
| CTO audit-proces | `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` |
| Repo quickstart | `docs/START_HERE.md` |
| Sources of truth map | `docs/SOURCES_OF_TRUTH.md` |
| Primary quality gate | `scripts/quality_gates.py` |
| Canonieke repo skills | `skills/` |

## Snelle start

### 1. Repo-governance valideren
```bash
python3 scripts/quality_gates.py
```

### 1b. Canonieke governance-bronnen tonen
```bash
python3 scripts/show_governance_status.py
```

Expected:
- `OK: all quality gates passed`

### 2. Toolkit installeren voor je lokale Claude setup
```powershell
.\INSTALL.ps1
```

### 3. Toolkit in een doelproject plaatsen
```powershell
.\INSTALL.ps1 -ProjectPath C:\path\to\target-repo
```

## Wat zit erin?

| Component | Functie |
|---|---|
| `skills/` | Canonieke repo-SSOT voor skills |
| `bmad_autopilot_kit/` | Exported prompts en playbooks |
| `tools/` | Helper tooling en legacy scripts |
| `scripts/` | Governance scripts + primary quality gate |
| `docs/` | Rule registry, scan-proces, quickstart, SSOT docs |
| `config/` | Golden queries + repo-root allowlist |

## Installatiegedrag

`INSTALL.ps1` doet twee dingen:
1. kopieert `skills/` naar `~/.claude/skills`
2. kopieert de governance-kit naar een doelproject als je `-ProjectPath` meegeeft

De governance-kit bevat minimaal:
- `docs/CTO_RULES.md`
- `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
- `docs/START_HERE.md`
- `docs/SOURCES_OF_TRUTH.md`
- `docs/FILE_LIMITS_EXCEPTIONS.md`
- `SECURITY.md`
- `scripts/validate_cto_rules_registry.py`
- `scripts/quality_gates.py`
- `scripts/check_repo_contract.py`
- `scripts/check_repo_10x_contract.py`
- `scripts/check_search_hygiene.py`
- `scripts/check_file_limits.py`
- `config/golden_queries.txt`
- `config/repo_root_allowlist.txt`
- `.ignore`

## Gebruik

### BMAD Autopilot
```text
/start-bmad-ralph
```

### BMAD Micro
```text
/bmad-micro
```
Kleine wijziging, geen planfile, geen worktree, wél CTO/universal/repo-10x quality guards.

### CTO Guard
```text
/cto-guard
```

### Ralph Loop
```text
/ralph-loop
```

## Quality contract

Deze repo mikt op:
- evidence-based audits
- fail-closed tooling
- 1 primary quality gate
- low-noise search voor LLMs en mensen
- non-test file limits: **max 300 regels, max 15 functies/methods**

Uitzonderingen staan alleen in:
- `docs/FILE_LIMITS_EXCEPTIONS.md`

## Legacy / non-SSOT paden

Deze paden zijn **niet canoniek** en horen niet als primaire bron gebruikt te worden:
- `.claude/skills/`
- `lars skills/`

Default search hygiene (`.ignore`) sluit deze paden uit om ruis te verminderen.

## Belangrijke documenten

- `docs/START_HERE.md`
- `docs/SOURCES_OF_TRUTH.md`
- `docs/CTO_RULES.md`
- `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
- `SECURITY.md`

## Licentie

MIT — zie `LICENSE`.
`.
