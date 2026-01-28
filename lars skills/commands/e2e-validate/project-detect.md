# Project Detectie Module

**Doel:** Identificeer project type, specs, en test scope.

## Detectie Volgorde

```
1. CLAUDE.md → Project specs, invariants, business rules
2. package.json → Node/JS project, scripts
3. openspec/ → API contracts
4. tests/ → Bestaande test patterns
5. src/ → Code structuur
```

## Output

```
PROJECT: driver_app_gps
TYPE: Web app (React + Node API)

SPECS GEVONDEN:
- CLAUDE.md (business rules, invariants)
- openspec/specs/shifts/spec.md
- openspec/specs/gps/spec.md

ENTRY POINTS:
- UI: http://localhost:3000
- API: http://localhost:3000/api/*

BESTAANDE TESTS:
- tests/lib/*.test.ts (unit)
- e2e/*.spec.ts (Playwright)

INVARIANTS:
- GPS data NOOIT verloren
- Shift NOOIT editen na approval
- Session NOOIT auto-logout tijdens GPS sync
```

## Contracts Vinden

```
ZOEK naar:
- openapi.yaml / swagger.json
- openspec/specs/
- TypeScript interfaces in src/types/
- API response types
```

## Test Scripts Vinden

```bash
# Uit package.json
npm run test        # Unit tests
npm run test:e2e    # E2E tests
npm run lint        # Linting
npm run typecheck   # TypeScript
```
