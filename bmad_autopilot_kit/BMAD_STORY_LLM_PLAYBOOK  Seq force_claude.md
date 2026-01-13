# BMAD Story (BMM) — LLM Playbook (Canonieke Story-Constructie)

Doel: een story schrijven die **direct implementeerbaar** is (zonder interpretatie), en die **mechanisch beoordeelbaar** is via meetbare acceptance criteria en bewijsbare verificatie.

Deze playbook is afgestemd op de BMM story-template structuur; de vaste kopjes/volgorde zijn belangrijk voor tooling (parsing, linting, CI-gates).

---

## 0) Kernprincipes (niet onderhandelbaar)

1. **Single source of truth = het storybestand.** De DEV-agent mag kunnen implementeren zonder “gissen”.
2. **AC’s zijn objectief meetbaar.** Elke AC heeft **exact 1** verificatiemethode: **1 command** + **expected output/exit/result**.
3. **Tasks/Subtasks mappen naar AC’s.** Elke taak refereert expliciet naar de AC die hij dient.
4. **Scope is hard; out-of-scope is bindend.** Geen refactor-creep. **Geen broad refactors** (geen repo-wide format, geen “cleanup imports” buiten scope) tenzij expliciet in scope.
5. **Fail-closed bij onzekerheid.** Als een contract/endpoint/field/ID onzeker is: **HALT** met expliciete assumptie + een verificatie-task/AC om het te bevestigen. Niet “verzinnen”.
6. **Evidence is verplicht.** `ready-for-dev` betekent: **alle** verification commands zijn uitvoerbaar. **Geen handmatige checks** in AC’s tenzij status `drafted` blijft.
7. **Command-context is expliciet.** Verification commands draaien **vanuit repo-root**, tenzij een AC expliciet een andere `cwd` noemt.
8. **Volgorde is canoniek.** Als een proces een `PROCESS.md` heeft met *Canonical Story Order*, dan is die volgorde bindend: geen “re-ordering”, geen “optimaliseren”.

---

## 1) Inputs die je (als LLM) eerst móét verzamelen

Voordat je één regel storytekst schrijft, moet je dit weten:

1. **Requirements bron** (epic/PRD/issue): wat moet er exact veranderen?
2. **Architectuur/constraints**: patterns, verboden acties, compatibiliteit (Python versie, tooling, deployment).
3. **Bestaande code realiteit**:
   - welke modules/paths zijn canonical?
   - welke bestaande interfaces/contracten móet je hergebruiken?
   - welke tests/gates bestaan al?
4. **Run- en quality-gates**: exacte commands die lokaal/CI gebruikt worden (ruff/pytest/coverage scripts, build steps).
5. **Omgevingsassumpties**: OS/CI runner, Python env manager (uv/poetry/pip), secrets/vars, fixtures.

6. **Procesvolgorde (sequentieel default):** de canonieke uitvoervolgorde staat in `PROCESS.md` (zie *Canonical Story Order*). Story’s mogen niet herordend worden door de LLM/agent.

Als één van deze ontbreekt: noteer dit onder **Dev Notes → Open Points** en voeg een **verificatie-step** toe die de aanname “locked” (bijv. `rg`, `pytest -q`, schema-check).

---

## 2) Canonieke BMM story-structuur (kopjes exact zo aanhouden)

Gebruik dit format (kopjes/volgorde is leidend):

1. `# Story <epic>.<story>: <title>`
2. `## Context`
3. `## Story`
4. `## Acceptance Criteria`
5. `## Tasks / Subtasks`
6. `## Dev Notes`
7. `## Dev Agent Record`
8. `## Status`

Tooling mag op deze kopjes vertrouwen. Niet hernoemen.

---

## 3) “## Story” sectie: 3 regels die alles dragen

Schrijf een user story in 1–3 regels:

> Als **<role>** wil ik **<action>** zodat **<benefit>**.

Regels:
- **Role** = actor die waarde ervaart (operator/admin/user/dev).
- **Action** = precies wat er verandert (geen oplossingstaal).
- **Benefit** = waarom dit waarde heeft (business/ops/UX).

---

## 4) “## Acceptance Criteria”: hoe je AC’s goed maakt (en LLM-fouten voorkomt)

### 4.1 Formaat

Een AC is “goed” als iemand anders hem kan uitvoeren zonder interpretatie.

Voorbeeld (Given/When/Then):
- **AC1:** Given `<preconditie>`, When `<actie>`, Then `<observeerbaar resultaat>`.

Of als verifieerbare statement:
- **AC2:** `<observeerbaar resultaat>` gebeurt onder `<conditie>`.

### 4.2 Verificatie is verplicht (1 AC = 1 command)

Elke AC bevat exact één verification command met expected resultaat.

Template:

- **AC<n>:** <statement>
  - **Verification (repo-root):** `<command>`
  - **Expected:** `<exitcode / key output / artifact>`

Regels:
- **Exact 1 command per AC.** Als je meerdere stappen nodig hebt, maak er één wrapper van (bijv. `make verify-ac1`, `python -m scripts/verify_ac1.py`) en roep die aan.
- **Geen handmatige checks** in AC’s als status `ready-for-dev` moet worden. Handmatig mag alleen bij `drafted` en moet expliciet als `MANUAL` gemarkeerd zijn.
- **Repo-root default.** Als een command niet vanuit repo-root draait, noteer expliciet: `Verification (cwd=<path>): ...`.

### 4.3 Failures moeten ook meetbaar zijn

Minimaal:
- 1 success-path AC
- 1 failure-mode AC (bijv. invalid input, missing file, missing env var, permission denied, schema mismatch)

Elke failure-mode AC heeft ook 1 verificatiecommand + expected error/exit.

---

## 4.4 Story-volgorde (sequentieel default)

Als de repo een procesbestand gebruikt (`PROCESS.md`), dan geldt:

- De story-ID’s zijn **genummerd** (bijv. `OPS-001`).
- De uitvoering is **sequentieel by default** en de **canonieke volgorde** staat in `PROCESS.md` onder *Canonical Story Order*.
- Een agent/LLM mag story’s **niet** herordenen op basis van eigen inschatting. Alleen wanneer `execution_mode: waves` expliciet gekozen is, is er een wave-sectie van toepassing.

## 5) “## Tasks / Subtasks”: bouwplan dat implementatie dwingt

Gebruik checkboxes en map elke taak aan een AC:

Voorbeeld:
```md
- [ ] Voeg/Update contract guard voor X (AC: 1)
  - [ ] Voeg unit test: success path (AC: 1)
  - [ ] Voeg unit test: failure-mode (AC: 2)
- [ ] Update wiring/startpad (AC: 3)
```

Regels:
- **Elke task** heeft `(AC: <nummer>)`.
- Subtasks splitsen zodat de DEV-agent niet “alles in één blob” doet.
- Tests zijn geen bijzaak: als een AC niet door tests/commands afgedekt wordt, is de story niet klaar.

---

## 6) “## Dev Notes”: dit is waar je de DEV-agent scherp stuurt

Dev Notes is geen essay; het is **implementation constraints + exact bewijs**.

Minimaal opnemen:

### 6.1 Scope

1. **Doel & non-goals (scope/out-of-scope)**  
   - Out-of-scope is kort maar hard.

2. **No broad refactors (hard rule)**  
   - Geen repo-wide formatting/cleanup.  
   - Geen import-sweeps buiten touched paths.  
   - Geen refactors tenzij expliciet in scope.

### 6.2 Touched paths allowlist (standaard)

**Touched paths allowlist (repo-relatief, exact):**
- `<pad/of/prefix 1>`
- `<pad/of/prefix 2>`

**Verificatie (subset-check):**
- `git diff --name-only <BASE_REF>...HEAD`

Eis:
- De output van `git diff --name-only` moet een **subset** zijn van de allowlist (paden/prefixes).  
- Als iets buiten allowlist moet: story aanpassen (scope expliciet maken) óf een aparte story.

> Tip voor tooling: allowlist + diff-check is ideaal voor wave/parallel worktrees, maar ook nuttig single-thread.

### 6.3 Constraints

- versie constraints (Python, Ruff, FastAPI, Node, etc.)
- architectuurregels (lagen, modulenaamgeving, import policy)
- verboden shortcuts (monkeypatching business logic, fake fixtures, netwerk in tests)
- compatibiliteit: backwards-compat, migrations, config keys

### 6.4 Test- en gate-commands

- **Commands draaien vanuit repo-root**, tenzij anders vermeld.
- Noteer exact welke commands moeten slagen (bijv.):
  - `python -m pytest -q tests/unit/test_x.py`
  - `ruff check .`
  - `pyright`
  - `python -m pytest -q && coverage report -m` (als relevant)

### 6.5 Observability/logging (als relevant)

Wat log je, waar, en waarom (incl. correlatie-id, error-classification).

### 6.6 Rollback plan

Hoe revert je veilig, welke checks draai je daarna (minimaal 1 command).

### 6.7 Open Points (alleen bij drafted)

Onzekerheden/assumpties + hoe die geverifieerd worden (task/AC).

### 6.8 References

Verwijs naar concrete bronnen met paden:
- `docs/...`
- `openspec/...`
- `api/...`
- bestaande codefiles

Geen externe claims zonder verwijzing of zonder “needs verification” task/AC.

---

## 7) “## Dev Agent Record”: regels voor later (en voor code-review)

Dit gedeelte is voor accountability (en review-kwaliteit). Minimaal:

- **Completion Notes List**: korte bullets wat echt gedaan is, incl. welke verification commands gedraaid zijn + resultaat.
- **File List**: alle gewijzigde/nieuwe/verwijderde files (repo-relatief).

De record is wat code-review vergelijkt met daadwerkelijke git changes. Als dit niet klopt: review faalt terecht.

---

## 8) Story status: wanneer “drafted” vs “ready-for-dev”

**drafted**:
- story is geschreven, maar nog niet “locked”: open points/assumpties bestaan nog, of verificatie is (deels) manual/onduidelijk.

**ready-for-dev** (pas zetten als alles hieronder waar is):
- **Elke AC heeft exact 1 verification command** en een **Expected** (exitcode/output/artifact).
- **Alle verification commands zijn uitvoerbaar** (geen “TODO”, geen “manual check”).
- Commands draaien **repo-root**, tenzij per AC expliciet anders vermeld.
- Tasks/subtasks zijn compleet en mappen naar AC’s.
- Scope/out-of-scope zijn expliciet, inclusief **No broad refactors** regel.
- Dev Notes bevat:
  - touched paths allowlist + diff subset-check command
  - test/gate commands
  - rollback plan

---

## 9) Snelle kwaliteit-checklist (voor je de story “FINAL” noemt)

1. AC’s: objectief, testbaar, **1 command per AC**, expected resultaat ingevuld.
2. Commands: **repo-root context** duidelijk; `cwd` alleen waar nodig expliciet.
3. Tasks: elke task heeft `(AC: n)` en er is testwerk per relevante AC.
4. Dev Notes:
   - touched paths allowlist + `git diff --name-only ...` subset-check
   - constraints + verboden acties
   - exacte test/gate commands
   - rollback plan
5. Geen hallucinatie-risico: geen verzonnen endpoints/payloads/IDs zonder bron of verificatie-step.
6. Out-of-scope is kort maar hard.

---

## 10) Praktisch “LLM schrijf-algoritme” (stap-voor-stap)

1. Lees requirements + architecture + project context.
2. Inventariseer bestaande code touchpoints (paths, contracts, tests).
3. Formuleer 1 zin user story (rol/actie/benefit).
4. Schrijf AC’s:
   - start met success path
   - voeg failure-mode(s) toe
   - voeg per AC exact 1 verificatiecommand + expected resultaat toe (repo-root default)
5. Splits tasks/subtasks en koppel aan AC’s.
6. Schrijf Dev Notes: scope, touched paths allowlist + subset-check, constraints, test commands, rollback.
7. Zet Status:
   - `drafted` als er nog onzekerheid/manual checks zijn
   - `ready-for-dev` als alles uitvoerbaar is zonder interpretatie
