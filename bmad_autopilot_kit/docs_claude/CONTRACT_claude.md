# BMAD Story Contract (canoniek)

Dit document is de **single source of truth** voor het story-/process-format dat:
- RUN1 **moet produceren** (canoniek),
- preflight/runner **moeten kunnen parsen**,
- en waar alle prompts/runbooks naar **moeten verwijzen**.

Als dit contract ontbreekt of de input niet parsebaar is volgens dit contract: **STOP fail-closed** (geen gokken).

## Canonical vs. legacy compat

- **Canoniek** = wat RUN1 schrijft en waar tooling naartoe normaliseert.
- **Legacy compat** = wat tooling tijdelijk mag accepteren als input, maar bij preflight normaliseert naar canoniek.
- Legacy compat is expliciet en beperkt; “best effort” parsing is verboden.

### Canoniek
- Story ID: `PREFIX.001` (punt-notatie, prefix is uppercase alfanumeriek/underscore; volgnummer is 3 digits).
- Voorbeelden: `ARCH.001`, `KIT.005`
- Story bestandsnaam: `<STORY_ID>.md`
- ACCEPTANCE CRITERIA markers zijn **bold** en per AC exact één verificatie + één expected.
- PROCESS.md bevat een genummerde “Canonical Story Order” die machine-parsebaar is.

### Legacy compat (tijdelijk toegestaan als input)
- Story ID: `PREFIX-001` (hyphen-notatie).
- Voorbeeld: `OPS-001`
- Verification/Expected markers zonder bold (wordt genormaliseerd).

## Parsing constants (MUST NOT DRIFT)

De volgende constanten zijn normatief; tooling moet hier exact op aansluiten:

```text
STORY_ID_REGEX = r'^[A-Z][A-Z0-9_]*\.[0-9]{3}$'
STORY_ID_REGEX_LEGACY = r'^[A-Z][A-Z0-9_]*-[0-9]{3}$'

PROCESS_ORDER_REGEX = r'^\s*\d+\.\s+(?P<story_id>[A-Z][A-Z0-9_]*[\.-][0-9]{3})\s+-\s+(?P<title>.+)$'

VERIFICATION_MARKERS = [
  '- **Verification (repo-root):**',
  '- **Expected:**',
]
VERIFICATION_MARKERS_LEGACY = [
  '- Verification (repo-root):',
  '- Expected:',
]
```

## Story markdown (verplicht format)

### Verplichte kopjes (in deze volgorde)
1. `# Story <STORY_ID>: <Title>`
2. `## Context`
3. `## Story`
4. `## Acceptance Criteria`
5. `## Tasks / Subtasks`
6. `## Dev Notes`
7. `## Dev Agent Record`
8. `## Status`

### Acceptance Criteria (mechanisch)
- Elke AC start met een bullet: `- **ACn:** ...` (n is 1-based).
- Elke AC bevat **exact één**:
  - `- **Verification (repo-root):** <command>`
  - `- **Expected:** <expected>`
- Verification commando’s zijn deterministisch, non-interactive en runnable vanuit repo-root.

### Touched paths allowlist (verplicht bij wijzigingen)
- Stories die bestanden wijzigen moeten in `## Dev Notes` een sectie bevatten:
  - `### Touched paths allowlist (repo-relatief, exact)`
  - met een expliciete lijst van toegestane paden.
- Als een wijziging buiten de allowlist nodig lijkt: **STOP fail-closed** en pas eerst de story aan (geen scope creep).

Canonical subset-check (voorbeeld):
- `git diff --name-only <BASE_REF_SHA>...HEAD`

### Status values
Canonieke statuswaarden:
- `ready-for-dev`
- `in-progress`
- `blocked`
- `done`

## PROCESS.md contract

- Locatie: `docs/processes/<Process>/PROCESS.md`
- Bevat `execution_mode: sequential`
- Bevat sectie “Canonical Story Order” met genummerde regels die matchen op `PROCESS_ORDER_REGEX`.
