# BMAD Input — Admin Uren Approval + Export (Accountant)

Doel: dit document is de primaire bron voor story-generatie en implementatie-instructies voor de **Admin Uren Approval Flow** in `driver_app_gps`, inclusief **accountant-proof CSV export**.

Regels:
- **Geen gokken**: als iets niet bewezen is uit repo-code of expliciet door Alexander is bevestigd, markeer als `UNKNOWN` en stel eerst 1–2 korte vragen.
- **Bestaande code behouden**: alleen **additieve** wijzigingen (geen refactors) en **geen breaking changes** aan bestaande API responses.
- **Geen implementatie in dit document**: dit is requirements + uitvoerbare instructies voor later.

---

## Context

- Repo: `driver_app_gps`
- Huidige feature: Admin-only dashboard `/admin/uren` toont shifts uit Google Sheets tab **"Uren"**.
- Databron: Google Sheets (source of truth).
- Export bestemming: **accountant** (payroll processing).

### Huidige relevante bestanden (repo-aligned)

- Frontend:
  - `web/src/pages/AdminUren.tsx` (admin dashboard UI)
  - `web/src/lib/api.ts` (API client; `api.patch()` bestaat al)
- Backend:
  - `api/admin/shifts.ts` (GET `/api/admin/shifts?from&to` bestaat)
  - `api/shifts/end.ts` (schrijft shifts naar Sheets; bevat al `status/approved_by/approved_at` in HEADER en zet nieuwe shifts op `pending`)
  - `lib/sheets.ts` (Sheets read/append helpers; mist nu een generieke “update row by key” helper)
  - `lib/auth.ts` (`requireAdmin()` is server-side gate)
  - `server.mjs` (lokale dev router mapping; heeft nu alleen exact `/api/admin/shifts`)
- Specs:
  - `docs/features/admin-uren-dashboard.md` (bestaande feature spec)
  - `docs/features/admin-uren-approval-prompt.md` (huidige prompt die geüpdatet moet worden door dit BMAD input)
  - `openspec/specs/shifts/spec.md`

### Google Sheets tab "Uren" — bekende kolommen

Huidig in spec/hand-off (historisch):

`date | employee_name | email | shift_id | start_ts | end_ts | duration_minutes | source | device_id | notes`

Feit uit code (`api/shifts/end.ts`): shifts worden al weggeschreven met extra kolommen:

`... | notes | status | approved_by | approved_at`

Conclusie:
- De code kan al “pending” schrijven, maar de echte sheet header kan achterlopen → **migratie blijft noodzakelijk**.

---

## Doel (wat de planner/urenregistratiemedewerker wil)

- Snel “pending” uren verwerken (approve/reject, ook in bulk).
- Geen discussie achteraf: “wie/wanneer/waarom” moet traceerbaar zijn.
- Export die direct bruikbaar is voor de accountant (Excel NL), met voorspelbare kolommen en filters.
- Geen dataverlies: chauffeur-input blijft intact; admin notities/audit los daarvan.

---

## Must-haves (P0)

### P0.1 — Approval datamodel (Sheets)

**Additieve schema-uitbreiding** in tab “Uren”:

- Voeg kolommen toe (rechts van bestaande):
  - `status`: `"pending" | "approved" | "rejected"` (default: `"pending"`)
  - `approved_by`: email van admin die actie deed (leeg bij pending)
  - `approved_at`: ISO timestamp (leeg bij pending)
  - `admin_notes`: admin-only notitie (leeg)

**Waarom `admin_notes` verplicht is (planner-proof):**
- `notes` wordt door chauffeurs gebruikt als context (“lekke band”), en mag niet overschreven worden door admin → anders verlies je bewijs bij disputes.

**Migratie/backfill eisen:**
- Header row moet worden uitgebreid als die al bestaat (niet alleen “als leeg”).
- Bestaande rijen:
  - lege/missende `status` → zet `status` op `"pending"`
  - laat `approved_by/approved_at` leeg
  - `admin_notes` leeg

### P0.2 — Backend API (admin-only) voor approve/reject + notities

**Belangrijk (repo-constraint):** minimaal riskante routing, zodat het zowel lokaal (`server.mjs`) als in productie (Vercel file-based functions) werkt **zonder** extra nested routes.

Daarom: **1 patch endpoint** (geen `/batch` of `/:id` paths), zodat `server.mjs` niet uitgebreid hoeft te worden.

#### Endpoint: `PATCH /api/admin/shifts`

**Admin check:** verplicht via `requireAdmin()` (server-side).

**Operation dispatch (body-based):**
- Single update (approve/reject en/of admin_notes):
  - Body: `{ shiftId: string, status?: "approved"|"rejected", admin_notes?: string }`
- Batch update:
  - Body: `{ shiftIds: string[], status: "approved"|"rejected" }`

**Semantiek (hard):**
- Status change:
  - `status` wordt gezet
  - `approved_by = session.email`
  - `approved_at = nowUtcIso()`
- Reject is ook een “review action”:
  - bij `rejected` worden `approved_by/approved_at` óók gevuld (audit: wie/wanneer heeft afgekeurd)
- Notes-only change:
  - update alleen `admin_notes`
  - **verander `approved_by/approved_at` niet**

**Response (hard):**
- Single: HTTP 200 met “updated shift object”
- Batch: HTTP 200 met `{ updated: number, failed: string[] }`

**Error contract (fail-fast):**
- 400: invalid body (missende shiftId(s), ongeldige status, verkeerde types)
- 403: admin required
- 404: shiftId(s) niet gevonden
- 500: Sheets read/update failed

**Normalisatie voor frontend eenvoud:**
- `status` ontbreekt of `""` → `"pending"`
- `approved_by/approved_at` lege string → `null` in API response (consistent)

### P0.3 — Approval UI in AdminUren

#### Status badge kolom
- Voeg kolom toe tussen “Duur” en “Notities”:
  - Pending: `text-amber-600 bg-amber-50`
  - Approved: `text-green-600 bg-green-50` met `✓`
  - Rejected: `text-red-600 bg-red-600 bg-red-50` met `✗`

#### Acties per rij (alleen bij pending)
- Laatste kolom: “Acties”
- Alleen zichtbaar als `status === "pending"`:
  - `[✓ Approve] [✗ Reject]` (compact)
- UX:
  - loading state per rij tijdens PATCH
  - foutmelding gebruikersvriendelijk (geen PII)
  - update-na-succes is OK (optimistic alleen met rollback)

#### “Wie + wanneer”
- Bij `approved` of `rejected` toon onder badge:
  - `door <localpart> • <korte datum>`
  - localpart = deel vóór `@` van `approved_by`
  - styles: `text-xs text-gray-400`

#### Batch approve/reject
- Checkbox kolom als eerste kolom
  - per rij checkbox alleen bij `pending`
  - header checkbox: selecteer alle **zichtbare pending** (na filters)
- Action bar:
  - fixed onderaan viewport óf sticky in tabel-container — `UNKNOWN` (kies 1 en leg vast)
  - toont: `X geselecteerd` + knoppen:
    - “Geselecteerde goedkeuren”
    - “Geselecteerde afwijzen”
    - “Wissen”
  - disabled tijdens batch request
  - na succes: selectie leeg (optioneel: bij partial failure alleen failed geselecteerd — `UNKNOWN`)

### P0.4 — Overzichten (UI-only, parallel)

#### Uren per chauffeur (collapsible)
- Component boven tabel (na summary stats), standaard open
- Groepeer op `employee_name` (leeg → “Onbekend”)
- Toon per chauffeur:
  - naam
  - progress bar relatief aan hoogste totaal in lijst
  - **totaal uren** en **goedgekeurde uren** apart
- Klik op rij → zet chauffeur filter

#### Maand-view toggle
- Breid bestaande toggle uit: `[Dag] [Week] [Maand]`
- Maand range:
  - from = eerste dag maand van `selectedDate`
  - to = laatste dag maand
  - Bereken timezone-safe op basis van `YYYY-MM-DD` string (niet via `toISOString()` voor local date logica)

### P0.5 — Admin notes inline edit

- Inline edit op admin-notitie kolom (UI label: “Admin notitie” of “Notities (admin)”)
- Flow:
  - view state: tekst + edit icon
  - edit state: input + save + cancel
  - Enter/save → PATCH
  - Escape/cancel → herstel
  - loading state tijdens save
- Werkt voor alle statussen (pending/approved/rejected)

### P0.6 — CSV export (accountant)

**Belangrijk voor accountant:** export moet Excel NL friendly zijn en voorspelbaar. In export hoort alleen payroll-relevante info, zonder device_id.

#### UI
- Export knop in controls bar (naast filters), met dropdown:
  - “Alle shifts” (review/export intern)
  - “Alleen goedgekeurd” (default voor accountant)
- Export gebruikt **huidige filters**:
  - periode (dag/week/maand)
  - chauffeur filter
  - (status filter, als die bestaat) — `UNKNOWN` (aanrader: respecteer statusfilter)
- Lege dataset → export disabled

#### CSV format (hard)
- Separator: `;` (NL Excel)
- Encoding: UTF‑8 met BOM
- Newlines: CRLF
- Escaping:
  - velden met `;` of `"` of newline → wrap in quotes
  - quotes in veld → verdubbel quotes (`"` → `""`)

#### CSV kolommen (hard, voor accountant)
`Datum;Chauffeur;Start;Eind;Duur (min);Status;Goedgekeurd door;Notities`

- Datum: `YYYY-MM-DD`
- Start/Eind: `HH:mm` of leeg als ontbreekt
- Status: `pending|approved|rejected`
- Goedgekeurd door:
  - Voor accountant: **verkort** (localpart + `@`, bv `alexander@`) om PII te beperken maar wel audit hint te houden
  - Volledige email blijft opgeslagen in Sheet (`approved_by`)
- Notities:
  - Gebruik `admin_notes` (niet chauffeur `notes`) voor accountant export, zodat het “payroll context” is.

#### Bestandsnaam (hard)
- dag: `uren_dag_<YYYY-MM-DD>.csv`
- week: `uren_week_<from>.csv`
- maand: `uren_maand_<YYYY-MM>.csv`

---

## Should-haves (P1)

- Status filter in UI: all | pending | approved | rejected
- Sorting (UI-only): datum desc, start asc
- Partial failure UX bij batch:
  - toon “X updated / Y failed”
  - failed ids niet als PII; eventueel “retry failed” knop

---

## Constraints / guardrails (project bindend)

- GEEN nieuwe npm dependencies
- GEEN refactoring (alleen additieve, minimale wijzigingen)
- GEEN breaking changes aan bestaande API responses
- TypeScript strict mode
- Tailwind CSS consistent met bestaand design
- Error handling met gebruikersvriendelijke meldingen
- Loading states voor alle async acties
- Mobile responsive (tabel horizontaal scrollbaar)
- Security:
  - Admin-only server-side gate (requireAdmin)
  - Geen secrets/PII in logs/toasts/Sentry
- Verplicht voor “klaar”:
  - `npm run lint`
  - `npm run typecheck`
  - `npm run test:all`
  - `openspec validate --all --strict --no-interactive`

---

## Out-of-scope

- Overtime/toeslagen/pauzes berekenen
- Nieuwe database/infra
- Undo approve via UI (terug naar pending) — tenzij expliciet toegevoegd
- Automatische payroll integratie met externe systemen (alleen CSV)

---

## Verification checklist (functioneel)

- `npm run dev` werkt
- `/admin/uren` laadt shifts
- Status badge toont correct
- Approve werkt → status + approved_by/approved_at opgeslagen + UI toont “door … • …”
- Reject werkt → idem
- Batch select + approve/reject werkt
- “Uren per chauffeur” toont en is klikbaar
- Maand-view toggle werkt (range klopt)
- Admin notes inline edit + save werkt (en overschrijft chauffeur notes niet)
- CSV download:
  - “Alle shifts” exporteert gefilterde data
  - “Alleen goedgekeurd” exporteert alleen approved
  - CSV opent correct in NL Excel (separator + encoding)

---

## Bronnen (repo-relative)

- `docs/features/admin-uren-dashboard.md`
- `docs/features/admin-uren-approval-prompt.md`
- `api/admin/shifts.ts`
- `api/shifts/end.ts`
- `lib/sheets.ts`
- `lib/auth.ts`
- `server.mjs`
- `web/src/pages/AdminUren.tsx`
- `web/src/lib/api.ts`
- `openspec/specs/shifts/spec.md`

