# Testing & QA

## Pyramid
- Many **unit** tests (pure logic), some **integration** (module + DB/API), few **e2e** (real user flows).

## Tooling
- JS/TS: **Vitest** or Jest (unit), **Playwright** (e2e, cross-browser), Testing Library (components).
- Python: **pytest** (+ pytest-asyncio), `httpx`/TestClient for APIs.
- Go: built-in `testing` + `testify`.

## Vitest example
```ts
import { expect, test } from 'vitest';
import { add } from './math';
test('adds', () => { expect(add(2,3)).toBe(5); });
```

## Playwright example
```ts
import { test, expect } from '@playwright/test';
test('login', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('a@b.com');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).toHaveURL('/dashboard');
});
```

## Discipline
- Write a failing test first for bug fixes (reproduce, then fix).
- Test behavior, not implementation. Cover edge cases + error paths.
- Run tests in CI on every push. Keep them fast and deterministic (no real network — mock it).
- After ANY change, run the test/build command and read the output before declaring success.
