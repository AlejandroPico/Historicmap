import { test, expect, type Page } from '@playwright/test';
import { geologicalMa, historicalYears, PRESENT } from '../../src/time';
async function disableRelief(page:Page){await expect(page.locator('#physical-layer')).toHaveAttribute('aria-pressed','false');}
async function date(page:Page,year:number){await page.locator('#date-button').click();await page.locator('#date-input').fill(String(year));await page.locator('#date-form button').click();}
async function present(page:Page){await page.locator('#ruler').focus();await page.keyboard.press('End');}
test('present map, projection, search, historical and geological snapshots',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  page.on('console',message=>{if(message.text().includes('Max vertices per segment'))errors.push(message.text());});
  await page.goto('/');
  await expect(page.locator('#map-status')).toContainText('Natural Earth',{timeout:45000});
  await expect(page.locator('#map')).toHaveAttribute('data-rendered','countries.geojson',{timeout:45000});
  await disableRelief(page);
  await page.getByRole('button',{name:'Ver mapa 2D',exact:true}).click();
  await expect(page).toHaveURL(/view=mercator/);
  await page.getByRole('button',{name:'Buscar un territorio',exact:true}).click();
  await page.getByLabel('Nombre del territorio').fill('España');
  await page.locator('#search-results button').first().click();
  await expect(page.locator('#selection-title')).toHaveText('España');
  await page.locator('#close-selection').click();
  await date(page,100);
  await expect(page.locator('#map-status')).toContainText('100 d. C.');
  await expect(page.locator('#map')).toHaveAttribute('data-rendered','world_100.geojson',{timeout:45000});
  await expect(page.locator('#physical-layer')).toBeEnabled();
  await page.screenshot({path:'test-results/ancient.png'});
  await date(page,-300000000);
  await expect(page.locator('#map-status')).toContainText('CAO2024',{timeout:45000});
  await expect(page.locator('#map')).toHaveAttribute('data-rendered','coastlines-300.geojson',{timeout:45000});
  await page.screenshot({path:'test-results/pangea.png'});
  await date(page,-4540000000);
  await expect(page.locator('#concept')).toBeVisible();
  await expect(page.locator('#concept-caption')).toContainText('CONCEPTUAL');
  await present(page);
  await expect(page.locator('#map-status')).toContainText('Natural Earth',{timeout:45000});
  await expect(page.locator('#map')).toHaveAttribute('data-rendered','countries.geojson',{timeout:45000});
  await page.screenshot({path:'test-results/present.png'});
  await page.getByRole('button',{name:'Ver globo 3D',exact:true}).click();
  await expect(page.locator('#map')).toHaveAttribute('data-rendered','countries.geojson');
  await page.screenshot({path:'test-results/globe.png'});
  await page.locator('#play').click();
  await page.waitForTimeout(8000);
  await page.locator('#play').click();
  await present(page);
  await expect(page).toHaveURL(new RegExp(`year=${PRESENT}&view=globe`));
  await expect(page.locator('#year')).toHaveText(`${PRESENT} d. C.`);
  expect(errors).toEqual([]);
});
test('fixed center cursor, keyboard navigation, exact date, about and narrow layout',async({page})=>{
  await page.goto('/#year=100&view=globe');
  await expect(page.locator('#map-status')).toContainText('100 d. C.',{timeout:45000});
  const cursor=await page.locator('.fixed-cursor').boundingBox();
  await page.locator('#ruler').focus();await page.keyboard.press('ArrowLeft');
  await expect(page.locator('#year')).not.toHaveText('100 d. C.');
  const after=await page.locator('.fixed-cursor').boundingBox();expect(after?.x).toBe(cursor?.x);
  await page.locator('#date-button').click();await page.getByLabel('Año (negativo para a. C.)').fill('117');await page.getByRole('button',{name:'Explorar fecha'}).click();
  await expect(page.locator('#year')).toHaveText('117 d. C.');await expect(page.locator('#map-status')).toContainText('100 d. C.');
  await page.locator('#about-button').click();await expect(page.locator('#modal-body')).toContainText('0.6.0');
  await expect(page.locator('.about-project-icon img')).toBeVisible();
  await expect(page.locator('.about-links a').first()).toHaveAttribute('href','https://alejandropico.github.io/Portfolio/');await page.keyboard.press('Escape');
  await page.setViewportSize({width:390,height:844});await page.screenshot({path:'test-results/mobile.png'});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
  await expect(page.locator('#chapters-button,.story-panel,#time-scale')).toHaveCount(0);
});
test('every shipped cartographic snapshot renders without exceeding GPU segments',async({page})=>{
  test.setTimeout(240000);
  const geometryWarnings:string[]=[];
  page.on('console',message=>{if(message.text().includes('Max vertices per segment'))geometryWarnings.push(message.text());});
  await page.goto('/');
  await expect(page.locator('#map')).toHaveAttribute('data-rendered','countries.geojson',{timeout:45000});
  await disableRelief(page);
  // A global planar view also covers snapshots whose land lies on the far hemisphere.
  await page.locator('#projection-button').click();
  const samples=[...historicalYears.map(y=>({year:y,file:y>=1000?`history-${y}`:`world_${y<0?`bc${-y}`:y}.geojson`})),...geologicalMa.map(ma=>({year:ma===1?-1000001:-ma*1e6,file:`coastlines-${ma}.geojson`}))];
  for(const sample of samples){
    await page.locator('#date-button').click();
    await page.getByLabel('Año (negativo para a. C.)').fill(String(sample.year));
    await page.getByRole('button',{name:'Explorar fecha'}).click();
    await expect(page.locator('#map')).toHaveAttribute('data-rendered',sample.file,{timeout:45000});
  }
  expect(geometryWarnings).toEqual([]);
});
test('compact tools and independent map/timeline wheel zoom',async({page})=>{
  await page.goto('/#year=1800&view=globe');
  await expect(page.locator('#map')).toHaveAttribute('data-rendered','history-1800',{timeout:45000});
  await expect(page.locator('.topbar,.map-controls,.time-toolbar,.time-bottom,#today,#method-button')).toHaveCount(0);
  expect(await page.locator('.toolbar>button').evaluateAll(nodes=>nodes.map(n=>n.id))).toEqual(['search-button','projection-button','filters-button','layers-button','sources-button','fullscreen','appearance-button','about-button']);
  const ruler=page.locator('#ruler');const bounds=(await ruler.boundingBox())!;
  const initialScale=Number(await ruler.getAttribute('data-scale'));const date=await page.locator('#year').textContent();
  const cursor=(await page.locator('.fixed-cursor').boundingBox())!.x;
  await page.mouse.move(120,bounds.y+15);await page.mouse.wheel(0,-240);
  await expect.poll(async()=>Number(await ruler.getAttribute('data-scale'))).toBeGreaterThan(initialScale);
  await expect(page.locator('#year')).toHaveText(date!);
  expect((await page.locator('.fixed-cursor').boundingBox())!.x).toBe(cursor);
  const scale=await ruler.getAttribute('data-scale');
  const mapScale=await page.locator('.maplibregl-ctrl-scale').textContent();
  await page.mouse.move(900,400);await page.mouse.wheel(0,-600);
  await expect.poll(()=>page.locator('.maplibregl-ctrl-scale').textContent()).not.toBe(mapScale);
  await expect(ruler).toHaveAttribute('data-scale',scale!);await expect(page.locator('#year')).toHaveText(date!);
  await page.locator('#layers-button').click();await expect(page.locator('#layers-panel')).toBeVisible();
  await page.locator('#political-layer').click();await expect(page.locator('#political-layer')).toHaveAttribute('aria-pressed','false');
  await page.keyboard.press('Escape');await expect(page.locator('#layers-panel')).toBeHidden();
  await expect(page.locator('#layers-button')).toBeFocused();
  await page.locator('#sources-button').click();await expect(page.locator('#sources-panel')).toBeVisible();await expect(page.locator('#modal')).not.toBeVisible();
  await page.keyboard.press('Escape');await page.locator('#about-button').click();await page.screenshot({path:'test-results/about.png'});
  await page.setViewportSize({width:390,height:844});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
  await expect(page.locator('.about-project-icon')).toBeVisible();await page.keyboard.press('Escape');
  await page.screenshot({path:'test-results/compact-mobile.png'});
});
