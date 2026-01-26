# Contract Testing Module

**Doel:** Controleer of frontend en backend dezelfde taal spreken.

## Wat is een Contract?

```
Frontend verwacht: { id: number, name: string }
Backend returned:  { id: number, name: string }
                   ↑ MATCH = ✅

Frontend verwacht: { id: number, name: string }
Backend returned:  { id: number, name: string | null }
                   ↑ MISMATCH = ❌ (null niet verwacht)
```

## Uitvoering

```
VOOR ELKE API call in frontend:
1. Vind TypeScript interface/type
2. Vind wat backend daadwerkelijk returned
3. VERGELIJK: exact match?
```

## Waar te Vinden

```
Frontend types:
- src/types/*.ts
- src/lib/api.ts (fetch calls)

Backend responses:
- api/*.ts (return statements)
- openspec/specs/ (als aanwezig)
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                   CONTRACT TEST                               ║
╠═══════════════════════════════════════════════════════════════╣
║ GET /api/shifts/my                                            ║
╠───────────────────────────────────────────────────────────────╣
║ Frontend (src/types/Shift.ts):                                ║
║   { id: number, start: string, end: string }                  ║
║ Backend (api/shifts/my.ts):                                   ║
║   { id: number, start: string, end: string | null }           ║
╠───────────────────────────────────────────────────────────────╣
║ ❌ MISMATCH: end kan null zijn                                ║
╚═══════════════════════════════════════════════════════════════╝
```

## Als MISMATCH

Fix frontend type OF backend response. Beide moeten EXACT matchen.
