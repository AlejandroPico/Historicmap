import{readFileSync,writeFileSync}from'node:fs';import{createHash}from'node:crypto';import{describe,it,expect,vi}from'vitest';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{identityFor}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';import{regionsAt}from'../src/cultural-regions';import{datedPlaces}from'../src/historical-places';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),ids=read('public/data/identities.json'),regions=read('public/data/cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),at=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
describe('100–199 courts and communities with uncertain chronology retained',()=>{
 it('consults every annual date without losing established cultural identities',async()=>{
  const years:any[]=[];
  for(let y=100;y<=199;y++){expect(snapshotFor(y).file).toBe('early-modern-100.geojson');expect(playbackYear(y)).toBe(y+1);const p=await world(y),r=regionsAt(regions,y,p);expect(p.features.length).toBeGreaterThan(15);expect(r.features.length).toBeGreaterThan(60);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);for(const key of ['CULTURE-SAMI','CULTURE-AMAZON'])expect(r.features.some(f=>f.properties?.contextKey===key)).toBe(true);years.push({year:y,politicalComponents:p.features.length,culturalReferences:r.features.length,documentedPlaces:datedPlaces(p,y).features.length,withoutAuthorities:p.features.filter(f=>!identityFor(f.properties!,y,ids).leaders.length).map(f=>({key:f.properties?.identityKey,name:f.properties?.name}))});}
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-100-199.json',JSON.stringify({scope:'Disponibilidad anual y carencias; no censo exhaustivo ni fronteras observadas anualmente.',years},null,2)+'\n');expect(snapshotFor(99).kind).toBe('historical');expect(snapshotFor(200).file).toBe('early-modern-200.geojson');
 },90000);
 it('preserves Roman continuity, joint augusti, caesars and regional claims',async()=>{
  expect(at('ROMAN-EMPIRE-CLASSICAL',100).leaders.some(l=>l.person==='Q1425')).toBe(true);expect(at('ROMAN-EMPIRE-CLASSICAL',161).leaders.filter(l=>l.role.includes('Augusto')).length).toBe(3);expect(at('ROMAN-EMPIRE-CLASSICAL',177).leaders.some(l=>l.name==='Cómodo'&&l.role.includes('Augusto'))).toBe(true);expect(at('ROMAN-EMPIRE-CLASSICAL',193).leaders.length).toBeGreaterThanOrEqual(5);expect(at('ROMAN-EMPIRE-CLASSICAL',194).leaders.some(l=>l.name.includes('Albino')&&l.role.includes('César'))).toBe(true);
  for(const y of [100,117,161,193,199,200])expect((await world(y)).features.filter(f=>f.properties?.identityKey==='ROMAN-EMPIRE-CLASSICAL').every(f=>f.properties?.politicalColor==='#8d3b68')).toBe(true);
 });
 it('keeps Armenian and Osroene offices from leaking into Parthian reigns',()=>{
  const q=at('HIST-Q237234',120).leaders.find(l=>l.name.includes('Partamaspates'))?.person;expect(q).toBeTruthy();expect(at('PARTHIAN-ARSACID',120).leaders.some(l=>l.person===q)).toBe(false);expect(at('PARTHIAN-ARSACID',185).leaders.some(l=>l.name.includes('Vologases V'))).toBe(false);expect(at('HIST-Q208404',185).leaders.some(l=>l.name.includes('Vologases V'))).toBe(true);
  expect(at('HIST-Q237234',150).leaders.some(l=>l.name==='Ma’nu VIII')).toBe(true);expect(at('HIST-Q237234',170).leaders.some(l=>l.name==='Ma’nu VIII')).toBe(true);
 });
 it('retains Han, dated regencies and approximate Kushan references without invented early Maya rulers',async()=>{
  expect(at('EASTERN-HAN',100).leaders.some(l=>l.name.includes('He de Han'))).toBe(true);expect(at('EASTERN-HAN',125).leaders.filter(l=>l.role.includes('Emperador')).length).toBeGreaterThanOrEqual(3);expect(at('EASTERN-HAN',145).leaders.some(l=>l.name.includes('Liang Na')&&l.role.includes('regente'))).toBe(true);expect(at('CAO-CAO-REGIME',199).leaders.some(l=>l.role.includes('Emperador'))).toBe(false);
  expect(at('KUSHAN-EMPIRE',100).leaders.some(l=>l.name==='Vima Takto')).toBe(true);expect(at('KUSHAN-EMPIRE',128).leaders.some(l=>l.name==='Kanishka')).toBe(true);expect(at('MAYA-TIKAL',150).leaders).toHaveLength(0);expect(datedPlaces(await world(133),133).features.some(f=>f.properties?.identityKey==='BAR-KOKHBA')).toBe(true);
 });
 it('preserves original political coordinates and excludes inappropriate visual candidates',()=>{
  const inventory=read('docs/PERIOD-INVENTORY-100.json'),published=read('public/data/early-modern-100.geojson');let count=0;
  for(const file of inventory.canonicalDossiers){const d=read(file);for(const g of d.geography??[]){const f=file.slice(0,file.lastIndexOf('/')+1)+g.file;expect(createHash('sha256').update(readFileSync(f)).digest('hex')).toBe(g.sha256);for(const original of read(f).features){expect(published.features.find((f:any)=>f.id==='clio-'+original.sourceIndex).geometry).toEqual(original.geometry);count++;}}
   for(const r of d.mediaReview??[])if(r.decision==='rejected')expect(d.leaders.filter((l:any)=>l.person===r.person).every((l:any)=>l.portrait?.title!==r.title)).toBe(true);for(const l of d.leaders)if(l.portrait){expect(l.portrait.license).toBeTruthy();expect(createHash('sha256').update(readFileSync(l.portrait.canonicalFile)).digest('hex')).toBe(l.portrait.sha256);}}
  expect(count).toBe(126);const pertinax=at('ROMAN-EMPIRE-CLASSICAL',193).leaders.find(l=>l.name==='Pertinax');expect(pertinax?.portrait?.title).toBe('Pertinax Denarius (obverse).jpg');expect(pertinax?.portrait?.caption).toContain('PERTIN AVG');
 });
});
