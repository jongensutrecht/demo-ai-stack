# AI-Stack Standard — BMAD Worktrees + Guardrails (Local-First)

Doel: deterministische delivery zonder merge-chaos.  
Werkwijze: **1 story = 1 branch = 1 worktree**; integreren gebeurt uitsluitend via de **integratie-worktree** (`main-merge`).

Belangrijk (jouw huidige setup):
- **Sequentiële run**: stories worden na afronden **automatisch gemerged** naar `main-merge` (integratie-worktree).  
- Dit gedrag blijft leidend: **geen extra handmatige merge-stappen** toevoegen aan het proces.

Scope:
- Dit document is de **baseline**. Repo-specifieke overrides horen in repo-root `AGENTS.md`.
- “Local-first” gaat over **werkcopies** (worktrees), niet over “docs buiten git”: proces- en storyfiles horen **in git**.

---

## 1) Kernregels (altijd)

- **Local-first:** worktrees onder `worktrees/**` zichtbaar als folders.
- **Git merge’t branches, niet mappen:** “merge map” = **worktree** die een **integratie-branch** uitcheckt.
- **Just-in-time story worktrees (hard):** maak een story-worktree pas wanneer je die story start (voorkomt baseline drift/merge-conflicten).
- **Geen destructieve git-acties** zonder expliciete instructie (reset/rebase/history rewrite/worktree remove/etc.).
- **Main/release merge alleen na expliciete GO**.

---

## 2) Naamgeving (simpel en consistent)

### Proces (initiative)
- Procesnaam: `<procesnaam>` (grepbare slug)  
  Voorbeeld: `dashboard_enterprise_grade`

### Branches
- **Integratie-branch:** `<procesnaam>`  
  Voorbeeld: `dashboard_enterprise_grade`
- **Story-branch:** `<procesnaam>-<STORY_ID>`  
  Voorbeeld: `dashboard_enterprise_grade-OPS-001`

### Worktree folders (local only)
Onder repo-root:
```
worktrees/
  <procesnaam>/
    main-merge/          # integratie-worktree (branch: <procesnaam>)
    OPS-001/             # story-worktree (branch: <procesnaam>-OPS-001)
    OPS-002/
    ...
```

---

## 3) Proces- en storyfiles (single source of truth)

### 3.1 Proces file (verplicht)
### 3.1 Proces file (verplicht — **deterministische volgorde**)

- Per proces precies één `PROCESS.md`, **in git**.
- Aanbevolen pad: `docs/processes/<procesnaam>/PROCESS.md`

**`PROCESS.md` is de canonieke bron voor uitvoervolgorde.** Dit voorkomt “random” story-volgordes door agents/LLM’s.

Minimaal verplichte inhoud:

1) **Execution mode (default = sequentieel)**
```md
execution_mode: sequential   # default
# only switch to: waves
```

2) **Baseline**
- baseline branch + commit SHA/tag waar het proces op start.

3) **Canonical Story Order (verplicht)**
Een genummerde, bindende lijst. Deze lijst is de **enige** waarheid voor sequentiële uitvoering.

```md
## Canonical Story Order (Sequential Default)
1. OPS-001 — <titel>
2. OPS-002 — <titel>
3. OPS-003 — <titel>
```

4) **Dependencies (verplicht, maar compact)**
Per story minimaal:
- `depends_on: [...]`
- korte reden (1 regel)

Voorbeeld:
```md
- OPS-003
  - depends_on: [OPS-001, OPS-002]
  - reason: needs scaffolding + harness
```

5) **QA gates**
- wat “groen” betekent (commands / scripts).

6) **Integratie-target**
- welke branch gaat uiteindelijk naar `main`/release.

7) **Rollback afspraken**
- hoe te revert’en + minimaal 1 command.

8) **Parallel waves (alleen als `execution_mode: waves`)**
Alleen opnemen wanneer je expliciet parallel wil ontwikkelen.

Vereist:
- `WAVE_BASE_SHA: <sha>` (vast vertrekpunt voor de wave)
- wave-indeling + **sequentiële merge-volgorde** in `main-merge`
- expliciet: merges blijven sequentieel, development kan parallel

```md
## Parallel Waves (Optional — only when enabled)
WAVE_BASE_SHA: <sha>
Wave 1: [OPS-002, OPS-003]
Wave 2: [OPS-004]
Merge order: OPS-002 -> OPS-003 -> OPS-004
```

**Hard rule:** als `execution_mode: sequential`, dan is de wave-sectie **niet van toepassing**.

### 3.2 Story file (verplicht)
- Per story precies één `.md`, **in git**.
- Aanbevolen: `stories/<procesnaam>/<STORY_ID>.md`
- Inhoud (minimaal):
  - user story + beschrijving
  - scope / out-of-scope (+ “no broad refactors” hard rule)
  - acceptance criteria (AC’s) met **exact 1 verification command per AC** + expected output/exit/result
  - **Touched paths allowlist** (repo-relatief, exact; zie 3.3)
  - dependencies (prerequisites)
  - test plan (targeted) + gate-commands
  - bewijs (commands + relevante output)
  - rollback plan
  - status: `drafted` of `ready-for-dev`

### 3.3 Touched paths allowlist (standaard, hard bij waves)
- Elke story bevat een sectie **Touched paths allowlist** met repo-relatieve paden/prefixes.
- Verificatie-eis (mechanisch):
  - `git diff --name-only <BASE_REF>...HEAD` moet **subset** zijn van de allowlist.
- Als een story buiten allowlist moet wijzigen:
  - story aanpassen (scope expliciet) of opsplitsen in extra story.

---

## 4) Code guardrails (hard)

Default (tenzij repo-root `AGENTS.md` anders zegt):

- **Python runtime-code (`*.py`)**
  - Max **250 regels** per gewijzigde/nieuwe `.py` (excl. lege regels).
  - Max **15 functies/methods** per gewijzigde/nieuwe `.py` (strict).
  - Bij limiet in zicht: vroegtijdig splitsen in modules.

- **Niet-runtime / niet-Python** (`.md`, `.yml`, `.json`, `.lock`, generated)
  - Geen harde line-limit, maar: reviewbaar houden en logisch splitsen.
  - Geen mega-wiring files met eindeloze registratielijsten: splits per domein/feature.

- **No broad refactors (hard)**
  - Geen repo-wide format/cleanup.
  - Geen import-sweeps buiten touched paths.
  - Geen refactors tenzij expliciet in scope.

---

## 5) Security guardrails (hard)

- Nooit secrets in git (ook niet “tijdelijk”).
- Geen plaintext wachtwoorden in configs.
- Secrets via env / OS keychain / password manager CLI.
- **Fail-closed:** ontbrekende/placeholder secrets => expliciete fout (geen stil “success”).

---

## 6) QA / tooling baseline (default)

- `pytest` (targeted tests voor gewijzigde paden)
- `ruff check` + `ruff format --check` (waar van toepassing)
- typechecks (mypy/pyright afhankelijk van repo)
- pre-commit gates waar mogelijk

Regel: geen “fake green” (geen thresholds verlagen, geen `skip/xfail` om groen te forceren).

---

## 6.9 Deterministische story-output (hard)

Regels voor story-generatie én execution:

- Story’s worden **uitgegeven** in exact dezelfde volgorde als `PROCESS.md` → *Canonical Story Order*.
- Sequentiële runner voert story’s uit in exact die volgorde; **geen heuristiek** en geen eigen “optimalisatie”.
- Er bestaan geen “extra” stories buiten de canonieke lijst (tenzij `execution_mode: waves` en ze expliciet in waves staan).

Mechanisch te linten:
- `PROCESS.md` bevat *Canonical Story Order*.
- Voor elke entry bestaat precies één bestand: `stories/<procesnaam>/<STORY_ID>.md`.
- Geen storyfiles buiten de canonieke lijst (strict).
- Story-ID’s zijn genummerd (`OPS-001` etc.); sorteerbaarheid is verplicht.

## 7) Definition of Done (per story)

Een story is “done” als:
- AC’s groen zijn via hun **verification commands**
- tests/lint/format/typechecks voor het gewijzigde pad groen zijn
- fail-closed gedrag klopt (geen stil succes)
- story is geïntegreerd naar de integratie-branch via `main-merge`
- `git diff --name-only <BASE_REF>...HEAD` (of wave-base) voldoet aan allowlist

---

## 8) Auto-merge (jouw sequentiële runner)

In jouw setup worden stories sequentieel uitgevoerd en aan het einde automatisch gemerged naar:
- `worktrees/<procesnaam>/main-merge/` (branch `<procesnaam>`)

Guardrails voor dit gedrag:
- merges gebeuren **alleen** naar de integratie-branch `<procesnaam>`
- de runner merge’t **sequentieel** (één story tegelijk)
- na elke merge worden gates/commands gedraaid; bij failure stopt de keten (fail-closed)
- **geen hotfixes direct op `<procesnaam>`** buiten de story-branches (fix via story, dan opnieuw mergen)

---

## 9) Preflight: worktree context check + lockdown (PowerShell)

Doel: voorkomen dat je (of een agent) per ongeluk in de verkeerde worktree/branch/origin werkt of pusht.

Belangrijk (tegen baseline drift):
- Run dit script **per story**.
- Laat `$STORY_ID` leeg om alleen de integratie-worktree te maken/locken.
- Zet `$STORY_ID` alleen voor de **story die je nu start**. Niet vooruit aanmaken.

Copy/paste (Windows PowerShell) — vul deze 4 in:
- `$REPO` (repo root)
- `$PROCESS` (procesnaam)
- `$STORY_ID` (bijv. `OPS-001`, of leeg)
- `$ORIGIN` (exacte `git remote get-url origin`)

```powershell
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# REQUIRED INPUTS
$REPO     = "C:\path\to\repo"
$PROCESS  = "dashboard_enterprise_grade"
$STORY_ID = ""          # e.g. "OPS-001" (leave empty to only ensure integration worktree)
$ORIGIN   = "https://github.com/org/repo.git"

function Normalize-WinPath([string]$p) {
  if (-not $p) { return $p }
  $x = $p.Trim() -replace '/', '\'
  try { $x = [System.IO.Path]::GetFullPath($x) } catch { }
  return $x.TrimEnd('\')
}

function Assert-RepoContext([string]$Path, [string]$ExpectedOrigin) {
  $top = (git -C $Path rev-parse --show-toplevel).Trim()
  $origin = (git -C $Path remote get-url origin).Trim()
  $branch = (git -C $Path branch --show-current).Trim()
  $head = (git -C $Path rev-parse --short HEAD).Trim()
  $dirty = (git -C $Path status --porcelain).Length
  "CTX: top=$top branch=$branch head=$head origin=$origin dirty=$dirty"

  if ((Normalize-WinPath $top).ToLowerInvariant() -ne (Normalize-WinPath $Path).ToLowerInvariant()) {
    throw "WRONG TOPLEVEL: expected=$Path got=$top"
  }
  if ($ExpectedOrigin -and $origin -ne $ExpectedOrigin) {
    throw "WRONG ORIGIN: expected=$ExpectedOrigin got=$origin"
  }
}

function Ensure-Worktree([string]$Repo, [string]$WorktreePath, [string]$Branch, [string]$StartPoint) {
  if (Test-Path $WorktreePath) {
    git -C $WorktreePath rev-parse --is-inside-work-tree 1>$null 2>$null
    if ($LASTEXITCODE -ne 0) { throw "DESTRUCTIVE RISK: path exists but is not a git worktree: $WorktreePath" }
    return
  }

  # Safety: never force-move an existing branch pointer.
  $branchRef = "refs/heads/$Branch"
  git -C $Repo show-ref --verify --quiet $branchRef
  $branchExists = ($LASTEXITCODE -eq 0)

  $sp = (git -C $Repo rev-parse $StartPoint).Trim()
  if ($LASTEXITCODE -ne 0 -or -not $sp) { throw "INVALID STARTPOINT: $StartPoint" }

  if ($branchExists) {
    git -C $Repo merge-base --is-ancestor $StartPoint $Branch
    if ($LASTEXITCODE -eq 1) {
      "WARN: startpoint is not an ancestor of branch (baseline drift or divergence): branch=$Branch startpoint=$StartPoint"
    } elseif ($LASTEXITCODE -ne 0) {
      throw "FAILED ANCESTOR CHECK: branch=$Branch startpoint=$StartPoint"
    }
  }

  New-Item -ItemType Directory -Force (Split-Path -Parent $WorktreePath) | Out-Null
  if ($branchExists) {
    git -C $Repo worktree add $WorktreePath $Branch
  } else {
    git -C $Repo worktree add -b $Branch $WorktreePath $StartPoint
  }
  if ($LASTEXITCODE -ne 0) { throw "FAILED WORKTREE ADD: path=$WorktreePath branch=$Branch" }
}

function Ensure-SharedVenvProvision([string]$Repo, [string]$WorktreePath) {
  # Worktrees only contain git-tracked files; .venv is usually gitignored. To avoid dependency drift,
  # provision .venv into each worktree from the PC repo root.
  $source = Join-Path $Repo ".venv"
  if (-not (Test-Path -LiteralPath $source -PathType Container)) { return }

  $target = Join-Path $WorktreePath ".venv"
  if (Test-Path -LiteralPath $target) { return }

  try {
    New-Item -ItemType Junction -Path $target -Target $source -ErrorAction Stop | Out-Null
    return
  } catch {
    # Fallback: physical copy if junctions are blocked by policy.
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    & robocopy $source $target /MIR /NFL /NDL /NJH /NJS /NP /R:2 /W:1 | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "FAILED VENV COPY: robocopy exitcode=$LASTEXITCODE" }
  }
}

function Set-WorktreeLockdown([string]$WorktreePath, [string]$ExpectedBranch, [string]$ExpectedOrigin) {
  $gitDir = (git -C $WorktreePath rev-parse --path-format=absolute --git-dir).Trim() -replace '/', '\'
  $hooksDir = Join-Path $gitDir "hooks"
  New-Item -ItemType Directory -Force $hooksDir | Out-Null

  if (Test-Path (Join-Path $WorktreePath ".githooks")) {
    throw "DESTRUCTIVE RISK: .githooks exists in working tree (must not be committable)."
  }

  $hook = @"
#!/bin/sh
set -eu
EXPECTED_BRANCH="$ExpectedBranch"
EXPECTED_ORIGIN="$ExpectedOrigin"
branch="$(git branch --show-current)"
origin="$(git remote get-url origin)"
[ "$branch" = "$EXPECTED_BRANCH" ] || { echo "ERROR: wrong branch: $branch" >&2; exit 1; }
[ "$origin" = "$EXPECTED_ORIGIN" ] || { echo "ERROR: wrong origin: $origin" >&2; exit 1; }
"@

  Set-Content -NoNewline -Encoding ASCII (Join-Path $hooksDir "pre-commit") $hook
  Set-Content -NoNewline -Encoding ASCII (Join-Path $hooksDir "pre-push")   $hook

  git -C $WorktreePath config --worktree core.hooksPath $hooksDir
}

Assert-RepoContext -Path $REPO -ExpectedOrigin $ORIGIN
git -C $REPO fetch origin --prune
git -C $REPO config --local extensions.worktreeConfig true

$WT_BASE  = Join-Path $REPO ("worktrees\" + $PROCESS)
$WT_INTEG = Join-Path $WT_BASE "main-merge"

# Integration worktree: branch = <procesnaam>, startpoint = origin/main (override if needed)
Ensure-Worktree -Repo $REPO -WorktreePath $WT_INTEG -Branch $PROCESS -StartPoint "origin/main"
Ensure-SharedVenvProvision -Repo $REPO -WorktreePath $WT_INTEG
Set-WorktreeLockdown -WorktreePath $WT_INTEG -ExpectedBranch $PROCESS -ExpectedOrigin $ORIGIN

if ($STORY_ID -and $STORY_ID.Trim()) {
  $WT_STORY = Join-Path $WT_BASE $STORY_ID
  $storyBranch = "$PROCESS-$STORY_ID"

  # Story worktree: branch = <procesnaam>-<STORY_ID>, startpoint = <procesnaam>
  Ensure-Worktree -Repo $REPO -WorktreePath $WT_STORY -Branch $storyBranch -StartPoint $PROCESS
  Ensure-SharedVenvProvision -Repo $REPO -WorktreePath $WT_STORY
  Set-WorktreeLockdown -WorktreePath $WT_STORY -ExpectedBranch $storyBranch -ExpectedOrigin $ORIGIN
} else {
  "INFO: STORY_ID is empty; only ensured integration worktree."
}
```

---

## 10) Uitvoeringsflow (per story, sequentieel)

1) Proces starten
- Maak integratie-branch `<procesnaam>` vanaf baseline (meestal `main`).
- Check uit in `worktrees/<procesnaam>/main-merge/`.

2) Story worktree maken (just-in-time)
- Maak branch `<procesnaam>-<STORY_ID>` pas als je die story start.
- Base op actuele integratie-branch `<procesnaam>` (na eerdere merges).
- Worktree: `worktrees/<procesnaam>/<STORY_ID>/`.

3) Implementeren
- Werk uitsluitend in story-worktree.
- Scope strikt: touched paths en no broad refactors.

4) Verifiëren (repo-root, tenzij expliciet anders)
- Draai story verification commands per AC.
- Draai repo gates voor gewijzigde paden.
- Zorg dat `python` in worktrees de repo-venv pakt (prepend `<worktree>\.venv\Scripts` aan `PATH` of run expliciet `<worktree>\.venv\Scripts\python.exe`).

5) Integreren
- Automatisch of handmatig: merge naar `<procesnaam>` gebeurt via `main-merge`.
- Conflicten los je in `main-merge` op.

6) Herhalen
- Volgende story pas starten als prerequisites duidelijk zijn.

---

## 11) Parallel waves (optioneel, zero-guesswork)

Belangrijk: jouw auto-merge werkt fijn bij sequentieel. **Bij parallel** is auto-merge zonder lock een liability (race conditions + baseline drift).
Daarom geldt:

- Parallel *development* mag, maar **integratie/merge blijft sequentieel** in `main-merge`.
- Runner/merge-stap moet een **exclusieve lock** nemen op integratie (mutex/file lock) vóór merge.
- Zonder lock: waves niet gebruiken (fail-closed).


Default = sequentieel. Parallel alleen als deterministisch te bewijzen; bij twijfel: niet parallel (fail-closed).

Voorwaarden:
- `PROCESS.md` bevat wave-plan + merge-volgorde + vast `WAVE_BASE_SHA`.
- Elke story in wave heeft touched paths allowlist.
- Allowlists in dezelfde wave zijn pairwise disjoint (geen overlap).
- Alle story-branches starten vanaf `<procesnaam>` op `WAVE_BASE_SHA`.

Verificatie (per story):
- `git diff --name-only <WAVE_BASE_SHA>...HEAD` is subset van allowlist.

Integratie:
- Ook bij parallel development: merges naar `<procesnaam>` gebeuren sequentieel in `main-merge`, exact volgens `PROCESS.md`.
- Na elke merge: gates draaien; bij failure: stop, fix via relevante story branch, opnieuw mergen.

---

## 12) Eind-integratie (pas als alles groen is)

- Als alle stories in `main-merge` zitten en alles groen is:
  - merge `<procesnaam>` -> target (release branch/worktree)
  - daarna pas (alleen na GO) merge target -> `main`/release

---

## 13) MVP-principe (scope discipline)

- Eerst maximale waarde met minimale complexiteit.
- High-friction integraties pas v2 (adapter-ready mag, geen scope creep).
