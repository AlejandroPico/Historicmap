import {test,expect,type Page} from '@playwright/test';
async function year(page:Page,y:number){await page.goto(`/#year=${y}&view=mercator`);await expect(page.locator('#map')).toHaveAttribute('data-loaded-year',String(y),{timeout:45000});if(y>=1789)await expect(page.locator('#map')).toHaveAttribute('data-rendered',y>=2020?'countries.geojson':`history-${y}`,{timeout:45000});}
async function search(page:Page,name:string){await page.locator('#search-button').click();await page.locator('#search-input').fill(name);await page.locator('#search-results button').first().click();}

test('an actual map click in Brazil after a Spanish faction selects Brazil, not Spain',async({page})=>{
 await year(page,1937);await search(page,'zona republicana');await expect(page.locator('.political-identity')).toHaveAttribute('data-identity','ESP-REPUBLIC');
 await year(page,1947);await expect(page.locator('#selection')).toBeVisible();await expect(page.locator('#selection')).toHaveAttribute('data-entity','ESP-REPUBLIC');await expect(page.locator('#selection-text')).toContainText('no tiene una representación territorial activa');await search(page,'Brazil');
 await expect(page.locator('.political-identity')).toHaveAttribute('data-identity','BRA');
 await expect(page.locator('#selection-title')).toHaveText('Brazil');
 await page.locator('#close-selection').click();
 await expect(page.locator('#map')).toHaveAttribute('data-camera-ready','true',{timeout:30000});
 const box=(await page.locator('#map').boundingBox())!;
 // Search centers on Rio; a short distance north is inland, avoiding the coast.
 await page.locator('#map').click({position:{x:box.width/2,y:box.height/2-35}});
 await expect(page.locator('#selection')).toBeVisible();await expect(page.locator('.political-identity')).toHaveAttribute('data-identity','BRA');
 await expect(page.locator('#selection-text')).not.toContainText('zona republicana');
});

test('current country tabs, dual authorities and portraits share the left card',async({page})=>{
 test.setTimeout(240000);await year(page,2026);
 for(const name of ['España','Francia','Alemania','Japón','Brasil','Australia','Reino Unido','India','Mozambique']){
  await search(page,name);await expect(page.getByRole('tab',{name:'Autoridades',exact:true})).toHaveAttribute('aria-selected','true');
  const card=(await page.locator('#selection').boundingBox())!;expect(card.x).toBe(20);
  await expect(page.locator('#pane-authorities .leader-name').first(),name).toBeVisible();
  const portraits=page.locator('#pane-authorities .leader-portrait');expect(await portraits.count(),name).toBeGreaterThan(0);
  await expect.poll(()=>portraits.evaluateAll(images=>images.every(img=>(img as HTMLImageElement).complete&&(img as HTMLImageElement).naturalWidth>0)),{timeout:15000}).toBe(true);
  if(name==='Mozambique'){await expect(page.locator('.full-frame-photo')).toHaveCSS('object-fit','contain');await expect(page.locator('.photo-caption')).toContainText('Fotografía íntegra');}
  if(name==='España'){await expect(page.locator('#pane-authorities')).toContainText('Felipe');await expect(page.locator('#pane-authorities')).toContainText('Sánchez');}
  await page.getByRole('tab',{name:'Datos',exact:true}).click();await expect(page.locator('#pane-authorities')).toBeHidden();await expect(page.locator('#pane-facts')).toBeVisible();
  await expect(page.locator('#pane-facts')).toContainText('Población');
  await page.getByRole('tab',{name:'Contexto',exact:true}).click();await expect(page.locator('#pane-context')).toContainText('2026');
  await page.getByRole('tab',{name:'Conflictos',exact:true}).click();await expect(page.locator('#pane-conflicts')).toBeVisible();
  await page.locator('#close-selection').click();
 }
 await year(page,1970);await search(page,'España');await expect(page.locator('#pane-authorities')).toContainText('Franco');await expect(page.locator('.leader-portrait').first()).toBeVisible();
 await year(page,2000);await search(page,'España');await expect(page.locator('#pane-authorities')).toContainText('Juan Carlos');
});

test('appearance cycles without a menu and automatic mode uses the local clock',async({page})=>{
 await page.clock.setFixedTime(new Date(2026,9,22,8,30));await page.goto('/');
 await expect(page.locator('html')).toHaveAttribute('data-appearance','morning');
 for(const mode of ['morning','afternoon','night','auto']){await page.locator('#appearance-button').click();await expect(page.locator('html')).toHaveAttribute('data-appearance-mode',mode);}
 await page.clock.setFixedTime(new Date(2026,9,22,21,30));await page.reload();await expect(page.locator('html')).toHaveAttribute('data-appearance','night');
 await expect(page.locator('#modal')).toBeHidden();
});

test('compact sources, relief and dated memberships preserve space and temporal scope',async({page})=>{
 await year(page,2026);await expect(page.locator('#chapters-button,.story-panel,#time-scale')).toHaveCount(0);
 await expect(page.locator('.maplibregl-ctrl-attrib')).not.toHaveClass(/maplibregl-compact-show/);
 await page.locator('#sources-button').click();await expect(page.locator('#sources-panel')).toBeVisible();await expect(page.locator('#modal')).toBeHidden();
 await expect(page.locator('#sources-panel')).toContainText('Natural Earth');
 const sources=await page.locator('#sources-panel').evaluate(e=>({height:e.clientHeight,scroll:e.scrollHeight}));expect(sources.scroll).toBeLessThanOrEqual(sources.height);
 await page.keyboard.press('Escape');await page.locator('#layers-button').click();await expect(page.locator('#physical-layer')).toHaveAttribute('aria-pressed','false');
 for(const [value,label] of [['nato','OTAN'],['eu','Unión Europea'],['brics','BRICS'],['threeSeas','Tres Mares']]){await page.locator('#affiliation-select').selectOption(value);await expect(page.locator('#map-legend')).toContainText(label);}
 await page.locator('#theme-select').selectOption('gdp');await expect(page.locator('#map-legend')).toContainText('PIB total');
 await page.locator('#affiliation-select').selectOption('nato');await expect(page.locator('#map-legend')).toContainText('OTAN');
 await page.locator('#theme-select').selectOption('gdp');await expect(page.locator('#map-legend')).toContainText('PIB total');await expect(page.locator('#map-legend')).not.toContainText('OTAN');
 await page.locator('#close-layers').click();const legend=(await page.locator('#map-legend').boundingBox())!;expect(legend.x).toBeGreaterThan(900);expect(legend.y+legend.height).toBeLessThan(784);
 await year(page,1947);await page.locator('#layers-button').click();await expect(page.locator('#affiliation-select')).toBeEnabled();await expect(page.locator('#affiliation-select')).toHaveValue('');await expect(page.locator('#physical-layer')).toBeEnabled();
 await expect(page.locator('#affiliation-help')).toContainText('1900');
 await page.locator('#affiliation-select').selectOption('un');await expect(page.locator('#map-legend')).toContainText('57 miembros');await expect(page.locator('#map-legend')).toContainText('1947');
 await page.locator('#affiliation-select').selectOption('nato');await expect(page.locator('#map-legend')).toContainText('no está activa');
 await page.locator('#physical-layer').click();await expect(page.locator('#physical-layer')).toHaveAttribute('aria-pressed','true');await page.locator('#physical-layer').click();await page.locator('#close-layers').click();
 await year(page,1899);await page.locator('#layers-button').click();await expect(page.locator('#affiliation-select')).toBeDisabled();await expect(page.locator('#affiliation-select')).toHaveValue('');await page.locator('#close-layers').click();
 await year(page,-300000000);await page.locator('#layers-button').click();await expect(page.locator('#physical-layer')).toBeDisabled();
 await page.setViewportSize({width:390,height:844});await expect(page.locator('.maplibregl-ctrl-scale')).toBeVisible();expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
});
