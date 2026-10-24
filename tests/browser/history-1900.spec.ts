import {test,expect,type Page} from '@playwright/test';
async function ready(page:Page,y:number){await expect(page.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});await expect(page.locator('#sources-button')).not.toHaveClass(/has-error/);}
async function year(page:Page,y:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(y));await page.locator('#date-form button[type=submit]').click();await ready(page,y);}
async function search(page:Page,name:string,key:string,text:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();await expect(page.locator('#selection')).toHaveAttribute('data-entity',key);await expect(page.locator('#pane-authorities')).toContainText(text);}
async function pictures(page:Page){const imgs=page.locator('#pane-authorities .leader-portrait');expect(await imgs.count()).toBeGreaterThan(0);for(const img of await imgs.all()){await img.scrollIntoViewIfNeeded();await expect.poll(()=>img.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0),{timeout:15000}).toBe(true);}}

test('1900–1919 imperial authorities, protection and republican succession preserve the country workspace',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1900&view=mercator');await ready(page,1900);await search(page,'Imperio ruso','RUE','Nicolás');await pictures(page);await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1905);await expect(page.locator('#selection')).toHaveAttribute('data-entity','RUE');await expect(page.locator('#pane-authorities')).toContainText('Nicolás');
 await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true');
 const box=(await page.locator('#map').boundingBox())!;await page.locator('#map').click({position:{x:box.width/2,y:box.height/2}});await expect(page.locator('#selection')).toHaveAttribute('data-entity','RUE');
 await year(page,1907);await search(page,'Imperio de Corea','KEM','Sunjong');await expect(page.locator('#pane-authorities')).toContainText('Estado administrador');await pictures(page);
 await year(page,1912);await search(page,'República de China','ROC','Sun Yat-sen');await expect(page.locator('#pane-authorities')).toContainText('Puyi');await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1914);await search(page,'Austria-Hungría','AUT-HUN','Francisco José');await pictures(page);
 await year(page,1917);await search(page,'Rusia soviética','RSR','Lenin');await expect(page.locator('#pane-authorities')).toContainText('Kerenski');
 await year(page,1918);await expect(page.locator('#selection')).toHaveAttribute('data-entity','RSR');await expect(page.locator('#pane-authorities')).toContainText('Lenin');await expect(page.locator('#pane-authorities')).not.toContainText('Kerenski');
 await year(page,1919);await page.setViewportSize({width:390,height:844});await search(page,'Alemania','DEU','Ebert');await expect(page.locator('.historic-flag')).toBeVisible();await pictures(page);
 await page.screenshot({path:'test-results/history-1919-mobile.png'});
 await year(page,1920);await expect(page.locator('#selection')).toHaveAttribute('data-entity','DEU');await expect(page.locator('#pane-authorities')).toContainText('Ebert');
 expect(errors).toEqual([]);
});
