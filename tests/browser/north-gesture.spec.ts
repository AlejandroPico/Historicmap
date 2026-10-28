import{test,expect,type Page}from'@playwright/test';
async function camera(p:Page){return JSON.parse((await p.locator('#map').getAttribute('data-camera'))!);}
for(const view of['mercator','globe'])test(`right double click faces north and preserves the camera in ${view}`,async({page})=>{
 test.setTimeout(150000);await page.goto(`/#year=1933&view=${view}`);await expect(page.locator('#map')).toHaveAttribute('data-rendered','history-1933',{timeout:90000});
 if(view==='mercator'){
  await page.locator('#search-button').click();await page.locator('#search-input').fill('Uruguay');await page.locator('#search-results button').first().click();await expect(page.locator('#selection')).toHaveAttribute('data-entity','URY');const portrait=page.locator('#selection img[src$="portrait-5d3e717ac58035dd253d.jpg"]');await expect(portrait).toBeVisible();await expect.poll(()=>portrait.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);await expect(page.locator('#selection')).toContainText('1 de marzo de 1931');await page.screenshot({path:'test-results/terra-1933-portrait.png'});await page.locator('#close-selection').click();
 }
 await page.mouse.move(900,450);await page.mouse.down({button:'right'});await page.mouse.move(1020,410,{steps:12});await page.mouse.up({button:'right'});await expect.poll(async()=>Math.abs((await camera(page)).bearing)).toBeGreaterThan(5);const before=await camera(page);
 await page.mouse.click(1000,430,{button:'right'});expect((await camera(page)).bearing).toBeCloseTo(before.bearing,4);await page.mouse.click(1000,430,{button:'left'});
 await page.locator('#map canvas').dblclick({button:'right',position:{x:1000,y:430}});await expect.poll(async()=>Math.abs((await camera(page)).bearing)).toBeLessThan(0.001);const after=await camera(page);expect(after.zoom).toBeCloseTo(before.zoom,7);expect(after.center[0]).toBeCloseTo(before.center[0],7);expect(after.center[1]).toBeCloseTo(before.center[1],7);expect(after.pitch).toBeCloseTo(before.pitch,7);
});
