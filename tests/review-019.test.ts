import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{datedPlaces}from'../src/historical-places';import{identityFor,type IdentityData}from'../src/identities';import{anchorFor,matchingFeature}from'../src/selection';import{snapshotFor,playbackYear}from'../src/time';import{withGovernance,governmentCounts}from'../src/governance';
const read=(p:string)=>JSON.parse(readFileSync('public/data/'+p,'utf8'));const ids:IdentityData=read('identities.json');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>withGovernance(politicalData(await annualData(y),y),y);
describe('1700 review and documentary source limits',()=>{
 it('loads every new annual year without backdating later snapshots and inventories actual availability',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1700;y<=1799;y++){
   expect(snapshotFor(y)).toMatchObject({kind:'annual',year:y,file:y<1789?'early-modern-1700.geojson':'early-modern.geojson'});expect(playbackYear(y)).toBe(y+1);
   const data=await world(y);expect(data.features.length).toBeGreaterThan(70);expect(new Set(data.features.map(f=>f.id)).size).toBe(data.features.length);
   let authorities=0,symbols=0;
   for(const f of data.features){const p=f.properties!,id=identityFor(p,y,ids);if(id.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:id.key,administrator:p.administratorKey});if(id.flag)symbols++;else missingSymbols.push({year:y,key:id.key,name:p.name});for(const l of id.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:id.key});}
   const seats=datedPlaces(data,y).features.filter(f=>f.properties?.sovereignSeat);years.push({year:y,territories:data.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:seats.length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1700-1799.json',JSON.stringify({scope:'Production-path availability audit, not a complete historical census. Polygon inventories and grouped-state seat references counted separately.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(1199).kind).toBe('historical');
 },90000);
 it('keeps German state references distinct from the imperial contour and resolves their own dated card',async()=>{
  const data=await world(1750),seats=withGovernance(datedPlaces(data,1750),1750);
  const hesse=seats.features.find(f=>f.properties?.identityKey==='HESSE-DARMSTADT')!;expect(hesse).toBeDefined();expect(hesse.geometry.type).toBe('Point');expect(hesse.properties?.note).toContain('agrupa');
  const anchor=anchorFor(hesse.properties!,1750,ids);expect(anchor.place).toBe(false);expect(anchor.key).toBe('HESSE-DARMSTADT');expect(identityFor(hesse.properties!,1750,ids).leaders.some(l=>/Luis VIII/.test(l.name))).toBe(true);
  expect(matchingFeature(anchor,seats,1750,ids)).toBe(hesse);expect(data.features.find(f=>f.properties?.identityKey==='HIST-Q12548')?.geometry.type).toMatch(/Polygon/);
  expect(governmentCounts(seats).get('monarchy')).toBeGreaterThan(0);
 });
 it('distinguishes dynastic devices from later national flags and fills representative early1800 symbols',()=>{
  for(const [key,y,title] of [['JPN',1800,'Tokugawa family crest'],['QING',1800,'Plain Yellow Banner'],['JOS',1800,'1776-1876'],['RUE',1800,'Flag of Russia'],['IRN',1800,'Fath Ali Shah Flag']] as const){const i=identityFor({identityKey:key},y,ids);expect(i.flag?.title).toContain(title);expect(i.flag?.symbolLabel).toBeTruthy();}
  expect(identityFor({identityKey:'PRUSSIA'},1720,ids).flag?.title).toContain('1701-1750');expect(identityFor({identityKey:'HIST-Q157367'},1700,ids).flag?.title).toContain('1657-1701');
  expect(identityFor({identityKey:'FRA'},1700,ids).leaders.some(l=>l.person==='Q7742')).toBe(true);
  expect(identityFor({identityKey:'JPN'},1700,ids).leaders.some(l=>l.person==='Q313745'&&l.portrait)).toBe(true);
 });
});
