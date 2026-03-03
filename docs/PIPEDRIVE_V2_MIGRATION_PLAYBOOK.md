# Pipedrive API v2 Migration Playbook (for all JVDP apps)

This document is a **repeatable procedure** to migrate any internal app that talks to Pipedrive from **API v1** to **API v2**.

It is based on:
- **Official Pipedrive docs** (auth, pagination, v2 migration guide)
- The **eventfoto-pipeline-seo-gbp** implementation (this repo)
- The **jongensutrecht/aanvraag_offerte** implementation (reference repo)

> Safety: never commit secrets. Put tokens only in local `.env` / secret stores.

---

## 0) What v2 changes (the checklist you must implement)

### v2 changes you must handle
1. **Base URL becomes tenant-specific**
   - v1: `https://api.pipedrive.com/v1`
   - v2: `https://<companydomain>.pipedrive.com/api/v2`

2. **Auth for API token integrations is header-based**
   - v2 requires header **`x-api-token: <token>`**

3. **Pagination switches from offset to cursor**
   - v1 uses `start` + `limit` and returns `additional_data.pagination.*`
   - v2 uses `cursor` + `limit` and returns `additional_data.next_cursor`

4. **Custom fields move under `custom_fields`**
   - v1: custom field hashes are often present at the **root** of an entity
   - v2: entity custom field hashes live under **`custom_fields`**

5. **Fields API response keys changed** (this breaks mapping validators)
   - v1 fields: `key` + `name`
   - v2 fields: `field_code` + `field_name`

---

## 1) Official docs (source of truth)

### Authentication (API token)
Pipedrive docs (API token integration):
- https://pipedrive.readme.io/docs/core-api-concepts-authentication

The docs include this example:

```bash
curl --request GET \
  --url "https://companydomain.pipedrive.com/api/v2/deals" \
  --header "x-api-token: <YOUR_TOKEN>"
```

### Pagination
- https://pipedrive.readme.io/docs/core-api-concepts-pagination

Key contract:
- `additional_data.next_cursor` is **null** at the end.

### v2 migration guide
- https://pipedrive.readme.io/docs/pipedrive-api-v2-migration-guide

Key contract:
- Custom fields moved to `custom_fields`
- Offset pagination replaced by cursor pagination
- Fields API uses `field_code` + `field_name`

### OpenAPI specs (useful for schema/contract checks)
- v2: https://developers.pipedrive.com/docs/api/v2/openapi.yaml
- v1: https://developers.pipedrive.com/docs/api/v1/openapi.yaml

### Rate limiting (important for bulk backfills)
- https://pipedrive.readme.io/docs/core-api-concepts-rate-limiting

### Webhooks v2 (if your app creates/consumes webhooks)
- https://pipedrive.readme.io/docs/guide-for-webhooks-v2

---

## 2) Choose your config strategy (recommended)

### Strategy A (simple, preferred for scripts/CLIs)
Set one env var:
- `PIPEDRIVE_BASE_URL=https://<tenant>.pipedrive.com/api/v2`

Plus:
- `PIPEDRIVE_API_TOKEN=...`

This is what **eventfoto-pipeline-seo-gbp** supports.

### Strategy B (auto-build base URL)
Use two env vars:
- `PIPEDRIVE_API_VERSION=v2`
- `PIPEDRIVE_COMPANY_DOMAIN=<tenant>`

This is what **aanvraag_offerte** uses in `src/adapters/pipedrive/http_factory.py`.

> Recommendation for a multi-app ecosystem: implement **both**.
> Rule: if `PIPEDRIVE_BASE_URL` is set, it wins; else build from VERSION+DOMAIN.

---

## 3) Implementation patterns (copy/paste mental model)

### 3.1 HTTP client: v2 header auth
**Must** send:
- header `x-api-token` (not `Authorization: Bearer` and not only query param)

Eventfoto implementation:
- `src/pipedrive/client.py` adds header `x-api-token`

Aanvraag_offerte implementation:
- `src/adapters/pipedrive/http_factory.py` sets `headers={"x-api-token": api_token}` for v2.

### 3.2 Pagination: cursor loop
Pseudo:

```python
cursor = None
while True:
    params = {"limit": 200}
    if cursor:
        params["cursor"] = cursor

    resp = GET(..., params=params)
    yield resp["data"]

    cursor = resp.get("additional_data", {}).get("next_cursor")
    if not cursor:
        break
```

Eventfoto implementation:
- `src/pipedrive/client.py` uses `_next_cursor()` when base url ends with `/api/v2`.

Aanvraag_offerte implementation:
- `src/adapters/pipedrive/client.py` reads `additional_data.next_cursor`.

### 3.3 Custom fields: keep your app stable
You have two good options:

**Option 1: Fallback lookup** (recommended for “mapping validators”)
- When you need `deal[field_hash]`:
  - check root key
  - else check `deal["custom_fields"][field_hash]`

Eventfoto implementation:
- `src/pipedrive/mapping.py` does root→custom_fields fallback.

**Option 2: Flatten** (recommended for “app logic expecting flat dicts”)
- Merge `custom_fields` into root (in memory) and continue.

Aanvraag_offerte implementation:
- `src/adapters/pipedrive/http_helper.py::_flatten_custom_fields()`.

### 3.4 Fields API rename: `key/name` vs `field_code/field_name`
If you have “field mapping validation” code, you must normalize:

```python
field_key = f.get("key") or f.get("field_code")
field_name = f.get("name") or f.get("field_name")
```

Eventfoto implementation:
- `src/pipedrive/mapping.py::_index_deal_fields()` normalizes both formats.

Aanvraag_offerte implementation:
- `src/core/schema_health.py` uses `f.get("key") or f.get("field_code")`.

---

## 4) Data quality reality: don’t let one bad deal break the whole app

Live production data contains deals missing required fields.
If your app is “match photos to deals” (needs event_date/lat/lon), you must **skip invalid deals**.

Eventfoto fix:
- `src/pipedrive/mapping.py::normalize_deals_in_range()` skips deals that fail required parsing.

Rule:
- If a field is required for the *workflow*, fail-closed at the workflow boundary.
- If a field is required only for matching/scoring and can be missing for many deals, **skip**.

---

## 5) Migration procedure (per app)

### Step 1 — Inventory endpoints you use
Make a list:
- Which endpoints do you call? (`/deals`, `/dealFields`, `/organizations`, `/persons`, `/products`, `/webhooks`)
- Which ones are writes (POST/PUT/PATCH)?

### Step 2 — Switch base URL + auth (in the smallest surface)
- Introduce `PIPEDRIVE_BASE_URL` (or VERSION+DOMAIN)
- Send header `x-api-token` for all requests

### Step 3 — Fix list pagination
- Replace any `start/limit` loops with `cursor/limit` when on v2

### Step 4 — Fix custom field access
- Add `custom_fields` fallback or flatten

### Step 5 — Fix field mapping validation
- Accept `field_code/field_name`

### Step 6 — Run **live** smoke tests
Minimum live smoke tests:
1) Fetch deal fields (schema):
   - `GET /dealFields`
2) Fetch one page of deals:
   - `GET /deals?limit=1`
3) Fetch a known deal id:
   - `GET /deals/<id>`

Store artifacts (sanitized) in:
- `test-results/live/<app>-pipedrive-v2-<timestamp>/...`

### Step 6b — If your app exposes a FastAPI surface (recommended)
Run the generic HTTP surface checklist:
- `docs/FASTAPI_RUNBOOK.md`

Minimum expectations (adjust paths to your app):
- liveness endpoint returns HTTP 200
- readiness endpoint enforces auth (401 without key, 200 with `X-Admin-Key`)
- OpenAPI JSON returns HTTP 200 (`/openapi.json`)

### Step 7 — Run your app’s real workflow
Examples:
- “Generate quote”
- “Sync products”
- “Match photos”

---

## 6) eventfoto-pipeline specific live checklist

### Required env vars
- `PIPEDRIVE_API_TOKEN`
- `PIPEDRIVE_BASE_URL=https://<tenant>.pipedrive.com/api/v2`
- `PIPEDRIVE_FIELD_MAPPING_PATH=/path/to/mapping.json`

### Suggested commands
- Validate mapping (live):
  - `python -m src.cli --config .env pipedrive validate-mapping`
- List deals (live):
  - `python -m src.cli --config .env pipedrive list-deals --from YYYY-MM-DD --to YYYY-MM-DD`
- Full audit run (live Pipedrive, local photos):
  - `python -m src.cli --config .env run --inbox <INBOX> --out <OUTPUT_ROOT> --dry-run`

---

## 7) Common pitfalls

1) **Using `Authorization: Bearer <api_token>`**
   - Wrong for API token integrations.
   - v2 docs specify `x-api-token`.

2) **Assuming `/dealFields` returns `key/name`**
   - v2 returns `field_code/field_name`.

3) **Breaking on the first deal that has missing fields**
   - Production CRMs always have incomplete data.

4) **Accidentally committing `.env`**
   - Ensure `.env` is gitignored.

5) **Assuming every v1 endpoint exists in v2**
   - v2 is not a 1:1 mirror of v1. Some endpoints used in legacy apps may be v1-only.
   - Example seen in real migrations: `filters`, `notes`.
   - Pattern: keep an explicit allowlist of v1-only endpoints and route those calls to `/v1`.
   - Fail-closed: if you cannot determine a v1 base URL, raise a hard error.

6) **Non-deterministic v1 fallback base URL**
   - If you derive v1 base URL from v2, require the v2 base URL to end with `/api/v2` and replace it with `/v1`.
   - This prevents “silent best-effort” behavior and makes misconfiguration obvious.

---

## 8) Quick reference: what to copy from which repo

### From eventfoto-pipeline-seo-gbp
- v2 auth + cursor pagination in a minimal stdlib client:
  - `src/pipedrive/client.py`
- custom_fields fallback + dealFields normalization:
  - `src/pipedrive/mapping.py`

### From aanvraag_offerte
- v1/v2 switchable http client factory:
  - `src/adapters/pipedrive/http_factory.py`
- custom_fields flatten helper:
  - `src/adapters/pipedrive/http_helper.py`
- schema drift check pattern:
  - `src/core/schema_health.py`
