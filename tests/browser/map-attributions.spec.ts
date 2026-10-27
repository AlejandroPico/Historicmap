import{test,expect}from'@playwright/test';
test('cartographic credits live in Sources while the geographic scale remains alone',async({page})=>{
 test.setTimeout(150000);await page.goto('/#year=2026&view=mercator');await expect(page.locator('#map')).toHaveAttribute('data-rendered','countries.geojson',{timeout:90000});
 await expect(page.locator('.maplibregl-ctrl-attrib,.maplibregl-ctrl-attrib-button')).toHaveCount(0);await expect(page.locator('.maplibregl-ctrl-bottom-left .maplibregl-ctrl-scale')).toBeVisible();await expect(page.locator('#sources-panel')).toBeHidden();
 await page.locator('#sources-button').click();const details=page.locator('.map-credits');await expect(details).not.toHaveAttribute('open');await details.locator('summary').click();await expect(details).toHaveAttribute('open','');
 for(const text of ['Natural Earth','CShapes','Ourednik','Cao et al.','Mapzen','Cliopatria','Tyk'])await expect(page.locator('#map-attributions')).toContainText(text);
 await expect(page.locator('#map-attributions a[href="https://github.com/Seshat-Global-History-Databank/cliopatria"]')).toBeVisible();await expect(page.locator('#modal')).toBeHidden();await page.screenshot({path:'test-results/review-026-map-credits.png'});
 await page.locator('#date-button').click();await page.locator('#date-input').fill('1000');await page.locator('#date-form button[type=submit]').click();await expect(page.locator('#map')).toHaveAttribute('data-rendered','history-1000',{timeout:90000});await expect(details).toHaveAttribute('open','');await expect(page.locator('#map-attributions')).toContainText('CShapes');
 await page.setViewportSize({width:390,height:844});await expect(page.locator('.maplibregl-ctrl-scale')).toBeVisible();expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);await expect(page.locator('.maplibregl-ctrl-attrib')).toHaveCount(0);
});
