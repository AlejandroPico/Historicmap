import {test,expect,type Page} from '@playwright/test';
async function ready(page:Page,y:number){await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(y),{timeout:60000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}
async function date(page:Page,y:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(y));await page.locator('#date-form button[type=submit]').click();await ready(page,y);}

test('1970 authorities, dated organisations and Soviet colour-family context stay usable while travelling',async({page})=>{
 test.setTimeout(240000);
 await page.goto('/#year=1970&view=globe');await ready(page,1970);
 await search(page,'Bulgaria');await expect(page.locator('#pane-authorities')).toContainText('Todor Zhivkov');
 await expect(page.locator('#pane-authorities .leader-portrait').first()).toBeVisible();
 await expect.poll(()=>page.locator('#pane-authorities .leader-portrait').first().evaluate((e:HTMLImageElement)=>e.naturalWidth)).toBeGreaterThan(0);
 await page.getByRole('tab',{name:'Territorio',exact:true}).click();await expect(page.locator('#pane-territory')).toContainText('bloque soviético');
 await date(page,1989);await expect(page.locator('#selection')).toHaveAttribute('data-entity','BGR');await expect(page.locator('#tab-territory')).toHaveAttribute('aria-selected','true');await expect(page.locator('#pane-territory')).not.toContainText('Vinculación política y color');
 await date(page,1970);await page.getByRole('tab',{name:'Relaciones',exact:true}).click();await expect(page.locator('#pane-relations')).toContainText('Varsovia');
 await page.locator('#pane-relations [data-map-affiliation="warsaw"]').click();await expect(page.locator('#map-legend')).toContainText('1970');
 await page.locator('#layers-button').click();await expect(page.locator('#affiliation-select')).toBeEnabled();await page.locator('#affiliation-select').selectOption('');await page.locator('#close-layers').click();
 await page.screenshot({path:'test-results/1970-authorities-and-relations.png'});
});

test('Vietnamese state succession keeps the open card without assigning a successor government backwards',async({page})=>{
 test.setTimeout(240000);
 await page.goto('/#year=1974&view=mercator');await ready(page,1974);await search(page,'Vietnam del Sur');
 await expect(page.locator('#selection')).toHaveAttribute('data-entity','RVN');await expect(page.locator('#pane-authorities')).toContainText('Nguyễn Văn Thiệu');
 await expect(page.locator('.historic-flag')).toBeVisible();
 await date(page,1975);await expect(page.locator('#selection')).toHaveAttribute('data-entity','RVN');await expect(page.locator('#pane-authorities')).toContainText('Trần Văn Hương');await expect(page.locator('#pane-authorities')).toContainText('Dương Văn Minh');
 await page.getByRole('tab',{name:'Historia',exact:true}).click();await page.locator('#pane-history [data-entity-key="VSR"]').first().click();
 await expect(page.locator('#selection')).toHaveAttribute('data-entity','VSR');await page.getByRole('tab',{name:'Autoridades',exact:true}).click();await expect(page.locator('#pane-authorities')).toContainText('Huỳnh Tấn Phát');
 await date(page,1977);await expect(page.locator('#selection')).toHaveAttribute('data-entity','VSR');await expect(page.locator('#pane-authorities')).not.toContainText('Huỳnh Tấn Phát');
 await page.getByRole('tab',{name:'Historia',exact:true}).click();await page.locator('#pane-history [data-entity-key="VNM"]').first().click();await ready(page,1976);await expect(page.locator('#selection')).toHaveAttribute('data-entity','VNM');
 await page.setViewportSize({width:390,height:844});expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
 await page.screenshot({path:'test-results/1976-vietnam-succession-mobile.png'});
});
