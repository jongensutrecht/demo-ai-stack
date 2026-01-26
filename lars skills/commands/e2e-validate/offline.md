# Offline Test Module

**Doel:** App werkt zonder internet, data synct na reconnect.

## Test Flow

```
1. Login (online)
2. Start shift (online)
3. ZET NETWERK UIT
4. Voer acties uit (GPS updates, etc.)
5. ZET NETWERK AAN
6. Check: ALLE data gesynchroniseerd?
```

## Simuleer Offline

```javascript
// Browser DevTools
// Network tab → Offline checkbox

// Of in code
await page.context().setOffline(true)
// ... doe acties ...
await page.context().setOffline(false)
```

## Verwacht Gedrag

```
OFFLINE:
- Data lokaal opgeslagen (IndexedDB/localStorage)
- UI toont "offline" indicator
- Geen errors/crashes

RECONNECT:
- Automatische sync start
- ALLE offline data verstuurd
- UI update naar "online"
- GEEN data verlies
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                    OFFLINE TEST                               ║
╠═══════════════════════════════════════════════════════════════╣
║ GPS points created offline: 15                                ║
║ GPS points synced on reconnect: 15                            ║
║ Data loss: 0                                                  ║
║ Status: ✅ PASS                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## Common Bugs

- Data niet gequeued tijdens offline
- Sync faalt silently (geen retry)
- Duplicate data na reconnect
- Queue niet persistent (verloren bij app restart)
