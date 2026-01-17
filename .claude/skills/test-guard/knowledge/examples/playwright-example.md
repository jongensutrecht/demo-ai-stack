# Playwright E2E Test Example

## Basic Page Test

```typescript
// tests/e2e/login.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Login Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('displays login form', async ({ page }) => {
    await expect(page.locator('h1')).toHaveText('Login');
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    // Fill form
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password123');

    // Submit
    await page.click('button[type="submit"]');

    // Verify redirect
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]')).toHaveText(
      /Welcome/
    );
  });

  test('invalid credentials shows error', async ({ page }) => {
    await page.fill('input[name="email"]', 'wrong@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toHaveText(
      'Invalid email or password'
    );
    await expect(page).toHaveURL('/login'); // Stay on login page
  });

  test('empty form shows validation errors', async ({ page }) => {
    await page.click('button[type="submit"]');

    await expect(page.locator('[data-error="email"]')).toBeVisible();
    await expect(page.locator('[data-error="password"]')).toBeVisible();
  });
});
```

## Component Test

```typescript
// tests/e2e/components/button.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Button Component', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/storybook/button'); // Or component showcase page
  });

  test('primary button renders correctly', async ({ page }) => {
    const button = page.locator('[data-testid="primary-button"]');

    await expect(button).toBeVisible();
    await expect(button).toHaveCSS('background-color', 'rgb(59, 130, 246)');
  });

  test('button click triggers action', async ({ page }) => {
    const button = page.locator('[data-testid="action-button"]');
    const output = page.locator('[data-testid="click-output"]');

    await button.click();

    await expect(output).toHaveText('Button clicked!');
  });

  test('disabled button cannot be clicked', async ({ page }) => {
    const button = page.locator('[data-testid="disabled-button"]');

    await expect(button).toBeDisabled();
    await expect(button).toHaveCSS('cursor', 'not-allowed');
  });

  test('loading button shows spinner', async ({ page }) => {
    const button = page.locator('[data-testid="loading-button"]');
    const spinner = button.locator('.spinner');

    await expect(spinner).toBeVisible();
    await expect(button).toBeDisabled();
  });
});
```

## User Flow Test

```typescript
// tests/e2e/checkout.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Checkout Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
  });

  test('complete checkout flow', async ({ page }) => {
    // 1. Add product to cart
    await page.goto('/products');
    await page.click('[data-testid="product-1"] [data-testid="add-to-cart"]');

    // Verify cart badge
    await expect(page.locator('[data-testid="cart-badge"]')).toHaveText('1');

    // 2. Go to cart
    await page.click('[data-testid="cart-icon"]');
    await expect(page).toHaveURL('/cart');
    await expect(page.locator('[data-testid="cart-item"]')).toHaveCount(1);

    // 3. Proceed to checkout
    await page.click('[data-testid="checkout-button"]');
    await expect(page).toHaveURL('/checkout');

    // 4. Fill shipping info
    await page.fill('input[name="address"]', '123 Main St');
    await page.fill('input[name="city"]', 'Amsterdam');
    await page.fill('input[name="postal"]', '1234 AB');

    // 5. Select payment method
    await page.click('[data-testid="payment-ideal"]');

    // 6. Place order
    await page.click('[data-testid="place-order"]');

    // 7. Verify confirmation
    await expect(page).toHaveURL(/\/order\/\d+/);
    await expect(page.locator('[data-testid="order-success"]')).toBeVisible();
  });

  test('empty cart shows message', async ({ page }) => {
    await page.goto('/cart');

    await expect(page.locator('[data-testid="empty-cart"]')).toBeVisible();
    await expect(page.locator('[data-testid="checkout-button"]')).not.toBeVisible();
  });
});
```

## API Mocking

```typescript
// tests/e2e/with-mock.spec.ts

import { test, expect } from '@playwright/test';

test('shows products from API', async ({ page }) => {
  // Mock API response
  await page.route('/api/products', async (route) => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify([
        { id: 1, name: 'Product 1', price: 10.0 },
        { id: 2, name: 'Product 2', price: 20.0 },
      ]),
    });
  });

  await page.goto('/products');

  await expect(page.locator('[data-testid="product"]')).toHaveCount(2);
  await expect(page.locator('[data-testid="product-1"]')).toContainText('Product 1');
});

test('shows error on API failure', async ({ page }) => {
  await page.route('/api/products', async (route) => {
    await route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Internal Server Error' }),
    });
  });

  await page.goto('/products');

  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
});
```

## Visual Regression

```typescript
// tests/e2e/visual.spec.ts

import { test, expect } from '@playwright/test';

test('homepage matches snapshot', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveScreenshot('homepage.png');
});

test('button states match snapshot', async ({ page }) => {
  await page.goto('/storybook/button');

  const button = page.locator('[data-testid="primary-button"]');

  // Normal state
  await expect(button).toHaveScreenshot('button-normal.png');

  // Hover state
  await button.hover();
  await expect(button).toHaveScreenshot('button-hover.png');
});
```

## Key Points

1. **data-testid**: Gebruik voor stabiele selectors
2. **expect(page).toHaveURL**: Verify navigation
3. **expect(locator).toBeVisible**: Check element visibility
4. **page.route**: Mock API responses
5. **Screenshots**: Visual regression testing
