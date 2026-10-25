import {test,expect,type Page} from '@playwright/test';
async function ready(page:Page,y:number){await expect(page.locator('#map')).toHaveAttribute('data-rendered',y>=2020?'countries.geojson':`history-${y}`,{timeout:90000});await expect(page.locator('#sources-button')).not.toHaveClass(/has-error/);}
async function year(page:Page,y:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(y));await page.locator('#date-form button[type=submit]').click();await ready(page,y);}
async function search(page:Page,name:string,key:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();await expect(page.locator('#selection')).toHaveAttribute('data-entity',key);}
async function photo(page:Page,name:RegExp){const card=page.locator('.leader-card').filter({has:page.locator('.leader-name').filter({hasText:name})}).first();await expect(card).toBeVisible();const img=card.locator('img');await img.scrollIntoViewIfNeeded();await expect.poll(()=>img.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0),{timeout:15000}).toBe(true);}
test('reported current and historical portraits decode in real country cards',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=2026&view=mercator');await ready(page,2026);
 await search(page,'Irak','IRQ');await photo(page,/Ali Falih/);await photo(page,/Nizar/);
 await search(page,'Mozambique','MOZ');await photo(page,/Daniel Chapo/);await expect(page.locator('.photo-caption')).toContainText('Maria Benvinda Levi (izquierda)');
 await search(page,'Tayikistán','TJK');await photo(page,/Rasulzoda/);
 await year(page,2020);await search(page,'Estados Unidos','USA');await photo(page,/Trump/);await expect(page.locator('#pane-authorities')).not.toContainText('Phil Baker');
 await year(page,2016);await search(page,'Bangladesh','BGD');await photo(page,/Abdul Hamid/);
 await search(page,'Vietnam','VNM');await photo(page,/Trần Đại Quang|Tran Dai Quang/);await photo(page,/Trương Tấn Sang|Truong Tan Sang/);
 await year(page,2011);await search(page,'India','IND');await photo(page,/Manmohan/);await photo(page,/Pratibha/);
 await year(page,2014);await search(page,'Nepal','NPL');await photo(page,/Sushil/);await photo(page,/Ram Baran/);
 await year(page,1970);await search(page,'Bután','BTN');await photo(page,/Jigme Dorji/);
 await year(page,1900);await search(page,'Francia','FRA');await photo(page,/Loubet/);
 await page.screenshot({path:'test-results/reported-france-1900.png'});expect(errors).toEqual([]);
});
test('Greenland is selectable by an actual map click and remains Danish across historical dates',async({page})=>{
 test.setTimeout(150000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=2016&view=mercator');await ready(page,2016);await search(page,'Groenlandia','GRL');
 for(const y of [2016,1970,1942,2016]){
  await year(page,y);await expect(page.locator('#selection')).toHaveAttribute('data-entity','GRL');await expect(page.locator('#pane-authorities')).toContainText('Dinamarca');
  await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});
  const box=(await page.locator('#map').boundingBox())!;await page.locator('#map').click({position:{x:box.width/2,y:box.height/2}});
  await expect(page.locator('#selection')).toHaveAttribute('data-entity','GRL');
 }
 expect(errors).toEqual([]);
});
