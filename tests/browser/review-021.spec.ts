import{test,expect,type Page}from'@playwright/test';import{openFilters,closeTools}from'./tools';
test.use({actionTimeout:15000});
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-form button[type=submit]').click();await ready(p,y);}
async function search(p:Page,s:string,key:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(s);await p.locator('#search-results button').first().click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);}
async function images(p:Page){for(const l of await p.locator('.leader-portrait,.historic-flag').all())await expect.poll(()=>l.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);}
test('sixteenth century crowns, regencies, dated symbols, filters and century continuity',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/#year=1500&view=mercator');await ready(page,1500);
 await search(page,'Corona de Castilla','CASTILE');await expect(page.locator('#pane-authorities')).toContainText('Isabel I');await images(page);await page.screenshot({path:'test-results/review-021-castile.png'});
 await year(page,1520);await expect(page.locator('#selection')).toHaveAttribute('data-entity','CASTILE');await expect(page.locator('#pane-authorities')).toContainText('Juana I');await expect(page.locator('#pane-authorities')).toContainText('Carlos I');
 await search(page,'Francia','FRA');await expect(page.locator('#pane-authorities')).toContainText('Francisco I');await expect(page.locator('.identity-header')).toContainText('Armas');
 await year(page,1555);await search(page,'Estados Pontificios','PAPAL-STATES');await expect(page.locator('#pane-authorities')).toContainText('Marcelo II');await expect(page.locator('#pane-authorities')).toContainText('Paulo IV');
 await year(page,1561);await openFilters(page);await page.locator('#government-select').selectOption('regency');await year(page,1500);await expect(page.locator('#government-empty')).toBeVisible();await page.locator('#government-empty button').click();await closeTools(page);
 await search(page,'Ming','MING');await year(page,1599);await expect(page.locator('#pane-authorities')).toContainText('Wanli');await year(page,1600);await expect(page.locator('#selection')).toHaveAttribute('data-entity','MING');await expect(page.locator('#pane-authorities')).toContainText('Wanli');expect(errors).toEqual([]);
});
test('American authorities, German seats, conflict markers and Japan on a mobile globe',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/#year=1500&view=globe');await ready(page,1500);
 await search(page,'Triple Alianza','AZTEC');await expect(page.locator('#pane-authorities')).toContainText('Ahuízotl');await year(page,1520);await expect(page.locator('#pane-authorities')).toContainText('Motecuhzoma');
 await search(page,'Hesse','HESSE-UNITED');await expect(page.locator('#pane-authorities')).toContainText('Felipe I');await page.getByRole('tab',{name:'Territorio',exact:true}).click();await expect(page.locator('#pane-territory')).toContainText('agrupa');
 await page.locator('#close-selection').click();await page.locator('#layers-button').click();await expect(page.locator('#occupations-layer')).toBeEnabled();await page.locator('#occupations-layer').click();await expect(page.locator('#map')).not.toHaveAttribute('data-conflict-events','0');await closeTools(page);
 await year(page,1560);await search(page,'Japón','JPN');await expect(page.locator('#pane-authorities')).toContainText('Ashikaga Yoshiteru');await expect(page.locator('.identity-header')).toContainText('Mon de losAshikaga');await images(page);
 await page.setViewportSize({width:390,height:844});await year(page,1590);await expect(page.locator('#selection')).toHaveAttribute('data-entity','JPN');await expect(page.locator('#pane-authorities')).toContainText('Toyotomi');expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);await images(page);await page.screenshot({path:'test-results/review-021-mobile-globe.png'});expect(errors).toEqual([]);
});
