# Fallback Code Scan Module

**Doel:** Vind en verwijder code die bugs maskeert met fallback data.

## Verboden Patterns

```javascript
// ❌ VERBODEN
data || []                    // Maskeert API failure
data ?? defaultValue          // Maskeert missing data
catch { return { ok: true } } // Slik error, fake success
"example", "test", "dummy"    // Hardcoded test data
```

## Toegestaan

```javascript
// ✅ OK
name || ''                    // Lege string in UI
count ?? 0                    // Numerieke default in UI
// CONFIG_DEFAULT: reason     // Expliciete config met comment
```

## Scan Commando

```bash
# Zoek || patterns
grep -rn "|| \[" src/
grep -rn "|| {" src/
grep -rn "?? \[" src/

# Zoek catch blocks met returns
grep -rn "catch.*return" src/

# Zoek dummy data
grep -rni "example\|dummy\|mock\|test.*data" src/
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                 FALLBACK CODE SCAN                            ║
╠═══════════════════════════════════════════════════════════════╣
║ ❌ GEVONDEN: 3 verboden fallbacks                             ║
╠───────────────────────────────────────────────────────────────╣
║ 1. src/api/gps.ts:45                                          ║
║    Code: return data || []                                    ║
║    Fix: throw new Error('GPS fetch failed')                   ║
╠───────────────────────────────────────────────────────────────╣
║ ACTIE: Verwijder fallbacks VOORDAT je verder test.            ║
╚═══════════════════════════════════════════════════════════════╝
```

## Als GEVONDEN

**STOP** - Verwijder alle fallbacks eerst. Ze maskeren echte bugs.
