import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{datedPlaces}from'../src/historical-places';import{withGovernance,governmentFor}from'../src/governance';import{identityFor,type IdentityData}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';
const read=(p:string)=>JSON.parse(readFileSync('public/data/'+p,'utf8'));const ids:IdentityData=read('identities.json');vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>withGovernance(politicalData(await annualData(y),y),y);const identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
describe('1500–1599 annual extension',()=>{
 it('renders every annual selection and inventories actual authority, symbol and portrait coverage',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1500;y<=1599;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-1500.geojson'});expect(playbackYear(y)).toBe(y+1);const d=await world(y);
   expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:datedPlaces(d,y).features.filter(f=>f.properties?.sovereignSeat).length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1500-1599.json',JSON.stringify({scope:'Production-path availability, not a complete state census, independent verification of all boundaries, daily fronts or historiographic certification. Grouped-state seats counted separately.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(499).kind).toBe('historical');expect(snapshotFor(1600).file).toBe('early-modern-1600.geojson');
 },90000);
 it('does not anticipate unions, empires or later office holders',async()=>{
  const key=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties.identityKey;
  expect(key(await world(1500),'Crown of Castile')).toBe('CASTILE');expect(identity('CASTILE',1500).leaders.some(l=>l.person==='Q45859')).toBe(true);expect(identity('CASTILE',1500).leaders.some(l=>l.person==='Q32500')).toBe(false);
  expect(identity('CASTILE',1506).leaders.some(l=>l.person==='Q157098')).toBe(true);expect(identity('CASTILE',1510).leaders.some(l=>l.person==='Q157098')).toBe(false);
  expect(identity('CASTILE',1520).leaders.filter(l=>['Q32500','Q171136'].includes(l.person)).length).toBe(2);
  expect(key(await world(1500),'Grand Principality of Moscow')).toBe('MUSCOVY');expect(identity('MUSCOVY',1540).leaders.some(l=>l.person==='Q7996')).toBe(true);expect(identity('RUSSIA-TSARDOM',1540).leaders).toHaveLength(0);
  expect(identity('PRT',1550).leaders.some(l=>l.person==='Q34417')).toBe(false);expect(identity('PRT',1590).leaders.some(l=>l.person==='Q34417')).toBe(true);expect(identity('IBERIAN-UNION',1570).leaders).toHaveLength(0);
  expect(key(await world(1550),'Republic of Florence')).toBe('FLORENCE-DUCHY');expect(identity('FLORENCE-DUCHY',1550).leaders.some(l=>l.person==='Q48547')).toBe(true);
  expect(identity('QING',1590).leaders).toHaveLength(0);expect(identity('MING',1590).leaders.some(l=>l.person==='Q10061')).toBe(true);
 });
 it('separates interrupted reigns, titles, conquest and annual institutional context',()=>{
  expect(identity('HIST-Q33296',1535).leaders.some(l=>l.person==='Q486188')).toBe(true);expect(identity('HIST-Q33296',1550).leaders.some(l=>l.person==='Q486188')).toBe(false);expect(identity('HIST-Q33296',1555).leaders.some(l=>l.person==='Q486188')).toBe(true);
  expect(identity('WURTTEMBERG-DUCHY',1525).leaders.some(l=>l.person==='Q61671')).toBe(false);expect(identity('WURTTEMBERG-DUCHY',1540).leaders.some(l=>l.person==='Q61671')).toBe(true);
  expect(identity('JPN',1560).leaders.some(l=>l.person==='Q447066')).toBe(true);expect(identity('JPN',1590).leaders.find(l=>l.person==='Q187550')?.role).toContain('Kanpaku');expect(identity('JPN',1590).leaders.some(l=>l.role.includes('Shogun'))).toBe(false);
  expect(identity('AZTEC',1520).leaders.some(l=>l.person==='Q141791')).toBe(true);expect(identity('AZTEC',1524).leaders).toHaveLength(0);expect(identity('NEO-INCA',1565).leaders.some(l=>l.person==='Q381752')).toBe(true);
  expect(identity('PAPAL-STATES',1500).leaders.some(l=>l.person==='Q108316')).toBe(true);expect(identity('PAPAL-STATES',1555).leaders.filter(l=>['Q169911','Q101776','Q101430'].includes(l.person)).length).toBe(3);
  expect(governmentFor({identityKey:'HESSE-UNITED'},1550).tags).toContain('principality');expect(governmentFor({identityKey:'MING'},1550).regimeTag).toBeUndefined();
 });
 it('uses only dated symbols and licensed local portraits for named rulers',()=>{
  expect(identity('FRA',1500).flag?.symbolLabel).toContain('Armas');expect(identity('FRA',1590).flag?.title).toBe('Royal Standard of the King of France.svg');
  expect(identity('PRT',1500).flag?.title).toContain('1495');expect(identity('PRT',1550).flag?.title).toContain('1521');expect(identity('JPN',1560).flag?.title).toBe('Ashikaga mon.svg');expect(identity('JPN',1590).flag).toBeUndefined();
  expect(identity('ESP',1520).flag?.title).not.toBe('Flag of Cross of Burgundy.svg');expect(identity('ESP',1540).flag?.title).toBe('Flag of Cross of Burgundy.svg');
  for(const [k,y,p]of [['CASTILE',1500,'Q45859'],['ENGLAND',1550,'Q83229'],['MING',1590,'Q10061'],['PAPAL-STATES',1500,'Q108316']]as const){const l=identity(k,y).leaders.find(v=>v.person===p);expect(l?.portrait?.file).toMatch(/^media\//);}
  const rejected=JSON.parse(readFileSync('scripts/historical-offices-021-research.json','utf8')).rejected;expect(rejected.some((r:any)=>r.candidate.person==='Q92784404')).toBe(true);expect(rejected.some((r:any)=>r.candidate.person==='Q133464985')).toBe(true);
 });
});
