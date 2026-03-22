# Operator Dark DNA — 10 Concrete Checks

Het Operator Dark design system is een dark-mode cockpit/control-center aesthetic. Dit document beschrijft de 10 concrete DNA-checks, afgeleid uit twee productie-apps: de Driver App (React+Vite, `--od-*` tokens) en de Todo App (Next.js, jvdp design system tokens).

Gebruik deze checks alleen wanneer de target-app het Operator Dark systeem gebruikt of nastreeft (`--vibe operator-dark`).

---

## 1. Deep Navy Base

**DNA:** Achtergrondkleur is een deep navy, niet pure black (`#000`) en niet grijs.

**Referentie-waarden:**
- Driver: `--od-bg: #0c1a2e`, `--od-bg-2: #0f1f36`
- Todo: `--bg-base: #0b1220` (dark mode)

**Check:**
- Hoofd-`background` is in de range `#080f1a` – `#142640` (deep navy zone)
- NIET `#000000`, `#111111`, `#1a1a1a` (pure black/grijs)

**Fail als:** Achtergrond is puur zwart, donkergrijs, of een warme tint

---

## 2. Glass Alleen op Chrome

**DNA:** `backdrop-filter: blur()` wordt alleen gebruikt op navigatie, toolbar, overlays, en modals. Nooit op content cards of lijstitems.

**Referentie:**
- Driver: `nav` heeft `backdrop-filter: blur(16px)`, cards hebben solide `--od-surface`
- Todo: `.nav` heeft `backdrop-filter: blur(10px)`, cards zijn solide `--bg-card`

**Check:**
- `backdrop-filter` op ≤3 elementen (nav, toolbar, modal/overlay)
- Content cards gebruiken solide `background` met optionele transparantie

**Fail als:** Glass op >5 elementen, of op reguliere content cards

---

## 3. Jewel-Tone Accents met Rollen

**DNA:** Accent kleuren zijn jewel-tones (amber, violet, blue) met semantische rollen, niet decoratief.

**Referentie-waarden:**
- Amber/gold = spotlight, waarschuwing, highlight: `--od-amber: rgba(254,249,195,0.85)`, `--accent-amber: #f59e0b`
- Violet/lilac = premium, speciaal: `--od-violet: #c4b5fd`, `--accent-lilac: #8b5cf6`
- Blue = primary, interactief: `--od-blue: #7dd3fc`, `--accent: #2563eb`
- Groen = success/utility only: `--od-success: rgba(134,239,172,0.95)`, `--success: #059669`
- Rood = error/danger only: `--od-error: rgba(252,165,165,0.95)`, `--danger: #dc2626`

**Check:**
- Elke accent kleur heeft een duidelijke semantische rol
- Geen accent kleur "zomaar" op decoratieve elementen

**Fail als:** Random accent kleuren zonder rol, of >6 accent kleuren in actief gebruik

---

## 4. DM Sans + JetBrains Mono

**DNA:** Two-font pairing met duidelijke rolverdeling.

**Referentie:**
- DM Sans (of equivalent sans): UI tekst, labels, buttons, body
- JetBrains Mono: data, cijfers, code, timestamps, IDs

**Check:**
- `font-family` tokens bevatten een sans + mono pairing
- Mono wordt specifiek gebruikt voor numerieke/data context
- Geen derde font in actief gebruik

**Fail als:** Alleen system fonts, geen bewuste pairing, of mono op niet-data elementen

---

## 5. Border-First Cards

**DNA:** Cards worden primair gedefinieerd door borders, niet door shadows. In dark mode zijn borders effectiever dan shadows.

**Referentie-waarden:**
- Driver: `--od-card-border: rgba(172,185,205,0.12)`, `--od-card-border-top: rgba(172,185,205,0.25)`
- Todo: `--border: rgba(148,163,184,0.22)`, `--border-subtle: rgba(148,163,184,0.18)`
- Beide: subtiele top-border (lighter) voor "lift" effect

**Check:**
- Cards hebben `border` declaratie
- Border opacity in range 0.08 – 0.30 (subtiel, niet hard)
- Optioneel: lichtere top-border voor depth

**Fail als:** Cards alleen met shadow, geen border, of harde borders (opacity >0.5)

---

## 6. Dual-Layer Shadows

**DNA:** Schaduwen gebruiken twee lagen: een brede diffuse schaduw + een scherpe close schaduw.

**Referentie-waarden:**
- Driver: `--od-card-shadow: 0 4px 24px rgba(0,0,0,0.55), 0 1px 3px rgba(0,0,0,0.4)`
- Todo: `--elevation-2: 0 18px 40px rgba(15,23,42,0.14)`

**Check:**
- Shadow tokens bevatten 2 comma-separated shadow layers
- Eerste laag: breed (>16px blur), laag opacity
- Tweede laag: scherp (1-4px blur), hogere opacity

**Fail als:** Single-layer shadows, of geen shadow-systeem (ad-hoc per component)

---

## 7. 120ms Micro-Transitions

**DNA:** Micro-interacties (hover, toggle, state change) gebruiken 120ms. Grotere transities (modals, page) mogen langer (200-300ms).

**Referentie:**
- Driver: transitions op hover/state changes
- Universeel: 100-150ms voelt "instant", 200-300ms voelt "smooth", >400ms voelt "traag"

**Check:**
- `transition-duration` op hover/state: 100-150ms range
- Geen `300ms` op kleine interacties
- Grotere transities (modal open/close): 200-300ms

**Fail als:** Alle transities >250ms, of geen transitions (instant/janky)

---

## 8. 44px Touch Targets

**DNA:** Alle interactieve elementen hebben minimaal 44×44px touch area (iOS HIG standaard).

**Referentie:**
- Todo: `--touch-target-min: 44px`
- Driver: buttons/inputs met adequate padding

**Check:**
- Buttons: `min-height: 44px` of padding die dit bereikt
- Links in nav: voldoende padding voor 44px hit area
- Icon buttons: ≥44px inclusief padding

**Fail als:** Buttons/links <36px hoogte, of compact links zonder voldoende padding

---

## 9. Uppercase Tracking-Widest Labels

**DNA:** Micro-labels en categorieën gebruiken uppercase + extra letter-spacing voor een "engineered" gevoel.

**Referentie:**
- `text-transform: uppercase` + `letter-spacing: 0.05em` – `0.1em` op:
  - Status badges
  - Section labels
  - Category tags
  - Metadata labels

**Check:**
- Zoek `text-transform: uppercase` + `letter-spacing` combinatie
- Gebruikt op labels/badges, niet op body text of headings

**Fail als:** Geen uppercase tracking, of uppercase zonder extra letter-spacing (ziet er gedrongen uit)

---

## 10. Groen Alleen voor Utility/Success

**DNA:** Groene accenten worden uitsluitend gebruikt voor success states en utility acties (confirm, save, active). Nooit als decoratie of primary brand kleur.

**Referentie-waarden:**
- Driver: `--od-success: rgba(134,239,172,0.95)`, `--od-success-bg: rgba(34,197,94,0.12)`
- Todo: `--success: #059669`, `--color-success-light: rgba(5,150,105,0.14)`
- Driver emerald action: `--od-emerald-action-bg: rgba(6,78,59,0.30)` (specifiek voor confirm/save)

**Check:**
- Groen alleen op: success toasts, confirm buttons, active/on toggles, "saved" indicators
- Niet op: navigation, headers, decoratieve elementen

**Fail als:** Groen als primary brand kleur, of groen op niet-success elementen

---

## Scoring

| Checks passed | Verdict |
|---------------|---------|
| 10/10 | **Pure Operator Dark** — volledig DNA-conform |
| 8-9/10 | **Sterk DNA** — kleine drift maar herkenbaar |
| 5-7/10 | **Gedeeltelijk** — inspiratie maar niet committed |
| <5/10 | **Ander systeem** — dit is geen Operator Dark |
