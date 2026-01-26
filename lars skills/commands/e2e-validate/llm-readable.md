# LLM-Leesbare Code

**Doel:** Code moet begrijpelijk zijn voor andere AI agents.

## Regels

### 1. Beschrijvende namen
```javascript
// ❌ SLECHT
const d = getData()
const x = d.filter(i => i.s === 'a')

// ✅ GOED
const shifts = getShifts()
const activeShifts = shifts.filter(shift => shift.status === 'active')
```

### 2. Eén functie = één taak
```javascript
// ❌ SLECHT - doet te veel
function processShift(data) {
  validate(data)
  save(data)
  notify(data)
  log(data)
}

// ✅ GOED - gesplit
function validateShift(data) { ... }
function saveShift(data) { ... }
function notifyShiftCreated(data) { ... }
```

### 3. Geen geneste callbacks
```javascript
// ❌ SLECHT
getData(d => {
  process(d, p => {
    save(p, s => {
      notify(s)
    })
  })
})

// ✅ GOED
const data = await getData()
const processed = await process(data)
const saved = await save(processed)
await notify(saved)
```

### 4. Expliciete types (TypeScript)
```typescript
// ❌ SLECHT
function process(data: any) { ... }

// ✅ GOED
interface Shift {
  id: number
  start: string
  end: string | null
  status: 'active' | 'ended'
}
function processShift(shift: Shift): ProcessedShift { ... }
```

### 5. Geen magic numbers/strings
```javascript
// ❌ SLECHT
if (attempts > 5) { ... }
if (status === 'a') { ... }

// ✅ GOED
const MAX_LOGIN_ATTEMPTS = 5
const STATUS_ACTIVE = 'active'

if (attempts > MAX_LOGIN_ATTEMPTS) { ... }
if (status === STATUS_ACTIVE) { ... }
```

### 6. Comments bij complexe logica
```javascript
// ❌ SLECHT - geen uitleg
const result = data.reduce((a, b) => ({ ...a, [b.k]: [...(a[b.k] || []), b] }), {})

// ✅ GOED - met uitleg
// Groepeer items per key: { key1: [items], key2: [items] }
const groupedByKey = data.reduce((groups, item) => {
  const key = item.key
  const existing = groups[key] || []
  return { ...groups, [key]: [...existing, item] }
}, {})
```

### 7. Consistente structuur
```
Elke module/file volgt:
1. Imports (gegroepeerd)
2. Types/Interfaces
3. Constants
4. Helper functions
5. Main exports
```

### 8. Error messages zijn specifiek
```javascript
// ❌ SLECHT
throw new Error('Failed')

// ✅ GOED
throw new Error(`Shift ${shiftId} not found for user ${userId}`)
```

## Check

```bash
# Zoek slechte patronen
grep -rn "any\>" src/         # any types
grep -rn "=> {$" src/         # inline arrow without name
grep -rn "// TODO" src/       # unfinished code
```

## Rapport

```
LLM-READABLE CHECK
─────────────────────────────────────────
Beschrijvende namen:    ✅
Single responsibility:  ✅
Geen nesting >2:        ✅
Expliciete types:       ❌ 3x 'any' gevonden
Geen magic values:      ✅
Comments bij complex:   ⚠️ 2 functies zonder
─────────────────────────────────────────
Status: ❌ FAIL - fix 'any' types
```
