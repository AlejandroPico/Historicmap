import {test,expect,type Page} from '@playwright/test';
async function date(page:Page,y:number){await page.goto(`/#year=${y}&view=mercator`);await expect(page.locator('#map')).toHaveAttribute('data-rendered',`history-${y}`,{timeout:60000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}
test('1960s authorities, historical entities and within-year administration changes retain the open country card',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await date(page,1960);await search(page,'Nigeria');await expect(page.locator('#pane-authorities')).toContainText('Abubakar Tafawa Balewa');await expect(page.locator('#pane-authorities')).toContainText('Isabel II');
 await expect(page.locator('.historic-flag')).toBeVisible();
 await search(page,'República Árabe Unida');await expect(page.locator('#selection')).toHaveAttribute('data-entity','UAR');await expect(page.locator('#pane-authorities')).toContainText('Nasser');
 await date(page,1963);await search(page,'Tanganica');await expect(page.locator('#selection')).toHaveAttribute('data-entity','TAN');await expect(page.locator('#pane-authorities')).toContainText('Julius Nyerere');
 await page.getByRole('tab',{name:'Historia',exact:true}).click();await page.locator('#pane-history [data-entity-key="TZA"]').first().click();
 await expect(page.locator('#map')).toHaveAttribute('data-rendered','history-1964',{timeout:60000});await expect(page.locator('#selection')).toHaveAttribute('data-entity','TZA');
 await date(page,1962);await search(page,'West Irian');await page.getByRole('tab',{name:'Autoridades',exact:true}).click();
 await expect(page.locator('#pane-authorities')).toContainText('José Rolz-Bennett');await expect(page.locator('#pane-authorities')).toContainText('Djalal Abdoh');
 await page.locator('.leader-portrait').first().scrollIntoViewIfNeeded();await expect.poll(()=>page.locator('.leader-portrait').first().evaluate((e:HTMLImageElement)=>e.naturalWidth)).toBeGreaterThan(0);
 await date(page,1963);await expect(page.locator('#pane-authorities')).toContainText('Djalal Abdoh');await expect(page.locator('#pane-authorities')).toContainText(/Sukarno|Soekarno/);
 await page.screenshot({path:'test-results/1963-administration-transfer.png'});expect(errors).toEqual([]);
});
