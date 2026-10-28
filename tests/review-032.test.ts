import{describe,it,expect,vi}from'vitest';
import{readFileSync,readdirSync,writeFileSync,existsSync}from'node:fs';
import{resolve,dirname}from'node:path';
import{annualData}from'../src/data';import{politicalData}from'../src/political';
import{identityFor}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';
import{datedPlaces}from'../src/historical-places';
import{regionsAt,hasRegionalCoverage,entitiesAt}from'../src/cultural-regions';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8')),ids=read('identities.json'),regions=read('cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
const dossiers=readdirSync('Países').flatMap(folder=>{const file='Países/'+folder+'/periodos/0800-0899.json';return existsSync(file)?[{file,data:JSON.parse(readFileSync(file,'utf8'))}]:[];});

describe('800–899 annual politics alongside cultures',()=>{
 it('loads all one hundred civil years, retaining cultural selections and disclosing actual authority gaps',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let year=800;year<=899;year++){
   expect(snapshotFor(year)).toEqual({kind:'annual',year,file:'early-modern-800.geojson'});expect(playbackYear(year)).toBe(year+1);
   const p=await world(year),r=regionsAt(regions,year,p);expect(p.features.length).toBeGreaterThan(70);expect(r.features.length).toBeGreaterThan(40);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);
   const contexts=r.features.map(f=>f.properties?.contextKey);expect(contexts).toContain('CULTURE-SAMI');expect(contexts).toContain('CULTURE-AMAZON');expect(hasRegionalCoverage(year)).toBe(true);
   let leaders=0,symbols=0;
   for(const f of p.features){const i=identityFor(f.properties!,year,ids);if(i.leaders.length)leaders++;else missingAuthorities.push({year,key:i.key,name:f.properties?.name});if(i.flag)symbols++;else missingSymbols.push({year,key:i.key,name:f.properties?.name});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year,politicalComponents:p.features.length,culturalReferences:r.features.filter(f=>f.properties?.kind==='cultural-region').length,additionalPolityReferences:r.features.filter(f=>f.properties?.kind==='polity-reference').length,withAuthorities:leaders,withSymbols:symbols,places:datedPlaces(p,year).features.length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-800-899.json',JSON.stringify({scope:'Disponibilidad por el mismo recorrido de datos que usa la aplicación. No es un censo exhaustivo, una verificación independiente de cada frontera o una observación anual de las áreas culturales.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueAuthorityRecords:dossiers.reduce((n,d)=>n+d.data.leaders.length,0),catalogueWithoutPortraits:dossiers.flatMap(d=>d.data.leaders.filter((l:any)=>!l.portrait).map((l:any)=>({key:d.data.key,person:l.person,name:l.name,start:l.start,end:l.end})))},null,2)+'\n');
  expect(snapshotFor(499).kind).toBe('historical');expect(snapshotFor(900).file).toBe('early-modern-900.geojson');expect(hasRegionalCoverage(499)).toBe(false);
 },90000);
 it('keeps Carolingian crowns, the imperial coronation and the Western accession separate',()=>{
  expect(identity('FRANKISH-REALM',800).leaders.some(l=>l.role==='Rey de los francos')).toBe(true);expect(identity('FRANKISH-REALM',800).leaders.some(l=>l.start==='0800-12-25')).toBe(true);
  expect(identity('FRA',830).leaders).toHaveLength(0);expect(identity('EAST-FRANCIA',830).leaders).toHaveLength(0);
  expect(identity('FRA',880).leaders.some(l=>l.name==='Carlos III el Gordo')).toBe(false);expect(identity('FRA',886).leaders.some(l=>l.name==='Carlos III el Gordo')).toBe(true);
  expect(identity('ENGLAND',878).leaders).toHaveLength(0);expect(identity('WESSEX',878).leaders.some(l=>l.name.includes('Alfredo'))).toBe(true);
  expect(identity('HIST-Q203817',895).leaders.find(l=>l.name.includes('Simeón'))?.role).toContain('Knyaz');
 });
 it('discloses the coarse source chronology around Verdun and exposes each crown through dated seats',async()=>{
  const p=await world(843),frank=p.features.find(f=>f.properties?.identityKey==='FRANKISH-REALM');expect(frank?.properties?.name).toContain('referencia anterior al reparto');
  const seats=datedPlaces(p,843).features.filter(f=>f.properties?.sovereignSeat);for(const key of ['FRA','EAST-FRANCIA','MIDDLE-FRANCIA'])expect(seats.some(f=>f.properties?.identityKey===key)).toBe(true);
  expect((await world(850)).features.some(f=>f.properties?.identityKey==='FRA')).toBe(true);
 });
 it('distinguishes Asian rulers and regents and dates the court in Samarra',async()=>{
  expect(identity('TANG',850).leaders.some(l=>l.name.includes('Xuān'))).toBe(true);expect(identity('TANG',850).leaders.some(l=>l.name==='Xuanzong')).toBe(false);
  expect(identity('JPN',860).leaders.some(l=>l.role.includes('Sesshō'))).toBe(true);expect(identity('JPN',888).leaders.some(l=>l.role.includes('Kanpaku'))).toBe(true);expect(identity('JPN',860).leaders.some(l=>l.role.includes('Shogun'))).toBe(false);
  expect(identity('HIST-Q1045322',850).leaders.some(l=>l.name==='Quanfengyou')).toBe(true);expect(identity('HIST-Q203817',820).leaders.some(l=>l.name==='Omurtag')).toBe(true);
  const abb=(y:number)=>world(y).then(p=>datedPlaces(p,y).features.filter(f=>f.properties?.identityKey==='ABBASID').map(f=>f.properties?.name));
  expect(await abb(835)).toContain('Bagdad');expect(await abb(836)).toContain('Samarra');expect(await abb(891)).toContain('Samarra');expect(await abb(892)).toContain('Bagdad');
 });
 it('preserves original source components and prevents rejected candidates from returning as portrait fallbacks',()=>{
  const geometry=read('early-modern-800.geojson');let count=0,rejections=0;
  for(const {file,data:d}of dossiers){for(const ref of d.geography??[]){const original=JSON.parse(readFileSync(resolve(dirname(file),ref.file),'utf8'));for(const f of original.features){expect(geometry.features.find((r:any)=>r.id==='clio-'+f.sourceIndex)?.geometry).toEqual(f.geometry);count++;}}
   const actual=ids.countries[d.key]?.leaders.filter((l:any)=>l.acquisition===d.acquisition)??[];
   for(const rejected of d.rejectedPortraits??[]){expect(actual.some((l:any)=>l.person===rejected.person&&l.portrait?.title===rejected.title)).toBe(false);rejections++;}
   for(const l of d.leaders)if(l.portrait){expect(l.portrait.caption?.length).toBeGreaterThan(20);expect(existsSync(l.portrait.canonicalFile)).toBe(true);}
  }
  expect(count).toBe(geometry.features.length);expect(count).toBeGreaterThan(500);expect(rejections).toBeGreaterThan(40);
 });
 it('shows alternative cultural selections under politics without erasing either record',async()=>{
  const p=await world(850),r=regionsAt(regions,850,p),before=JSON.stringify(p);regionsAt(regions,850,p);expect(JSON.stringify(p)).toBe(before);
  const overlaps=[[18,67],[27.8,66.9],[33,60],[50,60],[85,55],[-89,17],[100,15],[110,1]].map(point=>entitiesAt(point,p,r));expect(overlaps.some(list=>list.length>1)).toBe(true);
  expect(regions.features.filter((f:any)=>f.properties.sourceYear===800&&f.properties.kind==='cultural-region').length).toBeGreaterThan(40);
  expect(identity('TOLTEC-EARLY-REFERENCE',800).leaders).toHaveLength(0);
 });
});
