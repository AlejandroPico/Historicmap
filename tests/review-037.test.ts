import{readFileSync,writeFileSync}from'node:fs';import{createHash}from'node:crypto';import{describe,it,expect,vi}from'vitest';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{identityFor,identityMarkup}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';import{regionsAt}from'../src/cultural-regions';import{datedPlaces}from'../src/historical-places';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),ids=read('public/data/identities.json'),regions=read('public/data/cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),at=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
describe('300–399 courts, communities and verified portrait framing',()=>{
 it('consults all dates without dropping cultures or inventing symbols',async()=>{
  const years:any[]=[];
  for(let y=300;y<=399;y++){expect(snapshotFor(y).file).toBe('early-modern-300.geojson');expect(playbackYear(y)).toBe(y+1);const p=await world(y),r=regionsAt(regions,y,p);expect(p.features.length).toBeGreaterThan(20);expect(r.features.length).toBeGreaterThan(45);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-SAMI')).toBe(true);expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-AMAZON')).toBe(true);const withoutAuthorities=p.features.filter(f=>!identityFor(f.properties!,y,ids).leaders.length).map(f=>({key:f.properties?.identityKey,name:f.properties?.name}));years.push({year:y,politicalComponents:p.features.length,culturalReferences:r.features.length,withoutAuthorities,documentedPlaces:datedPlaces(p,y).features.length});}
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-300-399.json',JSON.stringify({scope:'Disponibilidad anual y carencias; no censo exhaustivo ni fronteras observadas anualmente.',years},null,2)+'\n');expect(snapshotFor(400).file).toBe('early-modern-400.geojson');
 },90000);
 it('distinguishes augusti, caesars and the395 courts while retaining Roman colours',async()=>{
  const leaders=at('ROMAN-EMPIRE-CLASSICAL',300).leaders;expect(leaders.filter(l=>l.role.includes('Augusto')).length).toBe(2);expect(leaders.filter(l=>l.role.includes('César')).length).toBe(2);expect(leaders.some(l=>l.name.includes('Constantino I'))).toBe(false);expect(leaders.find(l=>l.person==='Q43107')?.portrait?.coinFace).toBe('left');
  expect(at('ROMAN-EMPIRE-CLASSICAL',355).leaders.some(l=>l.person==='Q46418')).toBe(true);expect(at('ROMAN-EMPIRE-CLASSICAL',352).leaders.some(l=>l.name.includes('Galo')&&l.role.includes('César'))).toBe(true);expect(at('WESTERN-ROMAN-EMPIRE',395).leaders.some(l=>l.person==='Q159798')).toBe(true);expect(at('BYZANTINE',395).leaders.some(l=>l.person==='Q159369')).toBe(true);
  expect((await world(300)).features.filter(f=>f.properties?.identityKey==='ROMAN-EMPIRE-CLASSICAL').every(f=>f.properties?.politicalColor==='#8d3b68')).toBe(true);
 });
 it('retains distinct Jin courts and source chronology qualifications',async()=>{
  expect(at('WESTERN-JIN',315).leaders.length).toBeGreaterThan(0);expect(at('EASTERN-JIN',320).leaders.some(l=>l.name.includes('Yuan'))).toBe(true);expect(at('FORMER-QIN',380).leaders.length).toBeGreaterThan(0);expect(at('FORMER-QIN',380).leaders.some(l=>l.person==='Q967998')).toBe(true);
  expect((await world(320)).features.filter(f=>f.properties?.identityKey==='WESTERN-JIN').every(f=>f.properties?.status==='source-reference')).toBe(true);expect(datedPlaces(await world(320),320).features.some(f=>f.properties?.identityKey==='EASTERN-JIN')).toBe(true);
 });
 it('keeps approximate testimony separate from complete reigns',()=>{
  expect(at('HIST-Q139377',340).leaders.some(l=>l.person==='Q379898'&&l.note?.includes('década'))).toBe(true);const testimony=at('MAYA-TIKAL',359).leaders.find(l=>l.person==='Q21934159');expect(testimony?.start).toBe('0359-01-01');expect(testimony?.end).toBe('0359-12-31');expect(at('HUNNIC-EMPIRE',350).leaders.some(l=>l.name.includes('Atila'))).toBe(false);
 });
 it('preserves every political source coordinate and licenses adopted images',()=>{
  const inventory=read('docs/PERIOD-INVENTORY-300.json'),source=read('public/data/early-modern-300.geojson');let count=0;
  for(const file of inventory.canonicalDossiers){const d=read(file);for(const g of d.geography??[]){const f=file.slice(0,file.lastIndexOf('/')+1)+g.file;expect(createHash('sha256').update(readFileSync(f)).digest('hex')).toBe(g.sha256);for(const original of read(f).features){const published=source.features.find((f:any)=>f.id==='clio-'+original.sourceIndex);expect(published.geometry).toEqual(original.geometry);count++;}}for(const l of d.leaders){if(!l.portrait)continue;expect(l.portrait.license).toBeTruthy();expect(createHash('sha256').update(readFileSync(l.portrait.canonicalFile)).digest('hex')).toBe(l.portrait.sha256);}}
  expect(count).toBe(232);
 });
 it('shows a reviewed coin face and a qualified Valentinian bust without replacing Joannes',()=>{
  const marcian=at('BYZANTINE',452).leaders.find(l=>l.name==='Marciano');expect(marcian?.portrait?.coinFace).toBe('left');const html=identityMarkup({identityKey:'BYZANTINE'},452,ids,'/','authorities');expect(html).toContain('coin-frame coin-left');expect(html).toContain('leader-portrait');
  const val=at('WESTERN-ROMAN-EMPIRE',452).leaders.find(l=>l.person==='Q170026');expect(val?.portrait?.title).toContain('Bust of Valentinian');expect(val?.portrait?.caption).toContain('425–450');expect(val?.portrait?.caption).toContain('restaurados');expect(at('WESTERN-ROMAN-EMPIRE',424).leaders.some(l=>l.name==='Juan'&&l.portrait)).toBe(true);
 });
});
