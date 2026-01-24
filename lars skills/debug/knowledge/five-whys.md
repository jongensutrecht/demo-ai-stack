# 5 Whys Techniek

## Principe
Blijf "waarom?" vragen tot je bij de ROOT CAUSE bent.
Stop niet bij het symptoom of de eerste verklaring.

## Voorbeeld

**Probleem:** API returned lege array

1. **Why?** → Query returned geen resultaten
2. **Why?** → Filter matcht geen records
3. **Why?** → Datum format is anders dan verwacht
4. **Why?** → Frontend stuurt ISO format, backend verwacht Unix timestamp
5. **ROOT CAUSE:** → Geen input validatie/conversie op API endpoint

## Veelgemaakte fouten

### Te vroeg stoppen
```
Probleem: Button werkt niet
Why? → onClick handler fired niet
STOP ← FOUT! Doorvragen!

Why? → Event listener niet attached
Why? → Component unmount voor attach
Why? → Race condition in useEffect
ROOT CAUSE: Missing dependency in useEffect array
```

### Symptoom als oorzaak zien
```
FOUT: "Het werkt niet omdat er een error is"
GOED: "Waarom is er een error? Wat veroorzaakt die error?"
```

## Tips

- Schrijf elke "why" stap op
- Elk antwoord moet BEWIJS hebben (code, logs, data)
- Als je geen bewijs hebt → eerst dat zoeken
- Soms zijn er meerdere root causes (vertakkende whys)
