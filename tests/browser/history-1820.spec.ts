import {test,expect,type Page} from '@playwright/test';
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string,key:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);const r=p.locator('#search-results button').first();await expect(r).toBeVisible();await r.click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);}
test('1820–1839 regimes, regencies, first Mexican empire and persistent conflict context',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1820&view=globe');await ready(page,1820);await search(page,'Francia','FRA');await expect(page.locator('#pane-authorities')).toContainText('Luis XVIII');
 await year(page,1830);await expect(page.locator('#selection')).toHaveAttribute('data-entity','FRA');await expect(page.locator('#pane-authorities')).toContainText('Luis Felipe');
 await year(page,1833);await search(page,'España','ESP');await expect(page.locator('#pane-authorities')).toContainText('María Cristina');await expect(page.locator('#pane-authorities')).toContainText('Isabel II');
 await year(page,1822);await search(page,'Primer Imperio mexicano','HIST-Q285658');await expect(page.locator('#pane-authorities')).toContainText('Iturbide');const image=page.locator('.leader-portrait').first();await expect.poll(()=>image.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);
 await year(page,1839);await search(page,'Qing','QING');await page.getByRole('tab',{name:'Conflictos',exact:true}).click();await expect(page.locator('#pane-conflicts')).toContainText('Opio');
 await year(page,1840);await expect(page.locator('#selection')).toHaveAttribute('data-entity','QING');await expect(page.locator('#tab-conflicts')).toHaveAttribute('aria-selected','true');await expect(page.locator('#pane-conflicts')).toContainText('Opio');
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'test-results/history-1820-mobile.png'});expect(errors).toEqual([]);
});
