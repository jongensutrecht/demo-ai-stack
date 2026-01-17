# Unit Test Example

## Python (pytest)

```python
# tests/unit/test_invoice_calculator.py

import pytest
from decimal import Decimal
from src.domain.invoice import InvoiceCalculator

class TestInvoiceCalculator:
    """Unit tests for InvoiceCalculator."""

    @pytest.fixture
    def calculator(self):
        return InvoiceCalculator(tax_rate=Decimal("0.21"))

    def test_calculate_subtotal_single_item(self, calculator):
        """Single item subtotal calculation."""
        items = [{"qty": 2, "unit_price": Decimal("10.00")}]

        result = calculator.calculate_subtotal(items)

        assert result == Decimal("20.00")

    def test_calculate_subtotal_multiple_items(self, calculator):
        """Multiple items subtotal calculation."""
        items = [
            {"qty": 2, "unit_price": Decimal("10.00")},
            {"qty": 1, "unit_price": Decimal("25.00")},
        ]

        result = calculator.calculate_subtotal(items)

        assert result == Decimal("45.00")

    def test_calculate_tax(self, calculator):
        """Tax calculation at 21%."""
        subtotal = Decimal("100.00")

        result = calculator.calculate_tax(subtotal)

        assert result == Decimal("21.00")

    def test_calculate_total(self, calculator):
        """Total = subtotal + tax."""
        items = [{"qty": 1, "unit_price": Decimal("100.00")}]

        result = calculator.calculate_total(items)

        assert result == Decimal("121.00")

    def test_empty_items_returns_zero(self, calculator):
        """Empty items list returns zero."""
        result = calculator.calculate_subtotal([])

        assert result == Decimal("0.00")

    def test_negative_quantity_raises(self, calculator):
        """Negative quantity raises ValueError."""
        items = [{"qty": -1, "unit_price": Decimal("10.00")}]

        with pytest.raises(ValueError, match="negative"):
            calculator.calculate_subtotal(items)
```

## TypeScript (Jest)

```typescript
// tests/unit/invoiceCalculator.test.ts

import { InvoiceCalculator } from '../src/domain/invoiceCalculator';

describe('InvoiceCalculator', () => {
  let calculator: InvoiceCalculator;

  beforeEach(() => {
    calculator = new InvoiceCalculator({ taxRate: 0.21 });
  });

  describe('calculateSubtotal', () => {
    it('calculates subtotal for single item', () => {
      const items = [{ qty: 2, unitPrice: 10.0 }];

      const result = calculator.calculateSubtotal(items);

      expect(result).toBe(20.0);
    });

    it('calculates subtotal for multiple items', () => {
      const items = [
        { qty: 2, unitPrice: 10.0 },
        { qty: 1, unitPrice: 25.0 },
      ];

      const result = calculator.calculateSubtotal(items);

      expect(result).toBe(45.0);
    });

    it('returns zero for empty items', () => {
      const result = calculator.calculateSubtotal([]);

      expect(result).toBe(0);
    });

    it('throws for negative quantity', () => {
      const items = [{ qty: -1, unitPrice: 10.0 }];

      expect(() => calculator.calculateSubtotal(items)).toThrow('negative');
    });
  });

  describe('calculateTax', () => {
    it('calculates 21% tax', () => {
      const result = calculator.calculateTax(100.0);

      expect(result).toBe(21.0);
    });
  });

  describe('calculateTotal', () => {
    it('returns subtotal plus tax', () => {
      const items = [{ qty: 1, unitPrice: 100.0 }];

      const result = calculator.calculateTotal(items);

      expect(result).toBe(121.0);
    });
  });
});
```

## Key Points

1. **Isolatie**: Geen database, geen API calls, geen filesystem
2. **Fixtures**: Setup via `@pytest.fixture` of `beforeEach`
3. **Arrange-Act-Assert**: Duidelijke structuur
4. **Edge cases**: Empty input, negative values, etc.
5. **Naming**: Beschrijft wat getest wordt
