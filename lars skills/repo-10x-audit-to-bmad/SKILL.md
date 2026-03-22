---
name: repo-10x-audit-to-bmad
description: "Assess a repo against a hard 10/10 rubric for LLM searchability + human usability, then generate BMAD-ready input (md+json) to reach 10/10. Includes enforced constraints: non-test files <=300 lines and <=15 functions."
metadata:
  short-description: "Repo audit -> BMAD plan to reach 10/10"
---

# Repo 10/10 Audit -> BMAD Plan

Doel: maak een repo 10/10 voor:
- LLM agents: snel, ruisvrij, deterministisch kunnen zoeken en wijzigen.
- Mensen: voorspelbaar, uitlegbaar, snel onboarden.

Gebruik deze skill vooral als je **specifiek een repo-shape audit + direct BMAD-plan** wilt. De master-review `/cto-guard` hoort dit volledige contract inmiddels ook mee te nemen binnen één gecombineerde CTO review.

Output is altijd tweeledig:
1. Assessment: `bmad_input/<PROCESS>_ASSESSMENT.md` (tekstueel oordeel + bewijs)
2. BMAD input: `bmad_input/<PROCESS>.md` + `bmad_input/<PROCESS>.json` (stories + proof gates)

Fail-closed: geen aannames.
- Als je iets niet hard kunt bewijzen: markeer als **UNKNOWN** + geef exact 1 verificatie-check.
- STOP alleen als je niet veilig kunt doorgaan (bijv. repo-root niet detecteerbaar, gate-entrypoint niet te vinden, of file-limit AST parsing onmogelijk).

Extra: **Universele guards gelden** — lees `~/.pi/agent/skills/_guards.md` en pas alle guards toe op assessment en BMAD-output.

## 10/10 contract (hard, meetbaar)

Een repo is pas 10/10 als ALLES hieronder "PASS" is.

### A) 1 knop bewijs (gates)
- PASS: er is exact 1 primaire gate-entrypoint (bijv. `scripts/quality_gates.py` of `make gates`) die lokaal en in CI draait.
- PASS: gate faalt hard bij rommel (geen stil succes).
- PASS: CI roept exact dit entrypoint aan (geen "bijna hetzelfde" parallel script).

### B) Zoeken is ruisvrij by default (LLM)
- PASS: `rg`/search negeert standaard ruis: worktrees, archives, outputs, venvs, logs, build artefacts.
- PASS: er is een expliciete repo-wide search ignore (`.ignore` of tool-config) en dit wordt afgedwongen door een gate.
- PASS: "golden queries" (vaste lijst termen) leveren top-hits op echte runtime-code, niet op archive/planning.
  - Vereist: een canonieke lijst in `config/golden_queries.txt` (1 query per regel; comments met `#`) of een gelijkwaardige SSOT-file.
  - Vereist: een gate die deze lijst draait en faalt als de top-hits vooral uit ruis/excluded dirs komen.

Minimale canonieke excludes (moeten in search-ignore én tooling-excludes terugkomen):
- `.worktrees/**`, `worktrees_claude/**`
- `node_modules/**`, `vendor/**`
- `.venv/**`, `venv/**`, `__pycache__/**`
- `dist/**`, `build/**`, `.next/**`, `out/**`
- `coverage/**`, `.pytest_cache/**`
- `logs/**`, `*.log`, `*.zip`, `*.tar.gz`

### C) Repo-root is klein en voorspelbaar (mens)
- PASS: repo-root heeft een allowlist; nieuwe top-level rommel laat CI falen.
- PASS: niet-runtime materiaal (planning, story input, artefacts) zit geconcentreerd onder 1 map (bijv. `planning/` of `archive/`), niet verspreid.

### D) Sources of truth zijn expliciet (geen dubbel)
- PASS: `docs/SOURCES_OF_TRUTH.md` bestaat en noemt letterlijk de truth voor:
- runtime entrypoints
- config: `.env` lokaal (nooit in git) vs `.env.example` (contract)
- dependencies + lockfile(s)
- tests + gates commando's
- CI pipeline(s)

### E) Onboarding is 10 minuten (mens)
- PASS: `docs/START_HERE.md` bevat: setup, run, gates, troubleshooting.
- PASS: link-check gate of equivalent: dode links breken CI.
  - Minimaal: interne Markdown links + anchors (offline-safe).
  - Externe links: alleen checken als netwerk expliciet beschikbaar is; anders fail-closed met duidelijke foutmelding.

### F) Geen secrets/artefacts/binaries in git
- PASS: `.env`, `.venv`, logs, outputs, tijdelijke zips, build outputs zijn niet tracked en worden genegeerd.
- PASS: binaries/zip alleen op 1 expliciete plek met policy, anders gate fail.

### G) Worktrees verpesten nooit lint/tests
- PASS: lint/test/coverage tooling loopt nooit per ongeluk door worktrees.

### H) Remote is ook hard (GitHub/CI)
- PASS: branch protection: required status checks op mainline, geen merge zonder gates groen.
- PASS: dit is aantoonbaar met hard bewijs (bijv. `gh api` tegen branch protection / required checks).
- Als je dit niet kunt bewijzen door ontbrekende GitHub-auth/permissions:
  - Markeer facet H als **UNKNOWN** met exact 1 `gh api ...` verificatie-commando.
  - Noteer dit als **stop condition voor 10/10** (je kunt de rest van de audit/plan wél afmaken).

### I) File limits (maintainability)
- PASS: niet-test files zijn <= 300 regels.
- PASS: niet-test files hebben <= 15 functies.
- PASS: er is een gate die dit afdwingt (en een documented uitzondering-proces als je echt niet anders kunt).

Uitzonderingenbeleid (hard, om "cheaten" te voorkomen):
- Uitzonderingen zijn ALLEEN toegestaan voor:
  - gegenereerde code (codegen)
  - migrations (als de stack dit oplegt)
  - large contract/spec artefacts (bijv. OpenAPI) wanneer splitten niet kan
  - grote test-fixtures/snapshots (alleen in test-scope)
- Elke uitzondering vereist SSOT + gate allowlist:
  - SSOT: `docs/FILE_LIMITS_EXCEPTIONS.md` (machineleesbaar; bijv. JSON list)
  - Velden minimaal: `path`, `reason`, `category`, `owner`, `expires_on` (of expliciet `never_expires=true`)
  - Gate faalt als er offenders zijn buiten de allowlist.

Test vs non-test scope (minimaal, uitbreidbaar per repo):
- Python tests: `tests/**`, `test_*.py`, `*_test.py`
- JS/TS tests: `**/__tests__/**`, `**/*.test.*`, `**/*.spec.*`
- PHP tests: `tests/**`, `*Test.php`

Function-count definitie (voor auditing; deterministisch, per taal; geen regex-tellen):
- HARD: tel via AST/parse (geen `rg`-regex), anders te veel false positives/negatives.
- Python: `def` + `async def` (incl. nested) + class methods (incl. `@staticmethod`, `@classmethod`, properties/getters/setters).
- JS/TS: function decl/expr, arrow functions (ook als export/assignment), class methods (incl. getters/setters), object-literal methods.
- PHP: named functions, class/trait/interface methods, closures `function (...) {}`, arrow functions `fn (...) =>`.
- FAIL (fail-closed) als parsing niet lukt (bijv. ontbrekende parser/deps) en noteer exacte oorzaak + required install/command in bewijs.

## Wat 10/10 voor deze skill WEL en NIET is

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Repo-10x-specifieke aanvullingen:

### 10/10 repo-shape specifiek WEL (bovenop universele guards)
- deterministisch: 1 knop gates, 1 SSOT per essentieel domein
- ruisvrij: zoeken landt op runtime-code, niet op archives/plans/output
- klein en uitlegbaar: root schoon, ownership zichtbaar, onboarding snel

### 10/10 repo-shape specifiek NIET (bovenop universele guards)
- extra docs bovenop tegenstrijdige runtime-truths
- nog een script dat "ongeveer hetzelfde" doet als de primaire gate
- FAILs kopiëren naar stories zonder transformatie-logica

## Assessment workflow (bewijsgestuurd)

### 0) Scope + regels laden
- Lees repo-wide instructies (`AGENTS.md`, `CONTRIBUTING.md`, `docs/START_HERE.md`).
- Detecteer "mainline" branch naam en CI systeem.
- Noteer "sources of truth" die al bestaan (of ontbreken).
- Detecteer stacks (Python / Node (JS/TS) / PHP) en monorepo-boundaries (waar begint/eindigt een project).

### 1) Evidence verzamelen (minimaal maar hard)
- **If `scripts/check_repo_health.py` exists: run it first.** Map PASS/FAIL results directly to the A-I scorecard. Health check output is deterministic ground truth — do not contradict it with ad-hoc checks.
- Draai het primaire gates-commando (of identificeer dat het ontbreekt).
- Inspecteer repo-root top-level items.
- Check of search-ignore bestaat en effectief is.
- Check `.gitignore` en policies rond binaries/secrets/artefacts.
- Tel file sizes en functie-aantallen (non-test) en verzamel overtreders.
- Verifieer per stack dat tooling excludes hanteert (worktrees/artefacts/vendor) en dat dit in gates afgedwongen wordt.
- Evidence hygiene (hard): toon nooit secrets/tokens/PII in output. Redacteer.

Als de repo meerdere talen heeft:
- Documenteer per taal exact hoe "functie" geteld wordt (zie sectie I).
- Maak 1 file-limit gate die alle stacks dekt, met dezelfde exclude/test-scope regels.

### 2) Scorecard invullen (PASS/FAIL + bewijs)
- Maak per contract-sectie A t/m I een PASS/FAIL.
- Bij FAIL: 1 zin "wat is er mis" + 1 zin "bewijs" (command/locatie).

### 3) P0/P1/P2/P3 backlog uit de FAILs
Mapping regels:
- P0: alles wat determinisme/veiligheid/CI-merge guard raakt (gates, secrets, branch protection, fail-closed).
- P1: searchability, repo-root allowlist, sources-of-truth docs.
- P2: structurele opschoning en verplaatsingen (planning/archive consolidatie).
- P3: polish (consistent naming, extra docs, nice-to-have tooling).

## BMAD-ready output workflow (assessment -> plan)

Doel: genereer een uitvoerbaar, proof-gated werkplan om alle FAILs naar PASS te krijgen.

Hard rules:
- Schrijf BMAD input niet op mainline; werk op een unieke process branch (en bij voorkeur een aparte worktree) om rommel te vermijden.
- Elke P0 heeft EXACT 1 `[command]` en EXACT 1 `[expected]` verificatie.
- Geen TODO's/open eindjes in de output.
- Universele guards (`_guards.md`) gelden op stories en plan. Aanvullend:
  - elke story benoemt welke **contract-secties (A-I)** van FAIL/UNKNOWN naar PASS bewegen.

### 1) Kies `PROCESS` slug
- `repo_10x_<repo>_<yyyymmdd>`

### 2) Schrijf BMAD input bestanden
- `bmad_input/<PROCESS>.md`
- `bmad_input/<PROCESS>.json`
- `bmad_input/<PROCESS>_ASSESSMENT.md`

Inhoud moet bevatten:
- P0/P1/P2/P3: elk item is concreet en testbaar.
- Invariants (NOOIT): geen secrets in git, fail-closed gates, CI required checks, worktrees excluded from tooling.
- Constraints: non-test files <=300 regels en <=15 functies (tests uitgezonderd); exceptions alleen met expliciete doc + gate allowlist.
- Out-of-scope: wat je bewust niet doet.
- `10/10 Kader`:
  - wat 10/10 voor deze repo concreet WEL betekent
  - wat 10/10 nadrukkelijk NIET betekent
- `Path to 10/10`:
  - waarom juist deze stories de hoogste hefboom hebben
  - in welke volgorde ze uitgevoerd moeten worden
  - waarom dit géén lui plan is

### 3) Verificatie-eisen (proof gates)
Minimaal voor P0:
- `[command]` gate run (lokaal/CI equivalent)
- `[expected]` "All checks passed" of equivalente harde output

Minimaal voor file limits:
- `[command]` run de file-limit gate
- `[expected]` "0 offenders" of "allowed exceptions only"

## Deliverable format (wat jij teruggeeft aan de user)

1. `bmad_input/<PROCESS>_ASSESSMENT.md` inhoud (in chat) met PASS/FAIL per A-I + evidence.
2. Exacte paden van de aangemaakte BMAD input files (`bmad_input/<PROCESS>.md` + `bmad_input/<PROCESS>.json`).
3. Een korte "stop condition": wat nog blokkeert voor 10/10 (typisch GitHub branch protection bewijs).

## Wat géén geldig stopmoment of output is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Skill-specifiek:

- een assessment zonder transformatieplan
- een plan zonder `10/10 Kader` en `Path to 10/10`
