# Audit Facets — Scoring Criteria & Detectie

## 1. Visual Hierarchy

**Wat je checkt:**
- Squint test: knijp ogen dicht, zie je nog structuur?
- Eén duidelijk focuspunt per view (hero element, primary action)
- Visuele pauzes tussen secties (breathing room)
- Contrastverhouding tussen primair/secundair/tertiair content
- **Section heading + actions alignment**: heading en actieknoppen op dezelfde baseline, knoppen horizontaal (niet gestapeld) — zie [layout-composition.md](layout-composition.md) Check 1
- **Orphaned elements**: geen zwevende status-pills of metadata tussen secties — zie [layout-composition.md](layout-composition.md) Check 3

**Detectie (code + visueel — screenshot vereist):**
- `font-weight` verdeling: max 3 weights in actief gebruik
- `font-size` verdeling: locked scale of ad-hoc?
- `z-index` gebruik: gestructureerd of wildgroei?
- **Visueel**: section heading + buttons alignment op gerenderde pagina
- **Visueel**: geen elementen die "zweven" zonder groepering

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Alles even groot, even bold, even belangrijk. Geen visuele rust. |
| 4-5 | Basis-hiërarchie aanwezig (headings vs body) maar geen bewuste flow. |
| 6-7 | Duidelijke niveaus, maar mist subtiliteit (bijv. secondary text niet gedimd). |
| 8-9 | Meerdere niveaus, bewuste witruimte, scanning patterns werken. |
| 10 | Op 3 meter afstand weet je wat belangrijk is. Information density voelt moeiteloos. |

---

## 2. Typography System

**Wat je checkt:**
- Type scale: locked (bijv. 12/14/16/20/24/32) of random sizes?
- Weight hierarchy: max 3 weights met duidelijke rollen
- Font pairing: bewust (bijv. sans voor UI, mono voor data) of default?
- Letter-spacing: bewust op uppercase/small-text, niet overal 0
- Line-height: afgestemd per context (body vs heading vs label)

**Detectie (code):**
- Zoek `font-size` waarden: zijn het tokens of magic numbers?
- Zoek `font-family` declaraties: hoeveel fonts in gebruik?
- Zoek `letter-spacing` op uppercase elementen
- Check of `--font-*` of `--text-*` tokens bestaan en consistent gebruikt worden

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | System font, één size, geen bewuste keuze. |
| 4-5 | Gekozen font maar geen systeem. Random sizes door de app. |
| 6-7 | Scale aanwezig, font pairing, maar niet overal consistent. |
| 8-9 | Locked scale, weight rollen, mono voor data, bewuste tracking. |
| 10 | Typografie voelt "engineered" — je zou het font herkennen als het merk. |

---

## 3. Spacing & Rhythm

**Wat je checkt:**
- Spacing scale: gebaseerd op een base unit (4px/8px) of ad-hoc?
- Vertical rhythm: consistent afstanden tussen secties
- Contextuele variatie: tighter spacing in dense areas, meer adem in hero areas
- Grouping via proximity: gerelateerde items dichter bij elkaar
- **Filter bar density**: max 4-5 controls per rij, actieknop gescheiden — zie [layout-composition.md](layout-composition.md) Check 2
- **Flex row vertical alignment**: `align-items` bewust gekozen bij ongelijke content heights — zie [layout-composition.md](layout-composition.md) Check 4
- **Section gap proportionality**: hero→content gap > peer gap > within-section gap — zie [layout-composition.md](layout-composition.md) Check 6

**Detectie (code + visueel — screenshot vereist):**
- Zoek `padding`/`margin`/`gap` waarden: tokens of magic numbers?
- Tel unieke spacing waarden: <10 = systeem, >20 = chaos
- Check `gap` in flex/grid: consistent per component-type?
- **Visueel**: filter bar druktegraad, flex row alignment, gap proportionaliteit

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Random padding overal. Geen ritme. |
| 4-5 | Basis spacing maar uniform (alles 16px). Geen context. |
| 6-7 | Scale aanwezig, maar soms inconsistent of te uniform. |
| 8-9 | Consistent scale, contextuele variatie, grouping werkt. |
| 10 | Spacing voelt onvermijdelijk — je zou niets verplaatsen. |

---

## 4. Color System & Restraint

**Wat je checkt:**
- Palette: gedefinieerd met semantische rollen (primary, success, danger, muted)?
- Restraint: max 5-7 kleuren in actief gebruik, niet elke sectie een eigen kleur
- Kleur als betekenisdrager: groen = success, rood = error, niet decoratief
- WCAG contrast: ≥4.5:1 voor tekst, ≥3:1 voor UI elementen
- Tonal consistency: warme of koele tint consistent door de hele app

**Detectie (code):**
- Zoek kleur-tokens: `--color-*`, `--od-*`, `--accent-*`
- Tel unieke hex/rgb waarden buiten tokens: 0 = perfect, >10 = probleem
- Check contrast van `--text` op `--bg`: bereken ratio

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Random kleuren, geen systeem, contrast violations. |
| 4-5 | Basispalette maar kleuren zonder rollen. Decoratief gebruik. |
| 6-7 | Semantische rollen, goede contrast, maar soms inconsistent. |
| 8-9 | Strak palette, restraint, kleur = taal, tonal consistency. |
| 10 | Kleurgebruik vertelt een verhaal. Restraint voelt als luxe. |

---

## 5. Surface & Depth

**Wat je checkt:**
- Surface stack: duidelijke lagen (background → canvas → card → elevated → overlay)
- Depth cues: borders, shadows, tints — niet allemaal tegelijk, bewuste keuze
- Glass/blur: spaarzaam (alleen nav/overlays), niet op elke card
- Dark mode specifiek: tonal separation > shadows (schaduwen werken slecht op donker)
- Card style: border-first of shadow-first? Consistent?

**Detectie (code):**
- Zoek `background` waarden: hoeveel surface levels?
- Zoek `box-shadow`: systeem (sm/md/lg) of ad-hoc?
- Zoek `backdrop-filter: blur`: op hoeveel elementen?
- Check of surfaces tokens gebruiken of hardcoded rgba

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Flat (geen depth) of shadow-soup (alles zweeft). |
| 4-5 | Basis cards met shadow maar geen systeem. |
| 6-7 | Surface levels aanwezig, maar depth cues inconsistent. |
| 8-9 | Logische stack, bewuste keuze border vs shadow, glass spaarzaam. |
| 10 | Je "voelt" de lagen zonder na te denken. Depth is informatie. |

---

## 6. Component Consistency

**Wat je checkt:**
- Consistent heights: buttons, inputs, selects — allemaal dezelfde hoogte per size
- Radius: één radius-systeem, niet 4px hier en 12px daar
- Border-style: overal dezelfde kleur/opacity, of drift?
- Token adherence: gebruiken componenten tokens of hardcoded waarden?
- Dezelfde component ziet er overal hetzelfde uit (geen contextafhankelijke styling-drift)
- **Layout patterns herhalen**: section heading+actions, card header+status, filter+submit — overal hetzelfde patroon — zie [layout-composition.md](layout-composition.md) Check 1, 2

**Detectie (code + visueel):**
- Zoek `border-radius` waarden: tokens of magic numbers?
- Zoek button/input `height`/`padding`: consistent?
- Check of er een gedeelde component-library is vs per-page styling
- **Visueel**: vergelijk heading+actions layout op verschillende pagina's — consistent?

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Elke page heeft eigen button-stijl. Geen systeem. |
| 4-5 | Gedeelde componenten maar zichtbare drift (radius, height, colors). |
| 6-7 | Redelijk consistent, maar af en toe afwijkingen. |
| 8-9 | Strakke token-adherence, consistent per size, één familie. |
| 10 | Elk component is dezelfde familie. Pixel-perfect consistent. |

---

## 7. Interactive States

**Wat je checkt:**
- Hover: subtiel maar zichtbaar (niet te dramatisch)
- Focus: duidelijke focus ring (niet `outline: none` zonder alternatief)
- Active/pressed: feedback dat je klikt/tapt
- Disabled: visueel duidelijk (opacity + cursor) maar niet onzichtbaar
- Selected/current: duidelijk onderscheid van unselected
- Samenhang: alle states volgen dezelfde logica (dimmen/highlighten/border change)

**Detectie (code):**
- Zoek `:hover`, `:focus`, `:active`, `:disabled`, `[aria-current]` selectors
- Check of `focus-visible` gebruikt wordt (niet `focus`)
- Check of disabled states `pointer-events: none` of `cursor: not-allowed` hebben

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Geen hover/focus styling. Browser defaults. |
| 4-5 | Hover aanwezig maar geen focus of disabled. |
| 6-7 | Meeste states aanwezig, maar niet samenhangend. |
| 8-9 | Alle states ontworpen, consistent, subtiel maar duidelijk. |
| 10 | Interactie voelt responsive en "alive". States vertellen een verhaal. |

---

## 8. Microinteractions & Motion

**Wat je checkt:**
- Timing: consistent (bijv. 120ms voor micro, 200-300ms voor page) of random?
- Purpose: animeert het om informatie te geven (in/out, state change) of decoratief?
- Easing: niet linear, bewuste curve (ease-out voor enter, ease-in voor exit)
- Choreography: stagger (items verschijnen na elkaar) vs simultaan
- `prefers-reduced-motion`: gerespecteerd?

**Detectie (code):**
- Zoek `transition` declaraties: hoeveel unieke durations?
- Zoek `animation`/`@keyframes`: purpose-driven?
- Check `@media (prefers-reduced-motion: reduce)`

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Geen animaties, of alles animeert (300ms op alles). |
| 4-5 | Basis transitions maar geen systeem. Random durations. |
| 6-7 | Consistent timing, maar geen choreography of stagger. |
| 8-9 | Purpose-driven, bewuste easing, stagger waar relevant. |
| 10 | Animaties voelen als physics. Alles beweegt "juist". |

---

## 9. Responsive & Touch

**Wat je checkt:**
- Touch targets: ≥44px (iOS HIG) op alle interactieve elementen
- Proportional scaling: past layout zich aan of is het "desktop gekrompen"?
- Geen horizontal scroll op <375px
- Geen tekst dat afsnijdt zonder truncation-indicator
- Mobile-first gevoel: niet "desktop-met-hamburger"
- **Content overflow / truncation**: lange emails, IDs, namen breken de layout niet — `text-overflow: ellipsis` op onvoorspelbare tekst — zie [layout-composition.md](layout-composition.md) Check 5

**Detectie (code + visueel — echte data vereist):**
- Zoek `min-height`/`min-width` op buttons/links: ≥44px?
- Zoek `@media` breakpoints: hoeveel en logisch?
- Check of `overflow-x: hidden` op body een workaround is
- **Visueel**: test met lange emails/namen/IDs — breken ze het grid?
- Zoek `text-overflow: ellipsis` / `truncate` classes op data-containers

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Niet responsive. Horizontal scroll. Tiny touch targets. |
| 4-5 | Basis responsive maar voelt als desktop-shrink. |
| 6-7 | Goed responsive, maar touch targets soms te klein. |
| 8-9 | Native feel op mobile, goede touch targets, proportional. |
| 10 | Voelt native op elk device. Geen concessies. |

---

## 10. Edge States

**Wat je checkt:**
- Empty states: is er een ontworpen empty state of "No data"?
- Loading: skeleton loaders of spinner? Skeleton = craft.
- Error states: informatief en gestyled, of rode tekst?
- Offline: indicator? Graceful degradation?
- First-time user: onboarding of cold start?

**Detectie (code):**
- Zoek "empty", "no data", "loading", "skeleton", "error" in componenten
- Check of er `Skeleton` / `EmptyState` / `ErrorBoundary` componenten bestaan
- Check of loading states skeleton dimensions matchen met content

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Geen edge states. Witte pagina bij loading. "Error" bij fout. |
| 4-5 | Spinner bij loading. "No items" tekst. Basis error. |
| 6-7 | Skeletons aanwezig, error states gestyled, maar niet overal. |
| 8-9 | Alle edge states ontworpen en consistent. Voelt "af". |
| 10 | Edge states zijn even mooi als happy path. De app voelt af zonder data. |

---

## 11. Accessibility Craft

**Wat je checkt:**
- Contrast: ≥4.5:1 tekst, ≥3:1 UI elementen (WCAG AA)
- Focus management: `focus-visible`, skip links, logische tab-volgorde
- Semantic HTML: `<nav>`, `<main>`, `<button>` (niet `<div onClick>`)
- ARIA: correct gebruik (niet aria-soup)
- `prefers-reduced-motion`: gerespecteerd
- `prefers-color-scheme`: dark/light toggle werkt

**Detectie (code):**
- Zoek `<div onClick` of `<span onClick` zonder `role="button"`
- Zoek `outline: none` / `outline: 0` zonder `focus-visible` alternatief
- Check `aria-label`, `aria-current`, `role` gebruik

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Div-soup, geen focus styles, contrast violations. |
| 4-5 | Basis semantic HTML, maar geen focus management. |
| 6-7 | Goede semantics, contrast OK, maar accessibility is afterthought. |
| 8-9 | Accessibility is een design-keuze. Focus rings zijn mooi. |
| 10 | Accessibility voelt niet als compliance maar als craft. |

---

## 12. Design Direction / Vibe

**Wat je checkt:**
- Herkenbare personality: zou je een screenshot herkennen zonder logo?
- Bewuste aesthetic: is er een duidelijke design richting (dark cockpit, warm minimal, brutalist)?
- Niet generiek: wijkt af van Material/Bootstrap/Tailwind defaults
- Cohesie: alles voelt alsof het bij hetzelfde merk hoort
- Opinie: durft de design keuzes te maken (niet alles is veilig-neutraal)

**Scoring:**
| Score | Beschrijving |
|-------|-------------|
| 1-3 | Bootstrap/Material default. Geen eigen identiteit. |
| 4-5 | Aangepaste kleuren maar nog steeds generiek framework-gevoel. |
| 6-7 | Eigen richting zichtbaar, maar nog dicht bij bekende patterns. |
| 8-9 | Herkenbare vibe. Screenshot = herkenbaar zonder logo. |
| 10 | Design direction is een statement. Dit is een merk. |
