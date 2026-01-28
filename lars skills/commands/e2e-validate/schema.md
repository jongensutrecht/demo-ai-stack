# Schema Validatie Module

**Doel:** API responses matchen exact met gedocumenteerde spec.

## Waar Staat de Spec?

```
- openapi.yaml / swagger.json
- openspec/specs/
- TypeScript types (als geen OpenAPI)
```

## Validatie

```javascript
// Met ajv (JSON Schema validator)
const Ajv = require('ajv')
const ajv = new Ajv()

const schema = loadOpenAPISchema('/api/shifts')
const response = await fetch('/api/shifts').then(r => r.json())

const valid = ajv.validate(schema, response)
if (!valid) {
  console.error(ajv.errors)
}
```

## Check Punten

```
□ Required fields aanwezig
□ Data types correct (string/number/boolean)
□ Enum values geldig
□ Nullable fields correct gemarkeerd
□ Array items correct type
□ Nested objects correct
```

## Rapport

```
╔═══════════════════════════════════════════════════════════════╗
║                  SCHEMA VALIDATION                            ║
╠═══════════════════════════════════════════════════════════════╣
║ GET /api/shifts                                               ║
║   Required fields: ✅                                         ║
║   Types: ✅                                                   ║
║   Enums: ✅                                                   ║
╠───────────────────────────────────────────────────────────────╣
║ GET /api/gps                                                  ║
║   Required fields: ❌ missing 'accuracy'                      ║
║   Types: ✅                                                   ║
╠───────────────────────────────────────────────────────────────╣
║ Status: ❌ 1 SCHEMA MISMATCH                                  ║
╚═══════════════════════════════════════════════════════════════╝
```

## Als Mismatch

1. **Spec is correct** → Fix backend response
2. **Backend is correct** → Update spec
3. **Beiden fout** → Bepaal gewenst gedrag, fix beide
