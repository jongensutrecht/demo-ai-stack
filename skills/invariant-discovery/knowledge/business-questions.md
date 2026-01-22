# Business Discovery Questions

## Checklist

- [ ] Welke waarden mogen NOOIT negatief?
- [ ] Welke state transitions zijn ongeldig?
- [ ] Welke operaties mogen NOOIT dubbel?
- [ ] Welke data moet altijd consistent?
- [ ] Welke acties vereisen audit trail?

## Typische Invarianten

| ID | Invariant |
|----|-----------|
| INV-BIZ-001 | Invoice totals are NEVER negative |
| INV-BIZ-002 | Payments are NEVER processed twice |
| INV-BIZ-010 | Order status NEVER skips intermediate states |
| INV-BIZ-020 | Parent-child relationships are NEVER orphaned |

## Details

Volledige vragen: `python scripts/questions.py business`
