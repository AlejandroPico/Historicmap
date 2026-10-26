import {test,expect,type Page} from '@playwright/test';
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-rendered',y>=2020?'countries.geojson':`history-${y}`,{timeout:90000});}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);const result=p.locator('#search-results button').first();await expect(result,s).toBeVisible({timeout:10000});await result.click();}
async function image(p:Page,name:string){const img=p.locator('.leader-card').filter({has:p.locator('.leader-name',{hasText:name})}).first().locator('img');await img.scrollIntoViewIfNeeded();await expect.poll(()=>img.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);return img;}
test('1885 land click, source reversals, globe, Pacific references and1860 authority coverage',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1885&view=mercator');await ready(page,1885);await search(page,'Francia');await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true');
 await page.locator('#map').click({position:{x:900,y:250}});await expect(page.locator('#selection')).toHaveAttribute('data-entity','FRA');await expect(page.locator('#selection')).toBeVisible();
 await year(page,1886);await year(page,1885);await expect(page.locator('#selection')).toHaveAttribute('data-entity','FRA');await page.locator('#projection-button').click();await expect(page.locator('#projection-button')).toHaveAttribute('data-view','globe');await expect(page.locator('#selection')).toBeVisible();
 await year(page,2016);await search(page,'Guam');await expect(page.locator('#selection')).toHaveAttribute('data-entity','GUM');await expect(page.locator('#pane-authorities')).toContainText('Obama');
 await year(page,1860);await search(page,'Estados Unidos');await expect(page.locator('#selection')).toHaveAttribute('data-entity','USA');await expect(page.locator('#pane-authorities')).toContainText('Buchanan');
 await year(page,1871);await search(page,'Francia');await expect(page.locator('#pane-authorities')).toContainText('Thiers');expect(errors).toEqual([]);
});
test('dated portraits decode and Ukraine observation date stays visible with optional hatching',async({page})=>{
 test.setTimeout(180000);await page.goto('/#year=1888&view=mercator');await ready(page,1888);await search(page,'Francia');await image(page,'Sadi Carnot');
 await year(page,2007);await search(page,'Vietnam');await image(page,'Tri');
 await year(page,1992);await search(page,'India');await image(page,'Sharma');await page.screenshot({path:'test-results/sharma-1992-014.png'});
 await year(page,2020);await search(page,'Estados Unidos');const first=await (await image(page,'Trump')).getAttribute('src');await year(page,2026);const second=await (await image(page,'Trump')).getAttribute('src');expect(second).not.toBe(first);
 await expect(page.locator('.control-observation')).toContainText('17/12/2025');await page.locator('#layers-button').click();await page.locator('#occupations-layer').click();await expect(page.locator('#map')).not.toHaveAttribute('data-overlays','0');await page.locator('#close-layers').click();await page.screenshot({path:'test-results/ukraine-2026-014.png'});
});
