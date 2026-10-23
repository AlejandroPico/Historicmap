import {test,expect,type Page} from '@playwright/test';
import {PRESENT} from '../../src/time';
async function date(page:Page,year:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(year));await page.locator('#date-form button').click();await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(year),{timeout:45000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}

test('all annual selections 1789 to system year render; no repeated history downloads',async({page})=>{
 test.setTimeout(480000);
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 page.on('console',m=>{if(m.text().includes('Max vertices per segment'))errors.push(m.text());});
 let historyRequests=0;page.on('request',r=>{if(r.url().endsWith('/data/history.topojson'))historyRequests++;});
 await page.goto('/#year=1789&view=mercator');
 for(let year=1789;year<=PRESENT;year++){
   // Same-document hash navigation exercises the shared-link contract without 381 dialog actions.
   if(year!==1789)await page.goto(`/#year=${year}&view=mercator`);
   await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(year),{timeout:45000});
   await expect(page.locator('#map')).toHaveAttribute('data-rendered',year<=2019?`history-${year}`:'countries.geojson',{timeout:45000});
   await expect(page.locator('#year')).toHaveText(`${year} d. C.`);
 }
 expect(historyRequests).toBe(1);expect(errors).toEqual([]);
});

test('WWII playback progresses annually, pauses precisely and opens historical profiles',async({page})=>{
 await page.goto('/#year=1938&view=mercator');
 await expect(page.locator('#map')).toHaveAttribute('data-rendered','history-1938',{timeout:45000});
 await page.locator('#play').click();
 await expect.poll(()=>page.locator('#map').getAttribute('data-loaded-year'),{timeout:25000}).toBe('1942');
 await page.locator('#play').click();
 const paused=await page.locator('#year').textContent();
 await page.waitForTimeout(1800);await expect(page.locator('#year')).toHaveText(paused!);
 await date(page,1942);
 await expect(page.locator('#map')).toHaveAttribute('data-overlays','0');
 await page.locator('#layers-button').click();await page.locator('#occupations-layer').click();
 await expect(page.locator('#map-legend')).toContainText('síntesis anual');
 await expect(page.locator('#map')).not.toHaveAttribute('data-overlays','0');await page.locator('#close-layers').click();
 await search(page,'Alemania nazi');await expect(page.locator('#selection-text')).toContainText('dictadura nacionalsocialista');
 await expect(page.locator('#pane-facts')).not.toContainText('PIB nominal');await expect(page.locator('#pane-economy .country-facts small')).toHaveCount(0);await expect(page.locator('#pane-economy')).toContainText('Sin dato para esta fecha');
 await page.screenshot({path:'test-results/1942-profile.png'});
 await page.locator('#close-selection').click();await date(page,1946);
 await search(page,'India');await expect(page.locator('#selection-text')).toContainText('Colonia');await expect(page.locator('#selection-text')).toContainText('Reino Unido');
 await page.locator('#close-selection').click();await date(page,1947);await search(page,'India');await expect(page.locator('#selection-text')).toContainText('Estado independiente');
});

test('modern country facts, global cities and economic layers retain observation years',async({page})=>{
 await page.goto('/');await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(PRESENT),{timeout:45000});
 await search(page,'Estados Unidos');await page.getByRole('tab',{name:'Datos',exact:true}).click();
 await expect(page.locator('#selection-text')).toContainText('Población');await expect(page.locator('#selection-text')).toContainText('PIB nominal');
 await expect(page.locator('#selection-text')).toContainText('Washington');await expect(page.locator('#selection-text')).not.toContainText('Geometría de Natural Earth');
 await page.screenshot({path:'test-results/country-profile.png'});await page.locator('#close-selection').click();
 await page.locator('#layers-button').click();await page.locator('#places-layer').click();
 await expect(page.locator('#map')).toHaveAttribute('data-places','323');
 await page.locator('#theme-select').selectOption('gdpPerCapita');
 await expect(page.locator('#map-legend')).toContainText('PIB por habitante',{timeout:45000});await expect(page.locator('#map-legend')).toContainText('Banco Mundial');
 await page.locator('#close-layers').click();await page.screenshot({path:'test-results/economy.png'});
 await date(page,1942);await page.locator('#layers-button').click();await expect(page.locator('#theme-select')).toHaveValue('political');await expect(page.locator('#theme-select')).toBeDisabled();
 await page.locator('#close-layers').click();expect(Number(await page.locator('#map').getAttribute('data-places'))).toBeGreaterThan(120);
 await page.setViewportSize({width:390,height:844});await search(page,'India');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
 const box=await page.locator('#selection').boundingBox();expect(box!.y).toBeGreaterThanOrEqual(0);expect(box!.y+box!.height).toBeLessThan(844);
 await page.screenshot({path:'test-results/historical-mobile.png'});
});

test('slow loading preserves the previous cartography and latest requested date wins',async({page})=>{
 await page.route('**/data/history.topojson',async route=>{await new Promise(r=>setTimeout(r,1800));await route.continue();});
 await page.goto('/');await expect(page.locator('#map')).toHaveAttribute('data-rendered','countries.geojson',{timeout:45000});
 await page.locator('#date-button').click();await page.locator('#date-input').fill('1942');await page.locator('#date-form button').click();
 await expect(page.locator('#map-status')).toContainText('conserva el mapa anterior');
 await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(PRESENT));
 await page.locator('#date-button').click();await page.locator('#date-input').fill('1947');await page.locator('#date-form button').click();
 await expect(page.locator('#map')).toHaveAttribute('data-rendered','history-1947',{timeout:45000});
 await expect(page.locator('#map')).toHaveAttribute('data-loaded-year','1947');
 await expect(page.locator('#map-status')).toContainText('31 dic 1947');
});

test('present endpoint follows the device year without an obsolete epoch panel or invented data',async({page})=>{
 await page.clock.setFixedTime(new Date('2028-06-15T12:00:00Z'));
 await page.goto('/');await expect(page.locator('#year')).toHaveText('2028 d. C.');
 await expect(page.locator('#map-status')).toContainText('referencia contemporánea 2026',{timeout:45000});
 await page.locator('#date-button').click();await expect(page.locator('#date-input')).toHaveAttribute('max','2028');await page.locator('#close-modal').click();
 await expect(page.locator('#chapters-button')).toHaveCount(0);await page.locator('#ruler').focus();await page.keyboard.press('End');await expect(page.locator('#year')).toHaveText('2028 d. C.');
});
