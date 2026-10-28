import{governmentFor}from'../src/governance';
import{describe,it,expect,vi}from'vitest';import{readFileSync,readdirSync,existsSync,writeFileSync}from'node:fs';import{resolve,dirname}from'node:path';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{identityFor}from'../src/identities';import{snapshotFor,playbackYear}from'../src/time';import{datedPlaces}from'../src/historical-places';import{regionsAt,hasRegionalCoverage}from'../src/cultural-regions';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8')),ids=read('identities.json'),regions=read('cultural-regions.geojson');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const world=async(y:number)=>politicalData(await annualData(y),y),identity=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
const dossiers=readdirSync('Países').flatMap(folder=>{const file='Países/'+folder+'/periodos/0600-0699.json';return existsSync(file)?[{file,data:JSON.parse(readFileSync(file,'utf8'))}]:[];});
describe('600–699 politics and regional evidence',()=>{
 it('consults every annual date with coexisting cultures and explicitly inventories gaps',async()=>{
  const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map();
  for(let year=600;year<=699;year++){
   expect(snapshotFor(year)).toEqual({kind:'annual',year,file:'early-modern-600.geojson'});expect(playbackYear(year)).toBe(year+1);const p=await world(year),r=regionsAt(regions,year,p);expect(p.features.length).toBeGreaterThan(40);expect(r.features.length).toBeGreaterThan(50);expect(new Set(p.features.map(f=>f.id)).size).toBe(p.features.length);
   expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-SAMI')).toBe(true);expect(r.features.some(f=>f.properties?.contextKey==='CULTURE-AMAZON')).toBe(true);
   let authorities=0,symbols=0;for(const f of p.features){const i=identityFor(f.properties!,year,ids);if(i.leaders.length)authorities++;else missingAuthorities.push({year,key:i.key,name:f.properties?.name});if(i.flag)symbols++;else missingSymbols.push({year,key:i.key,name:f.properties?.name});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
   years.push({year,politicalComponents:p.features.length,culturalReferences:r.features.length,withAuthorities:authorities,withSymbols:symbols,places:datedPlaces(p,year).features.length});
  }
  if(process.env.WRITE_REVIEW==='1')writeFileSync('docs/REVIEW-600-699.json',JSON.stringify({scope:'Disponibilidad anual por el recorrido de producción. No censo exhaustivo ni fronteras culturales observadas cada año. Las ventanas discutidas no certifican mandatos continuos.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()],catalogueAuthorityRecords:dossiers.reduce((n,d)=>n+d.data.leaders.length,0),catalogueWithoutPortraits:dossiers.flatMap(d=>d.data.leaders.filter((l:any)=>!l.portrait).map((l:any)=>({key:d.data.key,person:l.person,name:l.name,start:l.start,end:l.end})))},null,2)+'\n');
  expect(hasRegionalCoverage(499)).toBe(false);expect(hasRegionalCoverage(600)).toBe(true);expect(snapshotFor(499).kind).toBe('historical');expect(snapshotFor(700).file).toBe('early-modern-700.geojson');
 },90000);

 it('distinguishes source-outline lag from the Sui/Tang transition and replaces Tang with Wu Zhou',async()=>{
  expect(identity('SUI',610).leaders.some(l=>l.person==='Q7419')).toBe(true);expect(identity('SUI',620).leaders).toHaveLength(0);
  expect((await world(600)).features.filter(f=>f.properties?.identityKey==='HIST-Q289577').every(f=>f.properties?.status==='source-reference')).toBe(true);expect(identity('HIST-Q943191',600).leaders.some(l=>l.person==='LOCAL-LAKHMID-AL-NUMAN-III')).toBe(true);const transition=await world(620);expect(transition.features.some(f=>f.properties?.identityKey==='SUI'&&f.properties?.status==='source-reference')).toBe(true);
  expect(datedPlaces(transition,620).features.some(f=>f.properties?.identityKey==='TANG'&&f.properties?.referenceKind==='documented-seat-without-polygon')).toBe(true);
  expect(identity('TANG',620).leaders.some(l=>l.person==='Q9700')).toBe(true);expect((await world(690)).features.some(f=>f.properties?.identityKey==='WU-ZHOU')).toBe(true);expect(identity('WU-ZHOU',695).leaders.some(l=>l.person==='Q9738')).toBe(true);
  expect(governmentFor({identityKey:'SUI'},620).known).toBe(false);expect(governmentFor({identityKey:'WU-ZHOU'},695).tags).toContain('monarchy');
 });
 it('separates Medina, the caliphates and the rival Zubayrid court without extending extinct authorities',async()=>{
  const medina=datedPlaces(await world(625),625).features.find(f=>f.properties?.identityKey==='MEDINA-COMMUNITY');expect(medina?.properties?.sovereignSeat).toBe(true);expect(identity('MEDINA-COMMUNITY',625).leaders[0].person).toBe('Q9458');expect(identity('RASHIDUN-CALIPHATE',625).leaders).toHaveLength(0);
  expect(identity('RASHIDUN-CALIPHATE',634).leaders.some(l=>l.person==='Q334923')).toBe(true);expect(identity('RASHIDUN-CALIPHATE',662).leaders).toHaveLength(0);expect(identity('UMAYYAD-CALIPHATE',660).leaders).toHaveLength(0);expect(identity('UMAYYAD-CALIPHATE',685).leaders.some(l=>l.person==='Q298577')).toBe(true);
  expect(identity('UMAYYAD-CALIPHATE',688).leaders.some(l=>l.person==='Q307665')).toBe(false);expect(identity('ZUBAYRID-CALIPHATE',688).leaders.some(l=>l.person==='Q307665')).toBe(true);expect(datedPlaces(await world(688),688).features.some(f=>f.properties?.identityKey==='ZUBAYRID-CALIPHATE')).toBe(true);
  expect(identity('SASANIAN',628).leaders.some(l=>l.person==='Q315873')).toBe(true);expect(identity('SASANIAN',652).leaders).toHaveLength(0);
 });
 it('keeps Japanese restorations, Korean reign chronology and manuscript-era dates distinct',()=>{
  expect(identity('JPN',643).leaders.find(l=>l.person==='Q235296')?.name).toContain('Kōgyoku');expect(identity('JPN',658).leaders.find(l=>l.person==='Q235296')?.name).toContain('Saimei');expect(identity('JPN',650).leaders.some(l=>l.person==='Q235296')).toBe(false);
  expect(identity('HIST-Q28370',600).leaders.some(l=>l.person==='Q498952')).toBe(false);expect(identity('HIST-Q28370',620).leaders.some(l=>l.person==='Q498952')).toBe(true);
  expect(identity('BYZANTINE',641).leaders.some(l=>l.person==='Q41615')).toBe(true);expect(identity('SUI',618).leaders.some(l=>l.person==='Q7420')).toBe(true);expect(identity('VISIGOTHIC-KINGDOM',680).leaders.some(l=>l.person==='Q312600')).toBe(true);
  expect(identity('HIST-Q6737189',640).leaders.some(l=>l.person==='LOCAL-MAITRAKA-DHRUVASENA-II')).toBe(true);
 });
 it('retains regional communities after conquests and explicitly reinterprets anachronistic names',()=>{
  const p=(n:string)=>regions.features.find((f:any)=>f.properties.sourceYear===600&&f.properties.originalNames.includes(n))?.properties;
  expect(p('Sasanian Empire').contextKey).toBe('REFERENCE-POST-SASANIAN');expect(p('Koguryo').contextKey).toBe('REFERENCE-POST-GOGURYEO');expect(p('Tuʻi Tonga Empire').interpretation).toContain('posterior');expect(p('Mataram').interpretation).toContain('sigloVIII');expect(p('Ostrogoths').interpretation).toContain('antes de600');
 });
 it('retains source geometry and prevents rejected portraits from returning through a fallback',()=>{
  const geo=read('early-modern-600.geojson');let originalCount=0,rejectedCount=0;
  for(const {file,data:d}of dossiers){for(const r of d.geography??[])for(const f of JSON.parse(readFileSync(resolve(dirname(file),r.file),'utf8')).features){expect(geo.features.find((p:any)=>p.id==='clio-'+f.sourceIndex)?.geometry).toEqual(f.geometry);originalCount++;}
   const actual=ids.countries[d.key]?.leaders.filter((l:any)=>l.acquisition===d.acquisition)??[];
   for(const rejected of d.rejectedPortraits??[]){expect(actual.some((l:any)=>l.person===rejected.person&&l.portrait?.title===rejected.title)).toBe(false);rejectedCount++;}
   for(const l of d.leaders)if(l.portrait){expect(l.portrait.caption.length).toBeGreaterThan(20);expect(existsSync(l.portrait.canonicalFile)).toBe(true);}
  }
  expect(originalCount).toBe(geo.features.length);expect(originalCount).toBeGreaterThan(300);expect(rejectedCount).toBeGreaterThan(30);
 });

});
