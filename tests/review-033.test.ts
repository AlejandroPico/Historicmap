import{governmentFor}from'../src/governance';
import{describe,it,expect,vi}from'vitest';import{readFileSync,readdirSync,existsSync,writeFileSync}from'node:fs';import{resolve,dirname}from'node:path';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{identityFor}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';import{datedPlaces}from'../src/historical-places';import{regionsAt,hasRegionalCoverage}from'../src/cultural-regions';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8')),ids=read('identities.json'),regions=read('cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
const dossiers=readdirSync('Países').flatMap(folder=>{const file='Países/'+folder+'/periodos/0700-0799.json';return existsSync(file)?[{file,data:JSON.parse(readFileSync(file,'utf8'))}]:[];});
describe('700–799 politics and regional evidence',()=>{
 it('consults every annual date with coexisting cultures and explicitly inventories gaps',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let year=700;year<=799;year++){
   expect(snapshotFor(year)).toEqual({kind:'annual',year,file:'early-modern-700.geojson'});expect(playbackYear(year)).toBe(year+1);const p=await world(year),r=regionsAt(regions,year,p);expect(p.features.length).toBeGreaterThan(40);expect(r.features.length).toBeGreaterThan(60);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);
   expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-SAMI')).toBe(true);expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-AMAZON')).toBe(true);
   let authorities=0,symbols=0;for(const f of p.features){const i=identityFor(f.properties!,year,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year,key:i.key,name:f.properties?.name});if(i.flag)symbols++;else missingSymbols.push({year,key:i.key,name:f.properties?.name});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year,politicalComponents:p.features.length,culturalReferences:r.features.length,withAuthorities:authorities,withSymbols:symbols,places:datedPlaces(p,year).features.length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-700-799.json',JSON.stringify({scope:'Disponibilidad anual por el recorrido de producción. No censo exhaustivo ni fronteras culturales observadas cada año. Las ventanas discutidas no certifican mandatos continuos.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueAuthorityRecords:dossiers.reduce((n,d)=>n+d.data.leaders.length,0),catalogueWithoutPortraits:dossiers.flatMap(d=>d.data.leaders.filter((l:any)=>!l.portrait).map((l:any)=>({key:d.data.key,person:l.person,name:l.name,start:l.start,end:l.end})))},null,2)+'\n');
  expect(hasRegionalCoverage(599)).toBe(false);expect(hasRegionalCoverage(700)).toBe(true);expect(snapshotFor(599).kind).toBe('historical');expect(snapshotFor(800).file).toBe('early-modern-800.geojson');
 },90000);
 it('distinguishes the dynasty, palace office and imperial title of the Frankish rulers',()=>{
  expect(identity('FRANKISH-REALM',740).leaders.some(l=>l.name.includes('Martel'))).toBe(true);expect(identity('FRANKISH-REALM',740).leaders.some(l=>l.role.startsWith('Rey'))).toBe(false);
  expect(identity('FRANKISH-REALM',750).leaders.some(l=>l.name.includes('Pipino')&&l.role.startsWith('Rey'))).toBe(false);expect(identity('FRANKISH-REALM',751).leaders.some(l=>l.name.includes('Pipino')&&l.role.startsWith('Rey'))).toBe(true);
  expect(identity('FRANKISH-REALM',780).leaders.some(l=>l.name==='Carlomagno'&&l.role.includes('emperador'))).toBe(false);expect(identity('FRANKISH-REALM',800).leaders.some(l=>l.name==='Carlomagno'&&l.role.includes('emperador'))).toBe(true);
 });
 it('separates Wu Zhou, restored Tang, short reigns and the two reigns of Kōken/Shōtoku',async()=>{
  expect((await world(700)).features.some(f=>f.properties?.identityKey==='WU-ZHOU')).toBe(true);expect(identity('TANG',700).leaders).toHaveLength(0);expect(identity('WU-ZHOU',700).leaders[0].name).toBe('Wu Zetian');
  expect((await world(705)).features.some(f=>f.properties?.identityKey==='TANG')).toBe(true);expect(identity('TANG',710).leaders.some(l=>l.person==='Q9743'&&l.start==='0710-07-08'&&l.end==='0710-07-25')).toBe(true);
  const first=identity('JPN',750).leaders.find(l=>l.person==='Q232955'),second=identity('JPN',765).leaders.find(l=>l.person==='Q232955');expect(first?.name).toContain('Kōken');expect(second?.name).toContain('Shōtoku');expect(identity('JPN',760).leaders.some(l=>l.person==='Q232955')).toBe(false);
  const centres=async(y:number)=>datedPlaces(await world(y),y).features.filter(f=>f.properties?.identityKey==='JPN').map(f=>f.properties?.name);expect(await centres(700)).toContain('Fujiwara-kyō');expect(await centres(712)).toContain('Heijō-kyō · Nara');expect(await centres(790)).toContain('Nagaoka-kyō');expect(await centres(795)).toContain('Heian-kyō · Kioto');
 });
 it('does not anticipate Abbasid government, Bagdad or the Cordoban caliphal title',async()=>{
  expect(identity('UMAYYAD-CALIPHATE',720).leaders.length).toBeGreaterThan(0);expect(identity('ABBASID',740).leaders).toHaveLength(0);expect(identity('ABBASID',755).leaders.length).toBeGreaterThan(0);expect(identity('CORDOBA-EMIRATE',740).leaders).toHaveLength(0);expect(identity('CORDOBA-EMIRATE',780).leaders.every(l=>l.role.includes('Emir'))).toBe(true);
  const centres=async(y:number)=>datedPlaces(await world(y),y).features.filter(f=>f.properties?.identityKey==='ABBASID').map(f=>f.properties?.name);expect(await centres(755)).not.toContain('Bagdad · fundación y corte');expect(await centres(770)).toContain('Bagdad · fundación y corte');
 });
 it('classifies documented institutions and keeps Piluoge’s identity across the union',()=>{
  for(const [key,y]of [['WU-ZHOU',700],['JPN',710],['HIST-Q1045322',750]]as const)expect(governmentFor({identityKey:key},y).tags).toContain('monarchy');
  expect(identity('HIST-Q1045322',730).leaders.find(l=>l.name.includes('Piluoge'))?.person).toBe('LOCAL-NANZHAO-PILUOGE');expect(identity('HIST-Q1045322',740).leaders.find(l=>l.name.includes('Piluoge'))?.person).toBe('LOCAL-NANZHAO-PILUOGE');
 });
 it('retains source geometry and prevents rejected portraits from returning through a fallback',()=>{
  const geo=read('early-modern-700.geojson');let originalCount=0,rejectedCount=0;
  for(const {file,data:d}of dossiers){for(const r of d.geography??[])for(const f of JSON.parse(readFileSync(resolve(dirname(file),r.file),'utf8')).features){expect(geo.features.find((p:any)=>p.id==='clio-'+f.sourceIndex)?.geometry).toEqual(f.geometry);originalCount++;}
   const actual=ids.countries[d.key]?.leaders.filter((l:any)=>l.acquisition===d.acquisition)??[];
   for(const rejected of d.rejectedPortraits??[]){expect(actual.some((l:any)=>l.person===rejected.person&&l.portrait?.title===rejected.title)).toBe(false);rejectedCount++;}
   for(const l of d.leaders)if(l.portrait){expect(l.portrait.caption.length).toBeGreaterThan(20);expect(existsSync(l.portrait.canonicalFile)).toBe(true);}
  }
  expect(originalCount).toBe(geo.features.length);expect(originalCount).toBeGreaterThan(300);expect(rejectedCount).toBeGreaterThan(30);
 });
 it('discloses inherited anachronisms and keeps geographic water names out of the cultural layer',()=>{
  const phase=(n:string)=>regions.features.find((f:any)=>f.properties.sourceYear===700&&f.properties.originalNames.includes(n))?.properties;
  expect(phase('Sui Empire').name).toContain('posteriores a Sui');expect(phase('Sasanian Empire').name).toContain('posteriores');expect(phase('Koguryo').name).toContain('antiguos');expect(phase('Paekche').name).toContain('antiguos');expect(phase('Lake Vygozero')).toBeUndefined();expect(phase('Lake Segozerskoye')).toBeUndefined();
  expect(identity('HIST-Q1045322',780).leaders.some(l=>l.person==='LOCAL-NANZHAO-YIMOUXUN')).toBe(true);expect(identity('BYZANTINE',785).leaders.some(l=>l.name==='Irene'&&l.role==='Emperatriz regente')).toBe(true);expect(identity('BYZANTINE',798).leaders.some(l=>l.name==='Irene'&&l.role==='Emperatriz reinante')).toBe(true);
 });
});
