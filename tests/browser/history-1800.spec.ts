import {test,expect,type Page} from '@playwright/test';
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string,key:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);const r=p.locator('#search-results button').first();await expect(r).toBeVisible();await r.click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);}
test('1800–1819 regimes, Italian state symbols, conflicts and persistent transition to1820',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1800&view=globe');await ready(page,1800);await search(page,'Francia','FRA');await expect(page.locator('#pane-authorities')).toContainText('cónsul');
 await year(page,1804);await expect(page.locator('#selection')).toHaveAttribute('data-entity','FRA');await expect(page.locator('#pane-authorities')).toContainText('Emperador');
 await year(page,1815);await expect(page.locator('#pane-authorities')).toContainText('Luis XVIII');await expect(page.locator('#pane-authorities')).toContainText('Napoleón');
 await year(page,1812);await search(page,'Reino de Italia napoleónico','NAPOLEONIC-ITALY');await expect(page.locator('#pane-authorities')).toContainText('Rey de Italia');await expect(page.locator('.historic-flag')).toBeVisible();
 const image=page.locator('.leader-portrait').first();await expect.poll(()=>image.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);
 await search(page,'España','ESP');await expect(page.locator('#pane-authorities')).toContainText('José');await page.getByRole('tab',{name:'Conflictos',exact:true}).click();await expect(page.locator('#pane-conflicts')).toContainText('peninsular');
 await year(page,1819);await year(page,1820);await expect(page.locator('#selection')).toHaveAttribute('data-entity','ESP');await expect(page.locator('#tab-conflicts')).toHaveAttribute('aria-selected','true');
 await page.getByRole('tab',{name:'Autoridades',exact:true}).click();await expect(page.locator('#pane-authorities')).toContainText('Fernando');await page.setViewportSize({width:390,height:844});await page.screenshot({path:'test-results/history-1800-mobile.png'});expect(errors).toEqual([]);
});
