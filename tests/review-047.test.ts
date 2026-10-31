import{readFileSync,writeFileSync}from'node:fs';import{join,dirname}from'node:path';import{createHash}from'node:crypto';import{describe,it,expect,vi}from'vitest';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{identityFor,type IdentityData}from'../src/identities';import{snapshotFor,playbackYear,navigationYear}from'../src/time';import{regionsAt,regionalAsset,hasRegionalCoverage,containsLocation}from'../src/cultural-regions';import{historicalColor}from'../src/historical-palette';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),ids=read('public/data/identities.json')as IdentityData,regions=read('public/data/cultural-regions.geojson'),inventory=read('docs/PERIOD-INVENTORY-bc3000.json'),cultural=read('docs/CULTURAL-EXTENSION-bc3000.json');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const at=(key:string,y:number)=>identityFor({identityKey:key},y,ids),world=async(y:number)=>politicalData(await annualData(y),y);
describe('3000–2001BCE: dated powers, urban centres and cultural references',()=>{
 it('loads every civil year through bounded original sources, retaining cultures without borrowing a future map',async()=>{
  const years=[];for(let y=-3000;y<=-2001;y++){const file=y<-2600?'early-modern-bc3000.geojson':y<-2200?'early-modern-bc2600.geojson':'early-modern-bc2200.geojson';expect(snapshotFor(y).file).toBe(file);const p=await world(y),r=regionsAt(regions,y,p);expect(p.features.length,String(y)).toBeGreaterThan(0);expect(r.features.length,String(y)).toBeGreaterThan(10);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);expect(r.features.every(f=>Number(f.properties?.sourceYear)<=y)).toBe(true);expect(hasRegionalCoverage(y)).toBe(true);years.push({year:y,politicalComponents:p.features.length,culturalReferences:r.features.length,withoutAnnualAuthorities:p.features.filter(f=>!at(String(f.properties?.identityKey),y).leaders.length).map(f=>({key:f.properties?.identityKey,name:f.properties?.name}))});}
  for(const y of[-2601,-2201,-2001]){expect(playbackYear(y)).toBe(y+1);expect(navigationYear(y,1)).toBe(y+1);}expect(regionalAsset(-3000)).toBe('cultural-regions-bc3000-bc2901.geojson');expect(snapshotFor(-3001).kind).toBe('historical');expect(navigationYear(-1,1)).toBe(1);if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-bc3000-bc2001.json',JSON.stringify({scope:'Disponibilidad y carencias, no mil fronteras observadas independientemente.',years},null,2)+'\n');
 },120000);
 it('corrects coarse Egyptian dynasty names without redrawing source components or equating accession with reunification',async()=>{
  for(const[y,key]of[[-2687,'EGYPT-EARLY-DYNASTIC'],[-2686,'EGYPT-OLD-KINGDOM']]as const)expect((await world(y)).features.filter(f=>f.properties?.originalName==='Early Dynastic Period of Egypt').every(f=>f.properties?.identityKey===key)).toBe(true);
  for(const y of[-2201,-2200])expect((await world(y)).features.some(f=>f.properties?.identityKey==='EGYPT-OLD-KINGDOM')).toBe(true);
  expect((await world(-2046)).features.filter(f=>f.properties?.originalName==='Upper Egypt').every(f=>f.properties?.identityKey==='EGYPT-MIDDLE-KINGDOM'&&String(f.properties?.name).includes('control variable'))).toBe(true);
  const egypt=(await world(-3000)).features.filter(f=>containsLocation(f.geometry,[29.95156,30.6507]));expect(egypt.some(f=>f.properties?.identityKey==='EGYPT-EARLY-DYNASTIC')).toBe(true);
 });
 it('keeps Mentuhotep, Ishbi-Erra and Emisum as the same people at2001/2000, without prolonging Ur III',async()=>{
  for(const key of['EGYPT-MIDDLE-KINGDOM','ISIN-FIRST-DYNASTY','LARSA-KINGDOM']){const a=at(key,-2001).leaders,b=at(key,-2000).leaders;expect(a.length,key).toBeGreaterThan(0);expect(a.some(l=>b.some(r=>r.person===l.person)),key).toBe(true);}
  expect(at('UR-III',-2004).leaders.some(l=>l.person==='Q352752')).toBe(true);expect(at('UR-III',-2003).leaders).toHaveLength(0);expect((await world(-2003)).features.some(f=>f.properties?.identityKey==='REFERENCE-ISIN-LARSA-CITY-STATES')).toBe(true);expect(historicalColor('AKKADIAN-EMPIRE')).not.toBe(historicalColor('UR-III'));
 });
 it('preserves every owned original component and keeps urban reference IDs globally unique',()=>{
  let total=0;const unique=new Set();for(const file of inventory.canonicalDossiers){const d=read(file),compiled=read(`public/data/early-modern-bc${-d.coverageStart}.geojson`);expect(d.coverageEnd-d.coverageStart+1).toBeLessThanOrEqual(400);for(const ref of d.geography){const raw=readFileSync(join(dirname(file),ref.file));expect(createHash('sha256').update(raw).digest('hex')).toBe(ref.sha256);for(const f of JSON.parse(raw.toString()).features){const actual=compiled.features.find((r:any)=>r.id==='clio-'+f.sourceIndex);expect(actual.geometry).toEqual(f.geometry);expect(actual.properties.identityKey).toBe(d.key);total++;unique.add(f.sourceIndex);}}}
  expect(total).toBe(29);expect(unique.size).toBe(25);
  for(const start of[-3000,-2600,-2200]){const expected=inventory.canonicalDossiers.map((f:string)=>read(f)).filter((d:any)=>d.coverageStart===start).map((d:any)=>d.key).sort(),resolution=read(`public/data/historical-bc${-start}-entities.json`);expect(Object.keys(resolution.names).sort()).toEqual(expected);
   for(let i=0;i<resolution.records.length;i++)for(const b of resolution.records.slice(i+1)){const a=resolution.records[i];expect(a.names.some((n:string)=>b.names.includes(n))&&a.start<=b.end&&b.start<=a.end,'ambiguous dated priority').toBe(false);}
  }
  const places=read('public/data/historical-places.json').records;expect(new Set(places.map((r:any)=>r.id)).size).toBe(places.length);expect(places.some((r:any)=>r.key==='REFERENCE-LIANGZHU-COMMUNITIES'||r.keys?.includes('REFERENCE-LIANGZHU-COMMUNITIES'))).toBe(true);
 });
 it('retains all25 named cultural originals, qualifying archaeological phases and anonymous land separately',()=>{
  expect(cultural.originalNamedGroups).toBe(25);expect(cultural.newPhases).toBe(31);expect(cultural.unnamedComponents).toBe(113);
  for(const f of cultural.canonicalDossiers){const d=read(f);expect(d.geometryProvenance.year).toBe(-3000);expect(d.phases.every((p:any)=>p.start>=-3000&&p.end<=-2001)).toBe(true);expect(createHash('sha256').update(readFileSync(join(dirname(f),d.geometryFile))).digest('hex')).toBe(d.geometrySha256);}
  const yam=regions.features.filter((f:any)=>f.properties.originalNames.includes('Yamnaya culture')&&f.properties.sourceYear===-3000);expect(yam.some((f:any)=>f.properties.temporalMode==='historical-area-context')).toBe(true);
  const indus=cultural.canonicalDossiers.map((f:string)=>read(f)).find((d:any)=>d.originalNames.includes('Indus valley civilization'));expect(indus.phases.find((p:any)=>p.start<=-2700&&p.end>=-2700).label).toContain('temprana');
 });
 it('names attested kings without inventing complete reigns, rulers for Indus, or national flags',()=>{
  expect(at('EGYPT-EARLY-DYNASTIC',-3000).note).toContain('Merneith');expect(at('LAGASH-EARLY',-2500).note).toContain('Ur-Nanshe');expect(at('REFERENCE-LIANGZHU-COMMUNITIES',-2900).leaders).toHaveLength(0);expect(at('REFERENCE-INDUS-URBAN-NETWORKS',-2700).leaders).toHaveLength(0);
  for(const f of inventory.canonicalDossiers){const d=read(f);expect(d.symbols).toHaveLength(0);expect(d.leaders.every((l:any)=>!['Q220320','Q1064913','Q352544','Q379896','Q1346234'].includes(l.person))).toBe(true);}
 });
 it('owns inspected representations and replaces written names with verified Ur-Nammu and Shulgi figures',()=>{
  const m=read('docs/MEDIA-REVIEW-bc3000.json');expect(m.candidates).toBe(42);expect(m.accepted).toBe(23);expect(m.rejected).toBe(19);for(const part of['Sargon of Akkad.jpg','Menkaura-FragmentaryStatueHead','Ur-Nammu (name)','Shulgi (drawing)','Umma2350'])expect(m.decisions.some((r:any)=>r.decision==='rejected'&&r.title.includes(part))).toBe(true);
  for(const f of inventory.canonicalDossiers)for(const l of read(f).leaders){if(!l.portrait)continue;expect(l.portrait.caption).toBeTruthy();expect(l.portrait.display).toBe('full-frame');expect(l.portrait.canonicalFile.startsWith(dirname(dirname(f))+'/retratos/')).toBe(true);expect(createHash('sha256').update(readFileSync(l.portrait.canonicalFile)).digest('hex')).toBe(l.portrait.sha256);}
  expect(at('UR-III',-2100).leaders.find(l=>l.person==='Q297417')?.portrait?.title).toContain('foundation');expect(at('UR-III',-2080).leaders.find(l=>l.person==='Q315893')?.portrait?.title).toContain('Foundation figure');
 });
});
