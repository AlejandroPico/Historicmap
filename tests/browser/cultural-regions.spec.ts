import{test,expect,type Page}from'@playwright/test';
import{readFileSync}from'node:fs';
import{snapshotFor}from'../../src/time';
const beforeCulturalAreas=Math.min(...JSON.parse(readFileSync('public/data/cultural-index.json','utf8')).windows.map((w:{start:number})=>w.start))-1;
test.use({actionTimeout:15000});
async function ready(p:Page,y:number){if(snapshotFor(y).kind!=='annual'){await expect(p.locator('#map')).toHaveAttribute('data-loaded-year',String(y),{timeout:90000});await expect(p.locator('#play')).toHaveAttribute('aria-busy','false');}else await expect(p.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:90000});}
async function year(p:Page,y:number){await p.locator('#date-button').click();await p.locator('#date-input').fill(String(y));await p.locator('#date-input').press('Enter');await ready(p,y);}
async function search(p:Page,name:string,key:string){await p.locator('#search-button').click();await p.locator('#search-input').fill(name);await p.locator('#search-results button').first().click();await expect(p.locator('#selection')).toHaveAttribute('data-entity',key);await expect(p.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});}
test('Amazonian references remain visible and selectable across annual source boundaries',async({page})=>{
 test.setTimeout(210000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/#year=999&view=mercator');await ready(page,999);await search(page,'amazónicas','CULTURE-AMAZON');await expect(page.locator('.regional-card')).toContainText('Casarabe');await expect(page.locator('.leader-name')).toHaveCount(0);await expect(page.locator('.regional-legend')).toBeVisible();await page.screenshot({path:'test-results/cultures-amazon-999.png'});
 for(const y of[1000,1100,1200]){await year(page,y);await expect(page.locator('#selection')).toHaveAttribute('data-entity','CULTURE-AMAZON');await expect(page.locator('.selection-unavailable')).toHaveCount(0);}
 await year(page,699);await expect(page.locator('.selection-unavailable')).toHaveCount(0);await year(page,beforeCulturalAreas);await expect(page.locator('.selection-unavailable')).toContainText('Sin representación activa');await year(page,900);await expect(page.locator('.selection-unavailable')).toHaveCount(0);expect(errors).toEqual([]);
});
test('political priority and alternate selection preserve Cyprus beneath Byzantine control',async({page})=>{
 test.setTimeout(180000);await page.goto('/#year=1000&view=globe');await ready(page,1000);await search(page,'Chipre','REFERENCE-CYPRUS');await page.locator('#map canvas').click({position:{x:640,y:450}});await expect(page.locator('#selection')).toHaveAttribute('data-entity','BYZANTINE');await expect(page.locator('#selection-alternatives')).toBeVisible();await page.locator('[data-overlap-entity]').filter({hasText:'Chipre'}).click();await expect(page.locator('#selection')).toHaveAttribute('data-entity','REFERENCE-CYPRUS');await expect(page.locator('.leader-name')).toHaveCount(0);await page.screenshot({path:'test-results/cultures-cyprus-overlap.png',timeout:45000});await page.locator('[data-overlap-entity]').filter({hasText:'bizantino'}).click();await expect(page.locator('#selection')).toHaveAttribute('data-entity','BYZANTINE');await expect(page.locator('.leader-name').first()).toBeVisible();
});
test('Sámi and Hokkaido cards remain readable on a narrow globe',async({page})=>{
 test.setTimeout(180000);await page.setViewportSize({width:390,height:844});await page.goto('/#year=1100&view=globe');await ready(page,1100);await search(page,'sámi','CULTURE-SAMI');await expect(page.locator('.regional-card')).toContainText('tributo');await page.screenshot({path:'test-results/cultures-sami-mobile.png'});await page.locator('.regional-card .country-content').evaluate(e=>e.scrollTop=e.scrollHeight);await expect(page.locator('.regional-card .profile-source').last()).toBeInViewport();expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);await year(page,1200);await search(page,'Satsumon','CULTURE-HOKKAIDO');await expect(page.locator('.regional-card')).toContainText('Kuriles');
});
// The polygon index does not include the older archaeological point coverage.
// Preserve both a populated prehistoric date and a genuinely empty geological one.
for(const target of [
 {label:'prehistoric evidence',year:beforeCulturalAreas,hasEvidence:true},
 {label:'geological cartography',year:-300000000,hasEvidence:false}
])test(`an obsolete regional download cannot replace newer ${target.label}`,async({page})=>{
 test.setTimeout(180000);
 let release!:()=>void,intercepted=0;
 const gate=new Promise<void>(r=>release=r),map=page.locator('#map');
 await page.route('**/data/cultural-regions-0900-0999.geojson',async route=>{intercepted++;await gate;await route.continue();});
 try{
 await page.goto('/#year=2026&view=mercator');
 await expect(map).toHaveAttribute('data-rendered','countries.geojson',{timeout:90000});
 await page.locator('#date-button').click();await page.locator('#date-input').fill('900');await page.locator('#date-input').press('Enter');
 await expect(page.locator('#play')).toHaveAttribute('aria-busy','true');
 await expect.poll(()=>intercepted).toBe(1);
 await year(page,target.year);
 const references=await map.getAttribute('data-cultural-regions'),humans=await map.getAttribute('data-human-evidence');
 if(target.hasEvidence){
  expect(Number(references)).toBeGreaterThan(0);expect(humans).toBe(references);
  await expect(map).toHaveAttribute('data-territories','0');
 }else await expect(map).toHaveAttribute('data-cultural-regions','0');
 const response=page.waitForResponse('**/data/cultural-regions-0900-0999.geojson');
 release();const completed=await response;expect(completed.ok()).toBe(true);await completed.finished();
 // Allow the completed fetch and its queued browser updates to settle.
 await page.evaluate(()=>new Promise<void>(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve()))));
 await expect(map).toHaveAttribute('data-loaded-year',String(target.year));
 await expect(map).toHaveAttribute('data-cultural-regions',references!);
 await expect(map).toHaveAttribute('data-human-evidence',humans!);
 if(target.hasEvidence){
  await search(page,'Aven des Iboussières','ARCH-PH-0007');
  await expect(page.locator('#pane-authorities')).toContainText('Aziliense');
  await page.locator('#close-selection').click();
 }
 await year(page,900);
 expect(Number(await map.getAttribute('data-cultural-regions'))).toBeGreaterThan(40);
 await expect(page.locator('#play')).toHaveAttribute('aria-busy','false');
 expect(intercepted).toBe(1);
 }finally{release();}
});
