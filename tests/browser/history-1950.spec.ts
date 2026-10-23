import {test,expect,type Page} from '@playwright/test';
async function ready(page:Page,year:number){await expect(page.locator('#map')).toHaveAttribute('data-rendered',`history-${year}`,{timeout:60000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}
async function year(page:Page,n:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(n));await page.locator('#date-form button[type=submit]').click();await ready(page,n);}
test('1950s leaders, stationary card header, inner scrolling and comparison actions',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1952&view=mercator');await ready(page,1952);await search(page,'Egipto');
 await expect(page.locator('#pane-authorities')).toContainText('Farouk I');await expect(page.locator('#pane-authorities')).toContainText('Fuad II');
 await expect(page.locator('.historic-flag')).toBeVisible();await expect(page.getByText('Fuente de la bandera',{exact:true})).toHaveCount(0);
 await expect(page.locator('#pin-country')).not.toBeVisible();
 const before=await page.locator('.country-tabs').boundingBox();
 await page.locator('.country-content').evaluate(e=>{e.scrollTop=250;});
 expect(await page.locator('.country-content').evaluate(e=>e.scrollTop)).toBeGreaterThan(100);
 const after=await page.locator('.country-tabs').boundingBox();expect(after!.y).toBeCloseTo(before!.y,1);
 await expect(page.locator('.historic-flag')).toBeVisible();
 await page.getByRole('tab',{name:'Comparar',exact:true}).click();await expect(page.locator('#pin-country')).toBeVisible();
 await expect(page.locator('#comparison-dates')).toBeVisible();
 await page.getByRole('tab',{name:'Autoridades',exact:true}).click();await year(page,1953);
 await expect(page.locator('#selection')).toHaveAttribute('data-entity','EGY');await expect(page.locator('#pane-authorities')).toContainText('Naguib');
 await year(page,1954);await search(page,'Estado de Vietnam');await expect(page.locator('#selection')).toHaveAttribute('data-entity','VSV');
 await expect(page.locator('#pane-authorities')).toContainText('Bảo Đại');
 await year(page,1959);await search(page,'Federación de Malaya');await expect(page.locator('#selection')).toHaveAttribute('data-entity','MAL');
 await expect(page.locator('#pane-authorities')).toContainText('Tunku Abdul Rahman');
 await page.setViewportSize({width:390,height:844});await expect(page.locator('.country-tabs')).toBeVisible();
 await page.locator('.country-content').evaluate(e=>{e.scrollTop=200;});await expect(page.locator('.historic-flag')).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
 await page.screenshot({path:'test-results/1959-card-mobile.png'});expect(errors).toEqual([]);
});
