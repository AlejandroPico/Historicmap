import{firstAnnualYear,firstRegionalYear}from'./coverage';
import{culturalDossiersForSource}from'./coverage';
import{describe,it,expect,vi}from'vitest';import{readFileSync,readdirSync,existsSync,writeFileSync}from'node:fs';import{resolve,dirname}from'node:path';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{identityFor}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';import{datedPlaces}from'../src/historical-places';import{regionsAt,hasRegionalCoverage}from'../src/cultural-regions';import{governmentFor}from'../src/governance';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8')),ids=read('identities.json'),regions=read('cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
const dossiers=readdirSync('Países').flatMap(folder=>{const file='Países/'+folder+'/periodos/0400-0499.json';return existsSync(file)?[{file,data:JSON.parse(readFileSync(file,'utf8'))}]:[];});
describe('400–499 political powers and regional communities',()=>{
 it('consults every annual date and inventories gaps without discarding cultures',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let year=400;year<=499;year++){
   expect(snapshotFor(year)).toEqual({kind:'annual',year,file:'early-modern-400.geojson'});expect(playbackYear(year)).toBe(year+1);const p=await world(year),r=regionsAt(regions,year,p);expect(p.features.length).toBeGreaterThan(30);expect(r.features.length).toBeGreaterThan(50);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);
   expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-SAMI')).toBe(true);expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-AMAZON')).toBe(true);
   let authorities=0,symbols=0;for(const f of p.features){const i=identityFor(f.properties!,year,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year,key:i.key,name:f.properties?.name});if(i.flag)symbols++;else missingSymbols.push({year,key:i.key,name:f.properties?.name});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year,politicalComponents:p.features.length,culturalReferences:r.features.length,withAuthorities:authorities,withSymbols:symbols,places:datedPlaces(p,year).features.length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-400-499.json',JSON.stringify({scope:'Disponibilidad anual por el recorrido de producción; no censo mundial exhaustivo ni fronteras observadas anualmente. Cortes puntuales y contornos regionales no equivalen a soberanía uniforme.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueAuthorityRecords:dossiers.reduce((n,d)=>n+d.data.leaders.length,0),catalogueWithoutPortraits:dossiers.flatMap(d=>d.data.leaders.filter((l:any)=>!l.portrait).map((l:any)=>({key:d.data.key,person:l.person,name:l.name,start:l.start,end:l.end})))},null,2)+'\n');
  expect(hasRegionalCoverage(firstRegionalYear-1)).toBe(false);expect(hasRegionalCoverage(400)).toBe(true);expect(snapshotFor(firstAnnualYear-1).kind).toBe('historical');expect(snapshotFor(500).file).toBe('early-modern-500.geojson');
 },90000);

 it('distinguishes the Western court, Nepos in Dalmatia and the Italian powers',async()=>{
  expect(identity('WESTERN-ROMAN-EMPIRE',421).leaders.some(l=>l.person==='Q201905')).toBe(true);expect(identity('WESTERN-ROMAN-EMPIRE',421).leaders.some(l=>l.person==='Q159798')).toBe(true);
  expect(identity('WESTERN-ROMAN-EMPIRE',477).leaders.some(l=>l.person==='Q130601')).toBe(false);expect(identity('WESTERN-ROMAN-EMPIRE',477).leaders.some(l=>l.person==='Q103860'&&l.role.includes('Dalmacia'))).toBe(true);
  expect(datedPlaces(await world(477),477).features.some(f=>f.properties?.identityKey==='WESTERN-ROMAN-EMPIRE'&&f.properties?.referenceKind==='documented-seat-without-polygon')).toBe(true);
  expect(identity('ODOACER-ITALY',480).leaders.some(l=>l.person==='Q103333')).toBe(true);expect(datedPlaces(await world(480),480).features.some(f=>f.properties?.identityKey==='ODOACER-ITALY')).toBe(true);expect(identity('OSTROGOTHIC-KINGDOM',495).leaders.some(l=>l.person==='Q105105')).toBe(true);
 });
 it('resolves Jin, the two unrelated Western Liang dynasties and Helian Xia by period',async()=>{
  expect(identity('EASTERN-JIN',410).leaders.some(l=>l.person==='Q7403')).toBe(true);expect(identity('EASTERN-JIN',425).leaders).toHaveLength(0);
  expect(datedPlaces(await world(422),422).features.some(f=>f.properties?.identityKey==='LIU-SONG')).toBe(true);expect(identity('LIU-SONG',422).leaders.length).toBeGreaterThan(0);expect(datedPlaces(await world(479),479).features.some(f=>f.properties?.identityKey==='SOUTHERN-QI')).toBe(true);
  const x=await world(420);expect(x.features.some(f=>f.properties?.identityKey==='HELIAN-XIA')).toBe(true);expect(x.features.some(f=>f.properties?.identityKey==='WESTERN-XIA')).toBe(false);
  const l=await world(408);expect(l.features.some(f=>f.properties?.identityKey==='EARLY-WESTERN-LIANG')).toBe(true);expect(l.features.some(f=>f.properties?.identityKey==='WESTERN-LIANG')).toBe(false);
 });
 it('keeps restored Persian offices, Hunnic co-rulers and Silla source titles',async()=>{
  expect(identity('SASANIAN',497).leaders.some(l=>l.person==='Q145432')).toBe(true);expect(identity('SASANIAN',499).leaders.some(l=>l.person==='Q244071')).toBe(true);
  expect(identity('HUNNIC-EMPIRE',440).leaders.some(l=>l.person==='Q36724')).toBe(true);expect(identity('HUNNIC-EMPIRE',440).leaders.some(l=>l.person==='Q313490')).toBe(true);expect(governmentFor({identityKey:'HUNNIC-EMPIRE'},440).tags).toContain('empire');
  expect((await world(460)).features.filter(f=>f.properties?.identityKey==='HUNNIC-EMPIRE').every(f=>f.properties?.status==='source-reference')).toBe(true);
  expect(identity('HIST-Q715257',430).leaders.some(l=>l.person==='Q485851')).toBe(true);
 });
 it('uses epigraphic accession evidence and keeps cultural originals without inventing States',async()=>{
  expect(identity('MAYA-COPAN',426).leaders.some(l=>l.person==='Q4164172')).toBe(true);expect(identity('MAYA-PALENQUE',430).leaders).toHaveLength(0);expect(identity('MAYA-PALENQUE',432).leaders.some(l=>l.person==='Q1151454')).toBe(true);
  expect(identity('MAYA-PALENQUE',499).leaders.some(l=>l.person==='Q1835954')).toBe(true);expect(identity('MAYA-PALENQUE',500).leaders.some(l=>l.person==='Q1835954')).toBe(true);
  expect(datedPlaces(await world(432),432).features.some(f=>f.properties?.identityKey==='MAYA-PALENQUE')).toBe(true);
  const docs=culturalDossiersForSource(400);expect(docs).toHaveLength(79);
  const excluded=docs.find(d=>d.originalNames.includes('Mill Creek Culture'));expect(excluded.phases).toHaveLength(0);expect(docs.filter(d=>d.decision==='adopted-reference')).toHaveLength(70);
  for(const f of regions.features.filter((f:any)=>f.properties.sourceYear===400)){if(f.properties.region.includes('mapa'))expect(f.properties.region).not.toMatch(/(?:500|600|700|800)/);}
 });
 it('retains every original political geometry and prevents rejected media fallback',()=>{
  const geo=read('early-modern-400.geojson');let originalCount=0,rejectedCount=0;
  for(const{file,data:d}of dossiers){for(const r of d.geography??[])for(const f of JSON.parse(readFileSync(resolve(dirname(file),r.file),'utf8')).features){expect(geo.features.find((p:any)=>p.id==='clio-'+f.sourceIndex)?.geometry).toEqual(f.geometry);originalCount++;}
   const actual=ids.countries[d.key]?.leaders.filter((l:any)=>l.acquisition===d.acquisition)??[];
   for(const r of d.rejectedPortraits??[]){expect(actual.some((l:any)=>l.person===r.person&&l.portrait?.title===r.title)).toBe(false);rejectedCount++;}
   for(const l of d.leaders)if(l.portrait){expect(l.portrait.caption.length).toBeGreaterThan(20);expect(existsSync(l.portrait.canonicalFile)).toBe(true);}
  }
  expect(originalCount).toBe(305);expect(originalCount).toBe(geo.features.length);expect(rejectedCount).toBeGreaterThan(0);
 });
});
