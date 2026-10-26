import{test,expect,type Page}from'@playwright/test';
import{openFilters,closeTools,selectFilter}from'./tools';
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string,key:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);await p.locator('#search-results button').first().click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);}
test('separate funnel, positive choices, zero-result persistence and mobile controls',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/#year=1797&view=mercator');await ready(page,1797);
 expect(await page.locator('.toolbar>button').evaluateAll(es=>es.map(e=>e.id))).toContain('filters-button');const a=(await page.locator('#filters-button').boundingBox())!,b=(await page.locator('#layers-button').boundingBox())!;expect(a.x).toBeLessThan(b.x);
 await openFilters(page);await expect(page.locator('#filters-panel #government-select,#filters-panel #affiliation-select,#filters-panel #theme-select')).toHaveCount(3);await expect(page.locator('#layers-panel select')).toHaveCount(0);
 expect(await page.locator('#government-select option[value]:not([value=""])').evaluateAll(es=>es.every(e=>Number(e.textContent?.split(' · ').at(-1))>0))).toBe(true);
 await selectFilter(page,'#government-select','directorial');await year(page,1700);await expect(page.locator('#filters-panel')).toBeVisible();await expect(page.locator('#map')).toHaveAttribute('data-government-filter','directorial');await expect(page.locator('#map')).toHaveAttribute('data-government-matches','0');await expect(page.locator('#government-empty')).toContainText('1700');await expect(page.locator('#government-select option[value="directorial"]')).toHaveCount(0);
 await page.locator('#government-empty button').click();await expect(page.locator('#map')).toHaveAttribute('data-government-filter','');await expect(page.locator('#government-empty')).toBeHidden();await page.keyboard.press('Escape');await expect(page.locator('#filters-button')).toBeFocused();
 await page.setViewportSize({width:390,height:844});await openFilters(page);expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);await page.screenshot({path:'test-results/review-019-filters-mobile.png'});await closeTools(page);expect(errors).toEqual([]);
});
test('new century, German grouped seats, Asian offices and authentic symbol types',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/#year=1700&view=globe');await ready(page,1700);
 await search(page,'Francia','FRA');await expect(page.locator('#pane-authorities')).toContainText('Luis XIV');await expect(page.locator('.historic-flag')).toBeVisible();
 await search(page,'Hesse-Darmstadt','HESSE-DARMSTADT');await expect(page.locator('#pane-authorities')).toContainText('Landgrave');await year(page,1750);await expect(page.locator('#selection')).toHaveAttribute('data-entity','HESSE-DARMSTADT');await expect(page.locator('#pane-authorities')).toContainText('Luis VIII');await expect(page.locator('.historic-flag')).toBeVisible();
 await page.getByRole('tab',{name:'Territorio',exact:true}).click();await expect(page.locator('#pane-territory')).toContainText('agrupa');await year(page,1800);await search(page,'Japón','JPN');await expect(page.locator('.identity-header')).toContainText('Mon de los Tokugawa');await expect(page.locator('#pane-authorities')).toContainText('Shogun');
 await year(page,1700);await search(page,'Mughal','HIST-Q33296');await expect(page.locator('#pane-authorities')).toContainText('Aurangzeb');await expect.poll(()=>page.locator('.leader-portrait').first().evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);
 await search(page,'Joseon','JOS');await expect(page.locator('.identity-header')).toContainText('Sello del rey');await year(page,1800);await expect(page.locator('.identity-header')).toContainText('Sello del rey');
 await page.screenshot({path:'test-results/review-019-joseon-globe.png'});expect(errors).toEqual([]);
});
