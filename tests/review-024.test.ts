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
describe('1200–1299 annual extension',()=>{
 it('renders every annual selection and inventories authority, symbol and portrait gaps',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1200;y<=1299;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-1200.geojson'});expect(playbackYear(y)).toBe(y+1);
   const d=await world(y);expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);
   let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   const seats=datedPlaces(d,y);expect(new Set(seats.features.map(f=>f.id)).size).toBe(seats.features.length);
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:seats.features.filter(f=>f.properties?.sovereignSeat).length});
  }
  const catalogueMissingPortraits=new Map<string,any>();for(const[key,c]of Object.entries(ids.countries))for(const l of c.leaders)if(l.start<'1300-01-01'&&l.end>='1200-01-01'&&!l.portrait){const r=catalogueMissingPortraits.get(l.person)??{person:l.person,name:l.name,keys:[]};if(!r.keys.includes(key))r.keys.push(key);catalogueMissingPortraits.set(l.person,r);}
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1200-1299.json',JSON.stringify({scope:'Production-path availability, not a complete world census, independent border verification or daily-front reconstruction. Additional seats counted separately. The catalogue portrait inventory also includes entities without their own polygon.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueMissingPortraits:[...catalogueMissingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(1199).kind).toBe('historical');expect(snapshotFor(1300).file).toBe('early-modern-1300.geojson');
 },90000);
 it('separates Castile and Leon, Byzantine successor states and inherited source contours',async()=>{
  const key=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties.identityKey;
  expect(key(await world(1220),'Kingdom of Castile')).toBe('CASTILE-KINGDOM');expect(key(await world(1220),'Kingdom of León')).toBe('LEON-KINGDOM');
  expect(key(await world(1235),'Kingdom of Castile')).toBe('CASTILE');expect(key(await world(1235),'Kingdom of León')).toBe('CASTILE');
  expect(identity('CASTILE-KINGDOM',1217).leaders.some(l=>l.person==='Q232323')).toBe(true);expect(identity('CASTILE',1220).leaders).toHaveLength(0);
  expect(identity('BYZANTINE',1250).leaders).toHaveLength(0);expect(identity('NICAEA',1250).leaders.some(l=>l.person==='Q37072')).toBe(true);expect(identity('LATIN-EMPIRE',1250).leaders.some(l=>l.person==='Q269573')).toBe(true);
  expect(identity('LATIN-EMPIRE',1265).leaders).toHaveLength(0);expect(identity('BYZANTINE',1265).leaders.some(l=>l.person==='Q200033')).toBe(true);
  const d=await world(1265);expect(d.features.find(f=>f.properties?.originalName==='Latin Empire')?.properties?.status).toBe('source-reference');expect(key(d,'Nicaean Empire')).toBe('BYZANTINE');
  expect(datedPlaces(await world(1261),1261).features.some(f=>f.properties?.identityKey==='BYZANTINE'&&f.properties?.sovereignSeat)).toBe(true);
  expect(key(await world(1272),'Comtat Venaissin')).toBe('UNRESOLVED-COMTAT-SOURCE');expect(key(await world(1274),'Comtat Venaissin')).toBe('PAPAL-STATES');
 });
 it('distinguishes Mongol regencies, Yuan proclamation, rival offices and false homonyms',async()=>{
  expect(identity('MONGOL-EMPIRE',1200).leaders).toHaveLength(0);
  for(const[y,q]of[[1206,'Q720'],[1228,'Q7517'],[1244,'Q1072396'],[1249,'Q2450507'],[1255,'Q7521']]as const)expect(identity('MONGOL-EMPIRE',y).leaders.some(l=>l.person===q)).toBe(true);
  expect(identity('YUAN',1265).leaders).toHaveLength(0);expect(identity('YUAN',1275).leaders.some(l=>l.person==='Q7523')).toBe(true);expect(identity('SOUTHERN-SONG',1277).leaders.some(l=>l.person==='Q7500')).toBe(false);expect(identity('SOUTHERN-SONG',1280).leaders).toHaveLength(0);
  const d=await world(1280);expect(d.features.find(f=>f.properties?.originalName==='Mongol Empire')?.properties?.status).toBe('source-reference');expect(datedPlaces(d,1280).features.some(f=>f.properties?.identityKey==='YUAN'&&f.properties?.sovereignSeat)).toBe(true);
  expect(identity('HUNGARY-KINGDOM',1259).leaders.some(l=>l.person==='Q158038')).toBe(false);expect(identity('HUNGARY-KINGDOM',1271).leaders.some(l=>l.person==='Q158038')).toBe(true);
  expect(identity('HIST-Q12548',1215).leaders.find(l=>l.person==='Q130221')?.role).toBe('Rey de Romanos');expect(identity('HIST-Q12548',1225).leaders.find(l=>l.person==='Q130221')?.role).toContain('Emperador');
  expect(identity('HESSE-UNITED',1260).leaders).toHaveLength(0);expect(identity('HESSE-UNITED',1265).leaders.some(l=>l.person==='Q76968')).toBe(true);
  expect(identity('MAMLUKS',1295).leaders.some(l=>l.person==='Q558359')).toBe(true);expect(identity('MAMLUKS',1295).leaders.some(l=>l.person==='Q602993')).toBe(false);
  expect(identity('JPN',1230).leaders.some(l=>l.person==='Q1188359'&&l.role.includes('Shikken'))).toBe(true);expect(identity('JPN',1230).leaders.some(l=>l.person==='Q471780'&&l.role.includes('Shogun'))).toBe(true);expect(identity('GORYEO',1250).leaders.some(l=>l.person==='Q2369258')).toBe(true);
  expect(governmentFor({identityKey:'MONGOL-EMPIRE'},1240).regimeTag).toBeUndefined();
 });
 it('uses period symbols and licensed portraits without extending later designs',()=>{
  expect(identity('FRA',1200).flag?.title).toContain('Ancien');expect(identity('CASTILE-KINGDOM',1217).flag?.title).toBe('Royal Banner of the Kingdom of Castile.svg');expect(identity('LEON-KINGDOM',1220).flag?.title).toBe('Royal Banner of Leon.svg');expect(identity('CASTILE',1235).flag?.title).toContain('Early Style');
  expect(identity('ENGLAND',1200).flag?.title).toBe('Royal arms of England.svg');expect(identity('SCOTLAND',1200).flag).toBeUndefined();expect(identity('SCOTLAND',1250).flag?.title).toBe('Royal Banner of Scotland.svg');expect(identity('FLORENCE-REPUBLIC',1240).flag).toBeUndefined();expect(identity('FLORENCE-REPUBLIC',1260).flag?.title).toBe('Flag of Florence.svg');expect(identity('JPN',1230).flag?.title).toBe('Japanese Crest mitu Uroko.svg');
  for(const[k,y,p]of[['FRA',1200,'Q34428'],['FRA',1250,'Q346'],['YUAN',1275,'Q7523'],['MONGOL-EMPIRE',1255,'Q7521']]as const)expect(identity(k,y).leaders.find(l=>l.person===p)?.portrait?.file).toMatch(/^media\//);
  expect(identity('MONGOL-EMPIRE',1244).leaders.find(l=>l.person==='Q1072396')?.portrait).toBeUndefined();expect(identity('SWE',1220).leaders.find(l=>l.person==='Q320989')?.portrait?.caption).toContain('Efigie numismática');
  const r=JSON.parse(readFileSync('scripts/historical-offices-024-research.json','utf8'));expect(r.rejected.some((v:any)=>v.candidate.person==='Q602993')).toBe(true);expect(r.records.some((v:any)=>v.key==='SAVOY-COUNTY'&&v.term.person==='Q723562'&&v.term.start.startsWith('1229'))).toBe(false);
 });
});
