---
name: pa
description: Probleem Analyse - 3 parallelle agents (online research, code analyse, LLM kennis) combineren bevindingen tot één rapport.
allowed-tools: Read, Bash, pa_run
user-invocable: true
---

# PA (Probleem Analyse)

Voer een grondige analyse uit van een probleem met drie parallelle perspectieven:
1. **Online Researcher** → zoekt op internet
2. **Code Analyst** → onderzoekt de lokale codebase
3. **Knowledge Expert** → redeneert vanuit LLM-kennis

## Gebruik

```
/skill:pa <beschrijving van het probleem>
```

Snelle alias:

```
/pa <beschrijving van het probleem>
```

## 10/10-kader voor probleemanalyse

Universele guards: zie `~/.pi/agent/skills/_guards.md`. PA-specifiek:

- één helder probleembeeld, niet drie losse mini-rapporten
- root cause is bewijs-gedragen vanuit minimaal twee perspectieven
- oplossingen zijn high leverage en sluiten aan op de kern, niet op symptomen

## Workflow

### Fase 1: Deterministische PA-run

Gebruik **altijd eerst** de `pa_run` tool. Deze tool start de 3 PA-agents parallel en voert daarna ook de synthese-run uit.

```
pa_run({
  problem: "<probleem beschrijving>"
})
```

### Fase 2: Rapport afronden

Na de `pa_run` tool:

1. Gebruik de tooloutput als primaire bron
2. Maak het eindrapport netjes af in exact het onderstaande output format
3. Voeg geen extra claims toe die niet terug te voeren zijn op de tooloutput
4. Start niet handmatig nog eens losse subagents of een aparte parallelrun; `pa_run` is de vaste route
5. Dwing de output naar één conclusiepad: consensus, conflict, root cause, aanbevolen route
6. Verwerp luie uitkomsten zoals "onderzoek X verder" als er al genoeg bewijs is voor de eerstvolgende high-leverage stap

### Fase 3: Eindrapport

## Output Format

```markdown
# Probleemanalyse: <korte titel>

## Probleem
<Wat is het probleem? Hoe uit het zich?>

---

## Agent Rapporten

### 🌐 Online Researcher
<samenvatting van online bevindingen>
- Belangrijkste bronnen: <urls>
- Conclusie: <wat zegt het internet>

### 💻 Code Analyst
<samenvatting van code analyse>
- Relevante locaties: <file:line>
- Conclusie: <wat zegt de code>

### 🧠 Knowledge Expert
<samenvatting van expert analyse>
- Patroon herkend: <type probleem>
- Conclusie: <wat zegt de expert>

---

## Synthese

### Consensus
De agents zijn het eens over:
- <punt 1>
- <punt 2>

### Conflicten
Verschillende perspectieven:
- Online zegt X, maar code toont Y

### Root Cause (gecombineerd)
<Wat is de oorzaak, met bewijs uit alle drie bronnen>

---

## Oplossingen

### Aanbevolen: <naam>
- **Onderbouwing**: Online ✓ | Code ✓ | Expert ✓
- **Waarom high leverage**: <waarom dit de kern raakt>
- **Aanpak**: ...
- **Risico**: ...
- **Verificatie**: <exacte check>

### Alternatief: <naam>
- **Onderbouwing**: Online ✓ | Code ✗ | Expert ✓
- **Waarom niet eerste keus**: <concreet>
- **Aanpak**: ...

---

## Volgende Stappen
1. <concrete actie>
2. <concrete actie>
3. <concrete verificatie of beslispunt>
```

## Hard Rules

- **Altijd alle 3 agents** - sla er geen over
- **Parallel, niet sequentieel** - voor snelheid
- **Synthese is verplicht** - rapporteer niet alleen de agent outputs
- **Consensus zoeken** - waar zijn ze het eens?
- **Conflicten benoemen** - waar spreken ze tegen?
- **Bronvermelding** - elke claim heeft bewijs (URL, file:line, of "expert kennis")
- **Universele guards gelden** — zie `~/.pi/agent/skills/_guards.md`

## Wat géén geldig stopmoment of output is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. PA-specifiek:

- alleen de ruwe `pa_run` output dumpen
- drie agentrapporten zonder gezamenlijke synthese
- een root cause zonder bewijs uit minimaal twee perspectieven
