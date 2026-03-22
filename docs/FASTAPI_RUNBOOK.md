# FastAPI Operator Runbook (Reusable)

Doel: een **deterministische** checklist om te verifiëren dat een FastAPI service (en eventuele UI proxy) echt werkt.

> Veiligheid: commit nooit secrets. Gebruik `.env`/secret stores.

---

## 1) Minimal env contract (aanbevolen)

Veel JVDP apps beschermen admin/config endpoints met een API key header.

- `ADMIN_API_KEY` (single key) **of** `ADMIN_API_KEYS` (rotatie; comma/semicolon-separated)
- Optioneel: `CORS_ORIGINS` (restrictive default is prima)

Als je service dependency checks doet (bijv. Pipedrive/Drive/OSRM), zet die env vars ook.

---

## 2) Start de service (voorbeeld)

Gebruik bij voorkeur repo-eigen scripts (start/stop) om port conflicts te voorkomen.

Voorbeeld:

```bash
uvicorn your_module.app:app --host 127.0.0.1 --port 8000
```

---

## 3) Verify HTTP surface (curl)

### 3.1 Liveness (publiek)

```bash
curl -s http://127.0.0.1:8000/health/live | jq .status
```

Verwacht:
- HTTP 200
- JSON met `status: ok` (of equivalent)

### 3.2 Readiness (meestal admin-protected)

Zonder admin key moet dit **401** zijn (auth enforced):

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/health/ready
```

Met admin key moet dit **200** zijn:

```bash
curl -s -H "X-Admin-Key: $ADMIN_API_KEY" http://127.0.0.1:8000/health/ready | jq .status
```

### 3.3 OpenAPI contract

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/openapi.json
```

Verwacht:
- HTTP 200
- JSON met `openapi` key

---

## 4) Verify auth enforcement (admin endpoints)

Als je app admin endpoints heeft (config/dashboard/pipedrive/etc):

- Zonder `X-Admin-Key`: **401**
- Met `X-Admin-Key`: **200**

Voorbeeld patroon:

```bash
# no auth
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/dashboard/config

# with auth
curl -s -o /dev/null -w "%{http_code}\n" -H "X-Admin-Key: $ADMIN_API_KEY" http://127.0.0.1:8000/dashboard/config
```

---

## 5) Frontend proxy (Vite/Next/etc) – optioneel

Als je UI een proxy naar backend heeft (bijv. `/api/*`):

- UI root moet **200** geven
- Proxy endpoint moet backend kunnen bereiken
- Indien nodig moet de proxy **X-Admin-Key** injecteren

Voorbeeld:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:34002/
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:34002/api/dashboard/config
```

---

## 6) Playwright E2E: minimale API checks (aanbevolen)

Als je Playwright gebruikt, maak minstens:
- liveness test
- readiness test (met en zonder auth)
- een admin endpoint test

Voorbeeld (Playwright `request` fixture):

```ts
const API_BASE = 'http://localhost:8000';

test('ready requires auth', async ({ request }) => {
  const r = await request.get(`${API_BASE}/health/ready`);
  expect(r.status()).toBe(401);
});

test('ready works with auth', async ({ request }) => {
  const r = await request.get(`${API_BASE}/health/ready`, {
    headers: { 'X-Admin-Key': process.env.ADMIN_API_KEY! },
  });
  expect(r.status()).toBe(200);
});
```

---

## 7) Pipedrive v1 → v2 migratie

Als je app Pipedrive gebruikt: zie `docs/PIPEDRIVE_V1_TO_V2_MIGRATION_PLAYBOOK.md`.

Kernverificaties daar:
- `x-api-token` header (v2 auth)
- cursor pagination (`additional_data.next_cursor`)
- `custom_fields` nesting
- `field_code/field_name` normalisatie

