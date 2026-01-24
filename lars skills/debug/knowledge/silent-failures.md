# Silent Failures - Waar te zoeken

## Patronen die bugs verbergen

### 1. Lege catch blocks
```javascript
// SLECHT - error verdwijnt
try { doSomething() } catch (e) { }

// SLECHT - error wordt gesluikt
try { doSomething() } catch (e) { console.log('error') }
```

### 2. Fallback defaults
```javascript
// SLECHT - maskeert null/undefined
const items = data?.items || []
const user = getUser() ?? { name: 'Unknown' }
```

### 3. Optional chaining overuse
```javascript
// SLECHT - faalt stil als path niet bestaat
const value = obj?.deeply?.nested?.value
```

### 4. Async zonder await/catch
```javascript
// SLECHT - promise rejection verdwijnt
someAsyncFunction()  // geen await, geen .catch()
```

### 5. Event handlers zonder error handling
```javascript
// SLECHT - errors in callbacks verdwijnen vaak
element.addEventListener('click', () => { riskyCode() })
```

## Zoek commando's

```bash
# Lege catch blocks
grep -rn "catch.*{.*}" --include="*.ts" --include="*.js"

# || [] fallbacks
grep -rn "|| \[\]" --include="*.ts" --include="*.js"

# || {} fallbacks
grep -rn "|| {}" --include="*.ts" --include="*.js"

# Unhandled async
grep -rn "async.*=>" --include="*.ts" --include="*.js"
```
