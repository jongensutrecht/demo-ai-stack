# Button & Control Micro-Craft

Buttons zijn het meest aangeraakte element in elke UI. Als de buttons niet kloppen, klopt niets. Dit document beschrijft wat een top designer checkt op micro-niveau — dingen die een AI-generated UI bijna altijd mist.

---

## 1. Interne Padding (ademruimte)

**Wat je checkt:**
- Horizontale padding ≥ verticale padding (buttons zijn breder dan hoog)
- Ratio: horizontaal minimaal 1.5× – 2× de verticale padding
- Voorbeeld craft: `padding: 10px 20px` of `padding: 8px 16px`, niet `padding: 12px 12px`
- Tekst mag nooit "tegen de rand aan" voelen
- Padding past bij font-size: grotere tekst = meer padding

**Detectie (code):**
- Zoek `padding` op buttons: is horizontaal > verticaal?
- Zoek `padding: Xpx` (uniform) vs `padding: Ypx Xpx` (bewust)
- Uniform padding (`padding: 12px`) = AI-default, niet craft

**Fail-signalen:**
- `padding: 8px` (uniform, te krap)
- `padding: 16px` (uniform, te veel verticaal)
- Tekst raakt visueel bijna de border

**Craft-referentie (Operator Dark):**
- Primary: `padding: 0.5rem 0.85rem` (8px/13.6px → ratio ~1.7×)
- Compact: `padding: 0.35rem 0.65rem`

---

## 2. Tekst-Uitlijning Binnen Buttons

**Wat je checkt:**
- Tekst is verticaal optisch gecentreerd (niet alleen `align-items: center`)
- Bij uppercase tekst: optisch centreren vereist soms 1px extra `padding-bottom` (uppercase heeft geen descenders)
- Icon + tekst: icon en tekst op dezelfde optische baseline
- Multi-word buttons: geen awkward line breaks

**Detectie (code):**
- Check `display: inline-flex; align-items: center` (basis)
- Check of er optische correcties zijn (`translateY(-1px)` op icons, extra padding-bottom op uppercase)
- Check `white-space: nowrap` om line breaks te voorkomen
- Check `line-height` op button tekst: te hoog = tekst "zweeft", te laag = tekst "plakt"

**Fail-signalen:**
- Icon zit visueel hoger/lager dan tekst
- Uppercase tekst voelt "te hoog" in de button
- `line-height: 1.5` op een button (te veel ruimte)

**Craft-referentie:**
- `line-height: 1` of `1.2` op buttons
- `gap: 0.5rem` tussen icon en tekst
- `align-items: center` + visuele check

---

## 3. Button Sizes (Size Scale)

**Wat je checkt:**
- Duidelijke size scale: xs / sm / md / lg (niet ad-hoc per pagina)
- Elke size heeft vaste height, padding, en font-size
- Inputs en buttons in dezelfde size matchen in hoogte (naast elkaar bruikbaar)
- Touch context: mobile buttons = md/lg, desktop toolbar = sm

**Size referenties (craft-level):**

| Size | Height | Padding (v/h) | Font-size | Gebruik |
|------|--------|---------------|-----------|---------|
| xs | 28-30px | 4px 8px | 12px | Inline actions, tags |
| sm | 32-36px | 6px 12px | 13-14px | Toolbar, compact forms |
| md | 40-44px | 8px 16px | 14-15px | Standaard, forms |
| lg | 48-52px | 12px 24px | 16px | Primary CTA, mobile |

**Detectie (code):**
- Zoek button varianten/sizes: is er een systeem?
- Tel unieke button `height`/`min-height` waarden
- Check of buttons en inputs dezelfde height hebben per size

**Fail-signalen:**
- Alle buttons dezelfde grootte (geen scale)
- Buttons naast inputs met verschillende hoogte
- >4 unieke button hoogtes zonder duidelijk systeem
- Mobile buttons <44px

---

## 4. Compact vs Leesbaar (Density)

**Wat je checkt:**
- Information density is een bewuste keuze, niet een accident
- Dense areas (tabellen, toolbars) gebruiken compact buttons (sm/xs)
- Spacious areas (hero, empty states, modals) gebruiken grotere buttons (md/lg)
- Minimale font-size op buttons: 12px (kleiner = onleesbaar)
- Minimale touch target: 44px (iOS HIG) zelfs als visueel kleiner

**Detectie (code):**
- Zoek buttons in tabellen/lijsten: gebruiken ze een kleinere variant?
- Zoek primary CTA buttons: zijn ze groter dan toolbar buttons?
- Check of er `min-height: 44px` of equivalent padding is op alle interactieve elementen
- Check of `font-size` op buttons ≥12px is

**Fail-signalen:**
- Alle buttons overal even groot (geen density-bewustzijn)
- Compact buttons met font-size <12px
- Grote buttons in dense lijsten (verspilt ruimte)
- Tiny buttons op mobile (touch target <44px)

**Craft-patroon:** Contextual density
```
Toolbar:     sm buttons, tight spacing, compact text
Forms:       md buttons, comfortable spacing
Hero/CTA:    lg buttons, generous spacing
Table rows:  xs/sm icon buttons, minimal padding
Mobile:      md/lg met 44px min touch target
```

---

## 5. Icon Buttons

**Wat je checkt:**
- Icon buttons zijn vierkant (gelijke width en height), niet rechthoekig
- Icon is optisch gecentreerd in het vierkant
- Hover/focus area is het hele vierkant, niet alleen het icon
- Icon size past bij button size (niet te groot, niet te klein)
- Tooltip aanwezig (icon-only buttons hebben `aria-label` + tooltip)

**Detectie (code):**
- Zoek icon-only buttons: `width === height`?
- Check `padding`: gelijk aan alle kanten?
- Check `aria-label` of `title` op icon buttons
- Icon SVG size vs button size: icon ≤60% van button height

**Fail-signalen:**
- Rechthoekige icon buttons (meer padding links/rechts)
- Icon vult de hele button (geen ademruimte)
- Geen tooltip/aria-label op icon-only buttons

**Craft-referentie:**
```css
.icon-btn {
  width: 36px;
  height: 36px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.icon-btn svg {
  width: 18px;   /* 50% van button */
  height: 18px;
}
```

---

## 6. Button Spacing (tussen buttons)

**Wat je checkt:**
- Spacing tussen buttons is consistent (8px of 12px, niet random)
- Primary + secondary button: primary rechts (LTR) of prominent geplaatst
- Button groups: `gap` in flex, niet margin per button
- Destructive buttons: visueel gescheiden van confirm buttons (extra spacing of andere positie)

**Detectie (code):**
- Zoek button containers: `display: flex; gap: Xpx`
- Check of `margin-left`/`margin-right` op individuele buttons wordt gebruikt (= geen systeem)
- Check of destructive (delete/remove) buttons links staan en confirm rechts

**Fail-signalen:**
- Buttons tegen elkaar aan (geen gap)
- Random spacing: 4px hier, 16px daar
- Delete button direct naast Save zonder visuele scheiding
- Buttons met individuele margins i.p.v. container gap

---

## Integratie met audit-facets.md

Dit document verdiept de volgende facetten:
- **Facet 3 (Spacing & Rhythm)** → sectie 1, 4, 6
- **Facet 6 (Component Consistency)** → sectie 3, 5
- **Facet 9 (Responsive & Touch)** → sectie 3, 4
- **Facet 11 (Accessibility Craft)** → sectie 5

Tijdens de audit: na de reguliere facet-scan, loop door dit document als deep-dive op button/control craft.
