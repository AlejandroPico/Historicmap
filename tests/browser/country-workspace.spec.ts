import {test,expect,type Page} from '@playwright/test';
async function ready(page:Page,y:number){await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(y),{timeout:60000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}
async function date(page:Page,y:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(y));await page.locator('#date-form button[type=submit]').click();await ready(page,y);}

test('country card, tab and reading position persist through date changes and playback',async({page})=>{
 test.setTimeout(240000);
 await page.goto('/#year=2026&view=mercator');await ready(page,2026);await search(page,'España');
 await expect(page.getByRole('tab')).toHaveCount(12);
 await page.getByRole('tab',{name:'Economía',exact:true}).click();
 await expect(page.locator('#pane-economy')).toContainText('Inflación');await expect(page.locator('#pane-economy svg')).toBeVisible();
 await page.locator('#selection').evaluate(e=>{e.scrollTop=180;});
 await date(page,2000);await expect(page.locator('#selection')).toBeVisible();await expect(page.locator('#selection')).toHaveAttribute('data-entity','ESP');
 await expect(page.locator('#tab-economy')).toHaveAttribute('aria-selected','true');expect(await page.locator('#selection').evaluate(e=>e.scrollTop)).toBeGreaterThan(50);
 await page.getByRole('tab',{name:'Autoridades',exact:true}).click();await expect(page.locator('#pane-authorities')).toContainText('Aznar');await expect(page.locator('#pane-authorities')).not.toContainText('Pedro Sánchez');
 await date(page,1990);await page.locator('#play').click();await expect.poll(async()=>Number(await page.locator('#map').getAttribute('data-loaded-year')),{timeout:45000}).toBeGreaterThan(1991);await page.locator('#play').click();
 await expect(page.locator('#selection')).toBeVisible();await expect.poll(async()=>await page.locator('#selection').getAttribute('data-year')).toBe(await page.locator('#map').getAttribute('data-loaded-year'));
});

test('extinct entity remains open and navigates explicitly to a successor',async({page})=>{
 await page.goto('/#year=1990&view=mercator');await ready(page,1990);await search(page,'Unión Soviética');
 await page.getByRole('tab',{name:'Historia',exact:true}).click();await expect(page.locator('.country-timeline')).toContainText('Gorbachov');
 await date(page,1992);await expect(page.locator('#selection')).toBeVisible();await expect(page.locator('#selection')).toHaveAttribute('data-entity','USSR');await expect(page.locator('#selection-text')).toContainText('no tiene una representación territorial activa');
 await expect(page.locator('#tab-history')).toHaveAttribute('aria-selected','true');await page.locator('#pane-history [data-entity-key="RUS"]').first().click();
 await expect(page.locator('#selection')).toHaveAttribute('data-entity','RUS');await expect(page.locator('#pane-history')).toBeVisible();
 await page.getByRole('tab',{name:'Autoridades',exact:true}).click();await expect(page.locator('#pane-authorities')).toContainText('Yeltsin');
});

test('date and country comparisons use dated data and support map navigation',async({page})=>{
 test.setTimeout(240000);
 await page.goto('/#year=2000&view=mercator');await ready(page,2000);await search(page,'Brasil');await page.locator('#pin-country').click();
 await expect(page.locator('#comparison-results')).toContainText('Brazil · 2000');
 await search(page,'Francia');await page.locator('#pin-country').click();await expect(page.locator('.pinned-countries>span')).toHaveCount(2);await expect(page.locator('#comparison-results')).toContainText('Francia · 2000');
 await page.locator('#comparison-metric').selectOption('gdpGrowth');await expect(page.locator('#comparison-results .trend-chart')).toContainText('Crecimiento');
 await page.locator('#comparison-results circle[data-jump-year="1990"]').first().focus();await page.keyboard.press('Enter');await ready(page,1990);await expect(page.locator('#tab-comparison')).toHaveAttribute('aria-selected','true');
 await page.locator('[data-comparison-mode="dates"]').click();await page.locator('#comparison-a').fill('1990');await page.locator('#comparison-b').fill('2000');await page.locator('#comparison-dates button').click();
 await expect(page.locator('#comparison-results')).toContainText('Diferencia B − A');await expect(page.locator('#comparison-results')).toContainText('Mitterrand');await expect(page.locator('#comparison-results')).toContainText('Chirac');
 await page.locator('#comparison-results button[data-jump-year="1990"]').first().click();await ready(page,1990);await expect(page.locator('#selection')).toHaveAttribute('data-entity','FRA');await expect(page.locator('#tab-comparison')).toHaveAttribute('aria-selected','true');
 await page.setViewportSize({width:390,height:844});expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);await expect(page.locator('#comparison-dates')).toBeVisible();
});

test('search, sources and layers stay open and update across time navigation',async({page})=>{
 await page.goto('/#year=2000&view=mercator');await ready(page,2000);await page.locator('#search-button').click();await page.locator('#search-input').fill('Brasil');
 await date(page,2001);await expect(page.locator('#search-panel')).toBeVisible();await expect(page.locator('#search-input')).toHaveValue('Brasil');await expect(page.locator('#search-scope')).toContainText('2001');await expect(page.locator('#search-results')).toContainText('Brazil');
 await page.locator('#close-search').click();await page.locator('#sources-button').click();await date(page,2002);await expect(page.locator('#sources-panel')).toBeVisible();await expect(page.locator('#source-reference')).toContainText('2002');
 await page.locator('#close-sources').click();await page.locator('#layers-button').click();await page.locator('#next').click();await ready(page,2003);await expect(page.locator('#layers-panel')).toBeVisible();
});
