import { test, expect } from '@playwright/test';

test('human evolution portal tree, unified index and browser history navigation', async ({ page }) => {
  test.setTimeout(180000);
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/#year=-45000');
  await expect(page.locator('#map')).toHaveAttribute('data-loaded-year', '-45000', { timeout: 90000 });
  await page.locator('#encyclopedia-button').click();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'fecha--45000');

  // El desplegable de la escala geológica abre su artículo introductorio.
  await page.locator('#encyclopedia-index summary[data-encyclopedia-intro="escala-temporal"]').click();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'escala-temporal');
  await expect(page.locator('#encyclopedia-index [data-encyclopedia-entry="escala-temporal"]')).toBeVisible();

  // «Evolución humana» abre su portada, que contiene el árbol completo; las especies van en su subdesplegable.
  await page.locator('#encyclopedia-index summary[data-encyclopedia-intro="humanidad-evolucion-humana"]').click();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'humanidad-evolucion-humana');
  const tree = page.locator('#encyclopedia-article .enc-htree');
  await expect(tree).toBeVisible();
  const rows = await tree.locator('.htree-row').count();
  expect(rows).toBe(39);
  await expect(tree.locator('.htree-flow-g')).toHaveCount(4);
  await expect(page.locator('#encyclopedia-index [data-encyclopedia-entry="hominin-afarensis"]')).toHaveCount(1);
  await tree.locator('[data-htree="all"]').click();
  await expect(tree).toHaveAttribute('data-all', 'false');
  expect(await tree.locator('.htree-row').count()).toBeLessThan(rows);
  await tree.locator('[data-htree="lin"]').click();
  await expect(tree).toHaveAttribute('data-log', 'false');
  await expect(tree.locator('.htree-flow-g')).toHaveCount(0);

  // Las fichas de especie conservan el comparador y enlazan al árbol general.
  await tree.locator('.htree-row[data-encyclopedia-entry="hominin-neanderthal"]').click();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'hominin-neanderthal');
  await expect(page.locator('#encyclopedia-article #human-compare-b')).toBeAttached();
  await expect(page.locator('#encyclopedia-article .enc-htree')).toHaveCount(0);
  await expect(page.locator('#encyclopedia-article .human-tree-link [data-encyclopedia-entry="humanidad-evolucion-humana"]')).toBeVisible();

  // Atrás y adelante del navegador recorren la enciclopedia y, al salir de ella, la cierran.
  await page.goBack();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'humanidad-evolucion-humana');
  await page.goForward();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'hominin-neanderthal');
  await page.locator('#encyclopedia-back').click();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'humanidad-evolucion-humana');
  await page.goBack(); await page.goBack();
  await expect(page.locator('#encyclopedia')).toHaveAttribute('data-article', 'fecha--45000');
  await page.goBack();
  await expect(page.locator('#encyclopedia')).not.toBeVisible();
  await expect(page.locator('#map')).toHaveAttribute('data-loaded-year', '-45000');
  expect(errors).toEqual([]);
});
