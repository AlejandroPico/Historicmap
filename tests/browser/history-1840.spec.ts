import {test,expect,type Page} from '@playwright/test';
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string,key:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);const result=p.locator('#search-results button').first();await expect(result,s).toBeVisible({timeout:10000});await result.click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);}
async function portrait(p:Page,name:string){const image=p.locator('.leader-card').filter({has:p.locator('.leader-name',{hasText:name})}).first().locator('img');await image.scrollIntoViewIfNeeded();await expect.poll(()=>image.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);return image;}
test('1840–1859 French regimes, constitutional offices and persistent conflict context',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1840&view=mercator');await ready(page,1840);await search(page,'Francia','FRA');await expect(page.locator('#pane-authorities')).toContainText('Luis Felipe');
 await year(page,1848);await expect(page.locator('#selection')).toHaveAttribute('data-entity','FRA');const cavaignac=page.locator('.leader-card').filter({has:page.locator('.leader-name',{hasText:'Cavaignac'})});await expect(cavaignac).toContainText('Poder Ejecutivo');await expect(cavaignac).not.toContainText('Presidente de la República');
 await year(page,1853);await expect(page.locator('#pane-authorities')).toContainText('Emperador de los franceses');await portrait(page,'Napoleón');await year(page,1854);await page.getByRole('tab',{name:'Conflictos',exact:true}).click();await expect(page.locator('#pane-conflicts')).toContainText('Crimea');
 await year(page,1855);await expect(page.locator('#tab-conflicts')).toHaveAttribute('aria-selected','true');await expect(page.locator('#pane-conflicts')).toContainText('Crimea');
 await page.getByRole('tab',{name:'Autoridades',exact:true}).click();await search(page,'Joseon','JOS');await expect(page.locator('#pane-authorities')).toContainText('Cheoljong');await expect(page.locator('#pane-authorities')).not.toContainText('Gojoseon');
 expect(errors).toEqual([]);
});
test('1840 portraits and regencies, early Hawaiian succession and Gregorian Russian handover',async({page})=>{
 test.setTimeout(180000);await page.goto('/#year=1840&view=globe');await ready(page,1840);await search(page,'Reino Unido','GBR');const first=await (await portrait(page,'Victoria')).getAttribute('src');await expect(page.locator('#pane-authorities')).toContainText('Retrato pintado en1838');
 await year(page,1855);const later=await (await portrait(page,'Victoria')).getAttribute('src');expect(later).not.toBe(first);await expect(page.locator('#pane-authorities')).toContainText('1854');
 await year(page,1840);await search(page,'España','ESP');await expect(page.locator('#pane-authorities')).toContainText('María Cristina');await year(page,1842);await expect(page.locator('#pane-authorities')).toContainText('Espartero');
 await year(page,1854);await search(page,'Hawái','HAW-KINGDOM');await expect(page.locator('#pane-authorities')).toContainText('Kamehameha III');await expect(page.locator('#pane-authorities')).toContainText('Kamehameha IV');
 await year(page,1855);await search(page,'Imperio ruso','RUE');await expect(page.locator('#pane-authorities')).toContainText('2/3/1855');await expect(page.locator('#pane-authorities')).not.toContainText('18/2/1855');
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'test-results/history-1840-mobile.png'});
});
