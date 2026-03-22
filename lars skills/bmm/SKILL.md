---
name: bmm
# prettier-ignore
description: Snelle micro-wijzigingen met harde quality guards - file limits, e2e tests (geen mocks), specs, fixed ports. Geen planfile, geen worktree.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# BMM (BMAD Micro)

> Kleine wijzigingen snel uitvoeren met harde quality guards. Geen plan, geen worktree, wel file limits, e2e tests, specs, en fixed ports.

## Trigger

```
/skill:bmm <wat je wilt>
```

## Scope

**Wel:** button tweak, CSS-fix, copy change, kleine bugfix, config-aanpassing, mini refactor, camera-functie, port/endpoint, nieuwe kleine spec.

**Niet:** meerdere schermen/flows, auth, API-contract, migrations, infra, data model, >5 files. Dan → `/skill:plan-to-bmad`.

---

## Anti-overthink (HARD)

1. **Micro-brief max 5 regels.** Geen essays, geen facet-scores, geen Path to 10/10.
2. **Max 3 files lezen vóór edit.** Alleen target + directe imports. Niet de hele architectuur.
3. **Geen Universal CTO full scan.** Noem alleen direct relevante CTO rule IDs.
4. **Geen P1/P2/P3 mapping.** Fix het, test het, klaar.
5. **Geen opties verkennen.** Kies de beste aanpak, voer uit. Eén route.
6. **Begin met editen binnen 60 seconden** als de wijziging duidelijk is.
9. **Verboden woorden zonder bewijs**: `done`, `fixed`, `working`, `correct`, `passed`, `verified` zijn verboden zonder runtime-bewijs. Gebruik feitelijke taal.
7. **Universele guards gelden** — lees `~/.pi/agent/skills/_guards.md` (anti-lui, proof-eisen). Schaal naar micro: geen ceremonie maar wél bewijs.

---

## 10/10-kader voor BMM

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Micro-specifiek: bewijs schaal naar micro-formaat maar wordt niet weggelaten.

## Workflow

```
1. LEES    → max 3 files (target + directe imports)
2. BRIEF   → 5-regels micro-brief (zie format)
3. BUDGET  → file limits VÓÓR edit (lines + functies per touched file)
4. BEFORE  → screenshot vóór edit (bij visuele wijzigingen)
5. TEST 1  → schrijf EERST een falende test voor het gewenste gedrag (TDD)
6. EDIT    → kleinste nette wijziging zodat de test slaagt
7. SPEC    → bestaande spec updaten OF kleine nieuwe spec toevoegen
8. BUDGET  → file limits NA edit
9. APP     → zorg dat de app draait (tmux, fixed port)
10. TEST 2 → e2e test (echt, geen mock) + bewijs in test-results/
11. BUILD  → docker build als Dockerfile/docker-compose aanwezig
12. GATE   → quality gate als aanwezig
13. COMMIT → commit na groene tests + build
14. KLAAR  → kort rapporteren: wat gewijzigd, bewijs, specs
```

**Twee testlagen:**
- **TEST 1 (TDD)**: schrijf eerst een test die faalt, dan pas code. Dit dwingt je na te denken over gedrag vóór implementatie. Geldt voor runtime-wijzigingen, niet voor pure styling.
- **TEST 2 (E2E)**: echte browser/API test als bewijs. Screenshots, responses, port checks.

---

## Micro-brief (max 5 regels)

```
Doel: <1 zin>
Files: <touched paths>
Out-of-scope: <wat je NIET raakt>
CTO rules: <direct relevante rule IDs, of "geen">
Test: <verificatiecommand(s)>
```

---

## File limits - vóór én na (HARD)

**Vóór edit:**
- Check lines + function count per touched non-test file
- File al ≥280 regels of ≥14 functies → **split eerst**

**Na edit:**
- Non-test files: **max 300 regels, max 15 functies/methods**
- Run `python3 scripts/check_file_limits.py` als aanwezig
- Overschrijding → split, niet opleveren

---

## Specs - updaten of aanmaken (HARD)

**Specs schalen mee met de wijziging.** Kleine change = kleine spec. Geen spec-ceremonie voor micro-werk.

### Check of er bestaande specs zijn die geraakt worden

Zoek in:
- `openspec/specs/*.md` en `openspec/changes/*/specs/*/spec.md`
- `docs/specs/ux_contracts*.json`
- `docs/features/*.md`
- `docs/api/openapi.yaml`

### Bestaande spec geraakt → update

Als een spec het gedrag beschrijft dat je wijzigt: **update die spec** zodat het het nieuwe gedrag beschrijft. Een stale spec is een regressie-bom.

### Geen bestaande spec → maak een kleine

Als er geen spec bestaat voor het gewijzigde gedrag:

**UX contract entry** (als `docs/specs/ux_contracts*.json` bestaat):
```json
{
  "id": "<COMPONENT-NNN>",
  "title": "<wat het doet in 1 zin>",
  "risk": "P1",
  "description": "<concreet verwacht gedrag>",
  "verification": {
    "command": "<test command>",
    "expected": "<verwacht resultaat>"
  },
  "evidence": [{
    "type": "playwright",
    "path": "<test file pad>",
    "mustContain": "<contract ID>"
  }]
}
```

**OpenSpec scenario** (als `openspec/` bestaat):
```markdown
#### Scenario: <wat er moet gebeuren>
- WHEN <trigger>
- THEN <verwacht resultaat>
- AND <extra constraint>
```

**Kies het format dat de repo al gebruikt.** Geen nieuw format introduceren.

### Spec-gate

Run `python3 scripts/check-ux-contracts.py` of `python3 scripts/check-openspec.py` als aanwezig. Moet groen zijn.

---

## Before/After (visuele wijzigingen)

Bij CSS, styling, layout, component-wijzigingen:

1. **BEFORE**: screenshot vóór edit → `test-results/before-<naam>.png`
2. Edit uitvoeren
3. **AFTER**: screenshot na edit → `test-results/after-<naam>.png`

Gebruik `agent-browser screenshot <pad>` of Playwright.

---

## App moet draaien (HARD)

E2E tests vereisen een draaiende app.

```bash
# 1. Check of de dev server al draait
curl -sf http://localhost:<PORT> > /dev/null 2>&1 && echo "running" || echo "not running"

# 2. Niet draaiend? Start in tmux:
tmux new-session -d -s dev "<start command>"

# 3. Wacht tot port luistert:
timeout 30 bash -c 'until curl -sf http://localhost:<PORT> > /dev/null 2>&1; do sleep 1; done'
```

Start command en port: gebruik wat de repo definieert (`package.json`, `scripts/`, `docs/START_HERE.md`).

---

## E2E test - echt, geen mock (HARD)

**Geen mocks. Geen fallbacks. Geen "het compileert dus het werkt".**

| Type wijziging | Test |
|----------------|------|
| Button | Open pagina, klik button, verifieer resultaat |
| Visuele component | Open pagina, screenshot, verifieer rendering |
| Camera/media | Verifieer permissions prompt + capture flow |
| API endpoint | Echte HTTP request, verifieer response |
| Port/server | Start server, verifieer dat port luistert |
| CSS/styling | Open pagina, screenshot |
| Config | Verifieer dat app start met nieuwe config |
| Copy/tekst | Open pagina, verifieer tekst zichtbaar |

**Hoe:**
- Browser: `agent-browser` of `playwright`
- API/port: `curl` / `bash`
- Bewijs: sla op in `test-results/`

**Persistente test:**
- Als de repo een e2e test suite heeft (`tests/e2e/`): voeg een testcase toe of verifieer dat een bestaande test het pad dekt.
- Geen e2e suite? Eenmalige verificatie met bewijs is voldoende.

**Wanneer GEEN e2e:** pure docs, `.gitignore`, commentaar-only.

---

## Fixed-port discipline (HARD)

- Gebruik **altijd** de port uit repo config/scripts
- Port bezet → **kill**, niet hoppen

```bash
lsof -ti :<PORT> | xargs -r kill -9
# Dan starten op dezelfde port
```

---

## Docker build (HARD)

Als de repo een `Dockerfile` of `docker-compose.yml` heeft: **herbouw na elke wijziging**.

```bash
# docker-compose repo:
docker compose build

# Alleen Dockerfile:
docker build -t <image-naam> .
```

- Gebruik `scripts/deploy.sh` of `scripts/verify.sh` als die bestaan (ze runnen gates + build)
- Build moet slagen vóór commit. Falende build = niet opleveren.
- Geen `--no-cache` tenzij caching bewezen stuk is.

---

## Quality gate

- `scripts/quality_gates.py` → run als aanwezig
- Kleinste relevante lint/test/build checks voor gewijzigde paden

---

## Commit

Na groene tests + groene gates:

```bash
git add -A
git commit -m "<type>(<scope>): <wat in 1 zin>"
```

Commit message types: `fix`, `feat`, `style`, `refactor`, `test`, `docs`, `chore`.

---

## Probe-before-block (HARD)

Voordat je BLOCKED claimt op tool/env-falen, draai 3 probes:
1. no-op: `pwd` of `echo ok`
2. target tool: `npm -v`, `python3 --version`, `playwright --help`
3. task-level: port check, file write, of build dry-run

Als één probe slaagt, is "tools kapot" geen geldige blocker zonder extra bewijs.

---

## Escalate

Meteen naar `/skill:plan-to-bmad` + `/skill:bmad-bundle` als:
- scope groeit
- touched paths > 5 files
- je auth/data/infra raakt
- niet meer "klein en lokaal"

---

## Wat géén geldig stopmoment of succesclaim is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Micro-specifiek:

- code aangepast maar geen runtime/e2e/screenshot bewijs
- spec vergeten bij gedragswijziging
- "klaar" zeggen terwijl fixed port, app-start of testbewijs ontbreekt
- spec update die alleen het smalle gewijzigde punt dekt terwijl het bredere gedrag ook stale is
- bewijs dat alleen code-presence checkt (grep) terwijl het claim runtime-gedrag betreft

## Samenvatting: wat BMM anders doet

| Aspect | plan-to-bmad | bmm |
|--------|-------------|-----|
| Planning | Worktree + CTO intake + stories | 5-regels brief |
| Analyse | Universal scan, facets, P1/P2/P3 | Max 3 files lezen |
| Specs | Nieuwe OpenSpec change proposals | Update bestaande of maak kleine entry |
| Tests | Story proof gate | E2E tegen echte runtime |
| Commit | Per story branch | Direct op working tree |
| Doorlooptijd | 30-120 min | < 10 min |
