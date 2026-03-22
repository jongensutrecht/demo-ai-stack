# AI-Slop Fingerprint — 12 signalen

AI-generated UIs zijn niet per se slecht. Maar ze zijn herkenbaar voor een ervaren designer. Deze 12 signalen verraden dat een interface door AI is gegenereerd of zwaar op AI-defaults leunt.

## 1. Uniform Spacing

**Signaal:** Alles heeft dezelfde padding/margin (16px of 24px). Geen contextuele variatie: een hero-sectie heeft dezelfde spacing als een compact lijstitem.

**Detectie:**
- Tel unieke `padding`/`margin`/`gap` waarden
- <5 unieke waarden in de hele app = verdacht uniform
- Geen verschil in spacing tussen dense areas (tabellen) en breathing areas (headers)

**Craft-alternatief:** Contextuele spacing — tighter in dense areas, meer adem in hero/summary areas. 8-12 unieke spacing waarden is gezond.

---

## 2. Purple-Blue Gradient Default

**Signaal:** Primary color is een purple-to-blue gradient, of indigo accent. Dit is de #1 AI default.

**Detectie:**
- `linear-gradient` met purple/blue/indigo als primary
- Geen brand-specifieke kleurkeuze, geen kleur-met-reden

**Craft-alternatief:** Kleurkeuze met rationale (brand, emotie, contrast). Zelfs blauw kan craft zijn als het bewust is.

---

## 3. Generieke Fonts (Inter/Roboto/System)

**Signaal:** Geen bewuste font-keuze. Inter, Roboto, of system-ui zonder personality.

**Detectie:**
- Alleen system fonts of Inter/Roboto
- Geen font pairing (alles dezelfde font)
- Geen bewuste letter-spacing op uppercase

**Craft-alternatief:** Bewuste pairing (bijv. DM Sans voor UI + JetBrains Mono voor data). Font keuze die de personality versterkt.

---

## 4. Glassmorphism Everywhere

**Signaal:** `backdrop-filter: blur()` op elke card, elke sectie, elke surface. Glass is "cool" maar verliest betekenis als alles glass is.

**Detectie:**
- Tel `backdrop-filter` declaraties: >3 = verdacht
- Glass op content cards (niet alleen nav/overlays) = slop
- Glass zonder logische reden (wat zit er achter de blur?)

**Craft-alternatief:** Glass alleen op chrome (nav, toolbar, overlays). Content cards krijgen solide surfaces. Glass = speciale laag.

---

## 5. Missing States

**Signaal:** Alleen het happy path is ontworpen. Geen loading, empty, error, disabled states. De app voelt "af" tot er iets misgaat.

**Detectie:**
- Zoek componenten zonder `:disabled`, loading prop, error prop
- Geen `Skeleton` of `EmptyState` componenten
- Error = rode tekst zonder styling

**Craft-alternatief:** Elke state is ontworpen. Empty states hebben illustraties of CTA's. Skeletons matchen content dimensions. Error states zijn informatief en gestyled.

---

## 6. Mathematical Centering (Optical Misalignment)

**Signaal:** Icons en tekst zijn technisch gecentreerd (`align-items: center`) maar voelen visueel "off". Dit is het verschil tussen mathematisch en optisch centreren.

**Detectie:**
- Icons naast tekst waar het icon visueel hoger/lager zit
- Play/arrow icons die optisch niet gecentreerd zijn
- Padding die gelijk is maar er ongelijk uitziet (bijv. button met icon links)

**Craft-alternatief:** Optical alignment — handmatige correctie met 1-2px offset op icons. `translateY(-1px)` op specifieke icons.

---

## 7. Simultaneous Animations

**Signaal:** Alles animeert tegelijk. Een lijst laadt en alle items verschijnen simultaan. Een page transition beweegt alle elementen op hetzelfde moment.

**Detectie:**
- Geen `animation-delay` of stagger patterns
- Alle transitions dezelfde duration
- Geen choreography (wat beweegt eerst, wat volgt?)

**Craft-alternatief:** Staggered entry (items verschijnen met 30-50ms delay). Choreography: primary content eerst, secondary volgt. Exit animaties sneller dan enter.

---

## 8. Shadow-Only Depth

**Signaal:** Depth wordt alleen gecreëerd met `box-shadow`. Geen borders, geen tints, geen surface color verschil. In dark mode werkt dit niet — schaduwen zijn bijna onzichtbaar op donkere achtergronden.

**Detectie:**
- Cards met alleen `box-shadow`, geen `border`
- In dark mode: shadows met `rgba(0,0,0,...)` die nauwelijks zichtbaar zijn
- Geen surface color verschil tussen niveaus

**Craft-alternatief:** Layered depth: surface color verschil + subtiele border + shadow. In dark mode: border-first met tonal separation (lichtere surface = meer elevated).

---

## 9. Decorative Color

**Signaal:** Kleuren worden gebruikt zonder semantische functie. Een card heeft een gekleurde rand "omdat het mooi is", niet omdat het status of categorie communiceert.

**Detectie:**
- Gekleurde borders/accenten zonder corresponderende betekenis
- Gradients op elementen die geen speciale status hebben
- Meer dan 5 kleuren in actief gebruik zonder duidelijke rolverdeling

**Craft-alternatief:** Elke kleur heeft een rol: primary (actie), success (bevestiging), danger (waarschuwing), muted (secondary). Decoratieve kleur is bewust en spaarzaam.

---

## 10. Pattern Collage

**Signaal:** Componenten uit verschillende design systems door elkaar. Een Material-achtige FAB naast een Bootstrap-achtige navbar naast custom cards. Alsof de AI uit 5 referenties cherry-picked.

**Detectie:**
- Inconsistente border-radius (4px, 8px, 12px, 16px door elkaar)
- Verschillende shadow-systemen per component
- Mix van icon-sets (Material Icons + Lucide + Heroicons)

**Craft-alternatief:** Eén coherent systeem. Eén icon-set. Eén radius-scale. Eén shadow-systeem.

---

## 11. "Alles Even Belangrijk"

**Signaal:** Flat visual hierarchy. Geen hero-element, geen visuele pauzes, geen scanbare structuur. Alles heeft dezelfde visuele weight.

**Detectie:**
- Geen verschil in `font-size` of `font-weight` tussen sections
- Geen `margin-top` verschil tussen secties (geen breathing room)
- Cards/items allemaal exact dezelfde grootte en prominentie

**Craft-alternatief:** Bewuste hiërarchie: hero element > section headers > cards > detail tekst. Visuele pauzes (extra whitespace) tussen logische groepen.

---

## 12. Emoji als UI-Iconen

**Signaal:** 🚀 ⚡ 🎨 ✨ als knopdecoratie of sectie-markers. Emoji's zijn niet ontworpen voor UI — ze zijn inconsistent across platforms, niet alignable, en verraden dat er geen icon-systeem is.

**Detectie:**
- Emoji in buttons, headers, navigation
- Emoji als status-indicator (🟢 🔴)
- Geen echte icon-library (Lucide, Heroicons, Phosphor)

**Craft-alternatief:** Consistent icon-set met dezelfde stroke width, size, en optical weight. Iconen die passen bij de typografie.

---

## Totaal-beoordeling

| Signalen gevonden | Verdict |
|-------------------|---------|
| 0-2 | **Menselijk** — geen significante AI fingerprints |
| 3-5 | **AI-assisted** — basis is AI maar er is bewust nabewerkt |
| 6-8 | **AI-generated** — duidelijk herkenbaar als AI output |
| 9-12 | **AI-slop** — recht uit de prompt, geen designer heeft dit gezien |
