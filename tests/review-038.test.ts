import{readFileSync,writeFileSync}from'node:fs';import{createHash}from'node:crypto';import{describe,it,expect,vi}from'vitest';
import{annualData}from'../src/data';import{politicalData,influenceFor,nationalInfluenceHatching,regimeColor,dependencyColor}from'../src/political';import{identityFor}from'../src/identities';import{snapshotFor,playbackYear,navigationYear,anchors,PRESENT}from'../src/time';import{regionsAt}from'../src/cultural-regions';import{datedPlaces}from'../src/historical-places';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),ids=read('public/data/identities.json'),regions=read('public/data/cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),at=(key:string,y:number)=>identityFor({identityKey:key},y,ids);

describe('200–299 authorities, cultures and shared temporal conventions',()=>{
 it('consults every date with cultural continuity and a catalogue of remaining gaps',async()=>{
  const years:any[]=[];
  for(let y=200;y<=299;y++){
   expect(snapshotFor(y).file).toBe('early-modern-200.geojson');expect(playbackYear(y)).toBe(y+1);const p=await world(y),r=regionsAt(regions,y,p);expect(p.features.length).toBeGreaterThan(15);expect(r.features.length).toBeGreaterThan(45);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);
   for(const key of ['CULTURE-SAMI','CULTURE-AMAZON'])expect(r.features.some(f=>f.properties?.contextKey===key)).toBe(true);
   years.push({year:y,politicalComponents:p.features.length,culturalReferences:r.features.length,documentedPlaces:datedPlaces(p,y).features.length,withoutAuthorities:p.features.filter(f=>!identityFor(f.properties!,y,ids).leaders.length).map(f=>({key:f.properties?.identityKey,name:f.properties?.name}))});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-200-299.json',JSON.stringify({scope:'Disponibilidad anual y carencias; no censo exhaustivo ni fronteras observadas anualmente.',years},null,2)+'\n');expect(snapshotFor(300).file).toBe('early-modern-300.geojson');
 },90000);
 it('distinguishes imperial dignity, regional claims and the Gallic reintegration',async()=>{
  expect(at('ROMAN-EMPIRE-CLASSICAL',238).leaders.length).toBeGreaterThanOrEqual(6);expect(at('ROMAN-EMPIRE-CLASSICAL',293).leaders.filter(l=>l.role.includes('Augusto')).length).toBe(2);expect(at('ROMAN-EMPIRE-CLASSICAL',293).leaders.filter(l=>l.role.includes('César')).length).toBe(2);
  const later=await world(276);expect(later.features.some(f=>f.properties?.originalName==='Gallic Empire'&&f.properties?.identityKey==='ROMAN-EMPIRE-CLASSICAL')).toBe(true);expect(later.features.some(f=>f.properties?.identityKey==='GALLIC-EMPIRE')).toBe(false);
  const palm=at('PALMYRENE-REGIME',272);expect(palm.leaders.some(l=>l.name.includes('Zenobia')&&l.role.includes('Augusta'))).toBe(true);expect(datedPlaces(await world(272),272).features.some(f=>f.properties?.identityKey==='PALMYRENE-REGIME')).toBe(true);
 });
 it('does not turn Cao Cao or Sima regencies into contemporary imperial reigns',()=>{
  expect(at('CAO-CAO-REGIME',210).leaders.some(l=>l.name.includes('Cao Cao'))).toBe(true);expect(at('CAO-CAO-REGIME',210).leaders.some(l=>l.role.includes('Emperador'))).toBe(false);
  expect(at('CAO-WEI',250).leaders.some(l=>l.name.includes('Sima Yi')&&l.role.includes('Regente'))).toBe(true);expect(at('SHU-HAN',230).leaders.some(l=>l.name.includes('Liu Shan'))).toBe(true);expect(at('WESTERN-JIN',280).leaders.length).toBeGreaterThan(0);
 });
 it('preserves source geometry and licenses, excluding rejected images from leaders',()=>{
  const inventory=read('docs/PERIOD-INVENTORY-200.json'),published=read('public/data/early-modern-200.geojson');let n=0;
  for(const file of inventory.canonicalDossiers){const d=read(file);for(const g of d.geography??[]){const f=file.slice(0,file.lastIndexOf('/')+1)+g.file;expect(createHash('sha256').update(readFileSync(f)).digest('hex')).toBe(g.sha256);for(const original of read(f).features){expect(published.features.find((f:any)=>f.id==='clio-'+original.sourceIndex).geometry).toEqual(original.geometry);n++;}}
   for(const r of d.mediaReview??[])if(r.decision==='rejected')expect(d.leaders.filter((l:any)=>l.person===r.person).every((l:any)=>l.portrait?.title!==r.title)).toBe(true);
   for(const l of d.leaders){if(!l.portrait)continue;expect(l.portrait.license).toBeTruthy();expect(createHash('sha256').update(readFileSync(l.portrait.canonicalFile)).digest('hex')).toBe(l.portrait.sha256);}
  }expect(n).toBe(153);
 });
 it('keeps the two Roman families continuous across the399/400 source boundary',async()=>{
  for(const y of [395,399,400,452]){const p=await world(y);for(const [key,color]of [['WESTERN-ROMAN-EMPIRE','#8d3b68'],['BYZANTINE','#70539c']]){const fs=p.features.filter(f=>f.properties?.identityKey===key);expect(fs.length).toBeGreaterThan(0);expect(fs.every(f=>f.properties?.politicalColor===color)).toBe(true);}}
 });
 it('uses dated military relations without changing country identity or inventing local fronts',async()=>{
  expect(influenceFor('AFG',1985)?.power).toBe('USSR');expect(influenceFor('AFG',1989)).toBeUndefined();expect(influenceFor('AFG',2005)?.power).toBe('USA');expect(influenceFor('AFG',2016)?.kind).toBe('military-support');expect(influenceFor('AFG',2021)).toBeUndefined();
  expect(influenceFor('IRQ',2003)?.kind).toBe('occupation');expect(influenceFor('IRQ',2004)?.kind).toBe('intervention');expect(influenceFor('IRQ',2011)).toBeUndefined();expect(influenceFor('IRQ',2015)).toBeUndefined();
  for(const [key,y,power]of [['AFG',1985,'USSR'],['AFG',2005,'USA'],['IRQ',2003,'USA']]as const){const p=await world(y),f=p.features.find(f=>f.properties?.identityKey===key)!;expect(f).toBeTruthy();expect(f.properties?.controlInfluenceColor).toBe(dependencyColor(regimeColor(power,y),key));const h=nationalInfluenceHatching(p,y).features.find(g=>g.properties?.occupiedKey===key)!;expect(h.geometry).toBe(f.geometry);expect(h.properties?.referenceScope).toBe('national-reference');expect(h.properties?.note).toMatch(/no |ni /i);expect(h.properties?.source).toMatch(/^https:/);expect(f.properties?.identityKey).toBe(key);}
 });
 it('steps annually in the common era, exposes the first year and skips zero',()=>{
  for(const y of [1,100,250,399,1000,1800]){expect(navigationYear(y,1)).toBe(y+1);if(y>1)expect(navigationYear(y,-1)).toBe(y-1);}
  expect(anchors).toContain(1);expect(anchors).not.toContain(0);expect(navigationYear(1,-1)).toBe(-1);expect(navigationYear(-1,1)).toBe(1);expect(navigationYear(PRESENT,1)).toBe(PRESENT);
 });
});
