import {test,expect,type Page} from '@playwright/test';
async function date(page:Page,year:number){await page.goto(`/#year=${year}&view=mercator`);await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(year),{timeout:45000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}
async function imagesLoaded(page:Page){await expect.poll(()=>page.locator('#selection img').evaluateAll(nodes=>nodes.every(n=>(n as HTMLImageElement).complete&&(n as HTMLImageElement).naturalWidth>0))).toBe(true);}

test('opaque control, historical flags and leaders follow the war and occupation periods',async({page})=>{
 await date(page,1942);await search(page,'Alemania nazi');
 await expect(page.locator('.leader-name')).toContainText('Adolf Hitler');
 await expect(page.locator('.historic-flag')).toBeVisible();await imagesLoaded(page);
 await expect(page.locator('.control-swatches i[style*="#50545a"]')).toBeVisible();
 await page.screenshot({path:'test-results/1942-flag-leader.png'});
 await page.locator('#close-selection').click();await page.locator('#layers-button').click();
 await page.locator('#occupations-layer').click();await expect(page.locator('#map')).toHaveAttribute('data-overlays','0');await expect(page.locator('#map-legend')).toBeHidden();
 await page.locator('#occupations-layer').click();await expect(page.locator('#map')).toHaveAttribute('data-overlays','7');await page.locator('#close-layers').click();
 await date(page,1946);await search(page,'zonas de ocupación occidentales');
 await expect(page.locator('#selection-text')).toContainText('Administración militar aliada');await expect(page.locator('.historic-flag')).toHaveCount(0);await expect(page.locator('.leader-name')).toHaveCount(0);
 await date(page,1960);await search(page,'República Democrática Alemana');await expect(page.locator('.historic-flag')).toBeVisible();await imagesLoaded(page);
});

test('civil-war factions, revolutionary chronology and modern authority cards work on mobile',async({page})=>{
 await date(page,1937);await search(page,'zona republicana');
 await expect(page.locator('.leader-name').filter({hasText:'Juan Negrín'})).toBeVisible();await expect(page.locator('.leader-name').filter({hasText:'Manuel Azaña'})).toBeVisible();await expect(page.locator('.leader-name').filter({hasText:'Largo Caballero'})).toBeVisible();await expect(page.locator('#selection-text')).not.toContainText('Francisco Franco');await imagesLoaded(page);
 await expect(page.locator('#selection-text')).toContainText('octubre de 1937');
 await page.screenshot({path:'test-results/spanish-front-1937.png'});
 await page.locator('#close-selection').click();await search(page,'zona sublevada');await expect(page.locator('.leader-name')).toContainText('Francisco Franco');
 await date(page,1939);await search(page,'victoria franquista');await expect(page.locator('.leader-name')).toContainText('Francisco Franco');await expect(page.locator('.historic-flag')).toBeVisible();
 await date(page,1789);await search(page,'Francia');await expect(page.locator('.leader-name')).toContainText('Luis XVI');
 await date(page,1812);await search(page,'Francia');await expect(page.locator('.leader-name')).toContainText('Napoleón');await imagesLoaded(page);
 await page.screenshot({path:'test-results/france-1812.png'});
 await date(page,2023);await search(page,'Estados Unidos');await expect(page.locator('.leader-name')).toContainText('Biden');
 await page.setViewportSize({width:390,height:844});await date(page,2026);await search(page,'España');
 await expect(page.locator('.leader-name').filter({hasText:'Pedro Sánchez'})).toBeVisible();await imagesLoaded(page);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
 const card=await page.locator('#selection').boundingBox();expect(card!.y).toBeGreaterThanOrEqual(0);expect(card!.y+card!.height).toBeLessThan(844);
 await page.screenshot({path:'test-results/authority-mobile.png'});
});
