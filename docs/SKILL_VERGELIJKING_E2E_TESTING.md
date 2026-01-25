# Skill Vergelijking: E2E Testing

## Twee Benaderingen

| | Lars (e2e-validate) | Alexander (test-guard-driver-app) |
|---|---|---|
| **Regels** | 507 | 224 |
| **Focus** | Alles-in-één QA proces | Specifiek: discovery + scaffolds |
| **Mocks** | Niet expliciet verboden | **VERBODEN** |
| **Fallbacks** | Toegestaan | **VERBODEN** |
| **Coverage** | Geen minimum | **100% vereist** |
| **Buttons** | Niet specifiek | **Alle buttons getest** |

---

## Lars: e2e-validate

### Wat het doet
Een uitgebreide "Senior QA Engineer" persona die het volledige testproces doorloopt:
1. Project detectie
2. Requirement extraction
3. Test plan generatie
4. Test execution
5. Result reporting
6. Continuous validation

### Problemen

**1. Te veel verantwoordelijkheden**
De skill probeert tegelijk:
- Requirements analyst te zijn
- Test planner te zijn
- Test executor te zijn
- Reporter te zijn
- Debugger te zijn

Dit leidt tot een skill die 507 regels lang is maar geen enkele taak uitstekend doet.

**2. Geen harde grenzen**
```
⚠️ SKIP │ OAuth flow
        │ Reden: Geen test credentials beschikbaar
```
Dit is een escape hatch. De skill accepteert dat dingen NIET getest worden.

**3. Dramatische framing**
```
Je werkt bij een Fortune 500 bedrijf waar bugs = ontslagen.
```
Dit voegt niets toe aan de kwaliteit van de tests.

**4. Mock-vriendelijk**
De skill zegt nergens expliciet dat mocks verboden zijn. Dit opent de deur naar:
- Fake data
- Gesimuleerde responses
- Tests die slagen maar niets valideren

---

## Alexander: test-guard-driver-app

### Wat het doet
Gefocuste skill met één doel: ontdek wat getest moet worden en genereer scaffolds.

### Waarom het werkt

**1. Absolute regels zonder uitzonderingen**
```markdown
1. **100% COVERAGE** - Elke invariant, elke button, elke flow wordt getest
2. **GEEN MOCKS** - Test tegen echte services, echte API's, echte data
3. **GEEN FALLBACKS** - Test faalt = bug, geen "graceful degradation" excuses
4. **ALLE BUTTONS** - Elke button in de UI krijgt een E2E test
```

Er is geen "skip" optie. Er is geen "later doen". Het werkt of het werkt niet.

**2. Blokkerende coverage check**
```
Als coverage < 100%: **BLOKKEER** en toon wat mist.
```

De skill stopt letterlijk als niet alles getest is. Geen workarounds.

**3. Button inventory**
```bash
grep -r "<button\|<Button\|onClick=" components/ app/ pages/
```

Elke button wordt gevonden en krijgt een test. Geen UI element blijft ongetest.

**4. Concrete output**
```
docs/INVARIANTS.md      → Wat mag NOOIT gebeuren
docs/BUTTON-INVENTORY.md → Alle buttons met test status
e2e/*.spec.ts           → Playwright tests
```

Je weet exact wat je krijgt.

---

## Waarom Alexander's Benadering Wint

### 1. Mocks zijn leugens

Mocks testen je mock, niet je systeem.

```typescript
// LARS APPROACH - Mock
await page.route('**/api.telegram.org/**', async (route) => {
  await route.fulfill({ status: 200, body: JSON.stringify({ ok: true }) });
});
// Test slaagt! Maar werkt Telegram echt? Niemand weet het.

// ALEXANDER APPROACH - Echte call
// Test faalt als Telegram niet werkt. Goed. Dan weet je het.
```

### 2. Fallbacks verbergen bugs

```
// LARS: "Graceful degradation"
if (telegramFails) {
  return fallbackBehavior(); // Bug verborgen achter fallback
}

// ALEXANDER: Geen fallback
// Telegram faalt = test faalt = bug = fix it
```

### 3. 100% coverage dwingt kwaliteit af

Met Lars kun je 67% coverage hebben en "klaar" zijn.
Met Alexander moet alles werken. Geen uitzonderingen.

### 4. Minder is meer

224 regels die precies doen wat nodig is > 507 regels die alles half doen.

---

## Praktijkvoorbeeld

**Scenario:** Login button werkt niet op mobile

**Lars approach:**
1. Test draait met mocks
2. Mock zegt "200 OK"
3. Test slaagt
4. Bug in productie
5. Gebruiker kan niet inloggen
6. Support ticket

**Alexander approach:**
1. Button inventory vindt login button
2. Test draait tegen echte service
3. Test faalt op mobile viewport
4. Bug gevonden vóór productie
5. Fix toegepast
6. Geen support ticket

---

## Conclusie

| Criterium | Lars | Alexander |
|-----------|------|-----------|
| Vindt echte bugs | ❌ Mocks verbergen ze | ✅ Geen mocks |
| Dwingt kwaliteit af | ❌ Skips toegestaan | ✅ 100% of blokkeer |
| Simpel te gebruiken | ❌ 507 regels lezen | ✅ `/test-guard-driver-app` |
| Voorspelbare output | ❌ Varieert per run | ✅ Altijd dezelfde files |

**Alexander's skill wint omdat het geen excuses accepteert.**

De beste test is niet de test die slaagt. De beste test is de test die faalt wanneer er een bug is.
