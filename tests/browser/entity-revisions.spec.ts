import{test,expect,type Page}from'@playwright/test';
const ready=async(p:Page,y:number)=>expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string,key:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);await p.locator('#search-results button').first().click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);}
async function images(p:Page){for(const img of await p.locator('.historic-flag,.leader-portrait').all()){await img.scrollIntoViewIfNeeded();await expect.poll(()=>img.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);}await p.locator('.country-content').evaluate(e=>e.scrollTop=0);}

test('Dutch provincial authorities, union ensigns and Río governments update in the open card',async({page})=>{
 test.setTimeout(240000);await page.goto('/#year=1723&view=mercator');await ready(page,1723);await search(page,'República de las Provincias Unidas','DUTCH-REPUBLIC');await expect(page.locator('#pane-authorities')).toContainText('Estatúder de Frisia');await expect(page.locator('#pane-authorities')).toContainText('María Luisa');await images(page);await expect(page.locator('.historic-flag')).toHaveAttribute('src',/flag-/);await page.screenshot({path:'test-results/entity-revisions-dutch.png'});
 await year(page,1755);await expect(page.locator('#pane-authorities')).toContainText('Ana de Hannover');await images(page);
 await year(page,1830);await search(page,'Unión de Suecia y Noruega','HIST-Q62589');await expect(page.locator('.identity-header')).toContainText('naval');await images(page);
 await search(page,'Provincias Unidas del Río de la Plata','RIO-DE-LA-PLATA');await expect(page.locator('#pane-authorities')).toContainText('Sin ejecutivo nacional común');await images(page);await year(page,1827);await expect(page.locator('#pane-authorities')).toContainText('Vicente López');await expect(page.locator('#pane-authorities')).toContainText('Rivadavia');await images(page);
});

test('medieval references expose their evidence date without inventing contemporary flags',async({page})=>{
 test.setTimeout(180000);await page.goto('/#year=1291&view=mercator');await ready(page,1291);await search(page,'Novgorod Republic','HIST-Q151536');await expect(page.locator('.identity-header')).toContainText('Referencia retrospectiva');await expect(page.locator('.identity-header')).toContainText('XIV');await images(page);await page.screenshot({path:'test-results/entity-revisions-novgorod.png'});
 await year(page,1146);await search(page,'Portugal','PRT');await expect(page.locator('.identity-header')).toContainText('reconstrucción');await images(page);await page.setViewportSize({width:390,height:844});expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);await page.screenshot({path:'test-results/entity-revisions-portugal-mobile.png'});
});
