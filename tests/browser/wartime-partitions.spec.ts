import {test,expect,type Page} from '@playwright/test';
async function ready(page:Page,y:number){await expect(page.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});}
async function year(page:Page,y:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(y));await page.locator('#date-form button[type=submit]').click();await ready(page,y);}
async function search(page:Page,name:string,key:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click({timeout:10000});await expect(page.locator('#selection')).toHaveAttribute('data-entity',key);}

test('prepared1940–1944 replacements load through the production path and retain neutral country clicks with hatching',async({page})=>{
 test.setTimeout(210000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error'||/too many vertices|exceed.*segment/i.test(m.text()))errors.push(m.text());});
 const requests:string[]=[];page.on('request',r=>{if(r.url().includes('wartime-partitions'))requests.push(r.url());});
 await page.goto('/#year=1940&view=mercator');await ready(page,1940);
 await search(page,'Alemania nazi','DEU');await expect(page.locator('#pane-authorities')).toContainText('Adolf Hitler');
 await search(page,'Sweden','SWE');
 for(const y of [1941,1942,1943,1944]){
  await year(page,y);await expect(page.locator('#selection')).toHaveAttribute('data-entity','SWE');
  await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});
  const b=(await page.locator('#map').boundingBox())!;await page.locator('#map').click({position:{x:b.width/2,y:b.height/2}});await expect(page.locator('#selection')).toHaveAttribute('data-entity','SWE');
 }
 await year(page,1942);await search(page,'Eslovaquia','SVK-1939');await expect(page.locator('#pane-authorities')).toContainText('Jozef Tiso');
 await page.locator('#layers-button').click();await page.locator('#occupations-layer').click();await page.locator('#close-layers').click();
 await expect.poll(async()=>Number(await page.locator('#map').getAttribute('data-hatching-rendered')),{timeout:45000}).toBeGreaterThan(0);
 await expect(page.locator('#selection')).toHaveAttribute('data-entity','SVK-1939');await page.screenshot({path:'test-results/wartime-partition-1942.png'});
 await search(page,'Alemania nazi','DEU');await expect(page.locator('#pane-authorities')).toContainText('Hitler');
 await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});await page.screenshot({path:'test-results/wartime-europe-1942.png'});
 await year(page,1939);await year(page,1943);await search(page,'Sweden','SWE');
 await search(page,'Eslovaquia','SVK-1939');await year(page,1944);await expect(page.locator('#selection')).toHaveAttribute('data-entity','SVK-1939');await expect(page.locator('#pane-authorities')).toContainText('Štefan Tiso');await expect(page.locator('#pane-authorities')).toContainText('Vojtech Tuka');
 expect(requests).toHaveLength(1);expect(errors).toEqual([]);
});

test('Italy1912 keeps a compact authority layout and Swiss original GIF portraits load across dates',async({page})=>{
 test.setTimeout(150000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=1912&view=mercator');await ready(page,1912);await search(page,'Italia','ITA');
 await expect(page.locator('#pane-authorities')).toContainText('Víctor Manuel');
 await expect(page.locator('#pane-authorities')).not.toContainText('Juramento');await expect(page.locator('#pane-authorities .leader-details>p')).toHaveCount(0);
 await page.getByRole('tab',{name:'Contexto',exact:true}).click();await page.locator('#pane-context .authority-notes summary').click();await expect(page.locator('#pane-context .authority-document')).not.toHaveCount(0);
 await page.screenshot({path:'test-results/italy-1912-context-notes.png'});
 await year(page,1913);await search(page,'Switzerland','CHE');await page.getByRole('tab',{name:'Autoridades',exact:true}).click();
 for(const y of [1913,1919,1950]){
  if(y!==1913)await year(page,y);
  await expect(page.locator('#selection')).toHaveAttribute('data-entity','CHE');
  const portraits=page.locator('#pane-authorities .leader-portrait');expect(await portraits.count()).toBeGreaterThan(2);
  for(const image of await portraits.all()){await image.scrollIntoViewIfNeeded();await expect.poll(()=>image.evaluate(n=>(n as HTMLImageElement).complete&&(n as HTMLImageElement).naturalWidth>0)).toBe(true);}
  await expect(page.locator('#pane-authorities img[src$=".gif"]').first()).toBeAttached();
 }
 await year(page,1919);await page.locator('.country-content').evaluate(n=>n.scrollTop=0);
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'test-results/swiss-1919-portraits-mobile.png'});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);expect(errors).toEqual([]);
});
