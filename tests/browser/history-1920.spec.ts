import {test,expect,type Page} from '@playwright/test';
test.afterEach(async({page},info)=>{if(info.status!==info.expectedStatus){await page.screenshot({path:'test-results/history-1920-failure.png'});console.log('Failure state:',await page.locator('#map').evaluate(e=>({attributes:[...e.attributes].map(a=>[a.name,a.value]),text:document.body.innerText.slice(-1800)})));}});
async function ready(page:Page,year:number){await expect(page.locator('#map')).toHaveAttribute('data-rendered',`history-${year}`,{timeout:90000});await expect(page.locator('#sources-button')).not.toHaveClass(/has-error/);}
async function search(page:Page,name:string,key:string,text:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();await expect(page.locator('#selection')).toHaveAttribute('data-entity',key);await expect(page.locator('#pane-authorities')).toContainText(text);}
async function year(page:Page,n:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(n));await page.locator('#date-form button[type=submit]').click();await ready(page,n);}
async function pictures(page:Page){const imgs=page.locator('#pane-authorities .leader-portrait');expect(await imgs.count()).toBeGreaterThan(0);for(const img of await imgs.all()){await img.scrollIntoViewIfNeeded();await expect.poll(()=>img.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0),{timeout:15000}).toBe(true);}}

test('1920–1949 historical authorities, flags and persistent country dates',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>{errors.push(e.message);console.log('Page error:',e.stack);});
 await page.goto('/#year=1920&view=mercator');await ready(page,1920);await search(page,'Rusia soviética','RSR','Lenin');
 await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1921);await expect(page.locator('#selection')).toHaveAttribute('data-entity','RSR');await expect(page.locator('#pane-authorities')).toContainText('Lenin');
 await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true');
 const box=(await page.locator('#map').boundingBox())!;await page.locator('#map').click({position:{x:box.width/2,y:box.height/2}});await expect(page.locator('#selection')).toHaveAttribute('data-entity','RSR');
 await year(page,1930);await search(page,'República de China','ROC','Chiang');await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1933);await search(page,'Alemania','DEU','Hitler');await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1938);await search(page,'Ciudad Libre de Danzig','DAN','Greiser');await expect(page.locator('.historic-flag')).toBeVisible();
 await year(page,1942);await search(page,'Alemania nazi','DEU','Hitler');await pictures(page);
 await year(page,1946);await expect(page.locator('#selection')).toHaveAttribute('data-entity','DEU');await expect(page.locator('#pane-authorities')).toContainText('Potencias aliadas');await expect(page.locator('.historic-flag')).toHaveCount(0);
 await year(page,1949);await search(page,'República Federal','DEU','Adenauer');await pictures(page);await expect(page.locator('.historic-flag')).toBeVisible();
 await page.screenshot({path:'test-results/history-1949-authorities.png'});expect(errors).toEqual([]);
});
