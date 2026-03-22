# Pipedrive v1 → v2 API Migration Playbook

Last re-verified against official Pipedrive documentation on **2026-03-07**.

This document is the canonical internal playbook for migrating JVDP apps from older Pipedrive integrations to the current API surface.

If this document and an older internal migration note disagree:
1. official Pipedrive documentation wins;
2. this playbook comes next;
3. repo-local migration notes come after that.

> Safety: never commit secrets. Keep API tokens only in local `.env`, secret stores, or CI secret managers.

---

## 1. Official sources of truth

Use these first whenever a migration detail is unclear:

- Authentication:
  - `https://pipedrive.readme.io/docs/core-api-concepts-authentication`
- Requests / request-level changes:
  - `https://pipedrive.readme.io/docs/core-api-concepts-requests`
- Pagination:
  - `https://pipedrive.readme.io/docs/core-api-concepts-pagination`
- API v2 overview:
  - `https://pipedrive.readme.io/docs/pipedrive-api-v2`
- API v2 migration guide:
  - `https://pipedrive.readme.io/docs/pipedrive-api-v2-migration-guide`
- Custom fields:
  - `https://pipedrive.readme.io/docs/core-api-concepts-custom-fields`
- Rate limiting:
  - `https://pipedrive.readme.io/docs/core-api-concepts-rate-limiting`
- Webhooks v2 guide:
  - `https://pipedrive.readme.io/docs/guide-for-webhooks-v2`
- Webhooks v2 migration guide:
  - `https://pipedrive.readme.io/docs/webhooks-v2-migration-guide`
- OpenAPI v2:
  - `https://developers.pipedrive.com/docs/api/v2/openapi.yaml`
- OpenAPI v1:
  - `https://developers.pipedrive.com/docs/api/v1/openapi.yaml`
- Company domain tutorial:
  - `https://pipedrive.readme.io/docs/how-to-get-the-company-domain`

---

## 2. Hard migration contract

These are the rules you must implement and verify.

### 2.1 Base URL: do not hardcode one official shape only

Official docs currently expose **two valid patterns**:

- auth/tutorial examples use:
  - `https://{COMPANYDOMAIN}.pipedrive.com/api/v2`
- official OpenAPI v2 currently declares:
  - `https://api.pipedrive.com/api/v2`

**Implication:**
- do not encode the migration as “v2 is always tenant-domain only”; that is too strict;
- instead, treat the full base URL as explicit configuration.

**Internal rule:**
- `PIPEDRIVE_BASE_URL` is the single runtime source of truth when present;
- if it is absent, you may build it from version + company domain;
- if you cannot derive it deterministically, fail closed.

### 2.2 API token auth: use `x-api-token`

Official auth docs require API token integrations to send the token in the header:

- `x-api-token: <token>`

Do **not** migrate a token-based integration to:
- `Authorization: Bearer <token>`
- query-param-only token auth

unless official docs for that exact flow explicitly require it.

### 2.3 Pagination: audit per endpoint, not per version label

Do **not** assume:
- “all v1 endpoints are offset-based”
- “all v2 endpoints are cursor-based”

Official docs confirm:
- many migrated v2 list endpoints use `cursor` + `limit` and return `additional_data.next_cursor`;
- some v1 surfaces also expose `next_cursor`;
- some v1 endpoints still use `start` + `limit` and return `additional_data.pagination.*`.

**Internal rule:**
- audit pagination contract endpoint-by-endpoint;
- implement pagination adapters based on actual endpoint behavior.

### 2.4 Custom fields moved under `custom_fields`

Official v2 migration docs state that entity custom fields moved into a separate `custom_fields` object.

**Internal rule:**
- keep app code stable by either:
  - fallback lookup: root key first, then `custom_fields`; or
  - flattening `custom_fields` into the in-memory entity.

### 2.5 Fields API renamed keys

Official v2 Fields API uses:
- `field_code`
- `field_name`

Legacy integrations often expect:
- `key`
- `name`

**Internal rule:**
normalize both forms in one place:

```python
field_key = field.get("key") or field.get("field_code")
field_name = field.get("name") or field.get("field_name")
```

### 2.6 Related objects were removed from many v2 responses

Official v2 migration docs explicitly say related objects were removed from API responses to avoid eager over-fetching.

**Internal rule:**
- do not assume owner/person/org nested data is still present;
- fetch related objects explicitly if the workflow still needs them.

### 2.7 Field selectors were removed from API v2

Official request docs explicitly state that support for field selectors was removed from API v2.

**Internal rule:**
- remove v2 code paths that depend on field selectors;
- if a workflow still depends on them, keep that exact endpoint on a verified v1 path or redesign the request flow.

### 2.8 Webhooks v2 are a separate migration track

Official webhooks v2 docs confirm an important nuance:
- webhook version 2 is still created via **`POST /v1/webhooks`**
- with a `version` parameter in the request body.

**Internal rule:**
- do not assume “v2 migration” means every endpoint path becomes `/api/v2/...`;
- audit webhooks separately from entity/list endpoints.

### 2.9 Rate limiting is part of the migration surface

Official rate limiting docs and v2 overview make rate-limit cost a first-class concern.

**Internal rule:**
- account for endpoint token cost in bulk backfills and syncs;
- migrate pagination and fetch shape before scaling up volume tests.

### 2.10 Treat endpoint availability as a compatibility matrix

Verified against the official v2 OpenAPI on 2026-03-07:
- `filters` are not exposed in the downloaded v2 OpenAPI
- `notes` are not exposed in the downloaded v2 OpenAPI

Official v1 docs still expose those API areas.

**Internal rule:**
- maintain an explicit allowlist of v1-only endpoints if your app still needs them;
- fail closed if a request is routed to v2 without a verified v2 contract.

---

## 3. Recommended config strategy

### Preferred variables

- `PIPEDRIVE_BASE_URL`
- `PIPEDRIVE_API_TOKEN`

Optional builder inputs:
- `PIPEDRIVE_API_VERSION`
- `PIPEDRIVE_COMPANY_DOMAIN`

### Resolution rule

1. If `PIPEDRIVE_BASE_URL` is set, use it.
2. Else, if `PIPEDRIVE_API_VERSION` and `PIPEDRIVE_COMPANY_DOMAIN` are set, build:
   - `https://{PIPEDRIVE_COMPANY_DOMAIN}.pipedrive.com/api/{PIPEDRIVE_API_VERSION}`
3. Else, fail closed with a configuration error.

### v1 fallback rule

If you must derive a v1 base URL from a configured v2 base URL:
- require the configured base URL to end with `/api/v2`;
- replace that suffix with `/v1`;
- if the suffix does not match, fail closed.

---

## 4. Implementation patterns

### 4.1 Centralize auth and base URL construction

Do not spread Pipedrive URL construction and auth headers across the codebase.

One shared adapter should own:
- base URL resolution
- `x-api-token` header injection
- v1/v2 routing decisions
- retry / timeout defaults

### 4.2 Centralize pagination adapters

Use endpoint-aware pagination helpers:

- offset adapter:
  - request: `start`, `limit`
  - response: `additional_data.pagination.*`
- cursor adapter:
  - request: `cursor`, `limit`
  - response: `additional_data.next_cursor`

### 4.3 Normalize response shape at the boundary

Recommended normalization layer:
- flatten or fallback for `custom_fields`
- normalize `key/name` vs `field_code/field_name`
- explicitly fetch related objects when required

Do not scatter migration-specific conditionals throughout business logic.

### 4.4 Separate app-policy from API-contract logic

Examples:
- “skip malformed deals in photo matching” is an app policy;
- “custom fields moved to `custom_fields`” is an API contract.

Keep those concerns separate.

---

## 5. Migration procedure per app

### Step 1 — Inventory the exact endpoints in use

For each endpoint, record:
- path
- read vs write
- current version (`v1`, `v2`, unknown)
- auth mode
- pagination mode
- field mapping dependency
- related-object dependency
- webhook dependency

### Step 2 — Build a compatibility matrix

For every endpoint classify it as one of:
- `v2-verified`
- `v1-only`
- `unknown-do-not-migrate-yet`

No endpoint should stay implicit.

### Step 3 — Migrate auth and base URL at the smallest possible boundary

Implement or update one shared HTTP layer first.

Verification:
- one GET request succeeds with `x-api-token`
- wrong/missing token fails cleanly
- base URL misconfiguration fails at startup or first request

### Step 4 — Migrate pagination per endpoint

Do not batch-convert all loops blindly.

Verification for each paginated endpoint:
- fetch first page
- fetch second page if available
- stop when `next_cursor` is null or pagination reports end-of-collection
- confirm no duplicates / no silent truncation

### Step 5 — Migrate custom field access and field metadata validation

Verification:
- fetch field metadata
- resolve required custom fields by normalized key/name
- fetch one entity with known custom field values
- confirm the app sees the same logical values after normalization

### Step 6 — Handle removed related objects explicitly

Verification:
- identify any code path reading owner/person/org nested objects directly
- replace with explicit follow-up fetches or cached lookups
- prove the workflow still behaves correctly

### Step 7 — Migrate webhooks separately if present

Verification:
- webhook registration path is correct
- webhook version is explicitly set to v2 where required
- payload parser is tested against v2 payload shape
- retry/idempotency handling is preserved

### Step 8 — Run live smoke tests

Minimum smoke tests:
1. fetch field metadata
2. fetch one page of entities
3. fetch one known entity by id
4. if applicable, write one safe test mutation in a non-production-safe object or sandbox pattern

Store sanitized artifacts under:
- `test-results/live/<app>-pipedrive-migration-<timestamp>/`

### Step 9 — Run the real application workflow

Examples:
- quote generation
- product sync
- debtor sync
- photo/deal matching
- webhook-driven state transitions

Migration is not complete until the real workflow passes.

---

## 6. Verification checklist

A migration is only done when all are true:

- [ ] Base URL resolution is explicit and deterministic
- [ ] API token auth uses `x-api-token`
- [ ] Every migrated endpoint has a verified pagination contract
- [ ] Custom field access works through a shared normalization layer
- [ ] Field metadata validation accepts both legacy and v2 names where needed
- [ ] Removed related objects no longer break runtime logic
- [ ] Any v1-only endpoints are explicitly routed and documented
- [ ] Webhooks were audited separately if the app uses them
- [ ] Live smoke tests passed
- [ ] Real workflow test passed

---

## 7. Reference implementations inside JVDP repos

### From `eventfoto-pipeline-seo-gbp`

Use as reference for:
- minimal stdlib Pipedrive client with `x-api-token`
- cursor handling
- custom field fallback lookup
- field metadata normalization

Files:
- `src/pipedrive/client.py`
- `src/pipedrive/mapping.py`

### From `aanvraag_offerte`

Use as reference for:
- switchable v1/v2 HTTP factory
- in-memory `custom_fields` flattening
- schema drift checks for fields metadata

Files:
- `src/adapters/pipedrive/http_factory.py`
- `src/adapters/pipedrive/http_helper.py`
- `src/core/schema_health.py`

---

## 8. Non-goals

This playbook does not define:
- app-specific business rules
- domain-specific skip/fail rules for malformed records
- rollout sequencing across unrelated services
- production secret rotation procedures

Those belong in the target app repo.

---

## 9. Practical conclusion

For JVDP apps, the safe migration pattern is:

1. centralize configuration and auth;
2. classify endpoints one by one;
3. normalize response shape at the boundary;
4. verify pagination per endpoint;
5. keep explicit v1 fallbacks only where officially necessary;
6. prove the real workflow, not just the transport layer.
