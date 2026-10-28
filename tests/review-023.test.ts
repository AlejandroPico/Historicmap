import{firstAnnualYear}from'./coverage';
import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{datedPlaces}from'../src/historical-places';import{withGovernance,governmentFor}from'../src/governance';import{identityFor,type IdentityData}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';
const read=(p:string)=>JSON.parse(readFileSync('public/data/'+p,'utf8'));const ids:IdentityData=read('identities.json');vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>withGovernance(politicalData(await annualData(y),y),y);const identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
describe('1300–1399 annual extension',()=>{
 it('selects all100 annual years and inventories actual authority, symbol and portrait coverage',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1300;y<=1399;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-1300.geojson'});expect(playbackYear(y)).toBe(y+1);const d=await world(y);expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:datedPlaces(d,y).features.filter(f=>f.properties?.sovereignSeat).length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1300-1399.json',JSON.stringify({scope:'Production-path availability, not an exhaustive world census, independent verification of all source borders or a daily-front reconstruction. Grouped-state seats counted separately.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(firstAnnualYear-1).kind).toBe('historical');expect(snapshotFor(1400).file).toBe('early-modern-1400.geojson');
 },90000);
 it('separates Yuan/Ming, Goryeo/Joseon, Serbian and Bosnian changes of title',async()=>{
  const key=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties.identityKey;
  expect(key(await world(1300),'Yuan Dynasty')).toBe('YUAN');expect(identity('YUAN',1300).leaders.some(l=>l.person==='Q8468')).toBe(true);expect(identity('MING',1360).leaders).toHaveLength(0);expect(identity('MING',1370).leaders.some(l=>l.person==='Q9957')).toBe(true);
  expect(identity('YUAN',1370).leaders).toHaveLength(0);expect(identity('NORTHERN-YUAN',1369).leaders.some(l=>l.person==='Q8666')).toBe(true);
  const transition=await world(1370);const inherited=transition.features.find(f=>f.properties?.originalName==='Yuan Dynasty')!;expect(inherited.properties?.status).toBe('source-reference');expect(inherited.properties?.identityKey).toBe('YUAN');expect(datedPlaces(transition,1370).features.some(f=>f.properties?.identityKey==='MING'&&f.properties?.sovereignSeat)).toBe(true);expect(datedPlaces(await world(1350),1350).features.some(f=>f.properties?.identityKey==='GORYEO'&&f.properties?.sovereignSeat)).toBe(true);expect(key(await world(1340),'Kenmu Restoration')).toBe('JPN');
  expect(key(await world(1370),'Goryeo')).toBe('GORYEO');expect(identity('JOS',1380).leaders).toHaveLength(0);expect(identity('GORYEO',1395).leaders).toHaveLength(0);expect(identity('JOS',1395).leaders.some(l=>l.person==='Q378483')).toBe(true);
  expect(identity('SERBIA-EMPIRE',1340).leaders).toHaveLength(0);expect(identity('SERBIA-KINGDOM',1340).leaders.some(l=>l.person==='Q207303')).toBe(true);expect(identity('SERBIA-EMPIRE',1350).leaders.some(l=>l.person==='Q207303')).toBe(true);expect(identity('BOSNIA-KINGDOM',1370).leaders).toHaveLength(0);expect(identity('BOSNIA-KINGDOM',1380).leaders.some(l=>l.person==='Q319605')).toBe(true);
 });
 it('keeps short and interrupted reigns and distinct offices rather than other titles or life dates',()=>{
  expect(identity('FRA',1316).leaders.some(l=>l.person==='Q8404')).toBe(true);expect(identity('FRA',1317).leaders.some(l=>l.person==='Q8404')).toBe(false);
  const shortReign=identity('FRA',1316).leaders.find(l=>l.person==='Q8404')!;expect(shortReign.startIsCoverageBoundary).toBe(false);expect(shortReign.endIsCoverageBoundary).toBe(false);expect(identity('FRA',1300).leaders[0].startIsCoverageBoundary).toBe(true);expect(identity('FRA',1300).leaders[0].endIsCoverageBoundary).toBe(false);
  expect(identity('GORYEO',1331).leaders.some(l=>l.person==='Q487766')).toBe(true);expect(identity('GORYEO',1336).leaders.some(l=>l.person==='Q487766')).toBe(false);expect(identity('GORYEO',1341).leaders.some(l=>l.person==='Q487766')).toBe(true);
  expect(identity('BYZANTINE',1378).leaders.some(l=>l.person==='Q37070')).toBe(false);expect(identity('BYZANTINE',1380).leaders.some(l=>l.person==='Q37070')).toBe(true);expect(identity('BYZANTINE',1390).leaders.some(l=>l.person==='Q37074')).toBe(true);
  expect(identity('CASTILE',1368).leaders.some(l=>l.person==='Q262363')).toBe(false);expect(identity('CASTILE',1370).leaders.some(l=>l.person==='Q262363')).toBe(true);expect(identity('ARAGON',1300).leaders.some(l=>l.person==='Q312735')).toBe(true);
  expect(identity('HESSE-UNITED',1330).leaders.some(l=>l.person==='Q76256')).toBe(true);expect(identity('JPN',1340).leaders.some(l=>l.role.includes('Norte'))).toBe(true);expect(identity('JPN',1340).leaders.some(l=>l.role.includes('Sur'))).toBe(true);
  expect(governmentFor({identityKey:'YUAN'},1320).regimeTag).toBeUndefined();
 });
 it('uses period symbols, verified human identities and licensed local portraits',()=>{
  expect(identity('FRA',1300).flag?.title).toContain('Ancien');expect(identity('FRA',1390).flag?.title).toContain('Moderne');expect(identity('CASTILE',1300).flag?.title).toContain('Early Style');expect(identity('HIST-Q12548',1350).flag?.title).toContain('single head');expect(identity('JPN',1320).flag).toBeUndefined();expect(identity('JPN',1350).flag?.title).toBe('Ashikaga mon.svg');
  for(const [k,y,p]of [['YUAN',1300,'Q8468'],['ENGLAND',1350,'Q129247'],['HIST-Q184536',1324,'Q309333'],['MING',1390,'Q9957']]as const)expect(identity(k,y).leaders.find(l=>l.person===p)?.portrait?.file).toMatch(/^media\//);
  const r=JSON.parse(readFileSync('scripts/historical-offices-023-research.json','utf8'));expect(r.rejected.some((v:any)=>v.candidate.person==='Q45602922')).toBe(true);expect(r.evidence.some((v:any)=>v.candidate.identityResolution?.requested==='Henry II, Landgrave of Hesse'&&v.candidate.human)).toBe(true);expect(identity('YUAN',1329).leaders.some(l=>l.name.toLowerCase().includes('mingzong')||l.name.toLowerCase().includes('kusala')||l.name.toLowerCase().includes('mingsong'))).toBe(true);
 });
});
