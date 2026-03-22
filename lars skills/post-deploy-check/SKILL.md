---
name: post-deploy-check
description: Verifieer na deploy of de service live echt werkt. Health checks, logs, metrics, fingerprints. Geen aannames — alleen hard bewijs.
allowed-tools: Read, Bash
user-invocable: true
---

# Post-Deploy Check

> **Doel**: Na een deploy controleren of de service **echt live werkt** met hard bewijs. Geen "deploy is klaar dus het werkt". Bewijs of het werkt, of rapporteer wat niet klopt.

## Wanneer gebruiken

```
/skill:post-deploy-check <service> [<server>]
```

Na elke deploy, herstart, config-wijziging of token-rotatie op een live service.

## Hard rules

1. **Geen aannames.** "Container draait" is geen bewijs dat de service werkt.
2. **Health check is verplicht** als de service een health endpoint heeft.
3. **Log check is verplicht** — kijk naar de eerste 30 seconden na deploy.
4. **Geen secrets tonen.** Gebruik fingerprints, presence checks, of masked output.
5. **UNKNOWN als je iets niet kunt checken** — niet overslaan.

## Workflow

### 1. Container/process status
```bash
ssh <server> "docker ps --filter name=<container> --format '{{.Names}} {{.Status}}'"
```
Verwacht: `Up` + geen restart loop.

### 2. Health endpoint
```bash
ssh <server> "curl -sf http://127.0.0.1:<port><health_path>"
```
Verwacht: HTTP 200 + relevante body.

Bekende health endpoints (uit RUNBOOK):
| Service | Poort | Pad |
|---------|-------|-----|
| offerte | 8000 | /health/live |
| driver | 4010 | /health |
| beller | 4020 | /health |
| planner | 8002 | /health/live |
| tracker | 8004 | / |
| portaal-api | 34001 | /health/live |
| finance | 8001 | /health/live |
| todo | 8003 | /api/health |

### 3. Recente logs (eerste 30 seconden)
```bash
ssh <server> "docker logs --since 30s <container> 2>&1 | tail -30"
```
Zoek naar:
- startup errors
- connection failures
- missing env vars
- 429 / 500 / crash loops

### 4. Config consistency (optioneel)
Als de deploy een secret/config wijziging bevatte:
```bash
ssh <server> "python3 - <<'PY'
import subprocess, hashlib
raw=subprocess.check_output(['docker','inspect','--format','{{range .Config.Env}}{{println .}}{{end}}','<container>']).decode().splitlines()
for key in ['PIPEDRIVE_API_TOKEN','ADMIN_API_KEY','SESSION_SECRET']:
    val=''
    for line in raw:
        if line.startswith(key+'='):
            val=line.split('=',1)[1].strip(); break
    fp=hashlib.sha256(val.encode()).hexdigest()[:12] if val else 'MISSING'
    print(key, fp)
PY"
```
Verwacht: fingerprints matchen met wat je hebt ingesteld.

### 5. Functionele smoke check (optioneel)
Als de service een publiek endpoint heeft, doe 1 echte request:
```bash
curl -sf https://<domain>/<pad> -o /dev/null -w "%{http_code}"
```
Verwacht: 200 of 401 (als auth nodig is).

## Output

```
POST-DEPLOY CHECK: <service> op <server>

Container status: OK / FAIL / UNKNOWN
Health endpoint:  OK / FAIL / UNKNOWN
Recent logs:      OK / WARN / FAIL / UNKNOWN
Config check:     OK / FAIL / SKIP
Smoke check:      OK / FAIL / SKIP

Verdict: HEALTHY / DEGRADED / BROKEN / UNKNOWN

Details:
- <concreet bewijs per check>
```

## Niet doen

- Niet claimen "deploy gelukt" zonder minimaal container status + health check.
- Niet secrets in plaintext tonen.
- Niet stoppen bij alleen "container draait" — dat is niet genoeg.
