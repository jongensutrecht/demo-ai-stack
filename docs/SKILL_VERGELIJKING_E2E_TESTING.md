# Skill Vergelijking: E2E Testing

> Lars (e2e-validate) vs Alexander (test-guard-driver-app)

## TL;DR

| Aspect | Lars | Alexander |
|--------|------|-----------|
| **Anti-mock** | ✅ Ja | ✅ Ja |
| **Coverage** | 67-87% OK | **100% of blokkeer** |
| **Skip optie** | ✅ Toegestaan | ❌ Niet mogelijk |
| **Button testing** | Impliciet | **Expliciet verplicht** |
| **Fallbacks** | Niet genoemd | **Verboden** |
| **Scope** | Generiek | Driver-app specifiek |

**Conclusie**: Beide skills zijn anti-mock. Het verschil zit in **coverage eisen** en **skip mogelijkheden**.

---

## Gedeelde Principes

Beide skills zijn het eens over:

### Anti-Mock
**Lars:**
```
❌ VERBODEN:
- Mock data gebruiken als echte data beschikbaar is
```

**Alexander:**
```
2. **GEEN MOCKS** - Test tegen echte services, echte API's, echte data
```

### Anti-Fake Data
**Lars:**
```
NOOIT:
- Hardcoded test values (tenzij uit spec)
- "Example" data
- Verzonnen user credentials
- Fictieve scenarios
```

**Alexander:**
```
6. **Geen hallucinatie** - Als iets niet bestaat, niet testen
```

### Evidence-Based Testing
**Lars:**
```
Voor ELKE test assertion:
1. BRON: Waar komt de expected value vandaan?
2. LOCATIE: Welk bestand/regel/endpoint?
3. VERIFICATIE: Hoe weet je dat dit correct is?
```

**Alexander:**
```
**Test status:** ✅ Tested / ❌ Needs test
**Locatie:** [file:line]
```

---

## Waar Ze Verschillen

### 1. Coverage Eisen

**Lars accepteert minder dan 100%:**
```
📊 Coverage Report:
✅ Tested: 6/12 invariants
❌ Needs test: 5/12
⚠️ Needs verification: 1/12

TOTAAL: 4/6 PASSED (67%)
```

**Alexander blokkeert bij < 100%:**
```
Als coverage < 100%: **BLOKKEER** en toon wat mist.

TOTAAL: 100% COVERAGE ✅
```

### 2. Skip Mogelijkheid

**Lars staat SKIP toe:**
```
⚠️ SKIP │ OAuth flow
        │ Reden: Geen test credentials beschikbaar
        │ Actie: User moet OAuth tokens configureren

⚠️ SKIP │ Route planning (blocked by API)
```

**Alexander heeft geen skip:**
Er is simpelweg geen `⚠️ SKIP` status. Alleen `✅ Tested` of `❌ Needs test`.

### 3. Button Testing

**Lars:** Buttons zijn onderdeel van "UI tests" maar niet expliciet geïnventariseerd.

**Alexander:** Expliciete button discovery en inventory:
```
2. BUTTON INVENTORY → alle buttons uit UI
   - Scan componenten voor <button>, <Button>, onClick handlers
   - Maak lijst: button tekst/id → verwachte actie
   - Elke button = 1 E2E test

Output: docs/BUTTON-INVENTORY.md
```

### 4. Fallback Handling

**Lars:** Niet expliciet genoemd. Impliceert dat graceful degradation OK is als het gedocumenteerd wordt.

**Alexander:** Expliciet verboden:
```
3. **GEEN FALLBACKS** - Test faalt = bug, geen "graceful degradation" excuses
```

### 5. Scope & Complexiteit

**Lars (507 regels):**
- 6 fases (detectie → extraction → planning → execution → reporting → continuous)
- Prioriteiten systeem (P0-P3)
- Requirements matrix generatie
- Flaky test detectie
- Meerdere output files (test-requirements.md, test-plan.md, test-reports/)

**Alexander (224 regels):**
- 5 stappen (discover → buttons → invariants → tests → coverage check)
- Geen prioriteiten (alles is P0)
- Gefocuste output (INVARIANTS.md, BUTTON-INVENTORY.md, e2e/*.spec.ts)

---

## Wanneer Welke Skill?

### Gebruik Alexander (test-guard-driver-app) als:

- Je **100% coverage** wilt afdwingen
- Je **geen excuses** wilt voor ontbrekende tests
- Je werkt aan **driver-app-gps** specifiek
- Je **alle buttons** expliciet wilt testen
- Je **fallbacks als bugs** wilt behandelen
- Je een **kortere, directere** workflow wilt

### Gebruik Lars (e2e-validate) als:

- Je **flexibiliteit** nodig hebt in coverage
- Je met **beperkte resources** werkt (skip low-priority tests)
- Je een **requirements matrix** nodig hebt voor stakeholders
- Je **flaky tests** wilt detecteren
- Je op **meerdere projecten** dezelfde skill wilt gebruiken
- Je **prioriteiten** wilt stellen (P0 vs P3)

---

## Voor Driver-App-GPS: Alexander Wint

De driver-app-gps heeft specifieke eisen:

| Eis | Lars | Alexander |
|-----|------|-----------|
| GPS tracking moet ALTIJD werken | Skip mogelijk | ✅ Geen skip |
| Alle shift buttons moeten werken | Impliciet | ✅ Button inventory |
| Geen fallback naar fake locatie | Niet expliciet | ✅ Fallbacks verboden |
| 100% van kritieke flows getest | 67% OK | ✅ 100% verplicht |

**Alexander's skill is gebouwd voor driver-app-gps. Lars's skill is gebouwd voor elk project.**

---

## Samenvatting

```
┌─────────────────────────────────────────────────────────────┐
│                    BEIDE SKILLS                             │
│  ✅ Anti-mock                                               │
│  ✅ Anti-fake data                                          │
│  ✅ Evidence-based testing                                  │
│  ✅ Playwright voor E2E                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────┐    ┌─────────────────────────────┐
│      LARS               │    │      ALEXANDER              │
│                         │    │                             │
│  Coverage: flexibel     │    │  Coverage: 100% verplicht   │
│  Skip: toegestaan       │    │  Skip: niet mogelijk        │
│  Buttons: impliciet     │    │  Buttons: expliciet         │
│  Fallbacks: niet genoemd│    │  Fallbacks: verboden        │
│  Scope: generiek        │    │  Scope: driver-app-gps      │
│  Regels: 507            │    │  Regels: 224                │
└─────────────────────────┘    └─────────────────────────────┘
```

**De keuze is niet "goed vs slecht" maar "flexibel vs strict".**

Voor driver-app-gps waar GPS en shifts MOETEN werken: **Alexander**.
Voor een generiek project met resource constraints: **Lars**.
