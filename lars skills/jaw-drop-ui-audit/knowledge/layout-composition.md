# Layout Composition & Content Overflow — Blinde vlekken

Dit document dekt layout-problemen die een code-only + token-only audit systematisch mist. Ze zijn alleen zichtbaar op een **gerenderde pagina met echte data**. Een audit die dit overslaat is onvolledig.

---

## Waarom dit apart staat

De bestaande 12 facetten dekken tokens, states, motion, responsive en color. Maar geen enkel facet checkt expliciet:

1. Hoe **secties intern gecomponeerd** zijn (heading + actions op één lijn?)
2. Hoe **echte content** zich gedraagt (lange emails, IDs die layouts breken)
3. Hoe **gerelateerde controls** visueel gegroepeerd zijn (filters + hun resultaten)

Dit zijn precies de problemen die een designer op het eerste screenshot ziet en die een LLM-audit mist als het alleen tokens en CSS telt.

---

## Check 1: Section Heading + Actions Alignment

**Wat je checkt:**
- Sectie-heading (titel + subtitel) en actie-knoppen staan op **dezelfde baseline/rij**
- Bij flex: `align-items: flex-start` of `center` — niet `stretch` waardoor knoppen uitrekken
- Knoppen naast heading: horizontaal (`flex-direction: row`), niet verticaal gestapeld
- Als er meerdere knoppen zijn: naast elkaar met consistent gap, niet onder elkaar tenzij bewust

**Detectie (code + visueel):**
- Zoek `flex-direction: column` op section-heading containers — verdacht als knoppen erin zitten
- Zoek `.od-section-heading` of equivalente heading+actions wrapper
- **Screenshot vereist**: code kan er correct uitzien maar op 1200px viewport toch breken

**Fail-signalen:**
- Heading links, knoppen rechts maar verticaal gestapeld (= onbedoeld column layout)
- Knoppen die "vallen" naar een volgende regel terwijl er ruimte is
- Heading en knoppen op verschillende verticale positie (niet aligned)

**Craft-referentie:**
```css
.section-heading {
  display: flex;
  align-items: flex-start; /* niet center als heading multi-line is */
  justify-content: space-between;
  gap: 16px;
}
.section-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0; /* voorkom dat knoppen krimpen */
}
```

---

## Check 2: Filter Bar Density & Action Separation

**Wat je checkt:**
- Filter bar heeft max 4-5 controls per rij op desktop
- **Actie-knoppen (submit/laden/zoeken) staan NIET in de filter-rij** — ze horen eronder of ernaast als een aparte groep
- Filters en hun "laden"/"zoeken" knop zijn visueel gescheiden (knop is geen "6e filter")
- Filter labels zijn leesbaar en niet te dicht op de inputs

**Detectie (code + visueel):**
- Tel `grid-template-columns` waarden: >5 = te druk
- Check of een submit/actie-button in dezelfde grid-row zit als filter-inputs
- **Screenshot vereist**: grid kan op papier kloppen maar visueel te druk zijn

**Fail-signalen:**
- 6+ controls op één rij (filters + actieknop)
- Submit/laden knop ziet eruit als een extra filter
- Filter labels overlappen of zijn onleesbaar door krapte
- Filters op mobile: nog steeds 3+ kolommen

**Craft-referentie:**
- Max 4 filters per rij op desktop
- Actieknop in aparte rij of visueel gescheiden groep
- Mobile: 1-2 filters per rij

---

## Check 3: Orphaned / Floating Elements

**Wat je checkt:**
- Elk element hoort visueel bij een groep (proximity principle)
- Status-indicators (pills, badges, counts) zijn visueel gekoppeld aan de data die ze beschrijven
- Geen elementen die "zweven" tussen secties zonder duidelijke groepering
- Summary-pills onder filters horen visueel bij de filterresultaten, niet los ertussen

**Detectie (visueel — niet te detecteren in code alleen):**
- Kijk of je een lijn kunt trekken om "wat bij wat hoort"
- Als een element evenveel afstand heeft tot de sectie erboven als eronder: het zweeft
- Status-pills zonder container/achtergrond die los tussen secties hangen

**Fail-signalen:**
- Count-pills ("13 shifts", "0 goedgekeurd") zonder visuele container of proximity-grouping
- Samenvattingsrij die geen onderdeel lijkt van de filter-sectie of de data-sectie
- Metadata die "in de lucht hangt" tussen twee cards

**Craft-referentie:**
- Summary/status pills direct onder de filter bar, in dezelfde card/container
- Of: als inline-text in de section heading
- Nooit: los zwevend met gelijke spacing boven en onder

---

## Check 4: Flex Row Vertical Alignment (Ongelijke Content)

**Wat je checkt:**
- Flex rows met ongelijke content height (bijv. 3 regels tekst links, 1 regel pills rechts)
- `align-items` is bewust gekozen: `flex-start` voor multi-line content, `center` voor single-line
- Items zijn **optisch** uitgelijnd, niet alleen technisch

**Detectie (code + visueel):**
- Zoek flex containers met `justify-content: space-between` — check `align-items`
- Multi-line heading links + single-line actions rechts: `align-items: center` maakt de heading "naar beneden zakken" terwijl pills "te hoog" zitten
- **Screenshot vereist**: `align-items: center` ziet er in code correct uit maar visueel niet

**Fail-signalen:**
- Topbar: heading+subtitle links (3 regels), pills rechts (1 rij) — pills zweven halverwege
- Card header: naam+email links (2 regels), status pill rechts (1 rij) — pill staat te hoog
- Section heading: titel+beschrijving links, knoppen rechts — knoppen staan niet op heading-niveau

**Craft-referentie:**
- Multi-line links + single-line rechts: `align-items: flex-start` zodat rechts op de eerste regel staat
- Of: `align-items: baseline` als de eerste regel aan beide kanten gelijk moet zijn

---

## Check 5: Content Overflow & Text Truncation

**Wat je checkt:**
- Lange content (emails, URLs, IDs, namen) breekt de layout NIET
- `text-overflow: ellipsis` + `overflow: hidden` + `white-space: nowrap` op containers met onvoorspelbare tekst
- `max-width` op data-velden die onbeperkt kunnen groeien
- Tooltip of expand-on-click voor afgekapte content (zodat de volledige waarde nog bereikbaar is)

**Detectie (code + visueel):**
- Zoek email-velden, ID-velden, naam-velden in componenten
- Check of er `truncate`/`overflow`/`text-overflow` classes zijn
- **Test met lange data**: vul een email van 60+ tekens in en kijk of het breekt
- **Screenshot vereist**: code kan `max-width` missen terwijl korte testdata het verbergt

**Fail-signalen:**
- Email als `alexander.vicero+driverapp-real-1773329372918@gmail.com` neemt de volle breedte
- Lange namen/bedrijfsnamen duwen andere kolommen/elementen opzij
- Tabel-kolommen worden disproportioneel breed door één lange waarde
- ID-strings wrappen naar meerdere regels in compacte gebieden

**Craft-referentie:**
```css
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 240px; /* contextafhankelijk */
}
```

---

## Check 6: Section Gap Proportionality

**Wat je checkt:**
- Gap tussen hero/summary en content is groter dan gap tussen peer-secties
- Gap tussen peer-secties is groter dan gap binnen secties
- Geen "gaten" — lege ruimte die geen doel dient
- De ruimte tussen secties communiceert de relatie: meer ruimte = minder verwant

**Detectie (code + visueel):**
- Check `gap`/`margin` op de hoofd-container (bijv. `od-stack`)
- Als alle secties dezelfde gap hebben: **geen proportionaliteit**, alles voelt even verwant
- **Screenshot vereist**: een uniform `gap: 24px` kan er in code consistent uitzien maar visueel als "gaten" voelen tussen ongelijk grote secties

**Fail-signalen:**
- Metric cards (klein) → 24px gap → data section (groot): de gap voelt als een scheiding, niet als een pauze
- Twee gerelateerde secties (filters + resultaten) hebben dezelfde gap als twee ongerelateerde secties
- Summary-sectie en detail-sectie lijken los van elkaar door te veel gap

**Craft-referentie:**
- Hero → content: 32-40px
- Peer sections: 24px
- Within section: 12-16px
- Gerelateerde subsecties: 8-12px

---

## Integratie met de 12 audit-facetten

Deze checks versterken bestaande facetten maar zijn alleen betrouwbaar te checken met **screenshots + echte data**:

| Check | Primair facet | Secundair |
|-------|--------------|-----------|
| 1. Section heading+actions | Facet 1 (Visual Hierarchy) | Facet 6 (Component Consistency) |
| 2. Filter bar density | Facet 3 (Spacing & Rhythm) | Facet 9 (Responsive) |
| 3. Orphaned elements | Facet 3 (Spacing & Rhythm) | Facet 1 (Visual Hierarchy) |
| 4. Flex row alignment | Facet 3 (Spacing & Rhythm) | Facet 6 (Component Consistency) |
| 5. Content overflow | Facet 9 (Responsive & Touch) | Facet 6 (Component Consistency) |
| 6. Section gap proportionality | Facet 3 (Spacing & Rhythm) | Facet 1 (Visual Hierarchy) |

---

## Hard rule voor de audit

> **Een audit die alleen CSS tokens en code inspecteert zonder de gerenderde pagina met echte (of realistische) data te bekijken, is onvolledig. Layout compositie en content overflow zijn alleen betrouwbaar te beoordelen op een screenshot of live pagina.**

Als er geen screenshot of browser-toegang beschikbaar is:
- Markeer facetten 1, 3, 6, 9 als `UNKNOWN (niet visueel geverifieerd)`
- Geef exact aan welke visuele checks ontbreken
- Claim NOOIT 10/10 op spacing, hierarchy of responsive zonder visueel bewijs
