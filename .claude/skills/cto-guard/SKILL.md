---
name: cto-guard
# prettier-ignore
description: Voer een volledige Universal CTO Review v2.5 uit op repo, diff, story of plan; combineert CTO registry, universal scan en het volledige repo-10x contract in één review.
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# CTO Guard

## Doel

`/skill:cto-guard` is de **uitvoerbare master-skill** voor de **volledige Universal CTO Review v2.5** **plus** het **volledige repo-10x contract** **plus** een verplichte **plan-to-BMAD handoff** wanneer er unresolved gaps zijn.

Gebruik deze skill om werk te reviewen tegen:
- `docs/CTO_RULES.md` (rule registry)
- `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` (repo-local kopie, als aanwezig)
- **canonieke Universal prompt fallback:** `/home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack/docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
- het volledige repo-10x contract A-I zoals uitgewerkt in `repo-10x-audit-to-bmad`
- repo-10x guardrails/scripts (`scripts/check_repo_10x_contract.py`, `scripts/quality_gates.py`, search/SSOT contracten)
- de `plan-to-bmad` workflow voor de opvolg-input

Deze skill mag **niet** terugvallen naar een korte compliance-samenvatting zonder facet scores, P1/P2/P3, Path to 10/10, BMAD follow-up en een korte Jip-en-Janneke TL;DR in chat.

## Wanneer gebruiken

- `/skill:cto-guard` voor een volledige CTO review
- op een repo / working tree / diff / story / plan
- vóór BMAD-generatie
- na story-generatie
- na uitvoering / vóór merge
- wanneer een change inhoudelijk groen lijkt maar je een CTO-level oordeel wilt

## Input

Geef aan wat je wilt reviewen:
- een repo of working tree
- een code diff (`git diff`, staged diff, PR delta)
- een story file
- een plan document
- een combinatie daarvan

## 10/10-kader voor CTO review

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Review-specifieke aanvullingen:

- facet scores, repo-10x contract, canonical gaps en Path to 10/10 vormen samen één geheel
- de TL;DR versimpelt de uitkomst, maar verslapt de inhoud niet
- een review die repo-10x of UNKNOWNs wegpoetst om sneller op COMPLIANT te landen is ongeldig

## Hard rules

1. **Volledige Universal CTO Review v2.5 is verplicht**
   - volg inhoudelijk **precies** het scan-contract uit `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
   - als die file in de repo ontbreekt, gebruik exact deze canonieke fallback: `/home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack/docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
   - gebruik de rijke rapportstructuur uit `knowledge/output-format.md`
   - geen afgeslankte verdict-only output
2. **Lees de Universal prompt volledig**
   - eerst repo-local `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` als aanwezig
   - anders de canonieke fallback file hierboven
3. **Lees `docs/CTO_RULES.md` volledig** als die bestaat en valideer parsebaarheid met `python3 scripts/validate_cto_rules_registry.py` als dat script bestaat
4. **Lees het repo-10x contract volledig**
   - lees `/home/mrbiggles/.pi/agent/skills/repo-10x-audit-to-bmad/SKILL.md`
   - gebruik de A-I contractdelen inhoudelijk, niet alleen de scripts
5. **Volledige repo-10x contractscan is verplicht**
   - behandel repo-10x niet als losse extra review maar als **verplicht onderdeel van deze CTO review**
   - laad inhoudelijk het contract uit `repo-10x-audit-to-bmad/SKILL.md` en beoordeel expliciet A t/m I
   - run `python3 scripts/check_repo_10x_contract.py` als die bestaat
   - run `python3 scripts/quality_gates.py` als die bestaat en de review om runtime/codekwaliteit draait
   - als een repo-10x script ontbreekt: beoordeel het contract alsnog handmatig met bewijs
   - `COMPLIANT` of `10/10` is niet toegestaan zolang er unresolved repo-10x FAILs/UNKNOWNs zijn die de repo-shape, gates, searchability of maintainability blokkeren
6. **P1/P2/P3 expliciet**
   - P3 mag nooit verdwijnen uit het eindrapport
7. **UNKNOWN fail-closed**
   - als iets niet hard bewijsbaar is: markeer `UNKNOWN` + exact 1 verificatie-check
8. **Evidence op elke claim**
   - `path:line` of `command + relevante output`
9. **Post-review BMAD is standaard verplicht**
   - tenzij de gebruiker expliciet `review-only` zegt
   - bij unresolved gaps moet direct daarna een `plan-to-bmad`-compatibele BMAD input (`.md` + `.json`) worden gemaakt in een unieke `main-merge` worktree
10. **Chat-TL;DR is verplicht**
   - geef na het volledige rapport een korte Jip-en-Janneke samenvatting
   - noem daarin de totaalscore en de cijfers per facet
11. **Universele guards gelden** — lees `~/.pi/agent/skills/_guards.md` en pas alle guards toe op de review en BMAD follow-up.

## Autonomous state machine (Pi contract)

Treat `/skill:cto-guard` as a deterministic review state machine.

### States

1. **TARGET_SCOPE**
   - Determine exact review target and scope.
   - Success -> `LOAD_SOURCES`
   - Failure -> `BLOCKED`

2. **LOAD_SOURCES**
   - Read CTO registry, Universal prompt, repo-10x contract, and repo sources of truth.
   - Success -> `UNIVERSAL_SCAN`
   - Failure -> `BLOCKED`

3. **UNIVERSAL_SCAN**
   - Execute the full Universal CTO scan in the documented order.
   - For large codebases (50+ files): use Serena (`/skill:serena`) for symbol-level architecture analysis and dependency tracing. Check `tmux has-session -t serena` first; start server if needed.
   - Success -> `REPO_10X_SCAN`

4. **REPO_10X_SCAN**
   - **If `scripts/check_repo_health.py` exists: run it as part of evidence collection.** Include PASS/WARN/FAIL output in the report as deterministic baseline. Health check results are ground truth for measurable facets — do not contradict them with ad-hoc checks.
   - Execute explicit A-I repo-10x assessment and script-backed checks where available.
   - Success -> `CONSOLIDATE_VERDICT`

5. **CONSOLIDATE_VERDICT**
   - Produce canonical gaps, facet scores, action plan, and Path to 10/10.
   - Hard rule: reject lazy closure paths and convert them into a smaller set of high-leverage moves.
   - Hard rule: when reviewing stories or a completed run, flag any AC that is narrower than the facet it claims to address. "AC groen ≠ facet opgelost." If a story claimed to fix naming consistency but the AC only checked 5 of 21 violations, score the facet based on the full reality, not the narrow AC.
   - Hard rule: flag any AC verification that uses code-presence (grep/rg) as proof for a runtime-behavior claim. That is not valid evidence.
   - Success -> `WRITE_REPORT`

6. **EXECUTION_HONESTY_SCAN**
   - Scan all story outputs, final.json, screenshots, logs, test output, and status claims.
   - Flag any mismatch between claims and evidence. Specifically:
     - success claims (`done`, `fixed`, `working`, `correct`, `passed`, `verified`) without matching runtime proof → P1-CRITICAL
     - BLOCKED claims without probe evidence (3 probes: no-op, target, task) → P1-QUICK
     - incomplete verify set for runtime changes (missing e2e/screenshots) → P2
     - run stopped while backlog has executable open stories without proven global blocker → P1-CRITICAL
   - Success -> `WRITE_REPORT`

7. **WRITE_REPORT**
   - Write the full CTO review artifact.
   - Include the Execution Honesty findings as a separate section in the report.
   - Success -> `BMAD_FOLLOWUP_DECISION`
   - Failure -> `BLOCKED`

7. **BMAD_FOLLOWUP_DECISION**
   - If `review-only`: terminal review path.
   - If unresolved gaps remain: generate BMAD follow-up via plan-to-bmad contract.
   - Success -> `COMPOUND_LEARNING`
   - Failure -> `BLOCKED`

8. **COMPOUND_LEARNING**
   - Action: run `/skill:compound-learning` — extract max 5 learnings from this review and save to `LEARNINGS.md` (repo) and/or `LEARNINGS_GLOBAL.md` (global).
   - Success -> `DONE`

9. **DONE / BLOCKED**
   - Terminal states only.
   - Do not stop at a short verdict or summary-only output.

## Workflow

1. **Bepaal review target en scope**
   - repo / working tree / diff / story / plan / mixed
   - `repo_only`, `repo_plus_db`, `repo_plus_infra`, `full_stack`, of een expliciet begrensde delta-scope
2. **Laad bronregels, de canonieke Universal scan en het repo-10x contract**
   - `docs/CTO_RULES.md`
   - repo-local `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` als aanwezig
   - anders `/home/mrbiggles/dev/github.com/jongensutrecht/demo-ai-stack/docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
   - `/home/mrbiggles/.pi/agent/skills/repo-10x-audit-to-bmad/SKILL.md`
   - `docs/START_HERE.md`, `docs/SOURCES_OF_TRUTH.md`, `SECURITY.md`, `README.md`, `AGENTS.md` waar relevant
3. **Voer de Universal scan-stappen in dezelfde volgorde uit als de prompt**
   - Stap 0: repo policy, archetype, context
   - Stap 1: quick scan / census
   - Stap 1.5: deterministische scope-cap / sampling indien nodig
   - Stap 2: deep scan per facet
   - Stap 3: database scan als applicable
   - Stap 3.5: infra / deploy scan als applicable
   - Stap 4: consolidatie, canonical gaps, actieplan, Path to 10/10
4. **Voer daarna expliciet de repo-10x contractscan A-I uit binnen dezelfde review**
   - A) 1 knop bewijs (gates)
   - B) search hygiene / golden queries
   - C) repo-root allowlist / root hygiene
   - D) sources of truth expliciet
   - E) onboarding 10 minuten
   - F) secrets/artefacts/binaries policy
   - G) worktrees uitgesloten van tooling
   - H) GitHub/CI hard bewijs of `UNKNOWN`
   - I) file limits + exception policy
   - map elk FAIL-item naar canonical gaps en koppel die aan de relevante Universal facetten
5. **Verifieer repo-10x / gates**
   - `python3 scripts/check_repo_10x_contract.py` als aanwezig
   - `python3 scripts/quality_gates.py` als aanwezig
6. **Genereer het volledige rapport** volgens [knowledge/output-format.md](knowledge/output-format.md)
   - schrijf het ook naar `docs/CTO_REVIEW_<repo>.md` volgens de Universal prompt
   - als schrijven niet lukt: fail-closed met `UNKNOWN` + exact 1 write-check/commando
7. **Run post-review BMAD hook** tenzij de gebruiker `review-only` vroeg
   - trigger: er bestaan unresolved `P1-CRITICAL`, `P1-QUICK`, `P2` of `P3` gaps
   - gebruik de `plan-to-bmad` regels inhoudelijk als contract
   - maak een process slug, bijvoorbeeld `cto_guard_followup_<target>_<yyyymmdd>`
   - schrijf in een unieke `main-merge` worktree: `bmad_input/<process>.md` + `bmad_input/<process>.json`
   - mapping van review naar BMAD:
     - unresolved `P1-CRITICAL` / `P1-QUICK` -> BMAD `P0`
     - unresolved `P2` -> BMAD `P1`
     - unresolved `P3` -> BMAD `P3`
   - neem over: scope map, relevante facetten, UNKNOWN external state, gap evidence, closure DoD, Path to 10/10 richting
   - de follow-up moet expliciet bevatten:
     - `10/10 Kader` (wat hier wel / niet telt als echte closure)
     - 3-7 hoge-hefboommoves, geen micro-story spam
     - per move: doelbeeld, waarom high leverage, niet-doen, proof of done
   - commit de BMAD input als de `plan-to-bmad` workflow dat vereist
   - als schrijven niet lukt: markeer `UNKNOWN` + geef exact 1 concrete verificatie-/herstelcheck
8. **Geef een Jip-en-Janneke TL;DR in chat**
   - 3-8 bullets
   - noem overall status, overall score en de cijfers per facet
   - leg in simpele taal uit wat de grootste problemen zijn en of er een BMAD-follow-up is gemaakt

## Output

Gebruik exact het rijke Universal CTO Review-format uit:
- [knowledge/output-format.md](knowledge/output-format.md)

Minimaal verplicht in elk geldig eindrapport:
- Executive Summary
- Facet Scores Overview
- Per-facet detail
- Consolidated Gap Table
- Prioritized Action Plan
- Path to 10/10
- expliciet `Wat 10/10 hier WEL is`
- expliciet `Wat 10/10 hier NIET is`

## Wat géén geldig stopmoment is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Review-specifiek:

Stop **niet** op:
- alleen een korte compliance-samenvatting
- alleen een totaalscore zonder facetdetails
- alleen een gaplijst zonder actieplan / Path to 10/10
- een review met unresolved gaps zonder BMAD follow-up (tenzij expliciet `review-only`)

## Verplichte extra output-sectie

### Execution Honesty & Verify Integrity
- welke succesclaims zijn gedaan
- welk bewijs daar wel of niet onder ligt
- welke verify-stappen ontbreken
- of blocker-claims voldoende probes hadden
- of de run te vroeg is gestopt (backlog open zonder bewezen globale blocker)

## Verdict

- ✅ **COMPLIANT** - reviewed scope is CTO-compliant én execution honesty is op orde
- ⚠️ **CONDITIONAL** - functioneel acceptabel, maar er blijven expliciete gaps over
- ❌ **NON-COMPLIANT** - blokkerende gaps of onbewezen succesclaims, werk moet stoppen tot fix
