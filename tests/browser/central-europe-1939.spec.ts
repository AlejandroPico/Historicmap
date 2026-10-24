import {test,expect,type Page} from '@playwright/test';
async function ready(page:Page,year:number){await expect(page.locator('#map')).toHaveAttribute('data-rendered',`history-${year}`,{timeout:90000});}
async function year(page:Page,n:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(n));await page.locator('#date-form button[type=submit]').click();await ready(page,n);}
async function search(page:Page,name:string,key:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();await expect(page.locator('#selection')).toHaveAttribute('data-entity',key);}
test('1939 Slovak client and unified German territory remain selectable with optional hatching and date navigation',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1939&view=mercator');await ready(page,1939);
 await search(page,'Eslovaquia','SVK-1939');await expect(page.locator('#pane-authorities')).toContainText('Jozef Tiso');await expect(page.locator('#pane-authorities')).toContainText('Vojtech Tuka');await expect(page.locator('.historic-flag')).toBeVisible();
 await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});
 const box=(await page.locator('#map').boundingBox())!;await page.locator('#map').click({position:{x:box.width/2,y:box.height/2}});await expect(page.locator('#selection')).toHaveAttribute('data-entity','SVK-1939');
 await page.locator('#layers-button').click();await page.locator('#occupations-layer').click();await page.locator('#close-layers').click();await expect(page.locator('#selection')).toHaveAttribute('data-entity','SVK-1939');
 await page.screenshot({path:'test-results/central-europe-1939.png'});
 await search(page,'Alemania nazi','DEU');await expect(page.locator('#pane-authorities')).toContainText('Hitler');
 await year(page,1940);await expect(page.locator('#selection')).toHaveAttribute('data-entity','DEU');await year(page,1939);await expect(page.locator('#selection')).toHaveAttribute('data-entity','DEU');
 await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});await page.screenshot({path:'test-results/central-europe-1939-map.png'});
 await search(page,'Eslovaquia','SVK-1939');expect(errors).toEqual([]);
});
