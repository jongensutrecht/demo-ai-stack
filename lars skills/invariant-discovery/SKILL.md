---
name: invariant-discovery
# prettier-ignore
description: Analyseer codebase en ontdek wat NOOIT mag gebeuren (invarianten).
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion
user-invocable: true
---

# Invariant Discovery

> **Doel**: Ontdek en documenteer wat NOOIT mag gebeuren in dit project, zonder te vervallen in generieke security- of kwaliteitsclichés.

## Wanneer Activeren

- `/invariant-discovery` bij project setup
- Na major features met security/business impact
- Na security incidents
- Voor het opzetten van NEVER-tests en harde fail-closed guardrails

## 10/10-kader voor invariant discovery

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Invariant-specifiek:

- elke invariant beschrijft wat NOOIT mag gebeuren, waarom dat catastrofaal is en hoe je het detecteert
- output is direct bruikbaar voor tests, guards, monitoring en reviews
- vragen aan de gebruiker gebeuren pas ná repo-analyse

## Workflow

1. **Analyseer codebase eerst**
   - zoek auth, permissions, data access, payments, external sync, deletes, state transitions, background jobs, retries, file IO, secrets, rate limits, migrations
   - zoek ook foutpaden, guard clauses, assertions en existing invariants/tests

2. **Lees bestaande docs en contracts**
   - README, ARCHITECTURE, SECURITY, AGENTS, START_HERE, SOURCES_OF_TRUTH
   - OpenSpec / API contracts / policy docs
   - incident notes of postmortems als aanwezig

3. **Leid kandidaat-invarianten af uit bewijs**
   - security: wat mag nooit uitlekken, escalen, bypassen?
   - business: welke beslissingen of staten mogen nooit inconsistent worden?
   - data: wat mag nooit corrupt/racey/dubbel/kwijt raken?
   - runtime: welke failure modes mogen nooit silent worden?
   - performance: welke resource- of latency-failures mogen nooit onbegrensd worden?

4. **Vraag alleen ontbrekende externe kennis uit**
   - alleen als het niet uit repo, config, tests of docs afleidbaar is
   - vragen moeten scherp zijn, geen brainstorm

5. **Genereer invariants-output**
   - volgens output format
   - per invariant: naam, never-statement, why, evidence, detection, test implication

6. **Review streng op luiheid**
   - verwijder generieke of niet-verifieerbare invarianten
   - voeg alleen invarianten toe die omzetbaar zijn naar guard/test/review-check

7. **Schrijf file**
   - pas na inhoudelijke complete set
   - geen halve placeholder-output

## Hard Rules

1. **Analyse vóór vragen** - eerst repo, dan pas uservragen als dat echt nodig is
2. **Geen generieke invarianten** - elke invariant moet specifiek, hard en omzetbaar zijn
3. **Bewijs per invariant** - code, contract, incident, config, test of docspoor
4. **Universele guards gelden** — zie `~/.pi/agent/skills/_guards.md`
5. **Elke invariant moet een NEVER-test of equivalent impliceren**

## Discovery Vragen

```bash
python scripts/questions.py security     # Security vragen
python scripts/questions.py business     # Business vragen
python scripts/questions.py performance  # Performance vragen
python scripts/questions.py commands     # Discovery commands
```

Gebruik deze pas nadat je repo-analyse concrete gaten heeft blootgelegd.

## Output Genereren

```bash
python scripts/generate.py              # Template
python scripts/generate.py examples     # Voorbeelden
```

## Output Format

Zie [knowledge/output-format.md](knowledge/output-format.md)

Minimaal per invariant:
- **Invariant ID / naam**
- **NOOIT-statement**
- **Waarom dit hard is**
- **Bewijs / bronnen**
- **Detectie / guard / test-route**
- **Scope** (security, business, data, runtime, performance)
- **Failure impact**

## Wat géén geldig stopmoment of succesclaim is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Invariant-specifiek:

- uservragen stellen terwijl de repo nog niet inhoudelijk is onderzocht
- een halve `invariants.md` ter review aanbieden met placeholders

## Gerelateerde Skills

- `/test-guard`, `/cto-guard`
