import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{datedPlaces}from'../src/historical-places';import{withGovernance,governmentFor}from'../src/governance';import{identityFor,type IdentityData}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';
const read=(p:string)=>JSON.parse(readFileSync('public/data/'+p,'utf8'));const ids:IdentityData=read('identities.json');vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>withGovernance(politicalData(await annualData(y),y),y);const identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
import{administrationFor}from'../src/territorial-administrations';
describe('1600–1699 extension and temporal continuity',()=>{
 it('does not assign the administrator of a retained colonial card before its source window',()=>{
  const p={originalName:'New France',identityKey:'HIST-Q170604',localAuthorityKey:'HIST-Q170604',administratorKey:'FRA',status:'colony',start:1608,end:1699};
  expect(administrationFor(p,1600)).toBeUndefined();expect(administrationFor(p,1610)?.admin).toBe('FRA');expect(administrationFor(p,1700)).toBeUndefined();
 });
 it('selects all100 annual years and inventories availability through the production resolver',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1600;y<=1699;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-1600.geojson'});expect(playbackYear(y)).toBe(y+1);
   const d=await world(y);expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:datedPlaces(d,y).features.filter(f=>f.properties?.sovereignSeat).length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1600-1699.json',JSON.stringify({scope:'Production-path availability, not a complete state census, daily front reconstruction or historiographic certification. Grouped-state seat references counted separately.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(1599).file).toBe('early-modern-1500.geojson');expect(snapshotFor(1700).file).toBe('early-modern-1700.geojson');
 },90000);
 it('separates interregnum and restoration, Ming/Qing and dynastic unions without future rulers',async()=>{
  const key=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties.identityKey;
  expect(key(await world(1600),'Ming Dynasty')).toBe('MING');expect(identity('MING',1600).leaders.some(l=>l.person==='Q10061')).toBe(true);
  expect(key(await world(1655),'Commonwealth of England')).toBe('ENGLISH-COMMONWEALTH');expect(identity('ENGLISH-COMMONWEALTH',1655).leaders.some(l=>l.person==='Q44279')).toBe(true);
  expect(identity('ENGLAND',1655).leaders.some(l=>l.person==='Q122553')).toBe(false);expect(identity('ENGLAND',1660).leaders.some(l=>l.person==='Q122553')).toBe(true);
  expect(identity('PRT',1600).leaders.some(l=>l.person==='Q34464')).toBe(true);expect(identity('PRT',1645).leaders.some(l=>l.person==='Q691402')).toBe(false);expect(identity('PRT',1645).leaders.some(l=>l.person==='Q1060796')).toBe(true);
  expect(identity('QING',1620).leaders).toHaveLength(0);expect(identity('LATER-JIN',1620).leaders.some(l=>l.person==='Q311189')).toBe(true);expect(identity('QING',1645).leaders.some(l=>l.person==='Q310453')).toBe(true);
  expect(identity('SOUTHERN-MING',1646).leaders.filter(l=>['Q45697','Q1046002','Q1326844'].includes(l.person)).length).toBe(3);
 });
 it('keeps titles, calendars and symbol dates explicit and avoids modern regime assessment',()=>{
  expect(identity('BAVARIA-DUCHY',1600).leaders.some(l=>l.person==='Q57206')).toBe(true);expect(identity('BAVARIA-ELECTORATE',1600).leaders).toHaveLength(0);
  expect(identity('ENGLISH-COMMONWEALTH',1655).flag?.title).toContain('1651');expect(identity('ENGLAND',1600).flag?.title).toBe('Flag of England.svg');expect(identity('PRT',1620).flag?.title).toContain('1616');
  expect(identity('JPN',1620).flag?.symbolLabel).toContain('Mon');expect(identity('JOS',1640).flag?.symbolLabel).toContain('Sello');
  expect(identity('RUSSIA-TSARDOM',1685).leaders.filter(l=>['Q8479','Q183698','Q233987'].includes(l.person)).length).toBe(3);expect(identity('RUSSIA-TSARDOM',1685).leaders.filter(l=>l.person==='Q8479').every(l=>l.precision===9)).toBe(true);
  expect(governmentFor({identityKey:'ENGLISH-COMMONWEALTH'},1655).tags).toContain('republic');expect(governmentFor({identityKey:'QING'},1645).regimeTag).toBeUndefined();
  const rejected=JSON.parse(readFileSync('scripts/historical-offices-020-research.json','utf8')).rejected;expect(rejected.some((r:any)=>r.candidate.person==='Q1463281')).toBe(true);expect(rejected.some((r:any)=>r.candidate.person==='Q2364427')).toBe(true);
 });
});
