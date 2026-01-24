# Assumption Check

## Vraag jezelf af

### Over de data
- Is de input ECHT wat ik denk dat het is?
- Is het type correct? (string vs number, array vs object)
- Is het format correct? (datum, encoding, etc)
- Kan het null/undefined/empty zijn?
- Kan het MEER items bevatten dan verwacht?

### Over de flow
- Wordt deze code ECHT aangeroepen?
- In welke VOLGORDE gebeuren dingen?
- Zijn er race conditions mogelijk?
- Wat als het 2x wordt aangeroepen?
- Wat als het NOOIT wordt aangeroepen?

### Over de state
- Is de state ECHT wat ik denk?
- Kan de state tussendoor wijzigen?
- Is er shared/global state die interfereert?
- Wordt state correct gereset?

### Over externe dependencies
- Is de API response ECHT zoals gedocumenteerd?
- Kan de response anders zijn bij errors?
- Wat als de service traag/offline is?
- Zijn er rate limits?

## Validatie technieken

```javascript
// Log ALLES om aannames te checken
console.log('INPUT:', JSON.stringify(input, null, 2))
console.log('TYPE:', typeof input)
console.log('IS ARRAY:', Array.isArray(input))
console.log('LENGTH:', input?.length)

// Assert verwachtingen
if (!Array.isArray(input)) throw new Error('Expected array!')
if (input.length === 0) console.warn('WARNING: Empty input')
```

## Red flags

- "Dit zou altijd moeten werken"
- "Dat kan niet null zijn"
- "Die functie wordt maar 1x aangeroepen"
- "De API geeft altijd dit format terug"
- "Dat hebben we al getest"
