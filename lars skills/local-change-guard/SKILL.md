---
name: local-change-guard
# prettier-ignore
description: Directe feature-edits in de huidige working tree zonder aparte worktree of plan-to-bmad. Gebruik dit wanneer je lokaal snelheid wilt, maar wel hard non-test files <=300 regels, <=15 functies/methods en repo CTO-guardrails wilt afdwingen.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
---

# Local Change Guard

> **Doel**: Werk direct in de huidige working tree, **zonder** aparte worktree en **zonder** plan-to-bmad overhead, maar **wel** met harde structurele limits en CTO-governance.

## Wanneer gebruiken

**Wel:**
- bestaande feature aanpassen in de huidige working tree
- user wil expliciet **geen** aparte worktree
- user wil expliciet **geen** plan-to-bmad route
- de wijziging is groter dan een pure copy/CSS tweak en je wilt harde structurele bewaking
- je wilt rechtstreeks kunnen zeggen: "doe deze change lokaal, maar houd de repo-shape strak"

**Typische triggers in user-taal:**
- "pas dit direct aan zonder worktree"
- "geen BMAD planfile hiervoor"
- "werk gewoon in deze tree maar houd 300/15 vast"
- "ik wil wel guardrails, niet de volle ceremony"

## Niet gebruiken

Gebruik deze skill **niet** als één van deze dingen geldt:
- nieuwe exception in `docs/FILE_LIMITS_EXCEPTIONS.md` nodig
- auth / infra / migrations / nieuwe externe contracten
- scope is onduidelijk of groeit tijdens het werk
- brede refactor over meerdere subsystemen
- je kunt niet hard bewijzen dat touched non-test files binnen 300 regels / 15 defs blijven

Dan: **escaleren naar** `/plan-to-bmad` + `/bmad-bundle` of `/bmad-codex`.

## 10/10-kader voor local changes

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Local-specifiek: geen plan-ceremonie, maar wél budgets, gates en bewijs.

## Hard rules

1. **Geen aparte worktree / geen BMAD input files**
   - werk in de huidige tree
   - geen `bmad_input/*.md`
   - geen story/worktree ceremony forceren via deze route

2. **Governance eerst lezen**
   Lees vóór codewijziging waar aanwezig:
   - repo-root `AGENTS.md`
   - `docs/CTO_RULES.md`
   - `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
   - `docs/FILE_LIMITS_EXCEPTIONS.md`
   - `docs/START_HERE.md`
   - `docs/SOURCES_OF_TRUTH.md`
   - `scripts/quality_gates.py`
   - `scripts/check_file_limits.py`
   - `scripts/check_repo_10x_contract.py`
   - relevante spec/SSOT voor businesslogica (bijv. `openspec/**`)

3. **Local Change Brief is verplicht vóór edit**
   Leg eerst vast:
   - doel in 1 zin
   - touched paths allowlist
   - out-of-scope
   - relevante CTO Rules
   - relevante Universal CTO facetten
   - verificatiecommands
   - **file budget table** per touched non-test file

4. **Numerieke file budgets zijn verplicht, niet optioneel**
   - noteer per touched non-test file de **huidige** lines en defs/methods met bewijs uit een repo-script of AST-check
   - noteer per file ook het **target after change**
   - **geen edit starten** voordat deze cijfers zijn vastgelegd
   - als het target niet hard binnen `<=300 lines` en `<=15 defs` blijft: eerst splitsen of escaleren

5. **File limits zijn hard en preventief**
   - non-test files: **max 300 regels**
   - non-test files: **max 15 functies/methods**
   - check dit **vóór** de edit en **na** de edit
   - als een file al dicht bij de limiet zit: **split eerst**, pas daarna feature toevoegen

6. **Legacy offenders mogen niet groeien**
   Als een touched file al in `docs/FILE_LIMITS_EXCEPTIONS.md` staat:
   - lines/defs na jouw wijziging mogen **niet hoger** uitkomen dan ervoor
   - voorkeur: code eruit trekken zodat de file kleiner wordt
   - **geen nieuwe exception entry toevoegen** in deze route

7. **CTO delta review blijft verplicht**
   Voor afronding moet je de diff langs deze lens nalopen:
   - relevante regels uit `docs/CTO_RULES.md`
   - relevante Universal CTO facetten
   - repo-native gates
   - UNKNOWNs expliciet fail-closed benoemen

8. **Primary gate blijft leidend**
   - als `docs/START_HERE.md` of `docs/SOURCES_OF_TRUTH.md` een canoniek gates-commando noemt, gebruik exact dat commando
   - als deze repo `uv run python scripts/quality_gates.py` als one true command hanteert: gebruik exact dat
   - run daarnaast de kleinste relevante lint/test/build checks voor het gewijzigde runtime-pad

9. **Escalate vroeg**
   Escaleer zodra één van deze dingen waar wordt:
   - je moet een file-limit exception toevoegen of verruimen
   - je touched paths allowlist breekt open
   - de wijziging dwingt tot architectuurkeuze/spec-uitzoekwerk
   - je kunt geen sluitende CTO/file-limit bewijsvoering meer geven
10. **Verboden woorden zonder bewijs**: `done`, `fixed`, `working`, `correct`, `passed`, `verified` zijn verboden in rapportage/commit tenzij runtime-bewijs aanwezig is.
11. **Probe-before-block**
   Voordat je claimt dat tools/env stuk zijn: draai 3 probes (no-op, target tool, task-level). Als één slaagt, is "tools kapot" geen geldige blocker.
11. **Universele guards gelden** — lees `~/.pi/agent/skills/_guards.md` en pas alle guards toe.

## Workflow

1. **Inspecteer repo-governance en bestaande patterns**
   - lees relevante docs/scripts/specs
   - inspecteer de files die je vermoedelijk raakt
   - voor refactors, renames of moves in codebases met 50+ files: gebruik Serena (`/skill:serena`) voor symbol lookup en referenties in plaats van handmatig grep+edit. Check `tmux has-session -t serena` eerst; start server als nodig.

2. **Maak een Local Change Brief**
   Gebruik `knowledge/local-change-brief-template.md`.
   Voeg expliciet toe:
   - het concrete **doelbeeld na wijziging**
   - wat expliciet **niet** geraakt wordt
   - waarom dit géén luie cleanup-route is

3. **Bepaal file budgets vóór code**
   Per touched non-test file noteer je minimaal:
   - huidige lines
   - huidige defs/methods
   - verwachte richting na wijziging
   - split/extract-strategie als budget krap is

4. **Implementeer de kleinste nette wijziging**
   - split voordat je groeit
   - liever 1 nieuwe kleine helper/module dan 1 bestaande file opblazen
   - behoud SSOT- en spec-traceability

5. **Draai post-change verificatie**
   Minimaal:
   - primary quality gate
   - file-limit gate (als aanwezig)
   - kleinste relevante targeted tests/lint/build

6. **Voer CTO delta review uit**
   Rapporteer kort:
   - welke CTO Rules zijn geraakt
   - welke Universal facetten relevant waren
   - welk bewijs je hebt (`path:line` of commando-uitkomst)
   - welke UNKNOWNs er nog zijn, met exact 1 next check

7. **Rond alleen af als alles hard bewijsbaar is**
   Geen "klaar" zonder:
   - file budgets gehaald
   - gates uitgevoerd
   - diff tegen CTO rules nagekeken
   - geen nieuwe exception nodig
   - bewijs is echt bewijs: code-presence (grep) is geen geldig bewijs voor runtime-gedrag. Runtime claims vereisen runtime proof (e2e, API calls, logs, screenshots).
   - als de change een breder probleem moest fixen: check of het HELE probleem is opgelost, niet alleen het smalle stuk dat je hebt aangeraakt.

## Praktische budget-check

Als de repo al een eigen `scripts/check_file_limits.py` heeft: gebruik die als primaire shape-check.

Als je eerst per touched file een snelle budgetmeting nodig hebt, gebruik een kleine AST-check in bash/python voor alleen de betrokken paden. Geen regex-tellen voor defs als AST mogelijk is.

## Wat géén geldig stopmoment of succesclaim is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Local-specifiek:

- een diff binnen budget maar zonder relevante gate/test-uitkomst
- "klaar" zeggen terwijl escalatie eigenlijk nodig was

## Output in chat

Eindrapport is kort en hard:
- wat gewijzigd is
- welke files binnen budget zijn gebleven
- welke gates/checks zijn gedraaid
- CTO delta verdict: `COMPLIANT`, `CONDITIONAL`, of `NON-COMPLIANT`
- of je bewust **niet** hoefde te escaleren naar full BMAD
