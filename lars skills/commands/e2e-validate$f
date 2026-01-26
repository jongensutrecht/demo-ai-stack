# Smoke Test Module

**Doel:** Snelle sanity check (<2 min) - werkt de basis?

## Checklist

```
□ App start zonder errors
□ Homepage/login laadt
□ API health endpoint bereikbaar
□ Database connectie werkt
```

## Uitvoering

```bash
# 1. Start app (als niet draait)
npm run dev &

# 2. Check health
curl http://localhost:3000/api/health

# 3. Check homepage
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

## Rapport

```
╔═══════════════════════════════════════╗
║         SMOKE TEST RESULTS            ║
╠═══════════════════════════════════════╣
║ ✅ App start         (0.8s)           ║
║ ✅ Homepage laadt    (1.2s)           ║
║ ✅ API health        (0.3s)           ║
║ ❌ Database          TIMEOUT          ║
╠═══════════════════════════════════════╣
║ STATUS: ❌ BLOCKED                    ║
╚═══════════════════════════════════════╝
```

## Als FAIL

**STOP ALLES** - geen punt om verder te testen als basis niet werkt.
