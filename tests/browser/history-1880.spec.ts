import {test,expect,type Page} from '@playwright/test';
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});await expect(p.locator('#sources-button')).not.toHaveClass(/has-error/);}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string,key:string,text:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);const result=key==='USA'?p.locator('#search-results').getByRole('button',{name:'Estados Unidos',exact:true}):p.locator('#search-results button').first();await result.click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);await expect(p.locator('#pane-authorities')).toContainText(text);}
test('1880–1899 source transition, regimes and annual workspace retain dated authorities and symbols',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1880&view=mercator');await ready(page,1880);await search(page,'Imperio del Brasil','BRA-EMPIRE','Pedro II');await expect(page.locator('.historic-flag')).toBeVisible();
 for(const y of [1885,1886,1888]){await year(page,y);await expect(page.locator('#selection')).toHaveAttribute('data-entity','BRA-EMPIRE');await expect(page.locator('#pane-authorities')).toContainText('Pedro II');}
 await year(page,1889);await search(page,'República de los Estados Unidos del Brasil','BRA','Deodoro');await expect(page.locator('#pane-authorities')).toContainText('Pedro II');await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1893);await search(page,'Hawái','HAW-PROVISIONAL','Dole');await expect(page.locator('#pane-authorities')).toContainText('Lili');
 await year(page,1897);await search(page,'Imperio de Corea','KEM','Gojong');
 await year(page,1898);await search(page,'Estados Unidos','USA','McKinley');await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1899);await page.setViewportSize({width:390,height:844});await search(page,'Francia','FRA','Loubet');
 const flag=page.locator('.historic-flag');await expect.poll(()=>flag.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);
 const img=page.locator('.leader-card').filter({hasText:'Loubet'}).first().locator('img');await img.scrollIntoViewIfNeeded();await expect.poll(()=>img.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);
 await page.screenshot({path:'test-results/history-1899-mobile.png'});expect(errors).toEqual([]);
});
