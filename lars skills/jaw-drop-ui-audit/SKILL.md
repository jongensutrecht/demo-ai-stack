---
name: jaw-drop-ui-audit
description: Brutaal eerlijke UI/UX audit vanuit het perspectief van een onafhankelijke Champions League designer, plus een niet-lui transformatieplan naar 10/10 craft. Geen usability-checklist maar craft-oordeel - zou een top designer zeggen "jaw-dropping"?
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# Jaw Drop UI Audit

## Doel

Neem de rol aan van een **onafhankelijke top UI/UX designer** (Champions League niveau, 15+ jaar, Dribbble/Awwwards jury-level) die voor het eerst een app opent.

Geen usability-checklist. Geen WCAG-only audit. Eén vraag:

> **Zou een senior designer zeggen: "Holy shit, dit is craft. Wie heeft dit ontworpen?"**

Wees **brutaal eerlijk**. Zeg wat je ziet, met bewijs uit code én screenshots.

## Wanneer gebruiken

```
/skill:jaw-drop-ui-audit
/skill:jaw-drop-ui-audit http://localhost:3000
/skill:jaw-drop-ui-audit src/
/skill:jaw-drop-ui-audit --vibe operator-dark
```

## Hard rules

1. **Designer-perspectief** - je bent NIET de developer, NIET de PM. Je bent een externe designer die de app voor het eerst ziet.
2. **Code + visueel** - inspecteer tokens/CSS/components EN de werkelijke gerenderde UI (screenshots via agent-browser/playwright).
3. **Visueel bewijs is verplicht** - facetten 1, 3, 6, 9 kunnen NIET betrouwbaar beoordeeld worden zonder screenshot of live pagina met echte/realistische data. Zonder visueel bewijs: markeer als `UNKNOWN (niet visueel geverifieerd)`. Zie [knowledge/layout-composition.md](knowledge/layout-composition.md).
4. **Bewijs op elke claim** - screenshot, `path:line`, token-waarde, of concrete meting. Geen vage indrukken.
5. **Geen complimenten zonder bewijs** - "ziet er goed uit" is geen oordeel.
6. **Vergelijk met de top 5%** - niet met "gemiddeld"; vergelijk met Vercel Dashboard, Linear, Raycast, Stripe Dashboard.
7. **AI-generated UI herkennen** - benoem patronen die typisch AI-slop zijn (zie [knowledge/ai-slop-fingerprint.md](knowledge/ai-slop-fingerprint.md)).
8. **Operator Dark DNA als optionele referentie** - wanneer de target-app het Operator Dark design system gebruikt of nastreeft, toets tegen [knowledge/operator-dark-dna.md](knowledge/operator-dark-dna.md). Niet als universele norm.
9. **Layout compositie checken** - section heading+actions alignment, filter bar density, orphaned elements, flex row alignment, content overflow, section gap proportionality. Zie [knowledge/layout-composition.md](knowledge/layout-composition.md). Alleen betrouwbaar met screenshot.
10. **Een 10/10-plan is verplicht** - eindig niet met alleen een audit; lever altijd een transformatieplan dat de route naar 10/10 beschrijft.
11. **Universele guards gelden** - lees `~/.pi/agent/skills/_guards.md` en pas alle guards toe (anti-lui, anti-fake-10/10, proof-eisen, scoreband-lat, ongeldige stopmomenten).

## Autonomous state machine

### States

1. **FIRST_IMPRESSION** (max 3 minuten)
   - Open de app (browser of screenshots).
   - Squint test: knijp je ogen dicht, wat zie je? Is er één focuspunt per view?
   - 3-seconden reactie: wat voel je? Professioneel? Generiek? Overweldigend? Clean?
   - Noteer je eerste indruk VOOR je dieper gaat.
   - Success -> `TOKEN_AUDIT`

2. **TOKEN_AUDIT**
   - Vind en lees alle design tokens (CSS custom properties, Tailwind config, theme files).
   - Check: type scale locked? Spacing consistent? Color palette met rollen? Shadows met systeem?
   - Lees [knowledge/audit-facets.md](knowledge/audit-facets.md) facetten 2-5 voor criteria.
   - Success -> `COMPONENT_SCAN`

3. **COMPONENT_SCAN**
   - Inventariseer alle UI componenten (buttons, cards, inputs, modals, nav, tables, lists).
   - Check per component: alle states aanwezig? (hover/focus/active/disabled/loading/error/empty)
   - Check token-adherence: gebruikt elk component tokens of hardcoded waarden?
   - **Button deep-dive**: lees [knowledge/button-micro-craft.md](knowledge/button-micro-craft.md) en check:
     - Interne padding (horizontaal ≥ 1.5× verticaal?)
     - Tekst optisch gecentreerd? (uppercase correctie, icon alignment)
     - Size scale aanwezig? (xs/sm/md/lg met vaste height+padding+font-size)
     - Compact vs leesbaar: density past bij context? (toolbar=sm, CTA=lg, mobile≥44px)
     - Icon buttons vierkant? Tooltip/aria-label aanwezig?
     - Spacing tussen buttons consistent? (gap, niet margin)
   - Lees [knowledge/audit-facets.md](knowledge/audit-facets.md) facetten 6-7 voor criteria.
   - Success -> `LAYOUT_COMPOSITION`

3b. **LAYOUT_COMPOSITION** (screenshot/live pagina verplicht)
   - Maak screenshots van elke unieke pagina/view met echte of realistische data.
   - Lees [knowledge/layout-composition.md](knowledge/layout-composition.md) en check alle 6 punten.
   - Zonder screenshot: markeer facetten 1, 3, 6, 9 als `UNKNOWN (niet visueel geverifieerd)`.
   - Success -> `INTERACTION_CHECK`

4. **INTERACTION_CHECK**
   - Inspecteer transitions, hover states, focus rings, animaties in CSS/code.
   - Check: consistent timing? Purpose-driven motion? Choreography (stagger) of alles tegelijk?
   - Lees [knowledge/audit-facets.md](knowledge/audit-facets.md) facet 8 voor criteria.
   - Success -> `RESPONSIVE_PROBE`

5. **RESPONSIVE_PROBE**
   - Check touch targets (≥44px), responsive breakpoints, proportional scaling.
   - Geen horizontal scroll op mobile? Geen truncated content?
   - Lees [knowledge/audit-facets.md](knowledge/audit-facets.md) facet 9 voor criteria.
   - Success -> `EDGE_STATES`

6. **EDGE_STATES**
   - Zoek naar empty states, loading states (skeletons?), error states, disabled states.
   - Zijn ze even gepolijst als het happy path?
   - Lees [knowledge/audit-facets.md](knowledge/audit-facets.md) facet 10-11 voor criteria.
   - Success -> `VIBE_MATCH`

7. **VIBE_MATCH**
   - Als `--vibe operator-dark` of als de app Operator Dark tokens gebruikt: toets tegen [knowledge/operator-dark-dna.md](knowledge/operator-dark-dna.md).
   - Anders: beoordeel of de app een herkenbare design direction heeft.
   - Lees [knowledge/audit-facets.md](knowledge/audit-facets.md) facet 12 voor criteria.
   - Success -> `AI_SLOP_DETECTION`

8. **AI_SLOP_DETECTION**
   - Loop door alle 12 signalen uit [knowledge/ai-slop-fingerprint.md](knowledge/ai-slop-fingerprint.md).
   - Per signaal: ja/nee + concreet bewijs.
   - Success -> `VERDICT`

9. **VERDICT**
   - Schrijf het volledige rapport in het output format hieronder.
   - Benoem expliciet of de huidige UI fundamenteel, systemisch of vooral cosmetisch tekortschiet.
   - Success -> `TEN_OUT_OF_TEN_PLAN`

10. **TEN_OUT_OF_TEN_PLAN**
   - Vertaal de audit naar een **niet-lui transformatieplan** met 3-5 moves die samen de route naar 10/10 vormen.
   - Elke move moet bevatten:
     - waarom dit high leverage is
     - welke facetten hiermee stijgen
     - het concrete doelbeeld na implementatie
     - welke tokens/components/layouts/states geraakt worden
     - wat expliciet NIET gedaan mag worden
     - proof of done
   - Als de huidige score `< 6.5` is: het plan is ongeldig zonder minimaal één system move, één component move en één layout/composition move.
   - Als de huidige score `6.5-7.9` is: het plan is ongeldig zonder een expliciete move voor design direction / personality én micro-craft.
   - Als de huidige score `8.0+` is: focus op optische correctie, density tuning, edge-state parity en screenshot-verifieerbaar verschil.
   - Success -> `COMPOUND_LEARNING`

11. **COMPOUND_LEARNING**
   - Action: run `/skill:compound-learning` — extract max 5 learnings from this UI audit and save to `LEARNINGS.md` (repo) and/or `LEARNINGS_GLOBAL.md` (global).
   - Success -> `DONE`

## De 12 auditfacetten

Volledige criteria per facet: [knowledge/audit-facets.md](knowledge/audit-facets.md)

| # | Facet | Kern-check |
|---|-------|-----------|
| 1 | Visual Hierarchy | Squint test + section heading+actions alignment + orphaned elements (screenshot vereist) |
| 2 | Typography System | Locked scale, weight hierarchy, mono voor data, letter-spacing bewust? |
| 3 | Spacing & Rhythm | Grid + vertical rhythm + filter bar density + flex alignment + section gap proportionality (screenshot vereist) |
| 4 | Color System & Restraint | Palette met semantische rollen, geen kleur zonder functie, WCAG contrast? |
| 5 | Surface & Depth | Logische surface stack, border vs shadow vs tint, glass spaarzaam? |
| 6 | Component Consistency | Heights, radius, tokens, layout patterns herhalen + [button deep-dive](knowledge/button-micro-craft.md) |
| 7 | Interactive States | Hover/focus/active/disabled allemaal ontworpen en samenhangend? |
| 8 | Microinteractions & Motion | Consistent timing, purpose-driven, staggering, physics-feel? |
| 9 | Responsive & Touch | Touch targets ≥44px, proportional scaling, content overflow/truncation (screenshot vereist) |
| 10 | Edge States | Empty, loading, error states even polished als happy path? |
| 11 | Accessibility Craft | Contrast ≥4.5:1, focus-visible, semantic HTML, prefers-reduced-motion? |
| 12 | Design Direction / Vibe | Herkenbare personality, bewuste aesthetic, niet generiek? |

## Scoring

Per facet: score 1-10.

| Score | Betekenis |
|-------|-----------|
| 1-3 | **Template-tier** - ongewijzigd UI kit, AI-default, of Material/Bootstrap out-of-box |
| 4-5 | **Functional** - werkt, maar niemand bookmarkt dit. Ziet eruit als 10.000 andere apps |
| 6-7 | **Professional** - solide, bewuste keuzes zichtbaar, maar eerder gezien |
| 8-9 | **Craft-level** - hier heeft een designer nagedacht. Details die je twee keer laten kijken |
| 10 | **Jaw-dropping** - dit deel je in je design-channel. Dit bookmarkt een designer |

Overall:
- **< 5.0**: Template-niveau. Niemand kijkt twee keer.
- **5.0-6.9**: Functioneel. Niet slecht, niet bijzonder.
- **7.0-7.9**: Professioneel. Boven gemiddeld. Niet jaw-dropping.
- **8.0-8.9**: Craft. Top designers zouden dit respecteren.
- **9.0+**: Jaw-dropping. Dit is referentiemateriaal.

## 10/10-kader voor het plan

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Hieronder alleen de UI-specifieke aanvullingen.

### Wat 10/10 UI specifiek WEL is (bovenop universele guards)
- **Optisch gecorrigeerd** - niet alleen mathematisch correct, maar visueel juist
- **Dicht maar moeiteloos** - veel informatie zonder drukte
- **Herkenbaar** - duidelijke design direction, niet generiek SaaS

### Wat 10/10 UI specifiek NIET is (bovenop universele guards)
- meer gradients, glassmorphism, kleurvariatie of animatie
- een hero mooier maken terwijl tabellen/forms nog middelmatig zijn
- een font toevoegen "voor personality" zonder systemische verbetering

## Output format

```markdown
# Jaw Drop UI Audit: <app naam>

## Eerste Indruk (3 seconden)
<Wat je ziet als je de app voor het eerst opent. Squint test resultaat. Rauw, onbewerkt.>

---

## Facet Scores

| # | Facet | Score | One-liner |
|---|-------|-------|-----------|
| 1 | Visual Hierarchy | X/10 | ... |
| 2 | Typography System | X/10 | ... |
| 3 | Spacing & Rhythm | X/10 | ... |
| 4 | Color System & Restraint | X/10 | ... |
| 5 | Surface & Depth | X/10 | ... |
| 6 | Component Consistency | X/10 | ... |
| 7 | Interactive States | X/10 | ... |
| 8 | Microinteractions & Motion | X/10 | ... |
| 9 | Responsive & Touch | X/10 | ... |
| 10 | Edge States | X/10 | ... |
| 11 | Accessibility Craft | X/10 | ... |
| 12 | Design Direction / Vibe | X/10 | ... |
| | **Overall** | **X.X/10** | |

---

## Deep Dive per Facet

### 1. Visual Hierarchy (X/10)
**Goed:**
- <bewijs: screenshot / path:line / concrete observatie>

**Slecht:**
- <bewijs>

**Jaw-drop?** Ja/Nee - <waarom>

(herhaal voor facet 2-12)

---

## AI-Slop Fingerprint Check
- [ ] Uniform spacing: <ja/nee + bewijs>
- [ ] Purple-blue gradient default: <ja/nee + bewijs>
- [ ] Generieke fonts: <ja/nee + bewijs>
- [ ] Glassmorphism everywhere: <ja/nee + bewijs>
- [ ] Missing states: <ja/nee + bewijs>
- [ ] Mathematical centering (optical misalignment): <ja/nee + bewijs>
- [ ] Simultaneous animations: <ja/nee + bewijs>
- [ ] Shadow-only depth: <ja/nee + bewijs>
- [ ] Decorative color: <ja/nee + bewijs>
- [ ] Pattern collage: <ja/nee + bewijs>
- [ ] "Alles even belangrijk": <ja/nee + bewijs>
- [ ] Emoji als UI-iconen: <ja/nee + bewijs>

**Verdict**: <AI-generated? Deels? Nee? Onderbouwing.>

---

## Operator Dark DNA Check (indien van toepassing)
(alleen als --vibe operator-dark of als de app OD tokens gebruikt)

| Check | Pass/Fail | Bewijs |
|-------|-----------|--------|
| Deep navy base | | |
| Glass alleen op chrome | | |
| Jewel-tone accents met rollen | | |
| DM Sans + JetBrains Mono | | |
| Border-first cards | | |
| Dual-layer shadows | | |
| 120ms transitions | | |
| 44px touch targets | | |
| Uppercase tracking-widest labels | | |
| Groen alleen voor utility/success | | |

---

## Het Eerlijke Verdict

### Zou een top designer zeggen "jaw-dropping"?
<Ja / Nee / Bijna - met onderbouwing>

### Wat is het BESTE aan deze UI?
<1-3 dingen die echt opvallen>

### Wat is het SLECHTSTE aan deze UI?
<1-3 dingen die echt pijn doen>

### Top 3 verbeteringen voor maximum impact
1. <concreet, met verwacht effect op score>
2. <concreet>
3. <concreet>

---

## 10/10 Kader

### Wat 10/10 hier WEL betekent
- <3-5 bullets: welke kwaliteiten deze app moet hebben om referentiemateriaal te zijn>

### Wat 10/10 hier NIET betekent
- <3-5 bullets: welke verleidelijke maar middelmatige routes expliciet verboden zijn>

---

## 10/10 Transformatieplan

### North Star
<één alinea: hoe de UI na de transformatie moet voelen>

### Move 1: <naam>
**Waarom deze move:**
- <waarom high leverage>

**Trekt deze facetten omhoog:**
- <facet + verwachte delta>

**Doelbeeld:**
- <concrete eindstaat>

**Concrete ingrepen:**
- <tokens>
- <componenten>
- <layouts/screens>
- <states/responsive>

**Niet doen:**
- <verboden shortcut>

**Proof of done:**
- <screenshot/path:line/meting/testcase>

(repeat voor Move 2-5 indien nodig)

### Uitvoervolgorde
1. <foundation>
2. <component family>
3. <screen composition>
4. <states/motion/responsive polish>

### Waarom dit géén lui plan is
- <leg uit waarom deze moves de score echt naar 10/10 trekken i.p.v. cosmetisch poetsen>
```

## Wat géén geldig stopmoment is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. UI-specifieke aanvullingen:

- Alleen screenshots zonder code-inspectie
- **Alleen code-inspectie zonder visuele beoordeling** — layout, overflow en alignment zijn NIET betrouwbaar zonder screenshot met echte data
- **Spacing/hierarchy/responsive als 7+ scoren zonder visueel bewijs** — tokens kunnen perfect zijn terwijl de gerenderde layout kapot is
- **Content overflow niet checken met realistische (lange) data** — korte testdata verbergt layout-breaks
