# Business Invariant Discovery Questions

Gebruik deze vragen om business rule invarianten te ontdekken.

---

## Financial Integrity

### Monetary Values
- Welke velden representeren geld (price, amount, total)?
- Mogen deze waarden OOIT negatief zijn?
- Hoe worden kortingen toegepast?
- Kunnen kortingen tot negatieve totalen leiden?

### Payments & Refunds
- Mogen refunds OOIT het originele bedrag overschrijden?
- Mogen dubbele betalingen OOIT voorkomen?
- Wat is de maximum korting percentage?

### Currency & Rounding
- Hoe wordt afgerond?
- Mag afrondingsverschil OOIT significant zijn?

**Typische invarianten:**
- `INV-BIZ-001`: Invoice totals are NEVER negative
- `INV-BIZ-002`: Payments are NEVER processed twice for same invoice
- `INV-BIZ-003`: Refunds NEVER exceed original payment amount
- `INV-BIZ-004`: Discounts NEVER result in negative total

---

## State Machines

### Order/Transaction States
- Welke statussen zijn er (pending, confirmed, shipped, etc.)?
- Wat is de geldige state flow?
- Welke transities zijn NOOIT toegestaan?
- Kunnen statussen overgeslagen worden?

### Terminal States
- Welke statussen zijn eindig (completed, cancelled)?
- Mag een terminal state OOIT verlaten worden?
- Mag data gewijzigd worden na een terminal state?

**Typische invarianten:**
- `INV-BIZ-010`: Order status NEVER skips intermediate states
- `INV-BIZ-011`: Completed orders are NEVER modified
- `INV-BIZ-012`: Cancelled orders are NEVER re-activated
- `INV-BIZ-013`: Shipped orders can NEVER be cancelled

---

## Data Integrity

### Relationships
- Welke parent-child relaties zijn er?
- Mogen orphaned records OOIT ontstaan?
- Wat gebeurt bij parent deletion?

### Unique Constraints
- Welke velden moeten uniek zijn?
- Mogen duplicates OOIT voorkomen?

### Consistency
- Welke data moet altijd consistent zijn?
- Zijn er berekende velden die altijd kloppen moeten?
- Mogen totalen OOIT afwijken van line items?

**Typische invarianten:**
- `INV-BIZ-020`: Parent-child relationships are NEVER orphaned
- `INV-BIZ-021`: Email addresses are NEVER duplicated
- `INV-BIZ-022`: Order total NEVER differs from sum of line items

---

## Business Rules

### Quantities & Limits
- Zijn er minimum/maximum waarden?
- Mogen negatieve hoeveelheden OOIT voorkomen?
- Zijn er stock/inventory limits?

### Time-based Rules
- Zijn er deadline rules (bijv. bestellingen voor 15:00)?
- Mogen acties OOIT buiten bepaalde tijden?
- Zijn er expiratie regels?

### Conditional Rules
- Welke acties vereisen voorwaarden?
- Mogen acties OOIT zonder vereiste voorwaarden?

**Typische invarianten:**
- `INV-BIZ-030`: Quantity is NEVER negative
- `INV-BIZ-031`: Stock is NEVER oversold
- `INV-BIZ-032`: Expired coupons are NEVER accepted
- `INV-BIZ-033`: Orders are NEVER placed outside business hours

---

## Audit & Compliance

### Audit Trail
- Welke acties moeten gelogd worden?
- Mogen wijzigingen OOIT zonder audit trail?
- Mogen deletes OOIT zonder backup/log?

### Compliance
- Zijn er compliance requirements (GDPR, PCI, etc.)?
- Mogen bepaalde data OOIT onversleuteld?

**Typische invarianten:**
- `INV-BIZ-040`: Deletions are NEVER without audit log
- `INV-BIZ-041`: User data is NEVER retained beyond retention period
- `INV-BIZ-042`: Payment data is NEVER stored unencrypted

---

## Questions to Ask User

```markdown
1. **Financial**
   - Welke velden representeren geldbedragen?
   - Mogen deze ooit negatief zijn?
   - Hoe worden kortingen/refunds afgehandeld?

2. **State Machines**
   - Welke statussen/states zijn er voor de belangrijkste entiteiten?
   - Wat is de toegestane flow tussen statussen?
   - Welke statussen zijn eindig (geen weg terug)?

3. **Data Integrity**
   - Welke velden moeten uniek zijn?
   - Welke relaties moeten altijd intact blijven?
   - Zijn er berekende velden die altijd moeten kloppen?

4. **Business Rules**
   - Welke specifieke business regels zijn er?
   - Zijn er minimum/maximum waarden?
   - Zijn er tijdgebonden regels?

5. **Audit**
   - Welke acties moeten worden gelogd?
   - Zijn er compliance requirements?
```

---

## Discovery Commands

```bash
# Find status/state fields
rg "status|state" --type py | head -50
rg "enum.*Status|Status.*enum" --type py

# Find financial fields
rg "price|amount|total|subtotal|tax|discount" --type py
rg "Decimal|decimal|money" --type py

# Find validation
rg "validate|validator|ValidationError" --type py
rg "if.*<.*0|>.*max|<.*min" --type py

# Find unique constraints
rg "unique=True|UniqueConstraint|unique_together" --type py

# Find audit logging
rg "audit|log.*created|log.*updated|log.*deleted" --type py

# Find state transitions
rg "transition|from.*to|valid_transitions" --type py
```
