import { test, expect } from '@playwright/test';

test('hominin tree changes scale, hides discussed proposals and opens lineage pages', async ({ page }) => {
  test.setTimeout(180000);
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/#year=-45000');
  await expect(page.locator('#map')).toHaveAttribute('data-loaded-year', '-45000', { timeout: 90000 });
  await page.locator('#encyclopedia-button').click();
  await page.locator('#encyclopedia-search').fill('afarensis');
  await page.locator('#encyclopedia-index [data-encyclopedia-entry="hominin-afarensis"]').first().click();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'hominin-afarensis');
  const tree = page.locator('#encyclopedia-article .enc-htree');
  await expect(tree).toBeVisible();
  await expect(tree.locator('.htree-row.is-focus')).toHaveAttribute('data-encyclopedia-entry', 'hominin-afarensis');
  const rows = await tree.locator('.htree-row').count();
  expect(rows).toBe(39);
  await expect(tree.locator('.htree-flow-g')).toHaveCount(4);
  await tree.locator('[data-htree="all"]').click();
  await expect(tree).toHaveAttribute('data-all', 'false');
  expect(await tree.locator('.htree-row').count()).toBeLessThan(rows);
  await tree.locator('[data-htree="lin"]').click();
  await expect(tree).toHaveAttribute('data-log', 'false');
  await expect(tree.locator('.htree-flow-g')).toHaveCount(0);
  await tree.locator('.htree-row[data-encyclopedia-entry="hominin-neanderthal"]').click();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'hominin-neanderthal');
  await expect(page.locator('#encyclopedia-article .htree-row.is-focus')).toHaveAttribute('data-encyclopedia-entry', 'hominin-neanderthal');
  expect(errors).toEqual([]);
});
