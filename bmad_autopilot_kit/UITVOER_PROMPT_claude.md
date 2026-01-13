Je bent Claude Code. Spreek Nederlands. Werk non-interactive: geen A/B/C menu's, kies de beste aanpak en voer uit. Stel alleen vragen als essentiele requirements ontbreken of als een actie onomkeerbaar/destructief is; anders fail-closed met een duidelijke foutmelding.

CONFIGURATIE (VERPLICHT - pas aan voor je plakt)
- BMAD_INPUT_FILE: <VUL IN>
  (VERPLICHT: vul pad in zoals: docs/mijn_project_input.md - leeg = STOP fail-closed)

DOEL
- Deze repo runner-ready maken en de autopilot starten:
  1) RUN1: BMAD stories genereren (deterministisch sequentieel).
  2) Preflight: story output linten en repareren tot groen.
  3) RUN2: Stories 1-voor-1 uitvoeren in eigen worktree, testen, merge naar main-merge.

HARD RULES
- Volg repo guardrails:
  - Lees `./CLAUDE.md` en volg die.
  - Volg `AI_STACK_STANDARD_BMAD_WORKTREES_GUARDRAILS seq force_claude.md` (deze map bevat een kopie; plaats hem in de repo-root als hij daar nog niet staat).
- **LEES EERST `openspec/specs/bmad-autopilot.md`** - dit is de single source of truth voor hoe de autopilot werkt.
- Volg het story-format contract: `docs/CONTRACT.md` (ontbreekt => STOP fail-closed; geen gokken).
- Geen broad refactors; blijf binnen story allowlist.
- Geen merge naar `main` - alleen naar `main-merge` worktree.
- Gebruik altijd `claude --dangerously-skip-permissions -p` voor prompt execution (niet optioneel; niet uitzetbaar binnen deze kit).
- **NOOIT nieuwe tooling genereren als er al werkende versies bestaan. Check EERST `tools/` voordat je iets maakt.**

MAAK EERST EEN PLAN
- Maak een kort plan (max 6 stappen) en werk het stap voor stap af. Vink af wat klaar is.

STAP 0 - Validatie (fail-closed)
- Je werkt in de repo-root van een git repo (controleer met `git rev-parse --show-toplevel`).
- Deze kit map bestaat in de repo-root: `./bmad_autopilot_kit_claude/`
- Het contract moet bestaan in `docs/CONTRACT.md` (single source of truth voor story-format).
  - Als `docs/CONTRACT.md` ontbreekt: kopieer `./bmad_autopilot_kit_claude/docs_claude/CONTRACT_claude.md` naar `docs/CONTRACT.md` (niet overschrijven).
  - Als bron ook ontbreekt => STOP fail-closed (geen gokken)

STAP 1 - Plaats de "seq force" docs in de repo-root (niet overschrijven)
- Als deze bestanden nog NIET bestaan in de repo-root, kopieer ze uit `./bmad_autopilot_kit_claude/`:
  - `BMAD_STORY_LLM_PLAYBOOK  Seq force_claude.md`
  - `AI_STACK_STANDARD_BMAD_WORKTREES_GUARDRAILS seq force_claude.md`

STAP 2 - Bepaal `Process` deterministisch (HARD, geen vragen)
HARD REGEL (geen auto-detect, geen alternatieven):
- `BMAD_INPUT_FILE` is VERPLICHT (zie CONFIGURATIE). Als leeg of bestand bestaat niet → STOP fail-closed.
- `Process = slug(basename(BMAD_INPUT_FILE))` met exact deze definitie:
  - `basename(path)` = bestandsnaam zonder extensie
  - `slug(name)`:
    1) lower-case
    2) elk niet-alfanumeriek karakter (`[^a-z0-9]`) → `_`
    3) meerdere `_` achter elkaar → één `_`
    4) trim `_` aan begin/eind
- Alle output paden zijn gebaseerd op `Process`:
  - Stories: `stories_claude/<Process>/OPS-001.md`, `OPS-002.md`, …
  - Worktrees root: `worktrees_claude/<Process>/`
  - Integratie-worktree: `worktrees_claude/<Process>/main-merge`
  - Story-worktree: `worktrees_claude/<Process>/<STORY_ID>`

STAP 3 - RUN1: genereer stories (sequentieel, deterministisch)
- Voer de instructies uit uit: `./bmad_autopilot_kit_claude/RUN1_STORY_GENERATION_PROMPT_claude.txt`
- Belangrijk:
  - Input file: gebruik `BMAD_INPUT_FILE` uit CONFIGURATIE (geen auto-detect, geen fallbacks)
  - Als bestand niet bestaat → STOP fail-closed
  - Output gaat naar `stories_claude/<Process>/OPS-001.md`, `OPS-002.md`, ... (waar `Process` is bepaald in STAP 2)

STAP 4 - Preflight: maak RUN1 output runner-proof (itereren tot groen)
- Run:
  - `pwsh ./bmad_autopilot_kit_claude/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1 -RepoRoot "<repo-root>" -Process "<Process>"`
- Als preflight faalt:
  - Repareer de story markdowns (markers/allowlist/status/canonical order) of rerun RUN1, totdat preflight groen is.
  - Blijf bij docs/stories; geen runtime-code wijzigingen in deze stap.

STAP 5 - RUN2: Voer stories 1-voor-1 uit in eigen worktree
Voor elke story (OPS-001, OPS-002, ...) in canonieke volgorde:

**BELANGRIJK: SEQUENTIËLE UITVOERING**
- Stories MOETEN één voor één worden uitgevoerd
- Elke nieuwe worktree MOET gebaseerd zijn op de BIJGEWERKTE main-merge (na merge van vorige story)
- NOOIT alle worktrees vooraf aanmaken - dan missen latere stories de wijzigingen van eerdere stories
- Dit voorkomt merge conflicts en zorgt dat elke story voortbouwt op de vorige

a) **Maak worktree** (ALLEEN als vorige story gemerged is):
   ```bash
   # Voor eerste story (OPS-001): base is main branch
   git worktree add worktrees_claude/<Process>/main-merge -b <process>-fixes main
   git worktree add worktrees_claude/<Process>/OPS-001 -b story/OPS-001 main

   # Voor volgende stories: base is main-merge branch (bevat alle vorige merges)
   git worktree add worktrees_claude/<Process>/<STORY_ID> -b story/<STORY_ID> <process>-fixes
   ```

b) **Start nieuwe Claude sessie** in de worktree:
   ```bash
   cd worktrees_claude/<Process>/<STORY_ID>
   claude --dangerously-skip-permissions -p "Voer story <STORY_ID> uit. Story bestand: stories_claude/<Process>/<STORY_ID>.md"
   ```

c) **Agent in worktree doet**:
   - Leest CLAUDE.md (eerste taak in story)
   - Voert alle story taken uit
   - Runt `pytest` (laatste taak in story)
   - Als tests NIET groen: STOP fail-closed (geen merge)

d) **Als tests groen - merge naar main-merge**:
   ```bash
   cd worktrees_claude/<Process>/main-merge
   git merge story/<STORY_ID> --no-edit
   ```

e) **Ga door naar volgende story**

STAP 6 - Cleanup (optioneel)
- Worktrees kunnen blijven staan voor debugging
- Of verwijderen met: `git worktree remove worktrees_claude/<Process>/<STORY_ID>`

EINDRESULTAAT
- Stories staan in `stories_claude/<Process>/OPS-001.md`, `OPS-002.md`, ...
- Alle stories zijn uitgevoerd met groene tests
- Alle stories zijn gemerged naar `worktrees_claude/<Process>/main-merge`
- Klaar voor review en eventuele merge naar main (met expliciete GO)
