---
name: cto-guard
# prettier-ignore
description: Voer een volledige Universal CTO Review v2.4 uit op repo, diff, story of plan; combineert CTO registry, universal scan en repo-10x guardrails.
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# CTO Guard

## Doel

`/cto-guard` is de **uitvoerbare skill** voor de **volledige Universal CTO Review v2.4**.

Gebruik deze skill om werk te reviewen tegen:
- `docs/CTO_RULES.md` (rule registry)
- `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` (volledige audit- en scoringsmodel)
- repo-10x guardrails (`scripts/check_repo_10x_contract.py`, `scripts/quality_gates.py`, search/SSOT contracten)

Deze skill mag **niet** terugvallen naar een korte compliance-samenvatting zonder facet scores, P1/P2/P3 en Path to 10/10.

## Wanneer gebruiken

- `/cto-guard` voor een volledige CTO review
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

## Hard rules

1. **Volledige Universal CTO Review v2.4 is verplicht**
   - gebruik de rijke rapportstructuur uit `knowledge/output-format.md`
   - geen afgeslankte verdict-only output
2. **Lees `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md` volledig** als die bestaat
3. **Lees `docs/CTO_RULES.md` volledig** als die bestaat en valideer parsebaarheid met `python3 scripts/validate_cto_rules_registry.py`
4. **Lees `docs/CTO_GUARD_PROJECT_ADDENDUM.md` volledig** als die bestaat
   - behandel dit document als repo-specifieke CTO Guard uitbreiding
   - neem alle verplichte repo-checks uit het addendum expliciet mee in de review
5. **Historische CTO gap-docs zijn context-only totdat ze opnieuw zijn bewezen**
   - documenten zoals `docs/CTO_GAPS*.md` mogen niet als canonieke open-gap lijst worden overgenomen zonder revalidatie tegen de huidige repo state
   - als een oude gap niet opnieuw is bewezen: markeer die oude claim als `historical-only`
6. **Neem repo-10x guardrails mee**
   - run `python3 scripts/check_repo_10x_contract.py` als die bestaat
   - noteer anders exact 1 eerstvolgende concrete check
7. **P1/P2/P3 expliciet**
   - P3 mag nooit verdwijnen uit het eindrapport
8. **UNKNOWN fail-closed**
   - als iets niet hard bewijsbaar is: markeer `UNKNOWN` + exact 1 verificatie-check
9. **Evidence op elke claim**
   - `path:line` of `command + relevante output`
10. **Native/mobile congruence is verplicht als de repo Capacitor/Android bevat**
   - verifieer source config, generated native config en embedded artifact config als artifacts aanwezig zijn
   - maak expliciet onderscheid tussen install artifacts (`.apk`) en store/upload artifacts (`.aab`)
11. **Credential storage hardening is verplicht als de repo auth secrets/PINs beheert**
   - scan expliciet op plaintext credential storage, migratiepaden en repo-specifieke auth hardening stories

## Workflow

1. **Bepaal review target en scope**
   - repo / working tree / diff / story / plan / mixed
   - `repo_only`, `repo_plus_db`, `repo_plus_infra`, `full_stack`, of een expliciet begrensde delta-scope
2. **Laad bronregels**
   - `docs/CTO_RULES.md`
   - `docs/CTO_GUARD_PROJECT_ADDENDUM.md`
   - `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
   - `docs/START_HERE.md`, `docs/SOURCES_OF_TRUTH.md`, `SECURITY.md`, `README.md`, `AGENTS.md` waar relevant
   - `docs/CTO_GAPS*.md` alleen als historische context, nooit als canonieke open-gap lijst
3. **Verifieer repo-10x / gates**
   - `python3 scripts/check_repo_10x_contract.py` als aanwezig
   - `python3 scripts/quality_gates.py` als aanwezig
4. **Voer repo-specifieke verplichte checks uit**
   - als Capacitor/Android aanwezig is: check `capacitor.config.*`, generated native config en embedded APK/AAB config op congruentie
   - als auth/PIN flows aanwezig zijn: check plaintext credential storage, migratiepad en relevante hardening stories
   - als historische CTO-gap docs bestaan: bewijs welke oude claims nog steeds open zijn en label de rest `historical-only`
5. **Bepaal facet applicability**
   - `Applicable` / `N/A` / `UNKNOWN`
   - noteer `in scope`, `out of scope`, `UNKNOWN external state`
6. **Voer de review uit met het volledige v2.4 model**
   - facet scores
   - canonical gap ownership
   - P1/P2/P3 classificatie
   - overall status / score / confidence
7. **Genereer het volledige rapport** volgens [knowledge/output-format.md](knowledge/output-format.md)
8. **Run post-review BMAD hook** tenzij de gebruiker `review-only` vroeg
   - trigger: er bestaan unresolved `P1-CRITICAL`, `P1-QUICK`, `P2` of `P3` gaps
   - maak een process slug, bijvoorbeeld `cto_guard_followup_<target>_<yyyymmdd>`
   - schrijf `bmad_input/<process>.md` + `bmad_input/<process>.json`
   - mapping van review naar BMAD:
     - unresolved `P1-CRITICAL` / `P1-QUICK` -> BMAD `P0`
     - unresolved `P2` -> BMAD `P1`
     - unresolved `P3` -> BMAD `P3`
   - neem over: scope map, relevante facetten, UNKNOWN external state, gap evidence, closure DoD, Path to 10/10 richting
   - als schrijven niet lukt: markeer `UNKNOWN` + geef exact 1 concrete verificatie-/herstelcheck

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

## Verdict

- ✅ **COMPLIANT** - reviewed scope is CTO-compliant
- ⚠️ **CONDITIONAL** - functioneel acceptabel, maar er blijven expliciete gaps over
- ❌ **NON-COMPLIANT** - blokkerende gaps, werk moet stoppen tot fix
