# Data Integrity Module

**Doel:** Data verstuurd = Data ontvangen. Geen afronding, geen conversie.

## Tests

### GPS Coördinaten
```
Stuur:    { lat: 52.12345678, lng: 4.65432100 }
Ontvang:  { lat: 52.12345678, lng: 4.65432100 }
          ↑ EXACT MATCH vereist

❌ FAIL als: 52.123457 (afgerond)
❌ FAIL als: 52.12345678000001 (floating point error)
```

### Timestamps
```
Stuur:    "2026-01-26T09:00:00.000Z"
Ontvang:  "2026-01-26T09:00:00.000Z"
          ↑ EXACT MATCH vereist

❌ FAIL als: "2026-01-26T10:00:00.000Z" (timezone bug)
❌ FAIL als: "2026-01-26T09:00:00Z" (milliseconds weg)
```

## Test Flow

```javascript
// 1. Stuur data
const sent = { lat: 52.12345678, timestamp: "2026-01-26T09:00:00.000Z" }
await api.post('/gps', sent)

// 2. Lees terug
const received = await api.get('/gps/latest')

// 3. Vergelijk EXACT
assert(sent.lat === received.lat)
assert(sent.timestamp === received.timestamp)
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                 DATA INTEGRITY TEST                           ║
╠═══════════════════════════════════════════════════════════════╣
║ GPS: Sent 52.12345678 → Received 52.12345678  ✅              ║
║ Time: Sent 09:00:00Z → Received 10:00:00Z     ❌ (+1 hour)    ║
╚═══════════════════════════════════════════════════════════════╝
```

## Common Bugs

- Timezone conversie (UTC vs local)
- Floating point precision loss
- String truncation
- JSON serialization issues
