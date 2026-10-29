import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{createHash}from'node:crypto';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{regionsAt,hasRegionalCoverage,regionalAsset,entitiesAt,regionalCard,containsLocation}from'../src/cultural-regions';import{anchorFor,matchingFeature}from'../src/selection';
const read=(f:string)=>JSON.parse(readFileSync(f,'utf8')),all=read('public/data/cultural-regions.geojson'),index=read('public/data/cultural-index.json'),ids=read('public/data/identities.json'),inventory=read('docs/CULTURAL-REVIEW-900-1905.json'),empty:any={type:'FeatureCollection',features:[]};
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const norm=(s:string)=>s.normalize('NFC').toLowerCase().trim();
describe('global regional review 900–1905',()=>{
 it('audits every year, political priority and remissions without treating name candidates as proved equivalences',async()=>{
  const years=[],transitions:any[]=[],remissions:any[]=[];let previous=new Map<string,any>();const anchors=new Set(inventory.sourceInventories.map((s:any)=>s.year));
  const referencesByYear=new Map<number,any[]>();for(const r of inventory.entities.filter((r:any)=>r.decision==='political-base'))referencesByYear.set(r.sourceYear,[...referencesByYear.get(r.sourceYear)??[],r]);
  for(let year=900;year<=1905;year++){
   expect(hasRegionalCoverage(year),String(year)).toBe(true);const p=politicalData(await annualData(year),year),before=p.features.map(f=>[f.id,f.properties?.identityKey,f.properties?.name,f.properties?.politicalColor]),r=regionsAt(all,year,p),raw=regionsAt(all,year,empty);expect(p.features.length===before.length&&p.features.every((f,i)=>[f.id,f.properties?.identityKey,f.properties?.name,f.properties?.politicalColor].every((v,j)=>Object.is(v,before[i][j]))),String(year)).toBe(true);
   const keys=new Set(p.features.map(f=>f.properties?.identityKey??f.properties?.entityCode));const current=new Map(r.features.map(f=>[String(f.properties?.contextKey),f.properties]));
   for(const[key,old]of previous)if(!current.has(key)){const rawPhase=raw.features.find(f=>f.properties?.contextKey===key);transitions.push({year,contextKey:key,name:old.name,reason:rawPhase?'political-representation-priority':'documentary-phase-ended',lastSourceYear:old.sourceYear,dateBasis:old.dateBasis,canonicalFile:old.canonicalFile});}
   previous=current;
   const culture=r.features.filter(f=>f.properties?.kind==='cultural-region');expect(culture.length,String(year)).toBeGreaterThan(40);
   years.push({year,politicalFeatures:p.features.length,regionalReferences:r.features.length,culturalAndGeographicReferences:culture.length,traditionalChronologyPending:r.features.filter(f=>f.properties?.temporalMode==='traditional-area-undated').length,olderHistoricalReferences:r.features.filter(f=>f.properties?.temporalMode==='historical-area-context').length});
   const nameCandidates=new Map<string,string[]>();if(anchors.has(year))for(const f of p.features)for(const value of[f.properties?.originalName,f.properties?.name])if(value){const name=norm(String(value)),key=String(f.properties?.identityKey??f.properties?.entityCode??'');nameCandidates.set(name,[...nameCandidates.get(name)??[],key]);}
   if(anchors.has(year))for(const item of referencesByYear.get(year)??[]){const d=read(item.file);const exact=d.politicalKeys.filter((k:string)=>keys.has(k));const candidates=d.originalNames.flatMap((n:string)=>nameCandidates.get(norm(n))??[]);const ownerPresent=keys.has(d.ownerKey),inFocus=p.features.filter(f=>containsLocation(f.geometry,d.focus)).map(f=>({key:f.properties?.identityKey??f.properties?.entityCode,name:f.properties?.name}));remissions.push({key:item.key,file:item.file,sourceYear:year,name:item.name,ownerKey:d.ownerKey,ownerPresent,status:exact.length?'explicit-key-present':ownerPresent?'owner-present-context-needs-validation':candidates.length?'name-candidate-needs-validation':'unresolved',explicitKeys:exact,candidateKeys:[...new Set(candidates.filter(Boolean))],politicalFeaturesAtReferenceFocus:inFocus,note:'Folder ownership, name candidates and a point overlap do not prove institutional equivalence or full territorial coverage. Unresolved means an unresolved crosswalk, not necessarily a missing country on the map.'});}
  }
  expect(hasRegionalCoverage(2028)).toBe(false);expect(years).toHaveLength(1006);
  if(process.env.WRITE_REGIONAL_AUDIT==='1')writeFileSync('docs/CULTURAL-GLOBAL-REVIEW-900-1905.json',JSON.stringify({scope:'Technical continuity, political selection and documentary-link review. Not independent validation of all regional extents, nor an ethnic or population census.',years,transitions,politicalBaseRemissions:remissions,unresolvedRemissions:remissions.filter(r=>r.status!=='explicit-key-present')},null,2)+'\n');
 },120000);
 it('uses complete century segments rather than downloading the worldwide inventory at every first visit',()=>{
  // Compare every property and coordinate while avoiding repeated matcher walks
  // through thousands of large geometries. The compiler retains object order.
  const digest=(f:unknown)=>createHash('sha256').update(JSON.stringify(f)).digest('hex');const hashes=new Map(all.features.map((f:any)=>[f.id,digest(f)]));
  for(const segment of index.segments){const data=read('public/data/'+segment.file),expected=all.features.filter((f:any)=>f.properties.start<=segment.end&&f.properties.end>=segment.start),expectedIds=new Set(expected.map((f:any)=>f.id));expect(data.features.length).toBe(expected.length);expect(new Set(data.features.map((f:any)=>f.id)).size).toBe(data.features.length);for(const f of data.features){expect(expectedIds.has(f.id),segment.file+' '+f.id).toBe(true);expect(digest(f),segment.file+' '+f.id).toBe(hashes.get(f.id));}}
  for(let year=900;year<=1905;year++){const file=regionalAsset(year);expect(file).toBeDefined();expect(file).not.toBe('cultural-regions.geojson');}expect(regionalAsset(2028)).toBeUndefined();
 });
 it('preserves the 1700 cultures through 1701 and the reviewed endpoint with visible reference dating',()=>{
  const active=(y:number)=>regionsAt(all,y,empty).features;const old=active(1700).filter(f=>f.properties?.kind==='cultural-region');
  const retained=[1701,1800,1886,1905].map(year=>({year,keys:new Set(active(year).map(f=>f.properties?.contextKey))}));for(const f of old)for(const{year,keys}of retained)expect(keys.has(f.properties?.contextKey),f.properties?.name+' '+year).toBe(true);
  const d=active(1905).find(f=>f.properties?.contextKey==='CULTURE-SAMI')!;expect(d).toBeDefined();expect(d.properties?.sourceYear).toBeLessThan(1905);expect(regionalCard(d.properties as any,1905,true)).toContain('Área histórica');expect(regionalCard(d.properties as any,2028,false)).toContain('no indica desaparición');
  const kalmar=active(1905).find(f=>f.properties?.contextKey==='CULTURE-KALMAR-UNION-E71C2DDD')!;expect(kalmar.properties?.name).toContain('Área histórica');expect(kalmar.properties?.sourceYear).toBe(1500);
 });
 it('retains an open traditional reference under colonial political control after the CShapes transition',async()=>{
  const old=regionsAt(all,1800,empty).features.find(f=>f.properties?.contextKey==='CULTURE-BURARRA-903375F8')!,anchor=anchorFor(old.properties!,1800,ids);for(const year of[1885,1886,1900,1905]){const p=politicalData(await annualData(year),year),r=regionsAt(all,year,p);expect(matchingFeature(anchor,r,year,ids)).toBeDefined();const at=entitiesAt([134.5,-12.5],p,r);expect(at.some(f=>f.properties?.contextKey),JSON.stringify(at.map(f=>f.properties?.name))).toBe(true);expect(at.some(f=>f.properties?.identityKey),JSON.stringify(at.map(f=>f.properties?.name))).toBe(true);expect(at[0].properties?.contextKey).toBeUndefined();}
 });
 it('keeps source decisions for all seven new anchors and preserves aliases across their spelling changes',()=>{
  const expected:any={1715:600,1783:549,1800:546,1815:312,1878:172,1880:169,1900:165};for(const[year,count]of Object.entries(expected))expect(inventory.sourceInventories.find((s:any)=>s.year===Number(year)).names.length,year).toBe(count);
  const maori=all.features.filter((f:any)=>f.properties.start>1700&&f.properties.originalNames.some((n:string)=>['Māori','M?ori','Maori','Maoris'].includes(n)));expect(new Set(maori.map((f:any)=>f.properties.contextKey)).size).toBe(1);expect(maori.length).toBeGreaterThan(4);
 });
});
