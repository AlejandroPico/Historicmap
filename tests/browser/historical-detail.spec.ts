import {test,expect,type Page} from '@playwright/test';
async function date(page:Page,y:number){await page.goto(`/#year=${y}&view=mercator`);await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(y),{timeout:45000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}

test('compact search has no backdrop, supports keyboard and closes on date changes',async({page})=>{
 await date(page,1990);await page.locator('#search-button').click();
 await expect(page.locator('#search-panel')).toBeVisible();await expect(page.locator('#modal')).toBeHidden();
 expect((await page.locator('#search-panel').boundingBox())!.width).toBeLessThanOrEqual(350);
 await page.locator('#search-input').fill('Brasil');await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');
 await expect(page.locator('#search-panel')).toBeHidden();await expect(page.locator('.political-identity')).toHaveAttribute('data-identity','BRA');
 await page.locator('#search-button').click();await page.keyboard.press('Escape');await expect(page.locator('#selection')).toBeVisible();
 await page.locator('#search-button').click();await page.locator('#date-button').click();await expect(page.locator('#search-panel')).toBeHidden();await page.keyboard.press('Escape');
 await page.setViewportSize({width:390,height:844});await page.locator('#search-button').click();
 expect((await page.locator('#search-panel').boundingBox())!.width).toBeLessThan(390);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
});

test('organizations remain selected through historical years and respect formation and dissolution',async({page})=>{
 await date(page,1990);await page.locator('#layers-button').click();
 expect(await page.locator('#affiliation-select option').count()).toBeGreaterThanOrEqual(28);
 await page.locator('#affiliation-select').selectOption('warsaw');await expect(page.locator('#map-legend')).toContainText('1990');
 await page.locator('#close-layers').click();await page.goto('/#year=1991&view=mercator');
 await expect(page.locator('#map')).toHaveAttribute('data-loaded-year','1991',{timeout:45000});
 await expect(page.locator('#affiliation-select')).toHaveValue('warsaw');await expect(page.locator('#map-legend')).toContainText('no está activa');
 await page.locator('#layers-button').click();await page.locator('#affiliation-select').selectOption('eu');await page.locator('#close-layers').click();
 await page.goto('/#year=2020&view=mercator');await expect(page.locator('#map')).toHaveAttribute('data-loaded-year','2020',{timeout:45000});
 await expect(page.locator('#map-legend')).toContainText('2020');await search(page,'Reino Unido');
 await page.getByRole('tab',{name:'Datos',exact:true}).click();await expect(page.locator('#pane-facts')).toContainText('Unión Europea');
 await expect(page.locator('#pane-facts')).toContainText('2020-02-01');
});

test('historical country cards include dated leaders, images, conflicts and disputed institutions',async({page})=>{
 test.setTimeout(240000);
 await date(page,1990);await search(page,'Brasil');
 await expect(page.locator('#pane-authorities')).toContainText('Sarney');await expect(page.locator('#pane-authorities')).toContainText('Collor');
 await expect(page.locator('#pane-authorities .leader-portrait').first()).toBeVisible();
 await page.locator('#close-selection').click();await search(page,'Unión Soviética');await expect(page.locator('.political-identity')).toHaveAttribute('data-identity','USSR');await expect(page.locator('#pane-authorities')).toContainText('Gorbachov');
 await date(page,1992);await search(page,'Checoslovaquia');await expect(page.locator('#pane-authorities')).toContainText('Havel');
 await date(page,2000);await search(page,'Federal de Yugoslavia');await expect(page.locator('.political-identity')).toHaveAttribute('data-identity','FRY');await expect(page.locator('#pane-authorities .leader-name').first()).toBeVisible();
 await date(page,2026);await search(page,'Sahara');await expect(page.locator('#pane-authorities')).toContainText('no autónomo');await expect(page.locator('#pane-authorities')).toContainText('RASD');await expect(page.locator('#pane-authorities')).toContainText('marroquí');
 await page.getByRole('tab',{name:'Conflictos',exact:true}).click();await expect(page.locator('#pane-conflicts')).toContainText('Sáhara');
 await date(page,2014);await search(page,'Ucrania');await page.getByRole('tab',{name:'Conflictos',exact:true}).click();await expect(page.locator('#pane-conflicts')).toContainText('2014');
 await expect(page.locator('#pane-conflicts')).not.toContainText('24 de febrero de 2022');
 await date(page,1990);await search(page,'Kuwait · ocupación iraquí');await expect(page.locator('.political-identity')).toHaveAttribute('data-identity','IRQ');await expect(page.locator('#pane-authorities')).toContainText('Huseín');
 await date(page,1991);await page.locator('#search-button').click();await page.locator('#search-input').fill('Kuwait · ocupación iraquí');await expect(page.locator('#search-results')).toContainText('Sin resultados');
});
