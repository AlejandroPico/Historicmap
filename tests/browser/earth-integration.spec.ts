import{test,expect,type Page}from'@playwright/test';
async function ready(p:Page,y:number){await expect(p.locator('#map')).toHaveAttribute('data-loaded-year',String(y),{timeout:90000});await expect(p.locator('#play')).toHaveAttribute('aria-busy','false');await expect(p.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:45000});}
async function date(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-input').press('Enter');await ready(p,y);}
async function article(p:Page,id:string,query:string){await p.locator('#encyclopedia-search').fill(query);await p.locator(`#encyclopedia-index [data-encyclopedia-entry="${id}"]`).click();await expect(p.locator('#encyclopedia')).toHaveAttribute('data-article',id);}

test('encyclopedia retains applicable dates, develops the Quaternary and decodes six newly credited fossil photographs',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#year=-2000000&view=mercator');await ready(page,-2000000);await page.locator('#encyclopedia-button').click();
 await article(page,'geo-Quaternary','Cuaternario');await expect(page.locator('#encyclopedia-article [data-encyclopedia-map]').first()).toHaveAttribute('data-encyclopedia-map','-2000000');await expect(page.locator('#encyclopedia-article')).toContainText('800–12ka');await expect(page.locator('#human-co2-age')).toHaveAttribute('max','800');
 for(const [key,name]of[['africanus','Australopithecus africanus'],['rudolfensis','Homo rudolfensis'],['sediba','Australopithecus sediba'],['heidelbergensis','Homo heidelbergensis'],['antecessor','Homo antecessor'],['luzon','Homo luzonensis']]){
  await article(page,'hominin-'+key,name);const photo=page.locator('#encyclopedia-article .human-fossil-photo img');await photo.scrollIntoViewIfNeeded();await expect.poll(()=>photo.evaluate((i:HTMLImageElement)=>i.complete&&i.naturalWidth>0)).toBe(true);expect(await photo.evaluate(i=>getComputedStyle(i).objectFit)).toBe('contain');await expect(page.locator('#encyclopedia-article .human-fossil-photo a').last()).toHaveAttribute('href',/^https:/);
 }
 await page.locator('#encyclopedia-close').click();await date(page,-3200000);await page.locator('#encyclopedia-button').click();await article(page,'hominin-afarensis','Australopithecus afarensis');await page.locator('#encyclopedia-article .encyclopedia-actions [data-encyclopedia-map]').click();await ready(page,-3200000);await expect(page.locator('#encyclopedia')).not.toBeVisible();expect(errors).toEqual([]);
});

test('ruler year text fits through deep-time seams and keeps year1 on the narrow globe',async({page},info)=>{
 test.setTimeout(180000);await page.setViewportSize({width:390,height:844});await page.goto('/#year=-300000&view=globe');await ready(page,-300000);
 for(const y of[-300000,-100000,-7000000,1]){
  if(y!==-300000)await date(page,y);
  const spans=page.locator('.tick.major span:visible');const rects=await spans.evaluateAll(elements=>elements.map(e=>{const r=e.getBoundingClientRect();return{left:r.left,right:r.right}}).sort((a,b)=>a.left-b.left));
  for(let i=1;i<rects.length;i++)expect(rects[i].left-rects[i-1].right).toBeGreaterThanOrEqual(10);
 }
 await expect(page.locator('.tick[data-year="1"] span')).toBeVisible();await expect(page.locator('.tick[data-year="0"]')).toHaveCount(0);await page.locator('#previous').click();await ready(page,-1);await page.locator('#next').click();await ready(page,1);expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
 if(process.env.EARTH_QA_SCREENSHOTS)await page.screenshot({path:info.outputPath('integral-ruler-mobile.png'),animations:'disabled',timeout:45000});
});
