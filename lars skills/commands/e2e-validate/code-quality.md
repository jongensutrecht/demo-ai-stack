# Code Quality Module

**Doel:** Vind dead code, duplicates, memory leaks, te grote bestanden.

---

## 0. File Size Check (HARDE REGEL)

**Limiet:** Max 300 regels, max 20 functies per bestand.

```bash
# Tel regels per bestand
find src/ api/ lib/ -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -rn

# Tel functies per bestand
grep -c "function\|const.*=.*=>" src/**/*.ts
```

**Check:**
```
VOOR ELK bestand:
- Regels > 300? → ❌ FAIL
- Functies > 20? → ❌ FAIL
```

**Rapport:**
```
FILE SIZE CHECK
─────────────────────────────────────────
❌ src/api/gps-sync.ts: 342 regels (max 300)
❌ lib/sheets.ts: 25 functies (max 20)
✅ Overige bestanden: OK
─────────────────────────────────────────
Status: ❌ FAIL - 2 bestanden te groot
Actie: Split bestanden op VOORDAT je merged
```

---

## 1. Dead Code Detectie

**Wat:** Code die nergens gebruikt wordt.

```bash
# TypeScript unused exports
npx ts-prune

# ESLint unused vars
npx eslint --rule 'no-unused-vars: error'

# Find unused components
grep -rL "import.*ComponentName" src/
```

**Rapport:**
```
DEAD CODE GEVONDEN:
- src/utils/oldHelper.ts (0 imports)
- src/components/LegacyButton.tsx (0 renders)
```

---

## 2. Duplicate Code Detectie

**Wat:** Copy-paste code die 1 functie moet zijn.

```bash
# Install jscpd
npm i -g jscpd

# Run
jscpd src/ --min-lines 10
```

**Rapport:**
```
DUPLICATES GEVONDEN:
- src/api/shifts.ts:45-60
- src/api/gps.ts:30-45
  ↑ 15 lines identical, refactor to shared function
```

---

## 3. Memory Leak Check

**Wat:** App vreet steeds meer geheugen.

**Test:**
```javascript
// 1. Meet baseline
const baseline = performance.memory.usedJSHeapSize

// 2. Voer 100x actie uit
for (let i = 0; i < 100; i++) {
  await navigateTo('/dashboard')
  await navigateTo('/shifts')
}

// 3. Meet opnieuw
const after = performance.memory.usedJSHeapSize
const growth = ((after - baseline) / baseline) * 100

// 4. Check
assert(growth < 20, `Memory grew ${growth}%`)
```

**Common Leaks:**
- Event listeners niet removed
- setInterval niet cleared
- Refs naar unmounted components
- WebSocket connections niet closed

**Rapport:**
```
╔═══════════════════════════════════════════════════════════════╗
║                  CODE QUALITY                                 ║
╠═══════════════════════════════════════════════════════════════╣
║ File size:      0 violations ✅ (max 300 lines, 20 functions) ║
║ Dead code:      0 files      ✅                               ║
║ Duplicates:     2 blocks     ⚠️ (15 lines, consider refactor) ║
║ Memory leak:    +3%          ✅ (<20% threshold)              ║
╚═══════════════════════════════════════════════════════════════╝
```

## File Size = BLOCKER

```
File size violation = ❌ FAIL
Geen merge tot bestanden gesplit zijn.
```
