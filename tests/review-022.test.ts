import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{datedPlaces}from'../src/historical-places';import{withGovernance,governmentFor}from'../src/governance';import{identityFor,type IdentityData}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';
const read=(p:string)=>JSON.parse(readFileSync('public/data/'+p,'utf8'));const ids:IdentityData=read('identities.json');vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>withGovernance(politicalData(await annualData(y),y),y);const identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
describe('1400–1499 annual extension',()=>{
 it('loads every annual year and inventories actual documentary availability',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1400;y<=1499;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-1400.geojson'});expect(playbackYear(y)).toBe(y+1);const d=await world(y);expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:datedPlaces(d,y).features.filter(f=>f.properties?.sovereignSeat).length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1400-1499.json',JSON.stringify({scope:'Production-path availability, not an exhaustive state census, independent border verification or daily-front reconstruction. Grouped sovereign seats counted separately.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(499).kind).toBe('historical');expect(snapshotFor(1500).file).toBe('early-modern-1500.geojson');
 },90000);
 it('separates collapsed empires, dynastic titles and corrected source identifiers',async()=>{
  const key=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties.identityKey;
  expect(key(await world(1400),'Byzantine Empire')).toBe('BYZANTINE');expect(identity('BYZANTINE',1400).leaders.some(l=>l.person==='Q37097')).toBe(true);expect(identity('BYZANTINE',1450).leaders.some(l=>l.person==='Q37142')).toBe(true);expect(identity('BYZANTINE',1454).leaders).toHaveLength(0);
  expect(identity('TREBIZOND',1460).leaders.length).toBeGreaterThan(0);expect(identity('TREBIZOND',1462).leaders).toHaveLength(0);
  expect(key(await world(1400),'Old Kingdom of Norway')).toBe('NORWAY-KINGDOM');expect(identity('NORWAY-KINGDOM',1400).leaders.some(l=>l.person==='Q202266')).toBe(true);
  expect(identity('SAVOY-DUCHY',1400).leaders).toHaveLength(0);expect(identity('SAVOY-COUNTY',1400).leaders.some(l=>l.person==='Q312636')).toBe(true);expect(identity('SAVOY-DUCHY',1420).leaders.some(l=>l.person==='Q312636')).toBe(true);
  expect(identity('GRANADA-EMIRATE',1490).leaders.some(l=>l.person==='Q312763')).toBe(true);expect(identity('GRANADA-EMIRATE',1493).leaders).toHaveLength(0);expect(identity('ESP',1450).leaders).toHaveLength(0);
 });
 it('preserves interruptions and rival offices instead of interpolating one stable reign',()=>{
  expect(identity('ENGLAND',1465).leaders.some(l=>l.person==='Q160337')).toBe(false);expect(identity('ENGLAND',1470).leaders.filter(l=>['Q160337','Q160341'].includes(l.person)).length).toBe(2);expect(identity('ENGLAND',1483).leaders.filter(l=>['Q160341','Q170470','Q133028'].includes(l.person)).length).toBe(3);
  expect(identity('MING',1450).leaders.some(l=>l.person==='Q9983')).toBe(false);expect(identity('MING',1450).leaders.some(l=>l.person==='Q9988')).toBe(true);expect(identity('MING',1460).leaders.some(l=>l.person==='Q9983')).toBe(true);
  expect(identity('OTT',1405).leaders.some(l=>l.person==='Q1095044')).toBe(true);expect(identity('OTT',1412).leaders.some(l=>l.person==='Q1095287')).toBe(true);expect(identity('OTT',1405).leaders.some(l=>l.person==='Q128358')).toBe(false);
  expect(identity('ETH',1475).leaders.some(l=>l.person==='Q713338')).toBe(false);expect(identity('ETH',1480).leaders.some(l=>l.person==='Q713338')).toBe(true);
  expect(identity('POLAND-KINGDOM',1442).leaders.some(l=>l.person==='Q53459')).toBe(false);expect(identity('LITHUANIA-DUCHY',1442).leaders.some(l=>l.person==='Q53459')).toBe(true);
  expect(governmentFor({identityKey:'MING'},1450).regimeTag).toBeUndefined();
 });
 it('keeps symbols and portraits local, dated and distinct from modern national flags',()=>{
  expect(identity('BYZANTINE',1400).flag?.title).toContain('Byzantine imperial flag');expect(identity('GRANADA-EMIRATE',1490).flag?.symbolLabel).toContain('nazarí');expect(identity('CASTILE',1400).flag?.title).not.toContain('Burgundy');expect(identity('JPN',1450).flag?.title).toBe('Ashikaga mon.svg');expect(identity('PRT',1400).flag?.title).toBe('PortugueseFlag1385.svg');expect(identity('PRT',1499).flag?.title).toContain('1495');
  expect(identity('AZTEC',1450).flag).toBeUndefined();expect(identity('INCA',1450).flag).toBeUndefined();
  for(const [k,y,p]of [['BYZANTINE',1400,'Q37097'],['ENGLAND',1450,'Q160337'],['MING',1490,'Q9994'],['PAPAL-STATES',1400,'Q165561']]as const)expect(identity(k,y).leaders.find(l=>l.person===p)?.portrait?.file).toMatch(/^media\//);
  const rejected=JSON.parse(readFileSync('scripts/historical-offices-022-research.json','utf8')).rejected;expect(rejected.some((r:any)=>r.candidate.person==='Q8089282')).toBe(true);
 });
});
