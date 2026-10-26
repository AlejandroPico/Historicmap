import {readFileSync,writeFileSync} from 'node:fs';
import {afterAll,beforeAll,it,expect,vi} from 'vitest';
import {annualData,overlaysFor} from '../src/data';
import {politicalData} from '../src/political';
import {composeControl} from '../src/control-map';
import {identityFor} from '../src/identities';
import {pacificComponents} from '../src/pacific';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const ids=read('identities.json'),profiles=read('profiles.json');
beforeAll(()=>vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync(new URL('../public/data/'+String(input).split('/').at(-1),import.meta.url)),{status:200})));
afterAll(()=>vi.unstubAllGlobals());
it('resolves every annual1860–1879 inventory and records nominal documentary gaps',async()=>{
 const missing:any[]=[],photos=new Map<string,any>(),symbols:any[]=[],years:any[]=[];
 for(let year=1860;year<=1879;year++){
  const world=politicalData(await annualData(year),year,profiles);
  expect(world.features.length).toBeGreaterThan(90);expect(new Set(world.features.map(f=>f.id)).size).toBe(world.features.length);
  for(const key of ['FRA','USA','ESP','RUE','QING','OTT']){
   const p=world.features.find(f=>f.properties?.identityKey===key)?.properties;expect(p,key+':'+year).toBeDefined();
   expect(identityFor(p!,year,ids).leaders.length,key+':'+year).toBeGreaterThan(0);
  }
  let withAuthorities=0;
  for(const f of world.features){const p=f.properties!,id=identityFor(p,year,ids);
   if(!id.leaders.length&&!id.territoryStatus)missing.push({year,name:p.name,key:id.key,sourceName:p.originalName});else withAuthorities++;
   if(!id.flag)symbols.push({year,name:p.name,key:id.key});
   for(const l of id.leaders)if(!l.portrait)photos.set(l.person,{person:l.person,name:l.name,key:id.key,year});
  }
  years.push({year,territories:world.features.length,withSomeAuthorityOrDocumentedAbsence:withAuthorities});
 }
 if(process.env.ATLAS_WRITE_AUDIT)writeFileSync('docs/REVIEW-1860-1879.json',JSON.stringify({reviewed:'2026-10-26',scope:'Availability through the production route, not a complete historical census or frontier validation.',years,missingAuthorities:missing,missingPortraits:[...photos.values()],missingSymbols:symbols},null,2)+'\n');
});
it('separates island components without changing or duplicating any source coordinates',()=>{
 const raw=read('early-modern.geojson');const before=raw.features.filter((f:any)=>f.properties.start<=1885&&f.properties.end>=1885);
 const after=pacificComponents({type:'FeatureCollection',features:before},1885);
 const polygons=(features:any[])=>features.flatMap(f=>f.geometry.type==='Polygon'?[JSON.stringify(f.geometry.coordinates)]:f.geometry.coordinates.map((p:any)=>JSON.stringify(p))).sort();
 expect(polygons(after.features)).toEqual(polygons(before));
 expect(after.features.find(f=>f.properties?.identityKey==='GUM')?.properties?.administratorKey).toBe('ESP');
});
it('provides dated selectable Pacific omissions without duplicating existing successors',async()=>{
 for(const year of [1885,1886,1916,1942,1970,2016]){const world=politicalData(await annualData(year),year,profiles);
  for(const key of ['GUM','NCL','ASM','COK','NIU','MHL','FSM'])expect(world.features.filter(f=>(f.properties?.identityKey??f.properties?.entityCode)===key).length,key+':'+year).toBe(1);
 }
 const modern=politicalData(await annualData(2016),2016,profiles);
 for(const key of ['PLW','FSM','MHL','WSM','KIR','TUV','NRU','VUT']){
  const p=modern.features.find(f=>f.properties?.identityKey===key)?.properties;
  expect(p?.status,key).toBe('independent');expect(p?.code,key).toBe(key);
 }
});
it('integrates dated Ukraine control and excludes the old incompatible Crimea mask',async()=>{
 for(const year of [2022,2023,2024,2025,2026]){
  const controls=await overlaysFor(year);expect(controls.features.some(f=>f.properties?.uid==='crimea')).toBe(false);
  const front=controls.features.find(f=>String(f.properties?.uid).startsWith('ukraine-russian-control'))!;expect(front.properties?.registrationUncertaintyMetres).toBe(7000);
  if(year===2026)expect(front.properties?.observationDate).toBe('2025-12-17');
 }
 const base=politicalData(read('countries.geojson'),2026,profiles),result=composeControl(base,await overlaysFor(2026),2026);
 expect(result.territories.features.filter(f=>f.properties?.identityKey==='RUS')).toHaveLength(1);
 expect(result.territories.features.find(f=>f.properties?.identityKey==='RUS')?.properties?.controlObservationDate).toBe('2025-12-17');
 expect(result.occupations.features.some(f=>f.properties?.occupiedKey==='UKR')).toBe(true);
},60000);
