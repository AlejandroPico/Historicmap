import {test,expect,type Page} from '@playwright/test';
async function date(page:Page,year:number){
 await page.locator('#date-button').click();await page.locator('#date-input').fill(String(year));await page.locator('#date-form button[type=submit]').click();
 await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(year),{timeout:45000});
 await expect(page.locator('#map')).toHaveAttribute('data-rendered',`history-${year}`,{timeout:45000});
 await expect(page.locator('#sources-button')).not.toHaveClass(/has-error/);
}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}
test('colonial and autonomous territory cards retain dated local and external authorities through independence and return',async({page})=>{
 test.setTimeout(240000);page.on('console',m=>{if(m.type()==='error')console.log('BROWSER ERROR:',m.text());});await page.goto('/#year=1970&view=mercator');await expect(page.locator('#map')).toHaveAttribute('data-loaded-year','1970',{timeout:45000});
 for(const [name,leader] of [['Angola','Américo Tomás'],['Mozambique','Marcelo Caetano'],['Guinea-Bissau','Américo Tomás'],['Namibia','Fouché'],['Sáhara Español','Francisco Franco'],['Surinam','Jules Sedney'],['French Guyana','Georges Pompidou'],['Puerto Rico','Richard Nixon'],['Guadeloupe','Georges Pompidou'],['Martinique','Georges Pompidou'],['Bahamas','Lynden Pindling']]){
  await search(page,name);await expect(page.locator('#pane-authorities')).toContainText(leader);await expect(page.locator('#pane-authorities')).toContainText('Autoridades del Estado administrador');
 }
 await search(page,'Angola');await page.getByRole('tab',{name:'Territorio',exact:true}).click();await date(page,1976);await expect(page.locator('#selection')).toHaveAttribute('data-entity','AGO');await expect(page.locator('#tab-territory')).toHaveAttribute('aria-selected','true');
 await page.getByRole('tab',{name:'Autoridades',exact:true}).click();await expect(page.locator('#pane-authorities')).toContainText('Agostinho Neto');await expect(page.locator('#pane-authorities')).not.toContainText('Marcelo Caetano');
 await date(page,1970);await expect(page.locator('#pane-authorities')).toContainText('Américo Tomás');await expect(page.locator('#pane-authorities')).not.toContainText('Agostinho Neto');
 await date(page,1954);await date(page,1970);await expect(page.locator('#pane-authorities')).toContainText('Américo Tomás');
 await page.screenshot({path:'test-results/dependent-angola-1970.png'});
});
