# Session Persistence Module

**Doel:** User blijft ingelogd na app restart, netwerk issues, etc.

## Test Scenarios

```
□ Login → app restart → nog ingelogd?
□ Login → 24 uur wachten → nog ingelogd?
□ Login → netwerk uit/aan → nog ingelogd?
□ Login → browser tab sluiten/openen → nog ingelogd?
□ Login → device restart → nog ingelogd?
```

## Test Flow

```javascript
// 1. Login
await login(user, pass)
const token1 = getSessionToken()

// 2. Simuleer restart (clear memory, NIET storage)
clearMemory()

// 3. Herlaad app
await reloadApp()

// 4. Check
const token2 = getSessionToken()
assert(isLoggedIn())
assert(token1 === token2) // Zelfde sessie
```

## Mobiel Specifiek

```
- App force close → heropen
- Background kill na 30 min inactiviteit
- Device restart
- OS memory pressure (app killed)
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║              SESSION PERSISTENCE TEST                         ║
╠═══════════════════════════════════════════════════════════════╣
║ App restart:     ✅ Still logged in                           ║
║ Network toggle:  ✅ Session preserved                         ║
║ 24h expiry:      ✅ Token valid (365 day max-age)            ║
║ Tab close/open:  ✅ Session restored                          ║
╚═══════════════════════════════════════════════════════════════╝
```

## Common Bugs

- Cookie not httpOnly (security risk)
- Cookie expires too soon
- Token not persisted to localStorage
- Session invalidated on IP change
