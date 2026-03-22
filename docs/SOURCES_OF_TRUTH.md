# Demo AI Stack SOURCES_OF_TRUTH

Dit document benoemt expliciet de **canonieke bronnen** in deze repo. Alles wat hiervan afwijkt is mirror, export, legacy of convenience-layer.

## Canonieke bronnen

| Onderwerp | Canonieke bron | Niet-canoniek / notities |
|---|---|---|
| CTO Rule IDs + DoD + verificatie | `docs/CTO_RULES.md` | Skills en prompts mogen alleen naar bestaande registry IDs verwijzen |
| CTO repo-audit proces | `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` | Historische review docs zijn geen SSOT |
| Repo setup + gates + troubleshooting | `docs/START_HERE.md` | README is de samenvatting; START_HERE is de snelle operationele gids |
| Repo quality gate | `scripts/quality_gates.py` | Subchecks zijn helper-scripts, geen primary gate |
| Repo contract checks | `scripts/check_repo_contract.py` | Alleen via `quality_gates.py` of directe debug-run |
| Repo-10x contract checks | `scripts/check_repo_10x_contract.py` | Bewaakt cross-links tussen README/START_HERE/SSOT/install/gate |
| Search hygiene checks | `scripts/check_search_hygiene.py` | `.ignore` en `config/golden_queries.txt` zijn input, niet de gate zelf |
| File limits checks | `scripts/check_file_limits.py` | `docs/FILE_LIMITS_EXCEPTIONS.md` is de allowlist-SSOT |
| File limit exceptions | `docs/FILE_LIMITS_EXCEPTIONS.md` | Geen ad-hoc uitzonderingen in comments of losse notes |
| Canonieke skills in de repo | `skills/` | `.claude/skills/` en `lars skills/` zijn niet de SSOT |
| Skill distributie naar lokale Claude | `INSTALL.ps1` + `tools/skills-sync/` | Sync tooling moet de canonieke `skills/` bron respecteren |
| Search-ignore defaults | `.ignore` | `.gitignore` is voor Git, niet voor default repo search |
| Golden search queries | `config/golden_queries.txt` | Queries horen op echte runtime/docs te landen |
| Repo-root allowlist | `config/repo_root_allowlist.txt` | Wordt door repo contract checks afgedwongen |
| Installer voor doelprojecten | `INSTALL.ps1` | README beschrijft de flow, script voert hem uit |
| CI quality gate | `.github/workflows/quality.yml` | CI moet exact dezelfde primary gate draaien als lokaal |
| Python tooling/dependencies | `pyproject.toml` | Losse versieclaims in README zijn niet de SSOT |

## Legacy / mirror paden

Deze paden bestaan, maar zijn **niet canoniek**:
- `.claude/skills/`
- `lars skills/`

Regel:
- default search en gates horen deze paden niet als primaire bron te behandelen
- docs moeten `skills/` als canonieke skill-bron benoemen

## Beslisregel bij conflict

Als twee documenten of paden elkaar tegenspreken:
1. volg de canonieke bron uit deze tabel
2. markeer de andere bron als drift/legacy
3. fix de verwijzing in docs/tooling zodat de drift verdwijnt
