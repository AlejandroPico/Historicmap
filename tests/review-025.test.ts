import{describe,it,expect,vi}from'vitest';
import{readFileSync,writeFileSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';
import{datedPlaces}from'../src/historical-places';import{withGovernance,governmentFor}from'../src/governance';
import{identityFor,type IdentityData}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';
const read=(p:string)=>JSON.parse(readFileSync('public/data/'+p,'utf8'));
const ids:IdentityData=read('identities.json');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>withGovernance(politicalData(await annualData(y),y),y);
const identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
describe('1100–1199 annual extension',()=>{
 it('renders every annual selection and inventories authority, symbol and portrait gaps',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1100;y<=1199;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-1100.geojson'});expect(playbackYear(y)).toBe(y+1);
   const d=await world(y);expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);
   let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   const seats=datedPlaces(d,y);expect(new Set(seats.features.map(f=>f.id)).size).toBe(seats.features.length);
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:seats.features.filter(f=>f.properties?.sovereignSeat).length});
  }
  const catalogueMissingPortraits=new Map<string,any>();for(const[key,c]of Object.entries(ids.countries))for(const l of c.leaders)if(l.start<'1200-01-01'&&l.end>='1100-01-01'&&!l.portrait){const r=catalogueMissingPortraits.get(l.person)??{person:l.person,name:l.name,keys:[]};if(!r.keys.includes(key))r.keys.push(key);catalogueMissingPortraits.set(l.person,r);}
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1100-1199.json',JSON.stringify({scope:'Production-path availability, not a complete world census, independent border verification or daily-front reconstruction. Additional seats counted separately. The catalogue portrait inventory also includes entities without their own polygon.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueMissingPortraits:[...catalogueMissingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(899).kind).toBe('historical');expect(snapshotFor(1200).file).toBe('early-modern-1200.geojson');
 },90000);
 it('keeps dynastic identities continuous and documents inherited chronology defects',async()=>{
  const feature=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties;
  expect(feature(await world(1120),'Northern Song')?.identityKey).toBe('NORTHERN-SONG');expect(feature(await world(1128),'Northern Song')?.status).toBe('source-reference');
  expect(identity('NORTHERN-SONG',1120).leaders.some(l=>l.person==='Q7486')).toBe(true);expect(identity('NORTHERN-SONG',1130).leaders).toHaveLength(0);expect(identity('SOUTHERN-SONG',1128).leaders.some(l=>l.person==='Q7489')).toBe(true);
  expect(datedPlaces(await world(1128),1128).features.some(f=>f.properties?.identityKey==='SOUTHERN-SONG'&&f.properties?.sovereignSeat)).toBe(true);
  expect(feature(await world(1150),'Kingdom of Portugal')?.identityKey).toBe('PRT');expect(identity('PORTUGAL-COUNTY',1120).leaders.some(l=>l.person==='Q237987')).toBe(true);expect(identity('PRT',1120).leaders).toHaveLength(0);
  expect(feature(await world(1140),'Kingdom of Aragon')?.identityKey).toBe('ARAGON');expect(identity('ARAGON',1140).leaders.some(l=>l.person==='Q235409')).toBe(true);
  expect(feature(await world(1190),'Kingdom of Serbia')?.identityKey).toBe('SERBIA-PRINCIPALITY');expect(feature(await world(1170),'Armenian Kingdom of Cilicia')?.identityKey).toBe('CILICIA-PRINCIPALITY');expect(feature(await world(1199),'Armenian Kingdom of Cilicia')?.identityKey).toBe('CILICIA-KINGDOM');
  expect(feature(await world(1180),'Fatimid Caliphate')?.status).toBeUndefined();expect(feature(await world(1174),'Fatimid Caliphate')?.status).toBe('source-reference');expect(identity('FATIMID',1174).leaders).toHaveLength(0);
  for(const[y,n,k]of[[1199,'Kara-Khitans','HIST-Q862304'],[1200,'Kara-Khitans','HIST-Q862304'],[1199,'Principality of Antioch','HIST-Q235030'],[1200,'Principality of Antioch','HIST-Q235030']]as const)expect(feature(await world(y),n)?.identityKey).toBe(k);
 });
 it('distinguishes royal, imperial, retired and military offices without importing other titles',()=>{
  expect(identity('HIST-Q12548',1140).leaders.find(l=>l.person==='Q157133')?.role).toBe('Rey de Romanos');expect(identity('HIST-Q12548',1153).leaders.find(l=>l.person==='Q79789')?.role).toBe('Rey de Romanos');expect(identity('HIST-Q12548',1160).leaders.find(l=>l.person==='Q79789')?.role).toContain('Emperador');
  expect(identity('ENGLAND',1142).leaders.some(l=>l.person==='Q150872'&&l.role.includes('pretendiente'))).toBe(true);expect(identity('ENGLAND',1175).leaders.some(l=>l.person==='Q235238'&&l.role.includes('sin gobierno independiente'))).toBe(true);
  expect(identity('BOHEMIA',1150).leaders).toHaveLength(0);expect(identity('BOHEMIA',1160).leaders.some(l=>l.person==='Q367578')).toBe(true);expect(identity('BOHEMIA-DUCHY',1150).leaders.some(l=>l.person==='Q367578')).toBe(true);
  expect(identity('SICILY-KINGDOM',1170).leaders.some(l=>l.person==='Q150953')).toBe(false);expect(identity('SICILY-KINGDOM',1195).leaders.some(l=>l.person==='Q150953')).toBe(true);
  expect(identity('AYYUBID',1170).leaders).toHaveLength(0);expect(identity('AYYUBID',1174).leaders.some(l=>l.person==='Q8581')).toBe(true);
  expect(identity('JPN',1185).leaders.some(l=>l.person==='Q242800'&&l.role.includes('todavía sin título'))).toBe(true);expect(identity('JPN',1195).leaders.some(l=>l.person==='Q242800'&&l.role==='Shogun de Kamakura')).toBe(true);expect(identity('JPN',1199).leaders.some(l=>l.person==='Q431052'&&l.role.includes('todavía sin título'))).toBe(true);
  expect(identity('GORYEO',1180).leaders.some(l=>l.person==='Q5624052'&&l.role.includes('militar'))).toBe(true);expect(identity('HIST-Q154667',1155).leaders.some(l=>l.person==='Q266754')).toBe(true);expect(identity('HIST-Q154667',1115).leaders.some(l=>l.person==='Q266754')).toBe(false);
  expect(governmentFor({identityKey:'JPN'},1185).regimeTag).toBeUndefined();
 });
 it('dates heraldry conservatively and rejects associated objects or false human homonyms',()=>{
  expect(identity('ENGLAND',1180).flag).toBeUndefined();expect(identity('ENGLAND',1199).flag?.title).toBe('Royal arms of England.svg');expect(identity('CASTILE-KINGDOM',1160).flag).toBeUndefined();expect(identity('CASTILE-KINGDOM',1180).flag?.title).toContain('Castile');expect(identity('LEON-KINGDOM',1180).flag?.title).toContain('Leon');expect(identity('ARAGON',1180).flag?.title).toContain('Aragón');
  expect(identity('JPN',1190).flag).toBeUndefined();expect(identity('FLORENCE-REPUBLIC',1190).flag).toBeUndefined();
  const r=JSON.parse(readFileSync('scripts/historical-offices-025-research.json','utf8'));expect(r.rejected.some((v:any)=>v.candidate.person==='Q1216913')).toBe(true);expect(r.records.some((v:any)=>v.term.person==='Q7486')).toBe(true);
  for(const row of r.records){expect(ids.countries[row.key].leaders.some(l=>l.person===row.term.person&&l.start===row.term.start&&l.end===row.term.end&&l.role===row.term.role)).toBe(true);expect(row.term.startIsCoverageBoundary&&row.term.start!=='1100-01-01').toBe(false);}
  const review=JSON.parse(readFileSync('scripts/media-corrections-025.json','utf8'));const bad=new Set(review.rejected.map((v:any)=>v.person+'|'+v.title));for(const c of Object.values(ids.countries))for(const l of c.leaders)if(l.portrait)expect(bad.has(l.person+'|'+l.portrait.title)).toBe(false);
  for(const[k,y,q]of[['FRA',1100,'Q58907'],['NORTHERN-SONG',1120,'Q7486'],['SOUTHERN-SONG',1150,'Q7489']]as const){const l=identity(k,y).leaders.find(l=>l.person===q);expect(l?.portrait?.file).toMatch(/^media\//);}
 });
});
