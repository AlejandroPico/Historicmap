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
describe('1000–1099 annual extension',()=>{
 it('renders every annual selection and inventories authority, symbol and portrait gaps',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let y=1000;y<=1099;y++){
   expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'early-modern-1000.geojson'});expect(playbackYear(y)).toBe(y+1);
   const d=await world(y);expect(d.features.length).toBeGreaterThan(70);expect(new Set(d.features.map(f=>f.id)).size).toBe(d.features.length);
   let authorities=0,symbols=0;
   for(const f of d.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year:y,name:p.name,sourceName:p.originalName,key:i.key,administrator:p.administratorKey});if(i.flag)symbols++;else missingSymbols.push({year:y,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   const seats=datedPlaces(d,y);expect(new Set(seats.features.map(f=>f.id)).size).toBe(seats.features.length);
   years.push({year:y,territories:d.features.length,withAuthorities:authorities,withSymbols:symbols,additionalGroupedStateSeats:seats.features.filter(f=>f.properties?.sovereignSeat).length});
  }
  const catalogueMissingPortraits=new Map<string,any>();for(const[key,c]of Object.entries(ids.countries))for(const l of c.leaders)if(l.start<'1100-01-01'&&l.end>='1000-01-01'&&!l.portrait){const r=catalogueMissingPortraits.get(l.person)??{person:l.person,name:l.name,keys:[]};if(!r.keys.includes(key))r.keys.push(key);catalogueMissingPortraits.set(l.person,r);}
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-1000-1099.json',JSON.stringify({scope:'Production-path availability, not a complete world census, independent border verification or daily-front reconstruction. Additional seats counted separately. The catalogue portrait inventory also includes entities without their own polygon.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueMissingPortraits:[...catalogueMissingPortraits.values()]},null,2)+'\n');
  expect(snapshotFor(499).kind).toBe('historical');expect(snapshotFor(1100).file).toBe('early-modern-1100.geojson');
 },90000);
 it('separates crowns, dynastic aggregates and corrected source identities',async()=>{
  const feature=(d:any,n:string)=>d.features.find((f:any)=>f.properties.originalName===n)?.properties;
  expect(feature(await world(1040),'Kingdom of Castile')?.identityKey).toBe('CASTILE-COUNTY');expect(feature(await world(1080),'Kingdom of Castile')?.identityKey).toBe('CASTILE-KINGDOM');
  expect(identity('CASTILE-COUNTY',1040).leaders.some(l=>l.person==='Q296863')).toBe(true);expect(identity('CASTILE-KINGDOM',1040).leaders).toHaveLength(0);
  expect(feature(await world(1000),'Duchy of Bohemia')?.identityKey).toBe('BOHEMIA-DUCHY');expect(datedPlaces(await world(1088),1088).features.some(f=>f.properties?.identityKey==='BOHEMIA'&&f.properties?.sovereignSeat)).toBe(true);expect(datedPlaces(await world(1095),1095).features.some(f=>f.properties?.identityKey==='BOHEMIA-DUCHY'&&f.properties?.sovereignSeat)).toBe(true);
  const d=await world(1040);expect(feature(d,'Buyid Dynasty')?.identityKey).toBe('BUYID');expect(feature(d,'Buyid Dynasty')?.sourceWikidata).toBe('Q12536');expect(ids.countries.BUYID.qid).toBe('Q273874');expect(datedPlaces(d,1040).features.some(f=>f.properties?.identityKey==='ABBASID'&&f.properties?.sovereignSeat)).toBe(true);
  expect((await world(1020)).features.filter(f=>f.properties?.originalName==='Denmark-England').every(f=>f.properties?.status==='source-reference')).toBe(true);
  expect(identity('WESTERN-XIA',1020).leaders).toHaveLength(0);expect(identity('WESTERN-XIA',1040).leaders.some(l=>l.person==='Q7438')).toBe(true);expect(identity('HIST-Q171740',1040).leaders).toHaveLength(0);
  expect(identity('NORTHERN-SONG',1080).leaders.some(l=>l.person==='Q7483')).toBe(true);expect(identity('SOUTHERN-SONG',1080).leaders).toHaveLength(0);
 });
 it('distinguishes restored reigns, coronations, regencies and nominal offices',()=>{
  expect(identity('ENGLAND',1066).leaders.map(l=>l.person)).toEqual(expect.arrayContaining(['Q130005','Q159597','Q215224','Q37594']));expect(identity('ENGLAND',1065).leaders.some(l=>l.person==='Q37594')).toBe(false);
  expect(identity('ENGLAND',1015).leaders.some(l=>l.person==='Q183499')).toBe(true);expect(identity('ENGLAND',1015).leaders.some(l=>l.person==='Q134128')).toBe(false);expect(identity('DNK',1017).leaders.some(l=>l.person==='Q134128')).toBe(false);
  expect(identity('HIST-Q12548',1025).leaders.find(l=>l.person==='Q152256')?.role).toContain('Rey');expect(identity('HIST-Q12548',1030).leaders.find(l=>l.person==='Q152256')?.role).toContain('Emperador');
  expect(identity('BYZANTINE',1053).leaders.some(l=>l.person==='Q41659')).toBe(false);expect(identity('BYZANTINE',1053).leaders.find(l=>l.person==='Q41666')?.role).toBe('Coemperatriz');expect(identity('BYZANTINE',1056).leaders.find(l=>l.person==='Q41666')?.role).toBe('Emperatriz reinante');
  expect(identity('BYZANTINE',1067).leaders.some(l=>l.person==='Q232223'&&l.role.includes('regente'))).toBe(true);expect(identity('BYZANTINE',1069).leaders.find(l=>l.person==='Q210564')?.role).toContain('Coemperador');
  expect(identity('JPN',1080).leaders.some(l=>l.person==='Q60949'&&l.role.includes('retirado'))).toBe(false);expect(identity('JPN',1090).leaders.some(l=>l.person==='Q60949'&&l.role.includes('retirado'))).toBe(true);expect(identity('JPN',1040).leaders.some(l=>l.person==='Q1370620'&&l.role.includes('Kanpaku'))).toBe(true);
  expect(identity('GORYEO',1000).leaders.some(l=>l.person==='Q493723')).toBe(true);expect(governmentFor({identityKey:'GORYEO'},1000).regimeTag).toBeUndefined();
 });
 it('uses documentary seals and removes unrelated objects without inventing later heraldry',()=>{
  expect(identity('FRA',1000).flag).toBeUndefined();expect(identity('FRA',1010).flag?.symbolLabel).toContain('sello');expect(identity('FRA',1035).flag).toBeUndefined();expect(identity('ENGLAND',1080).flag).toBeUndefined();expect(identity('CASTILE-KINGDOM',1080).flag).toBeUndefined();expect(identity('ARAGON-KINGDOM',1080).flag).toBeUndefined();
  const r=JSON.parse(readFileSync('scripts/historical-offices-026-research.json','utf8'));for(const row of r.records)expect(ids.countries[row.key].leaders.some(l=>l.person===row.term.person&&l.start===row.term.start&&l.end===row.term.end&&l.role===row.term.role)).toBe(true);
  const review=JSON.parse(readFileSync('scripts/media-corrections-026.json','utf8'));const bad=new Set(review.rejected.map((v:any)=>v.person+'|'+v.title));for(const c of Object.values(ids.countries))for(const l of c.leaders)if(l.portrait)expect(bad.has(l.person+'|'+l.portrait.title)).toBe(false);
  expect(identity('FRA',1010).leaders.find(l=>l.person==='Q178918')?.portrait?.file).toMatch(/^media\//);expect(identity('NORTHERN-SONG',1080).leaders.find(l=>l.person==='Q7483')?.portrait?.file).toMatch(/^media\//);
 });
});
