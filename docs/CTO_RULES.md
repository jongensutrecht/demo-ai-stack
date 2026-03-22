# CTO Rule Registry

Dit document is de **SSOT voor CTO Rule IDs** (bijv. `SEC-001`, `OPS-001`).

- **Scan-proces SSOT** (11 facetten, evidence-regels, scoring, output-structuur): `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
- **Registry SSOT** (dit bestand): stabiele Rule IDs + DoD + verificatie

## Regels voor deze registry (hard)

- Rule IDs zijn **stabiel**: nooit hernoemen of hernummeren
- Nieuwe regels: alleen **append-only** toevoegen
- Elke rule heeft:
  - `id`, `title`, `facets[]`, `intent`
  - `definition_of_done[]` (concrete, toetsbare eisen)
  - `verification[]` met ofwel `command` + `expected`, of `manual: true` + concrete check

## Registry (SSOT)

```yaml
version: 1

facet_vocab:
  - Architecture
  - Code Quality
  - Complexity & Bugs
  - Testing
  - Dependencies
  - Security
  - Ops/Reliability
  - Documentation
  - Developer Experience
  - Feature Flags
  - Domain/Spec Compliance

rules:
  - id: SEC-001
    title: "No public mutation endpoints"
    facets: [Security]
    intent: "Mutaties (POST/PUT/PATCH/DELETE) mogen niet publiek/anonymous zijn; vereisen authn+authz."
    definition_of_done:
      - "Alle mutatie endpoints vereisen authentication en authorization (role/ownership check)."
      - "Bij missing/invalid auth: 401/403 (geen silent success)."
    verification:
      - command: "rg -n \"\\b(POST|PUT|PATCH|DELETE)\\b\" -S ."
        expected: "Voor elke mutatie route is evidence van auth middleware/dependency aanwezig (file:line)."

  - id: SEC-002
    title: "No secrets in repo"
    facets: [Security]
    intent: "Secrets mogen niet in git; alleen via env/secrets manager."
    definition_of_done:
      - "Geen credentials, tokens, private keys, service account JSON of .env secrets in git-tracked files."
      - "Docs bevatten een veilige bootstrap (waar secrets moeten staan) zonder secrets zelf."
    verification:
      - command: "rg -n \"(BEGIN( RSA)? PRIVATE KEY|AIza[0-9A-Za-z\\-_]{20,}|xox[baprs]-|sk-[A-Za-z0-9]{20,}|service_account|client_secret|password\\s*=|api[_-]?key\\s*=)\" -S ."
        expected: "0 matches in git-tracked files (vals-positieven moeten expliciet whitelisted worden)."

  - id: OPS-001
    title: "Destructive operations are opt-in + recoverable"
    facets: [Ops/Reliability, Security]
    intent: "Scripts met delete/overwrite blast-radius zijn safe-by-default en recoverable."
    definition_of_done:
      - "Destructieve acties vereisen expliciete vlag (bijv. --apply/--i-understand-delete)."
      - "Default is dry-run (of no-op) met duidelijke output."
      - "Bij apply: maak timestamped backup + documenteer restore."
    verification:
      - command: "rg -n \"\\b(rm -rf|--delete|truncate|DROP TABLE|DELETE FROM|git reset --hard)\\b\" -S tools scripts ."
        expected: "Elke destructieve call is achter expliciete opt-in + backup/restore pad gedocumenteerd."

  - id: OPS-002
    title: "Health/readiness checks exist"
    facets: [Ops/Reliability]
    intent: "Runtime services hebben health/ready checks zodat deploy/run deterministisch is."
    definition_of_done:
      - "Er is minimaal 1 health endpoint/check die afhankelijkheden dekt."
      - "CI/guard scripts kunnen deze check gebruiken."
    verification:
      - manual: true
        check: "Zoek in de repo naar health endpoints/scripts; bewijs met file:line + 1 run-command die exit 0 oplevert."

  - id: TEST-001
    title: "New logic has tests"
    facets: [Testing]
    intent: "Nieuwe business logic wordt afgedekt door tests die falen zonder de fix."
    definition_of_done:
      - "Nieuwe of gewijzigde business-logic heeft unit/integration tests."
      - "Tests zijn deterministisch (geen sleeps/timeouts zonder reden)."
    verification:
      - manual: true
        check: "Toon nieuwe/gewijzigde tests + run command (pytest/npm test/etc.) met exit 0."

  - id: TEST-002
    title: "Critical flows have an executable smoke test"
    facets: [Testing, Ops/Reliability]
    intent: "Minstens een end-to-end of smoke test bewijst dat het systeem start en een kernflow werkt."
    definition_of_done:
      - "Er is 1 command die een kritieke flow verifieert (login/health/core endpoint) met expected output."
    verification:
      - manual: true
        check: "Leg 1 smoke command vast (curl/playwright) + expected output; draai het in CI of lokaal."

  - id: ARCH-001
    title: "Single source of truth (SSOT) for skills/tooling"
    facets: [Architecture, Developer Experience]
    intent: "Er is 1 canonieke plek voor skills/tooling om drift te voorkomen."
    definition_of_done:
      - "Er is 1 canonical skills directory en sync tooling verwijst daar eenduidig naar."
      - "Dubbele skill sets zijn verwijderd of expliciet 'examples/legacy' gemarkeerd."
    verification:
      - command: "ls -la"
        expected: "Docs/README wijzen naar 1 SSOT pad; duplicaten zijn verwijderd of duidelijk non-SSOT."

  - id: DEP-001
    title: "Dependencies are reproducible"
    facets: [Dependencies, Developer Experience]
    intent: "Tooling runt op pinned/gedocumenteerde versies."
    definition_of_done:
      - "Er is een manifest/lock of een expliciete versie-check + bootstrap script."
    verification:
      - manual: true
        check: "Bewijs met pyproject/package-lock/go.mod/etc. of een script dat versions checkt en faalt bij mismatch."

  - id: DATA-001
    title: "No silent data loss"
    facets: [Ops/Reliability, Domain/Spec Compliance, Security]
    intent: "Data-loss risico's zijn expliciet en beschermd (soft-delete/backup/migrations)."
    definition_of_done:
      - "DELETE/overwrite acties hebben safeguard (auth, confirmation, backup, soft-delete of audit)."
      - "Migrations zijn reversible of hebben een rollback plan."
    verification:
      - command: "rg -n \"\\b(DELETE FROM|DROP TABLE|TRUNCATE|rm -rf|--delete)\\b\" -S ."
        expected: "Elke match heeft een expliciete safeguard of is uitgesloten met rationale in docs/tests."

  - id: DOC-001
    title: "License exists if claimed"
    facets: [Documentation]
    intent: "Repo licentie is consistent en aanwezig."
    definition_of_done:
      - "Als README een licentie claimt: er is een LICENSE bestand met overeenkomende tekst."
    verification:
      - command: "ls -la LICENSE* || true"
        expected: "LICENSE bestaat als de README een licentie claimt."

  - id: DOC-002
    title: "Docs have a specific H1"
    facets: [Documentation, Developer Experience]
    intent: "Docs zijn scanbaar en niet generiek."
    definition_of_done:
      - "Elke README/.md in subfolders start met een inhoud-specifieke H1 (niet 'README')."
    verification:
      - manual: true
        check: "Run de docs-lint (of `rg -n '^# (README|Docs|Documentation)$'`) en toon 0 violations."

  - id: DX-001
    title: "One-command local run"
    facets: [Developer Experience, Ops/Reliability]
    intent: "Een nieuwe dev kan met 1 command het systeem draaien of tooling gebruiken."
    definition_of_done:
      - "README bevat 1 snelle start command (docker compose/script) + expected outcome."
    verification:
      - manual: true
        check: "Volg README quickstart exact; bewijs met command + output dat het werkt."

  - id: FF-001
    title: "Feature flags are explicit"
    facets: [Feature Flags, Ops/Reliability]
    intent: "Feature flags zijn vindbaar, gedocumenteerd en veilig defaulted."
    definition_of_done:
      - "Flags hebben 1 definitie plek + docs + veilige defaults."
    verification:
      - manual: true
        check: "Toon flag registry/config + docs + 1 test of smoke die default gedrag bewijst."

  - id: SPEC-001
    title: "Spec compliance is enforced"
    facets: [Domain/Spec Compliance, Documentation]
    intent: "Als er een OpenSpec/OpenAPI is, dan zijn implementatie en spec consistent."
    definition_of_done:
      - "Spec changes en code changes blijven in sync (geen 'spec drift')."
      - "Breaking changes zijn expliciet en gemarkeerd."
    verification:
      - manual: true
        check: "Toon spec file(s) + bewijs dat endpoints/flows overeenkomen (tests of curl)."

  - id: SEC-003
    title: "Security policy is documented"
    facets: [Security, Documentation]
    intent: "Iedere deelbare repo heeft een minimale security policy en disclosure pad."
    definition_of_done:
      - "Er is een SECURITY.md met disclosure-instructies en ondersteunde onderhoudsverwachting."
      - "README of START_HERE verwijst naar deze policy waar passend."
    verification:
      - command: "test -f SECURITY.md && rg -n \"(security|vulnerability|disclosure|report)\" SECURITY.md"
        expected: "SECURITY.md bestaat en bevat disclosure/security guidance."

  - id: ARCH-002
    title: "Repo root is predictable"
    facets: [Architecture, Developer Experience]
    intent: "De repo-root blijft klein en voorspelbaar; nieuwe top-level rommel wordt zichtbaar."
    definition_of_done:
      - "Er is een canonieke top-level allowlist."
      - "Een gate detecteert onverwachte top-level entries."
    verification:
      - command: "python3 scripts/check_repo_contract.py"
        expected: "OK: repo contract valid"

  - id: ARCH-003
    title: "Worktrees and mirrors are excluded from default tooling"
    facets: [Architecture, Developer Experience]
    intent: "Tooling, search en gates mogen niet per ongeluk door worktrees, mirrors of build-artefacts lopen."
    definition_of_done:
      - "Repo-wide search ignore sluit worktrees, mirrors en artefactdirs uit."
      - "De primaire quality gate controleert deze excludes."
    verification:
      - command: "python3 scripts/check_search_hygiene.py"
        expected: "OK: search hygiene valid"

  - id: DOC-003
    title: "START_HERE exists"
    facets: [Documentation, Developer Experience]
    intent: "Een nieuwe engineer of agent kan binnen minuten setup, run, gates en troubleshooting vinden."
    definition_of_done:
      - "docs/START_HERE.md bestaat en bevat setup, run, gates en troubleshooting."
      - "README verwijst naar START_HERE of vervult aantoonbaar dezelfde rol."
    verification:
      - command: "test -f docs/START_HERE.md && rg -n \"(Setup|Run|Gate|Troubleshooting)\" docs/START_HERE.md"
        expected: "docs/START_HERE.md bestaat en bevat setup/run/gates/troubleshooting secties."

  - id: DOC-004
    title: "Sources of truth are explicit"
    facets: [Documentation, Architecture]
    intent: "SSOT-documentatie voorkomt drift tussen docs, tooling en runtime."
    definition_of_done:
      - "docs/SOURCES_OF_TRUTH.md benoemt expliciet de truth voor rules, scan-proces, gates, skills en config."
      - "Legacy of non-SSOT mappen zijn expliciet gemarkeerd."
    verification:
      - command: "test -f docs/SOURCES_OF_TRUTH.md && rg -n \"(CTO_RULES|UNIVERSAL_CTO_REPO_SCAN_PROMPT|quality_gates.py|skills/)\" docs/SOURCES_OF_TRUTH.md"
        expected: "docs/SOURCES_OF_TRUTH.md bestaat en noemt de canonieke bronnen."

  - id: DX-002
    title: "One-command local quality gate"
    facets: [Developer Experience, Testing, Ops/Reliability]
    intent: "Er is exact één primaire lokale gate die de repo-governance afdwingt."
    definition_of_done:
      - "Er is 1 primair gate-entrypoint."
      - "README en CI verwijzen naar exact dat entrypoint."
      - "Gate faalt hard bij contractschending."
    verification:
      - command: "python3 scripts/quality_gates.py"
        expected: "OK: all quality gates passed"

  - id: DX-003
    title: "Search is low-noise by default"
    facets: [Developer Experience, Documentation]
    intent: "LLM's en mensen moeten standaard op echte runtime/docs landen, niet op mirrors en artefacts."
    definition_of_done:
      - "Er is een repo-wide search ignore (`.ignore`)."
      - "Er is een canonieke lijst met golden queries."
      - "De search gate faalt als de basis-search hygiene ontbreekt."
    verification:
      - command: "python3 scripts/check_search_hygiene.py"
        expected: "OK: search hygiene valid"

  - id: CODE-001
    title: "File limits are enforced"
    facets: [Code Quality, Complexity & Bugs, Developer Experience]
    intent: "Niet-test code blijft klein en leesbaar voor mensen en LLMs."
    definition_of_done:
      - "Non-test files zijn maximaal 300 regels en maximaal 15 functies/methods."
      - "Uitzonderingen staan expliciet in docs/FILE_LIMITS_EXCEPTIONS.md."
      - "De primaire quality gate faalt op niet-geallowliste overtreders."
    verification:
      - command: "python3 scripts/check_file_limits.py"
        expected: "OK: file limits valid"

  - id: OPS-003
    title: "CI runs the primary quality gate"
    facets: [Ops/Reliability, Testing, Developer Experience]
    intent: "Dezelfde governance-gate draait lokaal en in CI."
    definition_of_done:
      - "Een CI workflow roept exact het primaire gate-entrypoint aan."
      - "Er is geen tweede, afwijkende hoofdgate met andere semantiek."
    verification:
      - command: "rg -n \"quality_gates.py\" .github/workflows README.md docs/START_HERE.md"
        expected: "CI en docs verwijzen naar hetzelfde primary gate entrypoint."

  - id: OPS-004
    title: "Mainline required checks are enforced"
    facets: [Ops/Reliability, Security]
    intent: "Mainline merges horen beschermd te zijn met verplichte checks."
    definition_of_done:
      - "Mainline heeft required status checks of equivalent branch protection."
      - "Ontbrekende GitHub-auth/permissions wordt expliciet als UNKNOWN gerapporteerd, niet verzwegen."
    verification:
      - manual: true
        check: "Verifieer met `gh api` of platform-equivalent dat branch protection / required checks voor mainline actief zijn; zonder auth = UNKNOWN met exact 1 commando."
```

## Notities

- Deze registry definieert **wat** aantoonbaar goed moet zijn.
- `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` definieert **hoe** je de repo auditeert en scoret.
- Als een repo een rule niet kan bewijzen, rapporteer dat fail-closed als `UNKNOWN` of gap; niet speculeren.
