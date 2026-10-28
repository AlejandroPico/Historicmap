import{describe,it,expect,vi}from'vitest';
import{readFileSync,writeFileSync,readdirSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';
import{datedPlaces}from'../src/historical-places';import{withGovernance,governmentFor}from'../src/governance';
import{identityFor,type IdentityData}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';
const read=(p:string)=>JSON.parse(readFileSync('public/data/'+p,'utf8'));
const ids:IdentityData=read('identities.json');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>withGovernance(politicalData(await annualData(y),y),y);
const identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
describe('900–999 annual extension',()=>{
 it('renders every annual selection and inventories authority, symbol and portrait gaps',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=900;y<=999;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-900.geojson'});expect(playbackYear(y)).toBe(y+1);
   const d=await world(y);expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);
   let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   const seats=datedPlaces(d,y);expect(new Set(seats.features.map(f=>f.id)).size).toBe(seats.features.length);
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:seats.features.filter(f=>f.properties?.sovereignSeat).length});
  }
  const catalogueMissingPortraits=new Map<string,any>();for(const[key,c]of Object.entries(ids.countries))for(const l of c.leaders)if(l.start<'1000-01-01'&&l.end>='0900-01-01'&&!l.portrait){const r=catalogueMissingPortraits.get(l.person)??{person:l.person,name:l.name,keys:[]};if(!r.keys.includes(key))r.keys.push(key);catalogueMissingPortraits.set(l.person,r);}
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-900-999.json',JSON.stringify({scope:'Production-path availability, not a complete world census, independent border verification or daily-front reconstruction. Additional seats counted separately. The catalogue portrait inventory also includes entities without their own polygon.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueMissingPortraits:[...catalogueMissingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(699).kind).toBe('historical');expect(snapshotFor(1100).file).toBe('early-modern-1100.geojson');
 },90000);
 it('keeps tenth-century dates before later rulers and modern organizations',async()=>{
  const {isoYear}=await import('../src/dates');const {organizationActive,membershipsAt}=await import('../src/historical-affiliations');
  expect(isoYear(900)).toBe('0900');expect(isoYear(999)).toBe('0999');expect(isoYear(2026)).toBe('2026');
  expect(identity('FRA',900).leaders.map(l=>l.name).join(' ')).toContain('Carlos III');expect(identity('FRA',900).leaders.map(l=>l.name).join(' ')).not.toContain('Roberto II');expect(identity('FRA',997).leaders.map(l=>l.name).join(' ')).toContain('Roberto II');
  expect(organizationActive('nato',950)).toBe(false);expect(membershipsAt('nato',950)).toHaveLength(0);expect(governmentFor({identityKey:'GORYEO'},950).regimeTag).toBeUndefined();
 });
 it('separates early kingdoms, imperial accessions and Asian successions',async()=>{
  const feature=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties;
  expect(feature(await world(900),'Kingdom of England')?.identityKey??feature(await world(900),'Kingdom of Wessex')?.identityKey).toBe('WESSEX');
  expect(feature(await world(950),'Kingdom of England')?.identityKey).toBe('ENGLAND');expect(identity('ENGLAND',920).leaders).toHaveLength(0);
  expect(identity('HIST-Q12548',950).leaders.filter(l=>l.start<'1000-01-01')).toHaveLength(0);expect(identity('HIST-Q12548',970).leaders.map(l=>l.name).join(' ')).toContain('Otón');
  expect(identity('GORYEO',910).leaders).toHaveLength(0);expect(identity('GORYEO',950).leaders.map(l=>l.name).join(' ')).toContain('Gwangjong');
  expect(identity('NORTHERN-SONG',950).leaders).toHaveLength(0);expect(identity('NORTHERN-SONG',970).leaders.map(l=>l.name).join(' ')).toContain('Taizu');
  expect(feature(await world(950),'Abbasid Caliphate/Buyid Dynasty')?.identityKey).toBe('BUYID');
 });
 it('retains all dated dossier rules and excludes rejected pictures from every card',()=>{
  let rules=0;
  const resolution=read('historical-900-entities.json');
  for(const folder of readdirSync('Países')){let d:any;try{d=JSON.parse(readFileSync('Países/'+folder+'/periodos/0900-0999.json','utf8'));}catch{continue;}
   for(const fix of d.entityRules??[]){expect(resolution.records.some((r:any)=>r.key===d.key&&r.start===fix.record.start&&r.end===fix.record.end&&JSON.stringify(r.names)===JSON.stringify(fix.record.names))).toBe(true);rules++;}
   for(const r of d.mediaReview??[])if(!r.accepted)for(const c of Object.values(ids.countries))expect(c.leaders.some(l=>l.person===r.person&&l.portrait?.title===r.title)).toBe(false);
  }
  expect(rules).toBeGreaterThan(65);expect(identity('FRA',997).flag?.referenceOnly).toBe(true);expect(identity('FRA',950).flag).toBeUndefined();
 });
});
