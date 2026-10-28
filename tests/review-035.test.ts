import{describe,it,expect,vi}from'vitest';import{readFileSync,readdirSync,existsSync,writeFileSync}from'node:fs';import{resolve,dirname}from'node:path';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{identityFor}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';import{datedPlaces}from'../src/historical-places';import{regionsAt,hasRegionalCoverage}from'../src/cultural-regions';import{governmentFor}from'../src/governance';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8')),ids=read('identities.json'),regions=read('cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
const dossiers=readdirSync('Países').flatMap(folder=>{const file='Países/'+folder+'/periodos/0500-0599.json';return existsSync(file)?[{file,data:JSON.parse(readFileSync(file,'utf8'))}]:[];});
describe('500–599 political powers and regional communities',()=>{
 it('consults every annual date and inventories gaps without discarding cultures',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let year=500;year<=599;year++){
   expect(snapshotFor(year)).toEqual({kind:'annual',year,file:'early-modern-500.geojson'});expect(playbackYear(year)).toBe(year+1);const p=await world(year),r=regionsAt(regions,year,p);expect(p.features.length).toBeGreaterThan(30);expect(r.features.length).toBeGreaterThan(50);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);
   expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-SAMI')).toBe(true);expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-AMAZON')).toBe(true);
   let authorities=0,symbols=0;for(const f of p.features){const i=identityFor(f.properties!,year,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year,key:i.key,name:f.properties?.name});if(i.flag)symbols++;else missingSymbols.push({year,key:i.key,name:f.properties?.name});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year,politicalComponents:p.features.length,culturalReferences:r.features.length,withAuthorities:authorities,withSymbols:symbols,places:datedPlaces(p,year).features.length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-500-599.json',JSON.stringify({scope:'Disponibilidad anual por el recorrido de producción; no censo mundial exhaustivo ni fronteras observadas anualmente. Cortes puntuales y contornos regionales no equivalen a soberanía uniforme.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueAuthorityRecords:dossiers.reduce((n,d)=>n+d.data.leaders.length,0),catalogueWithoutPortraits:dossiers.flatMap(d=>d.data.leaders.filter((l:any)=>!l.portrait).map((l:any)=>({key:d.data.key,person:l.person,name:l.name,start:l.start,end:l.end})))},null,2)+'\n');
  expect(hasRegionalCoverage(499)).toBe(false);expect(hasRegionalCoverage(500)).toBe(true);expect(snapshotFor(499).kind).toBe('historical');expect(snapshotFor(600).file).toBe('early-modern-600.geojson');
 },90000);
 it('separates imperial accession from Caesar designation, regency and restored reigns',()=>{
  expect(identity('BYZANTINE',526).leaders.some(l=>l.person==='Q41866')).toBe(false);expect(identity('BYZANTINE',528).leaders.some(l=>l.person==='Q41866')).toBe(true);expect(identity('BYZANTINE',590).leaders.some(l=>l.person==='Q181764')).toBe(true);
  expect(identity('BYZANTINE',575).leaders.find(l=>l.person==='Q31491')?.role).toContain('regente');expect(identity('BYZANTINE',580).leaders.find(l=>l.person==='Q31491')?.role).toContain('Emperador');
  expect(identity('SASANIAN',500).leaders.some(l=>l.person==='Q244071')).toBe(true);expect(identity('SASANIAN',590).leaders.some(l=>l.person==='Q311283')).toBe(true);expect(identity('SASANIAN',592).leaders.some(l=>l.person==='Q212732')).toBe(true);
  expect(identity('OSTROGOTHIC-KINGDOM',534).leaders.filter(l=>l.person==='Q371670').some(l=>l.role.includes('Reina'))).toBe(true);
  expect(identity('WESTERN-TURKIC',560).leaders.find(l=>l.name==='Istämi')?.role).toContain('Yabghu');
 });
 it('keeps early Chinese courts selectable when source outlines begin after proclamations',async()=>{
  for(const[key,y]of[['LIANG',505],['NORTHERN-QI',551],['NORTHERN-ZHOU',558],['CHEN',558],['SUI',583]]as const){expect(identity(key,y).leaders.length).toBeGreaterThan(0);expect(datedPlaces(await world(y),y).features.some(f=>f.properties?.identityKey===key&&f.properties?.sovereignSeat)).toBe(true);}
  expect(identity('SUI',580).leaders).toHaveLength(0);expect(identity('SUI',590).leaders.length).toBeGreaterThan(0);expect(governmentFor({identityKey:'SUI'},590).tags).toContain('empire');
  expect((await world(580)).features.filter(f=>f.properties?.identityKey==='NORTHERN-QI').every(f=>f.properties?.status==='source-reference')).toBe(true);
 });
 it('exposes independent Maya courts and corrects copied reigns with epigraphic evidence',async()=>{
  expect(identity('MAYA-COPAN',505).leaders.some(l=>l.person==='Q17155810')).toBe(false);expect(identity('MAYA-COPAN',525).leaders.some(l=>l.person==='Q17155810')).toBe(true);expect(identity('MAYA-COPAN',540).leaders.some(l=>l.person==='LOCAL-COPAN-8')).toBe(true);
  expect(identity('MAYA-TIKAL',515).leaders.some(l=>l.person==='Q6470694')).toBe(true);expect(identity('MAYA-TIKAL',515).leaders.some(l=>l.person==='Q4210292')).toBe(true);
  for(const key of ['MAYA-PALENQUE','MAYA-TIKAL','MAYA-COPAN']){expect(datedPlaces(await world(590),590).features.some(f=>f.properties?.identityKey===key)).toBe(true);expect(datedPlaces(await world(601),601).features.some(f=>f.properties?.identityKey===key)).toBe(true);}
  expect(identity('MAYA-PALENQUE',590).leaders.some(l=>l.name.includes('Yohl'))).toBe(true);expect(identity('MAYA-PALENQUE',601).leaders.some(l=>l.name.includes('Yohl'))).toBe(true);
  expect(identity('HIST-Q11774',545).leaders.some(l=>l.person==='Q7908815')).toBe(false);expect(identity('SAMATATA-VAINYA',507).leaders.some(l=>l.person==='Q7908815')).toBe(true);expect(identity('SAMATATA-VAINYA',520).leaders).toHaveLength(0);
 });
 it('quarantines source anachronisms while retaining their original evidence',()=>{
  const docs=readdirSync('Países').flatMap(folder=>{const p='Países/'+folder+'/poblamiento';return existsSync(p)?readdirSync(p).filter(n=>n.endsWith('-Y0500.json')).map(n=>JSON.parse(readFileSync(p+'/'+n,'utf8'))):[];});
  for(const name of ['Poverty Point','Mill Creek']){const d=docs.find(d=>JSON.stringify(d).includes(name));expect(d).toBeDefined();expect(d.phases).toHaveLength(0);}
  expect(regions.features.some((f:any)=>f.properties.sourceYear===500&&f.properties.originalNames.includes('Western Roman Empire')&&f.properties.contextKey==='REFERENCE-POST-WESTERN-ROME')).toBe(true);
  for(const f of regions.features.filter((f:any)=>f.properties.sourceYear===500)){const p=f.properties;if(p.region.includes('mapa'))expect(p.region).not.toMatch(/(?:600|700|800)/);}
 });
 it('retains every original political geometry and prevents rejected media fallback',()=>{
  const geo=read('early-modern-500.geojson');let originalCount=0,rejectedCount=0;
  for(const{file,data:d}of dossiers){for(const r of d.geography??[])for(const f of JSON.parse(readFileSync(resolve(dirname(file),r.file),'utf8')).features){expect(geo.features.find((p:any)=>p.id==='clio-'+f.sourceIndex)?.geometry).toEqual(f.geometry);originalCount++;}
   const actual=ids.countries[d.key]?.leaders.filter((l:any)=>l.acquisition===d.acquisition)??[];
   for(const r of d.rejectedPortraits??[]){expect(actual.some((l:any)=>l.person===r.person&&l.portrait?.title===r.title)).toBe(false);rejectedCount++;}
   for(const l of d.leaders)if(l.portrait){expect(l.portrait.caption.length).toBeGreaterThan(20);expect(existsSync(l.portrait.canonicalFile)).toBe(true);}
  }
  expect(originalCount).toBe(270);expect(originalCount).toBe(geo.features.length);expect(rejectedCount).toBeGreaterThan(0);
 });
});
