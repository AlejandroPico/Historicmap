import {test,expect,type Page} from '@playwright/test';
import{snapshotFor}from'../../src/time';
async function date(page:Page,year:number){await page.goto(`/#year=${year}&view=mercator`);const s=snapshotFor(year);await expect(page.locator('#map')).toHaveAttribute('data-rendered',s.kind==='annual'?`history-${year}`:s.file!,{timeout:90000});await expect(page.locator('#sources-button')).not.toHaveClass(/has-error/);}
test('control geometry remains selectable with optional hatching disabled or enabled, and land has a reference background',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await date(page,1942);await expect(page.locator('#occupations-layer')).toHaveAttribute('aria-pressed','false');
 await expect(page.locator('#map')).toHaveAttribute('data-overlays','0');
 await page.locator('#search-button').click();await page.locator('#search-input').fill('Alemania nazi');await page.locator('#search-results button').first().click();
 await expect(page.locator('#selection')).toHaveAttribute('data-entity','DEU');await expect(page.locator('#pane-authorities')).toContainText('Adolf Hitler');
 await page.locator('#layers-button').click();await page.locator('#occupations-layer').click();await expect(page.locator('#map')).not.toHaveAttribute('data-overlays','0');
 await expect(page.locator('#map-legend')).toContainText('Franja fina');await expect(page.locator('#selection')).toHaveAttribute('data-entity','DEU');await page.locator('#close-layers').click();
 await expect.poll(async()=>Number(await page.locator('#map').getAttribute('data-hatching-rendered')),{timeout:45000}).toBeGreaterThan(0);
 await page.screenshot({path:'test-results/control-hatching-1942.png'});
 await page.locator('#close-selection').click();
 for(const year of [1889,1918]){await date(page,year);await expect(page.locator('#map')).toHaveAttribute('data-reference-land','true');}
 await page.screenshot({path:'test-results/land-reference-1918.png'});
 await date(page,100);await expect(page.locator('#map')).toHaveAttribute('data-reference-land','true');
 expect(errors).toEqual([]);
});
