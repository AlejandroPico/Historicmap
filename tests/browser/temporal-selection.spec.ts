import {test,expect,type Page} from '@playwright/test';
async function date(page:Page,year:number){
 await page.locator('#date-button').click();await page.locator('#date-input').fill(String(year));await page.locator('#date-form button[type=submit]').click();
 await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(year),{timeout:45000});
 await expect(page.locator('#map')).toHaveAttribute('data-rendered',year>=2020?'countries.geojson':`history-${year}`,{timeout:45000});
 await expect(page.locator('#sources-button')).not.toHaveClass(/has-error/);
}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}
test('real country clicks recover complete identities after travelling outside the reviewed period and back',async({page})=>{
 test.setTimeout(240000);await page.goto('/#year=1970&view=mercator');await expect(page.locator('#map')).toHaveAttribute('data-loaded-year','1970',{timeout:45000});
 for(const [name,key] of [['Francia','FRA'],['España','ESP']]){
  for(const y of [1970,1954,1970,1980,1954,1980,2026,1970]){
   await date(page,y);await search(page,name);await expect(page.locator('#selection')).toHaveAttribute('data-entity',key);
   await page.locator('#close-selection').click();await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});
   const box=(await page.locator('#map').boundingBox())!;
   await page.locator('#map').click({position:{x:box.width/2,y:box.height/2}});
   await expect(page.locator('#selection')).toHaveAttribute('data-entity',key);
   await expect(page.locator('#selection-title')).not.toHaveText('Área del mapa');
   if(y>=1970)await expect(page.locator('#pane-authorities .leader-name').first()).toBeVisible();
  }
 }
});
