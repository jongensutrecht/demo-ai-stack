# Nieuwe aanpak: AGENTS.md en CLAUDE.md regels

**Datum:** 2026-03-21
**Context:** Na maanden power-user ervaring met Claude Code, Pi CLI en Codex is gebleken dat de manier waarop je AI-agent regels formuleert direct bepaalt of je 10/10 code krijgt of monolieten met mock tests.

## Het probleem

### Zonder regels
- Monolieten van 500-1000+ regels per file
- `MagicMock` overal, geen echte integratietests
- `try/except: pass` en `or []` silent fallbacks
- Geen e2e tests, alleen happy-path unit tests
- Half werk: stopt na eerste werkende versie

### Met te veel regels (>50)
- Claude begint regels te droppen naarmate context groeit
- Duplicaten over meerdere files verwateren de prioriteit
- "Default mode" van het model overschrijft custom regels
- Instructies worden "advisory" in plaats van "mandatory"

### De sweet spot
**20-30 harde regels**, negatief geformuleerd, zonder duplicaten, verdeeld over max 3 compacte bestanden.

## Bewezen bronnen
- GitHub #7777: Claude erkent zelf dat "default mode always wins because it requires less cognitive effort"
- Reddit r/ClaudeAI: "Once I passed ~50 rules, Claude started silently dropping them"
- Reddit r/ClaudeCode: "Instructions without enforcement are just suggestions apparently"
- Bagel.ai gids: "Without negative instructions, it defaults to verbose, over-cautious, and prone to scope creep"

## De drie bestanden

### 1. AGENTS.md (~30 regels) — gedragsregels

Twee secties: **NOOIT** en **ALTIJD**. Geen uitleg, geen context, alleen harde regels.

```markdown
# AGENTS.md — [Projectnaam] (leidend)

## NOOIT
- Geen vragen stellen. Kies en voer uit. Enige uitzondering: destructieve/onomkeerbare acties.
- Geen A/B/C opties. Geen keuzemenu's. Geen samenvattingen als stopmoment.
- Geen git stash. Commit WIP of gebruik branch/worktree.
- Geen fake green (thresholds verlagen, tests skippen, lint uitzetten).
- Geen mocks voor businesslogica. IO-randen mogen gestubd.
- Geen silent fallbacks (`try/except: pass`, `or []`, default die fout maskeert).
- Geen files >300 regels of >15 functies (tests uitgezonderd).
- Geen stoppen bij context-druk. Comprimeer en ga door.

## ALTIJD
- Handel als CTO. Jij beslist. Hoge kwaliteitsbar.
- Werk op feature-branch/worktree. Merge pas als groen.
- Runtime-wijzigingen → draai linter + tests + coverage. Docs-only → geen tests.
- Fail-closed: expliciete error + log + test die het valideert.
- BMAD gestart → afmaken tot RALPH_COMPLETE of hard BLOCKED.
- Laat de gebruiker NOOIT commands voor jou uitvoeren.

## Bronnen (volgorde)
1. Systeem/platformregels
2. `CTO_RULES.md`
3. Dit bestand
```

**Waarom dit werkt:**
- NOOIT-lijst is krachtiger dan positieve instructies (bewezen door community)
- 8 + 6 = 14 regels. Ver onder de ~50 drempel waar degradatie begint.
- Geen duplicaten met andere files.
- Geen uitleg die tokens verspilt.

### 2. CLAUDE.md (~25 regels) — projectcontext

Alleen feiten die het model nodig heeft om correcte code te schrijven. Geen gedragsregels (die staan in AGENTS.md).

```markdown
# [Projectnaam]

**Stack:** [tech stack]
**Taal:** Nederlands

## Platform
- [primair device en OS]
- [hardware specifics: printer, camera, etc.]

## Gates
```bash
[exact gate commands]
```

## Key dirs
- [dir] — [purpose]

## Verboden op [platform]
[platform-specifieke verboden, kort]
```

**Waarom dit werkt:**
- Puur referentie, geen regels → geen conflict met AGENTS.md
- Onder 25 regels → minimale context-impact
- Gate commands exact → model kan ze copy-pasten

### 3. CTO_RULES.md (~35 regels) — technische standaarden

De harde technische constraints. Geen overlap met AGENTS.md.

```markdown
# CTO Rules — [Projectnaam]

## Code
- Max 300 regels, max 15 functies per non-test file.
- Type hints op alle parameters en return types. Pydantic voor validatie.
- Structured logging. JSON in productie.
- Blocking I/O in thread pool. Nooit event loop blokkeren.

## Tests
- 100% line coverage.
- Geen mocks voor businesslogica. IO-randen mogen gestubd.
- Integration tests met echte test-DB.

## Foutafhandeling
- Geen silent fallbacks. Fail-fast op unexpected state.
- Alle inputs valideren. Alle file paths sanitizen.

## Architectuur
- Hardware via service interfaces. Implementaties swappable.
- [project-specifieke invarianten]
- Offline-first waar van toepassing.

## Security
- Secrets via env vars. `.env` nooit in git.

## Pre-commit
```bash
[exact gate commands]
```

## Bij violation
IDENTIFY → FIX → RESCAN → CONTINUE. Nooit stoppen.
```

## Principes

### 1. Negatief > positief
`NOOIT mock tests` werkt beter dan `schrijf altijd integratietests`. Het model heeft een sterker signaal van wat het moet vermijden dan van wat het moet doen.

### 2. Geen duplicaten
Elke regel staat op precies één plek. File limits staan in CTO_RULES.md, niet ook in AGENTS.md. Mock-regels staan in CTO_RULES.md (technisch) en AGENTS.md (gedrag), maar met verschillende scope.

### 3. Enforcement buiten het model
Regels die het model kan negeren, worden ook genegeerd. Enforcement via:
- `quality_gates.py` — script dat ruff + pytest + coverage + file limits draait
- CI workflow die exact dat script aanroept
- Branch protection op main
- Pre-commit hooks

Het model kan een regel vergeten. CI niet.

### 4. Minder = meer
228 regels → 90 regels. Dezelfde bescherming, minder context-druk, betere naleving.

### 5. 1 taak = 1 sessie
De community consensus: verse context = betere compliance. Gebruik handoffs niet als pauze maar als architectuur.

## Externe enforcement stack

| Laag | Wat | Waar |
|---|---|---|
| Gate script | `scripts/quality_gates.py` | Repo root |
| CI | `.github/workflows/gates.yml` | GitHub Actions |
| Branch protection | Required status checks op main | GitHub settings |
| File limits | `tools/quality/check_file_limits.py` | Onderdeel van gate |
| Coverage | `pytest --cov --cov-fail-under=100` | Onderdeel van gate |
| Lint | `ruff check + ruff format --check` | Onderdeel van gate |

## Resultaat

| Metriek | Oude aanpak | Nieuwe aanpak |
|---|---|---|
| Totaal regels | 228 | 90 |
| Bestanden | 3 (met duplicaten) | 3 (geen duplicaten) |
| Duplicaten | ~15 regels | 0 |
| Enforcement | Alleen prompt-gebaseerd | Prompt + CI + gates + hooks |
| Naleving (geschat) | ~60-70% | ~85-90% |

## Toepassing

Dit patroon is getest op de `jvdp-booth` repo (photobooth rental fleet) met:
- 94 non-test Python files
- 160 test files
- 759+ tests
- 100% coverage gate
- BMAD bundle workflow met 11+ stories per run

De trimming van 228 → 90 regels is toegepast op 2026-03-21.
