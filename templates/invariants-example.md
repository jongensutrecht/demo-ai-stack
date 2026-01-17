# Invariants - Finance Insights Hub

> Dit document definieert wat NOOIT mag gebeuren in deze applicatie.
> Elke invariant moet een NEVER-test hebben in `tests/invariants/`.

---

## Security Invariants

### Authentication & Authorization

- [ ] **INV-SEC-001**: Protected endpoints NEVER return data without valid API key
  - Alle `/insights/*`, `/tools`, `/chat` endpoints vereisen `X-API-Key`
  - Test: Request zonder header → 401/403

- [ ] **INV-SEC-002**: Admin endpoints NEVER accessible without admin key
  - `/admin/*`, `/metrics`, `?include_tool_trace=true` vereisen `X-Admin-Key`
  - Test: Request met alleen client key → 403

- [ ] **INV-SEC-003**: API key validation NEVER uses simple string comparison
  - Moet HMAC constant-time comparison gebruiken (timing attack preventie)
  - Test: Verify `secrets.compare_digest` wordt gebruikt

### Token & Credential Management

- [ ] **INV-SEC-010**: OAuth tokens NEVER exposed in API responses
  - Access tokens, refresh tokens nooit in response body
  - Test: Alle endpoints → geen token fields in response

- [ ] **INV-SEC-011**: OAuth tokens NEVER logged
  - Tokens niet in logs, errors, of traces
  - Test: Capture logs tijdens token refresh → geen tokens

- [ ] **INV-SEC-012**: Fernet encryption keys NEVER in responses or logs
  - `FERNET_KEY`, `FERNET_SECONDARY_KEYS` alleen in memory
  - Test: Grep alle responses en logs

- [ ] **INV-SEC-013**: WeFact API key NEVER exposed
  - Key alleen in outgoing requests naar WeFact
  - Test: Geen API key in responses, logs, errors

### External API Security

- [ ] **INV-SEC-020**: External API credentials NEVER sent to wrong endpoints
  - WeFact key alleen naar `api.wefact.nl`
  - Exact tokens alleen naar `exactonline.nl`
  - Test: Mock requests, verify destinations

- [ ] **INV-SEC-021**: Redirect URLs NEVER accepted without validation
  - OAuth redirect_uri moet whitelist matchen
  - Test: Malicious redirect_uri → rejected

---

## Business Invariants

### Financial Calculations

- [ ] **INV-BIZ-001**: Invoice totals NEVER inconsistent
  - `amount_inc_vat` moet gelijk zijn aan `amount_ex_vat + vat_amount`
  - Test: Alle documents → verify totals

- [ ] **INV-BIZ-002**: Open amounts NEVER negative
  - `open_amount` op documents >= 0
  - Test: Insert document met negative open_amount → rejected

- [ ] **INV-BIZ-003**: KIA deduction NEVER exceeds investment amount
  - `kia_deduction_estimate <= qualifying_investments_ytd`
  - Test: Edge cases KIA schedule

- [ ] **INV-BIZ-004**: VAT position calculation NEVER wrong sign
  - Positive balance = receivable (BTW terug te krijgen)
  - Negative balance = payable (BTW te betalen)
  - Test: Known GL snapshots → verify position

- [ ] **INV-BIZ-005**: Cost variance percentage NEVER division by zero
  - Als previous period = 0, geen percentage berekenen
  - Test: Period met 0 costs → geen crash

### Data Integrity

- [ ] **INV-BIZ-010**: Document external_id NEVER duplicate per provider
  - Unique constraint: (provider, external_id)
  - Test: Insert duplicate → rejected

- [ ] **INV-BIZ-011**: Sync watermark NEVER goes backwards
  - Nieuwe watermark >= oude watermark
  - Test: Sync met oudere data → watermark unchanged

- [ ] **INV-BIZ-012**: Sync records NEVER updated without payload change
  - Alleen update als `payload_hash` verschilt
  - Test: Re-sync zelfde data → upserted_count = 0

- [ ] **INV-BIZ-013**: GL snapshots NEVER overwrite different fiscal periods
  - Unique: (division, gl_account_id, fiscal_year, fiscal_period, snapshot_date)
  - Test: Insert conflicting snapshot → rejected

### Sync Operations

- [ ] **INV-BIZ-020**: Concurrent syncs NEVER run for same provider
  - Lock mechanism voorkomt duplicate runs
  - Test: Twee syncs tegelijk → één krijgt "skipped_locked"

- [ ] **INV-BIZ-021**: Failed sync NEVER leaves partial data
  - Transaction rollback bij errors
  - Test: Sync met error halfway → geen partial records

- [ ] **INV-BIZ-022**: Sync run status NEVER invalid transition
  - running → success/failed/skipped_locked (niet terug naar running)
  - Test: State machine transitions

---

## Performance Invariants

### Response Times

- [ ] **INV-PERF-001**: Insight endpoints NEVER exceed 2 seconds (cached)
  - Met warme cache < 2s response time
  - Test: Benchmark met cache hit

- [ ] **INV-PERF-002**: Insight endpoints NEVER exceed 10 seconds (uncached)
  - Eerste request met DB query < 10s
  - Test: Benchmark met cache miss

- [ ] **INV-PERF-003**: Health endpoints NEVER exceed 100ms
  - `/health/live` en `/health/ready` instant
  - Test: Benchmark health checks

### Resource Limits

- [ ] **INV-PERF-010**: Database queries NEVER unbounded
  - Alle queries hebben LIMIT of pagination
  - Test: Verify geen `SELECT *` zonder limit

- [ ] **INV-PERF-011**: External API pagination NEVER skipped
  - WeFact en Exact itereren door alle pages
  - Test: Mock 1000+ records → alle gefetched

- [ ] **INV-PERF-012**: Insight cache NEVER grows unbounded
  - TTL-based expiry werkt
  - Test: Old cache entries worden opgeruimd

### Retry & Timeout

- [ ] **INV-PERF-020**: External API retries NEVER exceed max attempts
  - Max 3 retries (configurable)
  - Test: Mock 10x failure → stops at 3

- [ ] **INV-PERF-021**: External API timeouts NEVER hang forever
  - WeFact: 10s, Exact: 30s timeout
  - Test: Mock slow response → timeout exception

---

## Reliability Invariants

### Error Handling

- [ ] **INV-REL-001**: Unhandled exceptions NEVER crash the server
  - Global exception handler returns 500
  - Test: Trigger unexpected error → server stays up

- [ ] **INV-REL-002**: External API errors NEVER expose internal details
  - WeFactError, ExactError wrapped in generic message
  - Test: API failure → no stack trace in response

- [ ] **INV-REL-003**: Database errors NEVER leave open transactions
  - Context manager sluit altijd session
  - Test: Error during query → transaction rolled back

### Token Refresh

- [ ] **INV-REL-010**: Expired access token NEVER blocks operations
  - Automatic refresh wanneer token expired
  - Test: Expired token → refresh → retry succeeds

- [ ] **INV-REL-011**: Failed token refresh NEVER corrupts token store
  - Bij refresh failure, oude tokens behouden
  - Test: Refresh failure → can retry later

- [ ] **INV-REL-012**: Token refresh NEVER runs concurrently for same tenant
  - Lock voorkomt race conditions
  - Test: Twee requests tegelijk → één refresh

### Data Recovery

- [ ] **INV-REL-020**: Full sync NEVER fails on existing data
  - FULL mode kan altijd draaien, ongeacht state
  - Test: Run FULL sync na partial failure

- [ ] **INV-REL-021**: Insight cache miss NEVER returns stale data
  - Cache miss → fresh compute, niet oude waarde
  - Test: Expire cache → next request = fresh

---

## Test Locaties

```
tests/invariants/
├── security/
│   ├── test_inv_sec_001_api_key_required.py
│   ├── test_inv_sec_002_admin_key_required.py
│   ├── test_inv_sec_010_tokens_not_exposed.py
│   └── ...
├── business/
│   ├── test_inv_biz_001_invoice_totals.py
│   ├── test_inv_biz_010_unique_external_id.py
│   └── ...
├── performance/
│   ├── test_inv_perf_001_cached_response_time.py
│   └── ...
└── reliability/
    ├── test_inv_rel_001_exception_handling.py
    └── ...
```

---

## Hoe NEVER-tests te schrijven

```python
# tests/invariants/security/test_inv_sec_001_api_key_required.py

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_NEVER_returns_data_without_api_key(client: AsyncClient):
    """INV-SEC-001: Protected endpoints NEVER return data without valid API key"""

    # Alle protected endpoints
    protected = [
        "/insights/vat?from=2024-01-01&to=2024-12-31",
        "/insights/kia?year=2024",
        "/insights/costs?from=2024-01-01&to=2024-12-31",
        "/insights/hours?from=2024-01-01&to=2024-12-31",
        "/insights/open-items",
        "/tools",
    ]

    for endpoint in protected:
        # WHEN: Request without API key
        response = await client.get(endpoint)

        # THEN: NEVER returns 200
        assert response.status_code in (401, 403), \
            f"INV-SEC-001 VIOLATED: {endpoint} returned {response.status_code} without API key"
```

---

**Document Version:** 1.0.0
**Last Updated:** 2025-01-17
**Project:** finance-insights-hub
