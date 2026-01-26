# Button Inventory Module

**Doel:** Vind en test ELKE klikbare element.

## Scan Alle Buttons

```
VOOR ELKE pagina:
1. Navigeer naar pagina
2. Identificeer alle klikbare elementen:
   - <button>
   - <a href>
   - onClick handlers
   - role="button"
   - Icons met click
   - Form submits
```

## Inventory Format

```markdown
| ID | Element | Pagina | Actie | Getest? |
|----|---------|--------|-------|---------|
| B1 | Login button | /login | Submit credentials | ❌ |
| B2 | Start shift | /dashboard | POST /api/shifts/start | ❌ |
| B3 | End shift | /dashboard | POST /api/shifts/end | ❌ |
| B4 | Menu toggle | Header | Open sidebar | ❌ |
| B5 | Logout | Header | Clear session | ❌ |
```

## Per Button Test

```
ELKE button MOET:
1. Click test → Werkt de click?
2. State test → Verandert UI correct?
3. Error test → Wat bij failure?
```

## Voorbeeld Test

```javascript
test('Login button submits form', async () => {
  // 1. Click
  await page.click('[data-testid="login-button"]')

  // 2. State check
  await expect(page).toHaveURL('/dashboard')

  // 3. Error case
  await page.fill('#password', 'wrong')
  await page.click('[data-testid="login-button"]')
  await expect(page.locator('.error')).toBeVisible()
})
```

## Rapport

```
╔══════════════════════════════════════════════════════════════╗
║                  BUTTON INVENTORY                            ║
╠══════════════════════════════════════════════════════════════╣
║ Total buttons found: 18                                      ║
║ Tested: 16                                                   ║
║ Missing: 2                                                   ║
╠──────────────────────────────────────────────────────────────╣
║ ❌ Settings button - no test                                 ║
║ ❌ Help icon - no test                                       ║
╠══════════════════════════════════════════════════════════════╣
║ Coverage: 89% - NEED 100%                                    ║
╚══════════════════════════════════════════════════════════════╝
```
